from decouple import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from track_it_all.configurations import Configurations

db = SQLAlchemy()
# bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configurations)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from track_it_all.main.routes import main
    from track_it_all.users.routes import users
    from track_it_all.bugs.routes import bugs

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(bugs, url_prefix='/')

    from track_it_all.models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app