from flask import Blueprint, render_template, request
from flask_login import current_user

from track_it_all.models import Bug

main = Blueprint('main', __name__)

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        bugs = Bug.query.order_by(Bug.date.desc()).paginate(page=page, per_page=5)
    else:
        bugs = None
    return render_template('home.html', user=current_user, bugs=bugs)