from sqlalchemy import (Column, Integer, String)
from db_setup import Base

'''This module contains All the SQLAlchemy Database Schemas or Model
'''
class User(Base): 
    __tablename__ = "user"
    user_id = Column(Integer, primary_key= True,autoincrement=True)
    username = Column(String(100),unique=True, index= True, nullable= False )
    _password = Column(String(100), nullable=False)