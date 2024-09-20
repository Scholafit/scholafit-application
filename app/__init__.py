import os

from .api.v1.views import app_views
from app.models import *
from app.models.database import Database
from dotenv import load_dotenv
from flask import Flask


def create_app(test_config=None):
    load_dotenv()
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI=os.getenv('DB_URL')
    )
    app.url_map.strict_slashes = False
    app.register_blueprint(app_views)

    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    database = Database()
    database.load_db(app=app)


    return app
