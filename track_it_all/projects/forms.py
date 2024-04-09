from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    about = TextAreaField('Description', validators=[DataRequired()])
    personal = BooleanField('Personal')
    group_project = BooleanField('Group')

    submit = SubmitField('Add')