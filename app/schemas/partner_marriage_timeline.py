from sqlalchemy import Column, Boolean, Text
from app.db.database import Base


class PartnerMarriageTimelineScore(Base):
    __tablename__ = "partner_marriage_timeline_score"

    user_id = Column(Text, primary_key=True, nullable=False)
    partner_agree_together = Column(Boolean, default=False)
    partner_within_1_year = Column(Boolean, default=False)
    partner_within_2_year = Column(Boolean, default=False)
    partner_within_3_year = Column(Boolean, default=False)
    partner_within_5_year = Column(Boolean, default=False) 