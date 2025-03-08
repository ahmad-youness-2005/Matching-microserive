from pydantic import BaseModel, Field
from enum import Enum

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    BOTH = "both"

class GenderBase(BaseModel):
    gender: GenderEnum = Field(..., description="Gender preference")

class GenderCreate(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    gender_score: int = Field(..., description="Gender score: 0 for male, 1 for female", ge=0, le=1)

class GenderUpdate(GenderBase):
    pass

class GenderResponse(BaseModel):
    user_id: str
    male: bool
    female: bool
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str