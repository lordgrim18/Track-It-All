from flask import Blueprint, render_template, request, flash, url_for, redirect, abort
from flask_login import login_required, current_user

from track_it_all.forms import UpdateAccountForm, BugForm
from track_it_all.models import Bug, User
from track_it_all.database import db
from track_it_all.utils import save_picture

views = Blueprint('views', __name__)

@views.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    bugs = Bug.query.order_by(Bug.date.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', user=current_user, bugs=bugs)

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
        bug = Bug(title=form.title.data, desc=form.desc.data, bug_adder=current_user)
        db.session.add(bug)
        db.session.commit()
        flash('Bug added!', category='success')
        return redirect(url_for('views.home'))
    return render_template('add_bug.html', user=current_user, form=form, legend='Add Bug')

@views.route('bug/get/<string:bug_id>')
@login_required
def get_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    return render_template('bug.html', user=current_user, bug=bug)

@views.route('bug/update/<string:bug_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('views.get_bug', bug_id=bug.id))
    elif request.method == 'GET':
        form.title.data = bug.title
        form.desc.data = bug.desc
        form.submit.label.text = 'Update'
    return render_template('add_bug.html', user=current_user, form=form, legend='Update Bug')

@views.route('bug/delete/<string:bug_id>', methods=['GET','POST'])
@login_required
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    if bug.bug_adder != current_user:
        abort(403)
    db.session.delete(bug)
    db.session.commit()
    flash('Bug deleted!', category='success')
    return redirect(url_for('views.home'))

@views.route('/user/<string:first_name>')
@login_required
def user_bugs(first_name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(first_name=first_name).first_or_404()
    bugs = Bug.query.filter_by(bug_adder=user).order_by(Bug.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_bugs.html', user=user, bugs=bugs)