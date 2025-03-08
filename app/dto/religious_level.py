from pydantic import BaseModel, Field, validator
    
VALID_RELIGIOUS_LEVELS = ["very_practising", "practising", "moderately_practising", "not_practising"]

class ReligiousLevelBase(BaseModel):
    religious_level: str = Field(..., description="Religious level preference")
    
    @validator('religious_level')
    def validate_religious_level(cls, v):
        if v not in VALID_RELIGIOUS_LEVELS:
            raise ValueError(f"Invalid religious level value. Must be one of: {', '.join(VALID_RELIGIOUS_LEVELS)}")
        return v

class ReligiousLevelCreate(ReligiousLevelBase):
    user_id: str = Field(..., description="Unique identifier for the user")

class ReligiousLevelUpdate(ReligiousLevelBase):
    pass

class ReligiousLevelResponse(BaseModel):
    user_id: str
    very_practising: bool
    practising: bool
    moderately_practising: bool
    not_practising: bool
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str 