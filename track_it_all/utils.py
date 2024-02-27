import os
import secrets

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join('track_it_all/static/profile_pics', picture_name)
    form_picture.save(picture_path)

    return picture_name