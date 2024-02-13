from decouple import config
from flask import Flask

from .database import db
from .views import views
from .auth import auth

DB_NAME = config('DB_NAME')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

