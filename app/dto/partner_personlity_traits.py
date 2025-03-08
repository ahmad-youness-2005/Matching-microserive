from pydantic import BaseModel, Field
from typing import List

class PartnerPersonalityTraitBase(BaseModel):
    trait: str = Field(..., description="The partner personality trait")

class PartnerPersonalityTraitsBase(BaseModel):
    partner_personality_traits: List[str] = Field(..., description="List of partner personality traits")

class PartnerPersonalityTraitsCreate(PartnerPersonalityTraitsBase):
    user_id: str = Field(..., description="Unique identifier for the user")

class PartnerPersonalityTraitsUpdate(PartnerPersonalityTraitsBase):
    pass

class PartnerPersonalityTraitsResponse(BaseModel):
    user_id: str
    partner_personality_traits: List[str]

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str