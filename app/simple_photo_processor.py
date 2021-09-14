from flask import Blueprint, redirect, render_template, request, send_file
from io import BytesIO
from PIL import Image, ImageFilter
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

spp = Blueprint("spp", __name__)

class FileUploadForm(FlaskForm):
    image = FileField('Select an image to upload')
    submit = SubmitField('Upload')

@spp.route('/')
def index():
    return render_template('index.html', name="Taylor")

@spp.route('/simple_photo_processor', methods=['GET'])
def upload():
    form = FileUploadForm()
    return render_template('upload.html', form=form)

@spp.route('/simple_photo_processor', methods=['POST'])
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
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
