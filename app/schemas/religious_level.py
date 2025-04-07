from sqlalchemy import Column, Boolean, Text
from app.db.database import Base

class ReligiousLevel(Base):
    __tablename__ = 'religious_level'
    
    user_id = Column(Text, primary_key=True, nullable=False)
    very_practising = Column(Boolean, default=False)
    practising = Column(Boolean, default=False)
    moderately_practising = Column(Boolean, default=False)
    not_practising = Column(Boolean, default=False) 