import pytest
from decouple import config

from track_it_all import create_app, db

@pytest.fixture()
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI_TEST_MYSQL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def test_client():
    flask_app = create_app()
    flask_app.app_context().push()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI_TEST_MYSQL')
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['WTF_CSRF_ENABLED'] = False

    with flask_app.app_context():
        db.create_all()

    client = flask_app.test_client()
    with flask_app.test_request_context():

        yield client  