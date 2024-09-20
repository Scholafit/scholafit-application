
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Database:

    def load_db(self, app):
        db.init_app(app)

        with app.app_context():
            db.create_all()
    

    