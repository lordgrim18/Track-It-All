from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError

from track_it_all.projects.utils import Project_Roles
from track_it_all.models import User

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('Description', validators=[DataRequired()])
    personal = BooleanField('Personal')
    group_project = BooleanField('Group')

    submit = SubmitField('Add')

class ProjectUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[(role.value, role.value) for role in Project_Roles], validators=[DataRequired()])

    submit = SubmitField('Add')

    def validate_email(form, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('No user with that email exists! Please ask them to sign up.')