from sqlalchemy import Column, Boolean, Text

from app.db.database import Base

class Sects(Base): 
    __tablename__ = 'sects'
    
    user_id = Column(Text, primary_key=True, nullable=False)
    sunni = Column(Boolean, default=False)
    shia = Column(Boolean, default=False)
    ahmadi = Column(Boolean, default=False)
    ismaili = Column(Boolean, default=False)
    ibadi = Column(Boolean, default=False)
    other = Column(Boolean, default=False) 