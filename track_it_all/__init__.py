from decouple import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

from track_it_all.configurations import Configurations

db = SQLAlchemy()
migrate = Migrate()

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

    migrate.init_app(app, db)

    # bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from track_it_all.main.routes import main
    from track_it_all.users.routes import users
    from track_it_all.projects.routes import projects
    from track_it_all.bugs.routes import bugs
    from track_it_all.errors.handlers import errors

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(projects, url_prefix='/')
    app.register_blueprint(bugs, url_prefix='/')
    app.register_blueprint(errors)

    from track_it_all.models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app