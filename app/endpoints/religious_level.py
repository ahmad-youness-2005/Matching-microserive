from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.religious_level import ReligiousLevel
from app.dto.religious_level import (
    ReligiousLevelBase, 
    ReligiousLevelCreate, 
    ReligiousLevelUpdate, 
    ReligiousLevelResponse,
    MessageResponse
)

router = APIRouter(
    prefix="/religious-level",
    tags=["religious-level"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_religious_level(religious_level: ReligiousLevelCreate, db: Session = Depends(get_db)):
    try:
        existing_record = db.query(ReligiousLevelScore).filter(ReligiousLevelScore.user_id == religious_level.user_id).first()
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The record with id {religious_level.user_id} already exists"
            )
        
        new_religious_level = ReligiousLevelScore(user_id=religious_level.user_id)
        
        new_religious_level.very_practising = False
        new_religious_level.practising = False
        new_religious_level.moderately_practising = False
        new_religious_level.not_practising = False
        
        setattr(new_religious_level, religious_level.religious_level, True)
        
        db.add(new_religious_level)
        db.commit()
        db.refresh(new_religious_level)
        
        return {"message": f"Religious level for user {religious_level.user_id} created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("", response_model=List[ReligiousLevelResponse])
def get_all_religious_level_preferences(db: Session = Depends(get_db)):
    try:
        religious_levels = db.query(ReligiousLevelScore).all()
        if not religious_levels:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No religious level records found")
        return religious_levels
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{user_id}", response_model=ReligiousLevelResponse)
def get_religious_level(user_id: str, db: Session = Depends(get_db)):
    try:
        religious_level = db.query(ReligiousLevelScore).filter(ReligiousLevelScore.user_id == user_id).first()
        if not religious_level:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Religious level not found for user {user_id}")
        return religious_level
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{user_id}", response_model=MessageResponse)
def update_religious_level(user_id: str, religious_level: ReligiousLevelUpdate, db: Session = Depends(get_db)):
    try:
        db_religious_level = db.query(ReligiousLevelScore).filter(ReligiousLevelScore.user_id == user_id).first()
        if not db_religious_level:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Religious level not found for user {user_id}")
        
        db_religious_level.very_practising = False
        db_religious_level.practising = False
        db_religious_level.moderately_practising = False
        db_religious_level.not_practising = False
        
        setattr(db_religious_level, religious_level.religious_level, True)
        
        db.commit()
        db.refresh(db_religious_level)
        return {"message": f"Religious level for user {user_id} updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{user_id}", response_model=MessageResponse)
def delete_religious_level(user_id: str, db: Session = Depends(get_db)):
    try:
        db_religious_level = db.query(ReligiousLevelScore).filter(ReligiousLevelScore.user_id == user_id).first()
        if not db_religious_level:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Religious level not found for user {user_id}")
        
        db.delete(db_religious_level)
        db.commit()
        return {"message": f"Religious level for user {user_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 