import uuid
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from decouple import config

from track_it_all import db

project_user = db.Table('project_user',
                        db.Column('id', db.String(36), primary_key=True, default=str(uuid.uuid4)),
                        db.Column('project_id', db.String(36), db.ForeignKey('project.id'), nullable=False),
                        db.Column('user_id', db.String(36), db.ForeignKey('user.id'), nullable=False),
                        db.Column('role', db.String(150), nullable=False),
                        db.Column('created_at', db.DateTime(timezone=True), default=func.now(), nullable=False),
                        db.Column('updated_at', db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False),
                        db.Column('created_by', db.String(36), db.ForeignKey('user.id'), nullable=False),
                        db.Column('updated_by', db.String(36), db.ForeignKey('user.id'), nullable=False),

                        db.UniqueConstraint('project_id', 'user_id', name='unique_project_user')
                        )

class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    # created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False) # more efficient than default=func.now()
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    bugs = db.relationship('Bug', backref='assigned_user', lazy='dynamic', foreign_keys='Bug.user_assigned')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(config('SECRET_KEY'), expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(config('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def get_all_projects(self):
        return Project.query.join(project_user).filter(project_user.c.user_id == self.id).all()

    def __repr__(self):
        return f"User('{self.email}', '{self.first_name}')"
    
class Project(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))
    name = db.Column(db.String(150), nullable=False)
    desc = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    updated_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    bugs = db.relationship('Bug', backref='project_bugs', lazy='dynamic', foreign_keys='Bug.project')

    def get_all_users(self):
        return User.query.join(project_user).filter(project_user.c.project_id == self.id).all()

    def __repr__(self):
        return f"Project('{self.name}')"

class Bug(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))
    title = db.Column(db.String(150), nullable=False)
    desc = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False)
    deadline_date = db.Column(db.DateTime(timezone=True), nullable=False)
    user_assigned = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    project = db.Column(db.String(36), db.ForeignKey('project.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    updated_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Bug('{self.title}')"