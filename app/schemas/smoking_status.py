from sqlalchemy import Column, Text, Boolean
from app.db.database import Base

class SmokingStatus(Base):
    __tablename__ = "smoking_status"

    user_id = Column(Text, primary_key=True, nullable=False)
    does_smoke = Column(Boolean, nullable=False, default=False) 