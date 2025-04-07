from sqlalchemy import Column,Text, Boolean
from app.db.database import Base

class AgeRange(Base):      
    __tablename__ = "age_range"
    
    user_id = Column(Text, primary_key=True)
    range_18_to_24 = Column(Boolean, default=False)
    range_25_to_34 = Column(Boolean, default=False)
    range_35_to_44 = Column(Boolean, default=False)
    range_above_44 = Column(Boolean, default=False) 