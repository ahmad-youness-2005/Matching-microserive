from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class MatchStatus(Enum):
    REQUESTED = 0
    MATCHED = 1
    DECLINED = 2


class CreateMatch(BaseModel):
    partner_id_1: str
    partner_id_2: str
    match_status: MatchStatus


class MatchResponse(BaseModel):
    partner_id_1: str
    partner_id_2: str
    match_status: MatchStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

        
class MessageResponse(BaseModel):
    message: str 