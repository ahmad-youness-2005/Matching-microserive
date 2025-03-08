from pydantic import BaseModel, Field
from typing import Literal


class PartnerChildrenExpectationsBase(BaseModel):
    partner_children_expectation: Literal["wants_children", "open_to_have_children", "does_not_want_children"] = Field(
        ..., description="Partner children expectation preference"
    )


class PartnerChildrenExpectationsCreate(PartnerChildrenExpectationsBase):
    user_id: str = Field(..., description="User ID")


class PartnerChildrenExpectationsUpdate(PartnerChildrenExpectationsBase):
    pass


class PartnerChildrenExpectationsResponse(BaseModel):
    user_id: str
    partner_wants_children: bool
    partner_open_to_have_children: bool
    partner_does_not_want_children: bool

    class Config:
        from_attributes = True 


class MessageResponse(BaseModel):
    message: str 