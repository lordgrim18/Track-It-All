from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError

from track_it_all import db
from track_it_all.projects.utils import Project_Roles
from track_it_all.models import User, project_user

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('Description', validators=[DataRequired()])
    personal = BooleanField('Personal')
    group_project = BooleanField('Group')

    submit = SubmitField('Submit')

class ProjectUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField(
        'Role',
        choices=[(role.value, role.value) for role in Project_Roles if role != Project_Roles.MANAGER],
        validators=[DataRequired(message="Please select a role.")]
    )

    submit = SubmitField('Submit')

    def __init__(self, project_id, request_method='POST', *args, **kwargs):
        super(ProjectUserForm, self).__init__(*args, **kwargs)
        self.project_id = project_id
        self.request_method = request_method

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError('No user with that email exists! Please ask them to sign up.')

        # Check if the user is already associated with the project
        if self.request_method == 'POST': 
            if db.session.query(project_user).filter(
                project_user.c.project_id == self.project_id,
                project_user.c.user_id == User.query.filter_by(email=email.data).first().id
            ).first():
                raise ValidationError('User is already associated with the project.')