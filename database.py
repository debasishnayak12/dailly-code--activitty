from sqlalchemy import Column,Integer,String,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session

DATABASE_URL = "mysql+pymysql://root:@localhost/atthah"

engine = create_engine(DATABASE_URL)

SessionLocal= sessionmaker(autocommit=False,autoflush = False ,bind = engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()