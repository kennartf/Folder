import os
import secrets
from PIL import Image
from web_app import app


def save_picture(form_picture):
    random_hex = secrets.token_hex(12)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext #this script help us to save the profile in the root dir
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)

    output_size = (1200, 2500) #this script resize or scale down our image before loading
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename
    