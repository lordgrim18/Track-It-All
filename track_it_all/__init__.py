from decouple import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from .views import views
from .models import User

db = SQLAlchemy()
DB_NAME = config('DB_NAME')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqllite:///{DB_NAME}'
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')

    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')