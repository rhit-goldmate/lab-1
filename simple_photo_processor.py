# This code is from https://github.com/miguelgrinberg/flasky/blob/2a/hello.py
import os
from io import BytesIO
from PIL import Image, ImageFilter
from flask import Flask, redirect, render_template, request, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
app = Flask(__name__)

# We will learn how to store our secrets properly in a few short weeks.
# In the meantime, we'll use this:
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or "Don't ever store secrets in your actual code"

# For local debugging purposes.  Not ideal for production environements:
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class FileUploadForm(FlaskForm):
    image = FileField('Select an image file to upload')
    submit = SubmitField('Upload')

@app.route('/')
def index():
    return render_template('index.html', name="Eliza")

@app.route('/simple_photo_processor', methods=['GET'])
def upload():
    form = FileUploadForm()
    return render_template('upload.html', form=form)

@app.route('/simple_photo_processor', methods=['POST'])
def process():
    form = FileUploadForm()
    if form.image.data:
        image_data = request.files['image']
        input_image = Image.open(image_data)
        ## TODO: Actually transform image here
        output_image = input_image
        return serve_pil_image(output_image)
    else:
        return redirect(url_for('upload'))

# This code borrowed directly from https://stackoverflow.com/a/10170635/35345
def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')
