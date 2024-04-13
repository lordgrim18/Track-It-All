import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from track_it_all.models import Project, Bug, User, project_user
from track_it_all import db
from track_it_all.projects.forms import ProjectForm, ProjectUserForm
from track_it_all.projects.utils import Project_Roles

projects = Blueprint('projects', __name__)

@projects.route('/add-project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            name=form.name.data, 
            about=form.about.data, 
            personal=form.personal.data,
            group_project=form.group_project.data,
            created_by=str(current_user.id), 
            updated_by=str(current_user.id)
            )
        db.session.add(project)
        db.session.commit()

        project_user_row = project_user.insert().values(
            project_id=project.id, 
            user_id=current_user.id, 
            user_role=Project_Roles.MANAGER.value,
            created_by=current_user.id,
            updated_by=current_user.id
            )
        db.session.execute(project_user_row)
        db.session.commit()

        flash('Project added!', category='success')
        return redirect(url_for('main.home'))
    return render_template('add_project.html', user=current_user, form=form, legend='Add Project')

@projects.route('/get-project/<string:project_id>', methods=['GET', 'POST'])
@login_required
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', user=current_user, project=project)

@projects.route('/update-project/<string:project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.manager().id != current_user.id:
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        project.name = form.name.data
        project.about = form.about.data
        project.personal = form.personal.data
        project.group_project = form.group_project.data
        project.updated_by = str(current_user.id)
        db.session.commit()
        flash('Project updated!', category='success')
        return redirect(url_for('projects.get_project', project_id=project.id))
    elif request.method == 'GET':
        form.name.data = project.name
        form.about.data = project.about
        form.personal.data = project.personal
        form.group_project.data = project.group_project
    return render_template('add_project.html', user=current_user, form=form, legend='Update Project')

@projects.route('/delete-project/<string:project_id>', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.manager().id != current_user.id:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted!', category='success')
    return redirect(url_for('main.home'))

@projects.route('/user-projects/<string:user_id>')
@login_required
def user_projects(user_id):
    page = request.args.get('page', 1, type=int)
    user = User.query.get_or_404(user_id)
    projects = user.get_all_projects().paginate(page=page, per_page=5)
    return render_template('user_projects.html', user=current_user, projects=projects)

@projects.route('/add-user-to-project/<string:project_id>', methods=['GET', 'POST'])
@login_required
def add_user_to_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.manager().id != current_user.id:
        abort(403)
    form = ProjectUserForm(project_id)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        project_user_row = project_user.insert().values(
            project_id=project.id, 
            user_id=user.id, 
            user_role=form.role.data,
            created_by=current_user,
            updated_by=current_user
            )
        db.session.execute(project_user_row)
        db.session.commit()
        flash('User added to project!', category='success')
        return redirect(url_for('projects.get_project', project_id=project.id))
    return render_template('add_user_to_project.html', user=current_user, form=form, legend='Add User To Project')

@projects.route('/remove-user-from-project/<string:project_id>/<string:user_id>', methods=['GET', 'POST'])
@login_required
def remove_user_from_project(project_id, user_id):
    project = Project.query.get_or_404(project_id)
    user = User.query.get_or_404(user_id)
    if project.manager().id != current_user.id:
        abort(403)
    if user.id == project.manager().id:
        flash('Cannot remove the project manager from the project!', category='danger')
        return redirect(url_for('projects.get_project', project_id=project.id))
    db.session.query(project_user).filter(
        project_user.c.project_id == project.id,
        project_user.c.user_id == user.id
    ).delete()
    db.session.commit()
    flash('User removed from project!', category='success')
    return redirect(url_for('projects.get_project', project_id=project.id))

@projects.route('/update-user-role/<string:project_id>/<string:user_id>', methods=['GET', 'POST'])
@login_required
def update_user_role(project_id, user_id):
    project = Project.query.get_or_404(project_id)
    user = User.query.get_or_404(user_id)
    if project.manager().id != current_user.id:
        abort(403)
    if user.id == project.manager().id:
        flash('Cannot update the project manager role!', category='danger')
        return redirect(url_for('projects.get_project', project_id=project.id))
    method = request.form.get('_method')
    form = ProjectUserForm(project_id, method)
    form.email.data = user.email
    if form.validate_on_submit():
        db.session.query(project_user).filter(
            project_user.c.project_id == project.id,
            project_user.c.user_id == user.id
        ).update({'user_role': form.role.data, 'updated_by': str(current_user.id)})
        db.session.commit()
        flash('User role updated!', category='success')
        return redirect(url_for('projects.get_project', project_id=project.id))
    elif request.method == 'GET':
        form.role.data = db.session.query(project_user).filter(
            project_user.c.project_id == project.id,
            project_user.c.user_id == user.id
        ).first().user_role
    return render_template('add_user_to_project.html', user=current_user, form=form, legend='Update User Role')