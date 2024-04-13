from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

from track_it_all.bugs.utils import Bug_Status, Bug_Priority
from track_it_all.models import Bug, Project

class BugForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    about = TextAreaField('Description', validators=[DataRequired()])
    bug_status = SelectField(
        'Status',
        choices=[],
        validators=[DataRequired(message="Please select a status.")]
    )
    priority = SelectField(
        'Priority',
        choices=[(priority.value, priority.value) for priority in Bug_Priority],
        validators=[DataRequired(message="Please select a priority.")]
    )
    user_assigned = SelectField(
        'Assigned User',
        choices=[],
        validators=[DataRequired(message="Please select a user.")]
    )

    submit = SubmitField('Submit')

    def __init__(self, project_id, creator_user, request_method='POST', *args, **kwargs):
        super(BugForm, self).__init__(*args, **kwargs)
        self.project_id = project_id
        self.request_method = request_method
        self.user_assigned.choices = [
            (user.id, user.first_name) \
                for user in Project.query.get(project_id).get_all_users() \
                    if user.id != Project.query.get(project_id).manager().id
                    ]
        if creator_user.get_role(project_id) == 'Developer':
            self.bug_status.choices = [
                (status.value, status.value) for status in Bug_Status if status not in [Bug_Status.VERIFIED, Bug_Status.CLOSED]
            ]
        elif creator_user.get_role(project_id) == 'Tester' or creator_user.get_role(project_id) == 'Designer':
            self.bug_status.choices = [
                (status.value, status.value) for status in Bug_Status if status not in [Bug_Status.CLOSED]
            ]
        else:
            self.bug_status.choices = [
                (status.value, status.value) for status in Bug_Status
            ] 

    def validate(self, extra_validators=None):
        initial_validation = super(BugForm, self).validate(extra_validators)
        if not FlaskForm.validate(self):
            return False
        if self.request_method == 'POST':
            bugs = Bug.query.filter_by(project=self.project_id).all()
            for bug in bugs:
                if bug.title == self.title.data and self.about.data == bug.about:
                    self.title.errors.append('Bug already exists with that title and description.')
                    self.about.errors.append('Bug already exists with that title and description.')
                    return False
        return True