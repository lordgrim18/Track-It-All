from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

from .models import Bug
from .database import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        bug = request.form.get('bug')

        if len(bug) < 1:
            pass
        else:
            new_bug = Bug(text=bug, user_id=current_user.id)
            db.session.add(new_bug)
            db.session.commit()
            flash('Bug added!', category='success')
        

    return render_template('home.html', user=current_user)