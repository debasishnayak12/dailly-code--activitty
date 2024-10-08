from sqlalchemy import Column, Integer, String ,DateTime
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    mobile = Column(Integer,index = True)
    image = Column(String(255),index = True)
    status = Column(Integer,index = True)
    time = Column(DateTime,index=True ,default=datetime.utcnow)

