from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from track_it_all.models import Bug, User, Project
from track_it_all import db
from track_it_all.bugs.forms import BugForm

bugs = Blueprint('bugs', __name__)

@bugs.route('/add-bug/<string:project_id>', methods=['GET', 'POST'])
@login_required
def add_bug(project_id):
    project = Project.query.get_or_404(project_id)
    if current_user not in project.get_all_users():
        abort(403)
    form = BugForm(project_id=project_id, creator_user=current_user)
    if form.validate_on_submit():
        bug = Bug(
            title=form.title.data, 
            about=form.about.data,
            bug_status=form.bug_status.data,
            priority=form.priority.data,
            user_assigned=form.user_assigned.data,
            project=form.project_id,
            created_by=str(current_user.id),
            updated_by=str(current_user.id)
            )
        db.session.add(bug)
        db.session.commit()
        flash('Bug added to project!', category='success')
        return redirect(url_for('projects.get_project', project_id=project.id))
    return render_template('add_bug.html', user=current_user, form=form, legend='Add Bug')

@bugs.route('bug/get/<string:bug_id>')
@login_required
def get_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    return render_template('bug.html', user=current_user, bug=bug)

@bugs.route('bug/update/<string:bug_id>', methods=['GET', 'POST'])
@login_required
def update_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if bug.bug_adder != current_user:
        abort(403)
    form = BugForm()
    if form.validate_on_submit():
        bug.title = form.title.data
        bug.desc = form.desc.data
        db.session.commit()
        flash('Bug updated!', category='success')
        return redirect(url_for('bugs.get_bug', bug_id=bug.id))
    elif request.method == 'GET':
        form.title.data = bug.title
        form.desc.data = bug.desc
        form.submit.label.text = 'Update'
    return render_template('add_bug.html', user=current_user, form=form, legend='Update Bug')

@bugs.route('bug/delete/<string:bug_id>', methods=['GET','POST'])
@login_required
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if bug.bug_adder != current_user:
        abort(403)
    db.session.delete(bug)
    db.session.commit()
    flash('Bug deleted!', category='success')
    return redirect(url_for('main.home'))

@bugs.route('/user/<string:first_name>')
@login_required
def user_bugs(first_name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(first_name=first_name).first_or_404()
    bugs = Bug.query.filter_by(bug_adder=user).order_by(Bug.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_bugs.html', user=user, bugs=bugs)