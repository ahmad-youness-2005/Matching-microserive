from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.gender import Gender
from app.dto.gender import (
    GenderCreate,
    GenderResponse,
    MessageResponse
)

router = APIRouter(
    prefix="/gender",
    tags=["gender"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_gender(gender: GenderCreate, db: Session = Depends(get_db)):
    try:
        existing_record = db.query(GenderScore).filter(GenderScore.user_id == gender.user_id).first()
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The record with id {gender.user_id} already exists"
            )
        
        new_gender = GenderScore(user_id=gender.user_id)
        
        if gender.gender_score == 0:
            new_gender.male = True
            new_gender.female = False
        elif gender.gender_score == 1:
            new_gender.male = False
            new_gender.female = True
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid gender_score. Must be 0 (male) or 1 (female)"
            )
        
        db.add(new_gender)
        db.commit()
        
        return MessageResponse(message=f"Gender preference for user {gender.user_id} created successfully")
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the gender preference: {str(e)}"
        )

@router.get("/{user_id}", response_model=GenderResponse)
def get_gender(user_id: str, db: Session = Depends(get_db)):
    gender = db.query(GenderScore).filter(GenderScore.user_id == user_id).first()
    if not gender:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gender preference for user with id {user_id} not found"
        )
    return gender