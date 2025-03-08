from sqlalchemy import Column, Text
from app.db.database import Base


class VisitedScore(Base):
    __tablename__ = "visited_score"

    user_id = Column(Text, primary_key=True, nullable=False)
    visited_user_id = Column(Text, primary_key=True, nullable=False) 