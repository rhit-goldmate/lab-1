import os
from flask import Blueprint, Flask

def create_app(opts = {}):
    app = Flask(__name__)

    # We will learn how to store our secrets properly in a few short weeks.
    # In the meantime, we'll use this:
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or "Don't ever store secrets in your actual code"

    # For local debugging purposes.  Not ideal for production environements:
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    from .simple_photo_processor import spp as spp_blueprint
    app.register_blueprint(spp_blueprint)
    return app