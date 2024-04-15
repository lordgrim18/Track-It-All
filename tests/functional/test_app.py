from flask import url_for
from track_it_all import db
from track_it_all.models import User
from track_it_all.users.forms import RegistrationForm

def test_home(client):
    response = client.get("/")
    assert b"<title>Home</title>" in response.data

def test_registration(test_client, app):
    with app.app_context(), app.test_request_context():
        response = test_client.get(url_for("users.register"), follow_redirects=True)
        assert response.status_code == 200

        registration_form = RegistrationForm()

        registration_form.email.data = "user1@gmail.com"
        registration_form.first_name.data = "john"
        registration_form.last_name.data = "doe"
        registration_form.password1.data = "hahahehe"
        registration_form.password2.data = "hahahehe"

        response = test_client.post(url_for("users.register"), data=registration_form.data, follow_redirects=True)

        assert response.status_code == 200

        new_user = db.session.query(User).filter_by(email="user1@gmail.com").first()
        assert new_user