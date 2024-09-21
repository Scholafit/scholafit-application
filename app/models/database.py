

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Database:
    
    """
    Provide Database connection.

    """
    @classmethod
    def new(cls, obj):
        """Adds obj to the scoped session.

        Args:
            obj: instance
                This is the instance Object being added to the session
        Returns:
            None
        """
        db.session.add(obj)
    
    @classmethod
    def save(cls):
        """saves object to the database
        """
        db.session.commit()

    @classmethod
    def delete(cls, obj):
        """Deletes obj from the database
        
        Args:
            obj: instance
                class Instance to be deleted
        Returns:
            None
        """
        db.session.delete(obj)
        Database.save()
        

    