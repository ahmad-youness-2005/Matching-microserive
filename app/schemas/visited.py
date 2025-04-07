from sqlalchemy import Column, Text
from app.db.database import Base


class Visited(Base):
    __tablename__ = "visited"

    user_id = Column(Text, primary_key=True, nullable=False)
    visited_user_id = Column(Text, primary_key=True, nullable=False) 