from sqlalchemy import Column, Boolean, Text
from app.db.database import Base

class Gender(Base): 
    __tablename__ = "gender"
    
    user_id = Column(Text, primary_key=True, nullable=False)
    male = Column(Boolean, nullable=False, default=False)
    female = Column(Boolean, nullable=False, default=False) 