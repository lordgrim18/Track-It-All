from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required, current_user

from .models import Bug
from .database import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/bug-manage', methods=['GET', 'POST'])
@login_required
def bug_manage():
    if request.method == 'POST':
        bug = request.form.get('bug')

        if len(bug) < 1:
            pass
        else:
            new_bug = Bug(text=bug, user_id=current_user.id)
            db.session.add(new_bug)
            db.session.commit()
            flash('Bug added!', category='success')
        

    return render_template('bug_manage.html', user=current_user)

@views.route('/account')
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', user=current_user, image_file=image_file)