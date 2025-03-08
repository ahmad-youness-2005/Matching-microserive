from pydantic import BaseModel, Field
from typing import Literal

class PrayerFrequencyBase(BaseModel):
    prayer_frequency: Literal["always_prays", "usually_prays", "sometimes_prays","never_prays"] = Field(..., description="The user's prayer frequency")

class PrayerFrequencyCreate(PrayerFrequencyBase):
    user_id: str = Field(..., description="Unique identifier for the user")

class PrayerFrequencyUpdate(PrayerFrequencyBase):
    pass

class PrayerFrequencyResponse(BaseModel):
    user_id: str
    always_pray: bool
    usually_pray: bool
    sometimes_pray: bool
    never_pray: bool

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str
