from sqlalchemy import or_, case
from flask import Blueprint, render_template, request
from flask_login import current_user

from track_it_all.models import Bug, User, Project
from track_it_all.bugs.utils import Bug_Status, Bug_Priority

main = Blueprint('main', __name__)

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        bugs = Bug.query.filter(
            Bug.user_assigned == current_user.id,
            or_(
                Bug.bug_status == Bug_Status.OPEN.value,
                Bug.bug_status == Bug_Status.IN_PROGRESS.value
            )
        ).order_by(
            case(
                (Bug.priority == Bug_Priority.CRITICAL.value, 1),
                (Bug.priority == Bug_Priority.HIGH.value, 2),
                (Bug.priority == Bug_Priority.MEDIUM.value, 3),
                (Bug.priority == Bug_Priority.LOW.value, 4),
                else_=5
            )
        ).paginate(page=page, per_page=5)
        projects = current_user.get_all_projects()
    else:
        bugs = Bug.query.filter(
            Bug.user_assigned == None,
            or_(
                Bug.bug_status == Bug_Status.OPEN.value,
                Bug.bug_status == Bug_Status.IN_PROGRESS.value
            )
        ).order_by(
            case(
                (Bug.priority == Bug_Priority.CRITICAL.value, 1),
                (Bug.priority == Bug_Priority.HIGH.value, 2),
                (Bug.priority == Bug_Priority.MEDIUM.value, 3),
                (Bug.priority == Bug_Priority.LOW.value, 4),
                else_=5
            )
        ).paginate(page=page, per_page=5)
        projects = Project.query.filter_by(personal=False).order_by(Project.created_at.desc()).all()
    return render_template('home.html', user=current_user,bugs=bugs, projects=projects)