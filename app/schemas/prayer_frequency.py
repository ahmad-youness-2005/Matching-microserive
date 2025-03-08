from sqlalchemy import Column, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base

from app.db.database import Base
class PrayerFrequencyScore(Base):
    __tablename__ = "prayer_frequency_scores"

    user_id = Column(Text, primary_key=True, index=True, nullable=False)
    always_pray = Column(Boolean, default=False)
    usually_pray = Column(Boolean, default=False)
    sometimes_pray = Column(Boolean, default=False)
    never_pray = Column(Boolean, default=False)