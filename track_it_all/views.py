from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user

from .forms import UpdateAccountForm, BugForm
from .models import Bug
from .database import db
from .utils import save_picture

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        db.session.commit()
        flash('Account updated!', category='success')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', user=current_user, image_file=image_file, form=form)

@views.route('/add-bug', methods=['GET', 'POST'])
@login_required
def add_bug():
    form = BugForm()
    if form.validate_on_submit():
        bug = Bug(title=form.title.data, desc=form.desc.data, user_id=current_user.id)
        db.session.add(bug)
        db.session.commit()
        flash('Bug added!', category='success')
        return redirect(url_for('views.home'))
    return render_template('add_bug.html', user=current_user, form=form)