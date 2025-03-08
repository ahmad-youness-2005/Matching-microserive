from pydantic import BaseModel, Field, validator

VALID_SECTS = ["sunni", "shia", "ahmadi", "ismaili", "ibadi", "other"]

class SectsBase(BaseModel):
    sects: str = Field(..., description="Sect value (e.g., 'sunni', 'shia')")
    
    @validator('sects')
    def validate_sects(cls, v):
        if v not in VALID_SECTS:
            raise ValueError(f"Invalid sect value. Must be one of: {', '.join(VALID_SECTS)}")
        return v

class SectsCreate(SectsBase):
    user_id: str = Field(..., description="Unique identifier for the user")

class SectsUpdate(SectsBase):
    pass

class SectsResponse(BaseModel):
    user_id: str
    sunni: bool
    shia: bool
    ahmadi: bool
    ismaili: bool
    ibadi: bool
    other: bool
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str 