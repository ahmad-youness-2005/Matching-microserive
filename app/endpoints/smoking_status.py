from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.smoking_status import SmokingStatusScore
from app.dto.smoking_status import (
    SmokingStatusBase,
    SmokingStatusCreate,
    SmokingStatusUpdate,
    SmokingStatusResponse,
    MessageResponse
)

router = APIRouter(
    prefix="/smoking-status",
    tags=["smoking-status"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_smoking_status(smoking_status: SmokingStatusCreate, db: Session = Depends(get_db)):
    try:
        existing_record = db.query(SmokingStatusScore).filter(SmokingStatusScore.user_id == smoking_status.user_id).first()
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The record with id {smoking_status.user_id} already exists"
            )
        
        new_smoking_status = SmokingStatusScore(
            user_id=smoking_status.user_id,
            does_smoke=smoking_status.does_smoke
        )
        
        db.add(new_smoking_status)
        db.commit()
        db.refresh(new_smoking_status)
        
        return {"message": f"Smoking status for user {smoking_status.user_id} created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("", response_model=List[SmokingStatusResponse])
def get_all_smoking_statuses(db: Session = Depends(get_db)):
    try:
        smoking_statuses = db.query(SmokingStatusScore).all()
        if not smoking_statuses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No smoking status records found")
        return smoking_statuses
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{user_id}", response_model=SmokingStatusResponse)
def get_smoking_status(user_id: str, db: Session = Depends(get_db)):
    try:
        smoking_status = db.query(SmokingStatusScore).filter(SmokingStatusScore.user_id == user_id).first()
        if not smoking_status:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Smoking status not found for user {user_id}")
        return smoking_status
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{user_id}", response_model=MessageResponse)
def update_smoking_status(user_id: str, smoking_status: SmokingStatusUpdate, db: Session = Depends(get_db)):
    try:
        db_smoking_status = db.query(SmokingStatusScore).filter(SmokingStatusScore.user_id == user_id).first()
        if not db_smoking_status:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Smoking status not found for user {user_id}")
        
        db_smoking_status.does_smoke = smoking_status.does_smoke
        
        db.commit()
        db.refresh(db_smoking_status)
        return {"message": f"Smoking status for user {user_id} updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{user_id}", response_model=MessageResponse)
def delete_smoking_status(user_id: str, db: Session = Depends(get_db)):
    try:
        db_smoking_status = db.query(SmokingStatusScore).filter(SmokingStatusScore.user_id == user_id).first()
        if not db_smoking_status:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Smoking status not found for user {user_id}")
        
        db.delete(db_smoking_status)
        db.commit()
        return {"message": f"Smoking status for user {user_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 