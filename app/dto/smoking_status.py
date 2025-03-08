from pydantic import BaseModel, Field

class SmokingStatusBase(BaseModel):
    does_smoke: bool = Field(..., description="Whether the user smokes")

class SmokingStatusCreate(SmokingStatusBase):
    user_id: str = Field(..., description="Unique identifier for the user")

class SmokingStatusUpdate(SmokingStatusBase):
    pass

class SmokingStatusResponse(BaseModel):
    user_id: str
    does_smoke: bool
    
    class Config:
        from_attributes = True 

class MessageResponse(BaseModel):
    message: str 