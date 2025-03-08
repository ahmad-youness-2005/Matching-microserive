from pydantic import BaseModel, Field
from typing import List

class PartnerEthnicsBase(BaseModel):
    partner_ethnic_origins: List[str] = Field(..., description="List of partner ethnic origins")

class PartnerEthnicsCreate(PartnerEthnicsBase):
    user_id: str = Field(..., description="Unique identifier for the user")

class PartnerEthnicsUpdate(PartnerEthnicsBase):
    pass

class PartnerEthnicsResponse(BaseModel):
    user_id: str
    partner_ethnic_origins: List[str]

    class Config:
        from_attributes = True

class PartnerEthnicsListResponse(BaseModel):
    user_id: str
    partner_ethnic_origins: List[str]

class MessageResponse(BaseModel):
    message: str    
