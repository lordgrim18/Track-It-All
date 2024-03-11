from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class BugForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    desc = TextAreaField('Content', validators=[DataRequired()])
    # date = StringField('Date', validators=[DataRequired()])

    submit = SubmitField('Add')