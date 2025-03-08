from pydantic import BaseModel, Field

class DateOfBirthBase(BaseModel):
    date_of_birth: str = Field(..., description="User's date of birth (YYYY-MM-DD)")

class AgeRangeCreate(DateOfBirthBase):
    user_id: str = Field(..., description="Unique identifier for the user")

class AgeRangeUpdate(DateOfBirthBase):
    pass

class AgeRangeResponse(BaseModel):
    user_id: str
    range_18_to_24: bool
    range_25_to_34: bool
    range_35_to_44: bool
    range_above_44: bool

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str
