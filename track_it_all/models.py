import uuid
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from decouple import config

from track_it_all import db


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    updated_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    bugs = db.relationship('Bug', backref='bugs_assigned', lazy=True)
    projects = db.relationship('Project', secondary='ProjectUser', backref='projects_present', lazy=True)

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

    members = db.relationship('User', secondary='ProjectUser', backref='project_members', lazy=True)

    def __repr__(self):
        return f"Project('{self.name}')"
    
class ProjectUser(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    updated_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"ProjectUser('{self.project_id}', '{self.user_id}')"

class Bug(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))
    title = db.Column(db.String(150), nullable=False)
    desc = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(150), nullable=False)
    deadline_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    user_assigned = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    updated_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Bug('{self.title}')"