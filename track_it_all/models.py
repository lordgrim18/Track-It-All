import uuid
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from decouple import config

from track_it_all import db
from track_it_all.projects.utils import Project_Roles

project_user = db.Table('project_user',
                        db.Column('id', db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True),
                        db.Column('project_id', db.String(36), db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False),
                        db.Column('user_id', db.String(36), db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
                        db.Column('user_role', db.String(150), nullable=False),
                        db.Column('created_at', db.DateTime(timezone=True), server_default=func.now(), nullable=False),
                        db.Column('updated_at', db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
                        db.Column('created_by', db.String(36), db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True),
                        db.Column('updated_by', db.String(36), db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True),

                        db.UniqueConstraint('project_id', 'user_id', name='unique_project_user')
                        )

class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    bugs = db.relationship('Bug', backref='assigned_user', lazy='dynamic', foreign_keys='Bug.user_assigned')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(config('SECRET_KEY'), salt='itsdangerous', expires_sec=expires_sec)
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(config('SECRET_KEY'), salt='itsdangerous')
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def get_all_projects(self):
        return Project.query.join(project_user).filter(project_user.c.user_id == self.id)
    
    def get_role(self, project_id):
        return db.session.query(project_user).filter(
            project_user.c.project_id == project_id,
            project_user.c.user_id == self.id
        ).first().user_role

    def __repr__(self):
        return f"User('{self.email}', '{self.first_name}')"
    
class Project(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    name = db.Column(db.String(150), nullable=False)
    about = db.Column(db.String(150), nullable=False)
    personal = db.Column(db.Boolean, nullable=False, default=False)
    group_project = db.Column(db.Boolean, nullable=False, default=True)
    created_by = db.Column(db.String(36), db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    updated_by = db.Column(db.String(36), db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                            server_default=func.now(),
                            onupdate=func.now())

    bugs = db.relationship('Bug', backref='project_bugs', lazy='dynamic', foreign_keys='Bug.project')

    def get_all_users(self):
        return User.query.join(project_user,
        onclause=project_user.c.user_id == User.id).filter(
            project_user.c.project_id == self.id
            ).all()
    
    def manager(self):
        return User.query.join(project_user, onclause=project_user.c.user_id == User.id).filter(
            project_user.c.project_id == self.id,
            project_user.c.user_role == Project_Roles.MANAGER.value
        ).first()

    def developers(self):
        return User.query.join(project_user, onclause=project_user.c.user_id == User.id).filter(
            project_user.c.project_id == self.id,
            project_user.c.user_role == Project_Roles.DEVELOPER.value
        ).all()

    def testers(self):
        return User.query.join(project_user, onclause=project_user.c.user_id == User.id).filter(
            project_user.c.project_id == self.id,
            project_user.c.user_role == Project_Roles.TESTER.value
        ).all()

    def designers(self):
        return User.query.join(project_user, onclause=project_user.c.user_id == User.id).filter(
            project_user.c.project_id == self.id,
            project_user.c.user_role == Project_Roles.DESIGNER.value
        ).all()

    def __repr__(self):
        return f"Project('{self.name}')"

class Bug(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)
    title = db.Column(db.String(150), nullable=False)
    about = db.Column(db.String(150), nullable=False)
    bug_status = db.Column(db.String(150), nullable=False)
    priority = db.Column(db.String(150), nullable=False)
    user_assigned = db.Column(db.String(36), db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    project = db.Column(db.String(36), db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    updated_by = db.Column(db.String(36), db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                            server_default=func.now(),
                            onupdate=func.now())

    def __repr__(self):
        return f"Bug('{self.title}')"