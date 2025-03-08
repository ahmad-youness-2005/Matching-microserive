from pydantic import BaseModel, Field

class PartnerDateOfBirthBase(BaseModel):
    date_of_birth: str = Field(..., description="Partner's date of birth (YYYY-MM-DD)")

class PartnerAgeRangeCreate(PartnerDateOfBirthBase):
    user_id: str = Field(..., description="Unique identifier for the user")

class PartnerAgeRangeUpdate(PartnerDateOfBirthBase):
    pass

class PartnerAgeRangeResponse(BaseModel):
    user_id: str
    partner_range_18_to_24: bool
    partner_range_25_to_34: bool
    partner_range_35_to_44: bool
    partner_range_above_44: bool

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str 