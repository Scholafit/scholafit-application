
from abc import ABC
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from typing import TypeVar


T = TypeVar('T')

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def get_db():
    return db



class Repository(ABC):
    def __init__(self, database: SQLAlchemy):
        self._database = database
    
    @property
    def database(self):
        return self._database
    
    
    def add(self, obj):
        self.database.session.add(obj)
        return obj
        
    def save(self, obj:T):
        self.database.session.add(obj)
        
        self.database.session.commit()
        self.database.session.refresh(obj)
        return obj
        
    def delete(self, obj):
        self.database.session.delete(obj)
        self.database.session.commit()
        
    
    def get_by_id(self, objClass:T, objId: int) -> T:
        instance = self.database.session.get(objClass, objId)
        return instance
        




        

    