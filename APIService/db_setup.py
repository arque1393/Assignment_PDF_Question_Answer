from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URL
'''This module contains Database Configuration Variable, Database connection String database engine and database access utility  '''
# SQLite setup
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# BASE ORM Model 
Base = declarative_base()

# DB Utilities 
def get_session ():
    session = SessionLocal()
    try: 
        yield session
    except Exception as e : 
        print(e)
    finally:
        session.close()
        