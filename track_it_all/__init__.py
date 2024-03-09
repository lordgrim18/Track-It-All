from decouple import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')

DB_NAME = config('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

# bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = config('EMAIL_HOST')
app.config['MAIL_PORT'] = config('EMAIL_PORT')
app.config['MAIL_USE_TLS'] = config('EMAIL_USE_TLS')
app.config['MAIL_USERNAME'] = config('EMAIL_HOST_USER')
app.config['MAIL_PASSWORD'] = config('EMAIL_HOST_PASSWORD')
mail = Mail(app)

from track_it_all.views import views
from track_it_all.auth import auth

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

from track_it_all.models import User
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))