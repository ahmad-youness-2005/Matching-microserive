from sqlalchemy import Column, Boolean, Text
from app.db.database import Base


class PartnerChildrenExpectationsScore(Base):
    __tablename__ = "partner_children_expectations_score"

    user_id = Column(Text, primary_key=True, nullable=False)
    partner_wants_children = Column(Boolean, default=False)
    partner_open_to_have_children = Column(Boolean, default=False)
    partner_does_not_want_children = Column(Boolean, default=False) 