from sqlalchemy import Column, Text, Integer, DateTime
from datetime import datetime
from app.db.database import Base

class Match(Base):
    __tablename__ = "matches"

    partner_id_1 = Column(Text, primary_key=True, nullable=False)
    partner_id_2 = Column(Text, primary_key=True, nullable=False)
    match_status = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)