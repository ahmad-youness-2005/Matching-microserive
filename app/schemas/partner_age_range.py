from sqlalchemy import Column, Text, Boolean
from app.db.database import Base

class PartnerAgeRange(Base):
    __tablename__ = "partner_age_ranges"

    user_id = Column(Text, nullable=False, primary_key=True)
    partner_range_18_to_24 = Column(Boolean, default=False)
    partner_range_25_to_34 = Column(Boolean, default=False)
    partner_range_35_to_44 = Column(Boolean, default=False)
    partner_range_above_44 = Column(Boolean, default=False) 
    