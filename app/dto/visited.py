from pydantic import BaseModel, Field


class VisitedBase(BaseModel):
    visited_user_id: str = Field(..., description="ID of the visited user")


class VisitedCreate(VisitedBase):
    user_id: str = Field(..., description="User ID")


class VisitedUpdate(BaseModel):
    user_id: str = Field(..., description="User ID")
    visited_user_id: str = Field(..., description="ID of the visited user")


class MessageResponse(BaseModel):
    message: str 