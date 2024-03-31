from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class BugForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()], default='Open')
    deadline_date = StringField('Deadline Date', validators=[DataRequired()])
    user_assigned = StringField('User Assigned', validators=[DataRequired()])
    project = StringField('Project', validators=[DataRequired()])

    submit = SubmitField('Add')