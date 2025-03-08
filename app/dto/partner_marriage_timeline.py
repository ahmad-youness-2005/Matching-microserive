from pydantic import BaseModel, Field
from typing import Literal


class PartnerMarriageTimelineBase(BaseModel):
    partner_marriage_timeline: Literal[
        "partner_agree_together", 
        "partner_within_1_year", 
        "partner_within_2_year", 
        "partner_within_3_year", 
        "partner_within_5_year"
    ] = Field(..., description="Partner marriage timeline preference")


class PartnerMarriageTimelineCreate(PartnerMarriageTimelineBase):
    user_id: str = Field(..., description="User ID")


class PartnerMarriageTimelineUpdate(PartnerMarriageTimelineBase):
    pass


class PartnerMarriageTimelineResponse(BaseModel):
    user_id: str
    partner_agree_together: bool
    partner_within_1_year: bool
    partner_within_2_year: bool
    partner_within_3_year: bool
    partner_within_5_year: bool

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str 