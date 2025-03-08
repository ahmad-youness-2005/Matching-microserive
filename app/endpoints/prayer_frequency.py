from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging

from app.db.database import get_db
from app.schemas.prayer_frequency import PrayerFrequencyScore
from app.dto.prayer_frequency import (
    PrayerFrequencyCreate, 
    PrayerFrequencyUpdate, 
    PrayerFrequencyResponse,
    MessageResponse
)

router = APIRouter(
    prefix="/prayer-frequency",
    tags=["prayer-frequency"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_prayer_frequency(prayer_frequency: PrayerFrequencyCreate, db: Session = Depends(get_db)):
    try:
        db_prayer_frequency = db.query(PrayerFrequencyScore).filter(PrayerFrequencyScore.user_id == prayer_frequency.user_id).first()
        if db_prayer_frequency:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {prayer_frequency.user_id} already has a prayer frequency preference"
            )
        
        db_prayer_frequency = PrayerFrequencyScore(
            user_id=prayer_frequency.user_id,
            always_pray=False,
            usually_pray=False,
            sometimes_pray=False,
            never_pray=False
        )
        
        if prayer_frequency.prayer_frequency == "always_prays":
            db_prayer_frequency.always_pray = True
        elif prayer_frequency.prayer_frequency == "usually_prays":
            db_prayer_frequency.usually_pray = True
        elif prayer_frequency.prayer_frequency == "sometimes_prays":
            db_prayer_frequency.sometimes_pray = True
        elif prayer_frequency.prayer_frequency == "never_prays":
            db_prayer_frequency.never_pray = True
        
        db.add(db_prayer_frequency)
        db.commit()
        db.refresh(db_prayer_frequency)
        return {"message": f"Prayer frequency preference for user {prayer_frequency.user_id} created successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating prayer frequency: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.get("", response_model=List[PrayerFrequencyResponse])
def get_all_prayer_frequency_preferences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        prayer_frequencies = db.query(PrayerFrequencyScore).offset(skip).limit(limit).all()
        if not prayer_frequencies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No prayer frequency preferences found"
            )
        return prayer_frequencies
    except Exception as e:
        logger.error(f"Error retrieving all prayer frequencies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.get("/{user_id}", response_model=PrayerFrequencyResponse)
def get_prayer_frequency(user_id: str, db: Session = Depends(get_db)):
    try:
        prayer_frequency = db.query(PrayerFrequencyScore).filter(PrayerFrequencyScore.user_id == user_id).first()
        if not prayer_frequency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prayer frequency preference for user {user_id} not found"
            )
        return prayer_frequency
    except Exception as e:
        logger.error(f"Error retrieving prayer frequency for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.put("/{user_id}", response_model=MessageResponse)
def update_prayer_frequency(user_id: str, prayer_frequency: PrayerFrequencyUpdate, db: Session = Depends(get_db)):
    try:
        db_prayer_frequency = db.query(PrayerFrequencyScore).filter(PrayerFrequencyScore.user_id == user_id).first()
        if not db_prayer_frequency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prayer frequency preference for user {user_id} not found"
            )
        
        db_prayer_frequency.always_pray = False
        db_prayer_frequency.usually_pray = False
        db_prayer_frequency.sometimes_pray = False
        db_prayer_frequency.never_pray = False
        
        if prayer_frequency.prayer_frequency == "always_prays":
            db_prayer_frequency.always_pray = True
        elif prayer_frequency.prayer_frequency == "usually_prays":
            db_prayer_frequency.usually_pray = True
        elif prayer_frequency.prayer_frequency == "sometimes_prays":
            db_prayer_frequency.sometimes_pray = True
        elif prayer_frequency.prayer_frequency == "never_prays":
            db_prayer_frequency.never_pray = True
        
        db.commit()
        db.refresh(db_prayer_frequency)
        return {"message": f"Prayer frequency preference for user {user_id} updated successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating prayer frequency for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.delete("/{user_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_prayer_frequency(user_id: str, db: Session = Depends(get_db)):
    try:
        db_prayer_frequency = db.query(PrayerFrequencyScore).filter(PrayerFrequencyScore.user_id == user_id).first()
        if not db_prayer_frequency:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Prayer frequency preference for user {user_id} not found"
            )
        
        db.delete(db_prayer_frequency)
        db.commit()
        return {"message": f"Prayer frequency preference for user {user_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting prayer frequency for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        ) 