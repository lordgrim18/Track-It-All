import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from track_it_all.models import Project, Bug, User, project_user
from track_it_all import db
from track_it_all.projects.forms import ProjectForm
from track_it_all.projects.utils import Project_Roles

projects = Blueprint('projects', __name__)

@projects.route('/add-project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            id=str(uuid.uuid4()),
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
            id=str(uuid.uuid4()),
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