from sqlalchemy import Column, Text, Boolean
from app.db.database import Base

class SmokingStatusScore(Base):
    __tablename__ = "smoking_status_score"

    user_id = Column(Text, primary_key=True, nullable=False)
    does_smoke = Column(Boolean, nullable=False, default=False) 