from flask import Blueprint, render_template, request
from flask_login import current_user

from track_it_all.models import Bug, User, Project

main = Blueprint('main', __name__)

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        bugs = Bug.query.filter_by(user_assigned=current_user.id).order_by(Bug.deadline_date.asc()).paginate(page=page, per_page=5)
        projects = current_user.get_all_projects()
    else:
        bugs = Bug.query.filter_by(user_assigned=None).order_by(Bug.deadline_date.asc()).paginate(page=page, per_page=5)
        projects = Project.query.filter_by(personal=False).order_by(Project.created_at.desc()).all()
    return render_template('home.html', user=current_user,bugs=bugs, projects=projects)