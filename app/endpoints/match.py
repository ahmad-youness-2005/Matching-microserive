from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from app.dto.match import CreateMatch, MatchResponse, MatchStatus, MessageResponse
from app.db.database import get_db
from app.models.match import Match

router = APIRouter(
    prefix="/match",
    tags=["match"],
    responses={404: {"description": "Not found"}}
)


@router.post("/relationship", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_match(match_data: CreateMatch, db: Session = Depends(get_db)):

    existing_match = db.query(Match).filter(
        ((Match.partner_id_1 == match_data.partner_id_1) & (Match.partner_id_2 == match_data.partner_id_2)) |
        ((Match.partner_id_1 == match_data.partner_id_2) & (Match.partner_id_2 == match_data.partner_id_1))
    ).first()
    
    if existing_match:
        raise HTTPException(status_code=400, detail="A match already exists between these users")
    
    new_match = Match(
        partner_id_1=match_data.partner_id_1,
        partner_id_2=match_data.partner_id_2,
        match_status=match_data.match_status.value,
        created_at=datetime.utcnow()
    )
    
    try:
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        
        return MessageResponse(
            message=f"Match created successfully between {match_data.partner_id_1} and {match_data.partner_id_2}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/relationship/{partner_id_1}/{partner_id_2}/accept", response_model=MatchResponse)
def accept_match(partner_id_1: str, partner_id_2: str, db: Session = Depends(get_db)):

    match = _get_match(partner_id_1, partner_id_2, db)
    
    if match.match_status != MatchStatus.REQUESTED.value:
        raise HTTPException(status_code=400, detail="Only REQUESTED matches can be accepted")
    
    match.match_status = MatchStatus.MATCHED.value
    
    try:
        db.commit()
        db.refresh(match)
        
        return MatchResponse(
            partner_id_1=match.partner_id_1,
            partner_id_2=match.partner_id_2,
            match_status=MatchStatus(match.match_status),
            created_at=match.created_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.put("/relationship/{partner_id_1}/{partner_id_2}/decline", response_model=MatchResponse)
def decline_match(partner_id_1: str, partner_id_2: str, db: Session = Depends(get_db)):
    match = _get_match(partner_id_1, partner_id_2, db)
    
    if match.match_status != MatchStatus.REQUESTED.value:
        raise HTTPException(status_code=400, detail="Only REQUESTED matches can be declined")
    
    match.match_status = MatchStatus.DECLINED.value
    
    try:
        db.commit()
        db.refresh(match)
        
        return MatchResponse(
            partner_id_1=match.partner_id_1,
            partner_id_2=match.partner_id_2,
            match_status=MatchStatus(match.match_status),
            created_at=match.created_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def _get_match(partner_id_1: str, partner_id_2: str, db: Session):
    match = db.query(Match).filter(
        ((Match.partner_id_1 == partner_id_1) & (Match.partner_id_2 == partner_id_2)) |
        ((Match.partner_id_1 == partner_id_2) & (Match.partner_id_2 == partner_id_1))
    ).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return match
