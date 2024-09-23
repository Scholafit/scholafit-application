import os

from .api.v1.views import app_views
from app.models import *
from app.models.database import db
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask import Flask

migrate = Migrate()


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

    db.init_app(app)
    migrate.init_app(app, db)


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)