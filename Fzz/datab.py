from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test123@db:5880/fuzzyappdatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

"""
SQLALCHEMY_DATABASE_URL2 = 'sqlite:///./base.db'

engine2 = create_engine(SQLALCHEMY_DATABASE_URL2, connect_args={'check_same_thread': False})
SessionLocal2 = sessionmaker(autocommit=False, autoflush=False, bind=engine2)
Base2 = declarative_base()


"""

