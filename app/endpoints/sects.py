from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.sects import Sects
from app.dto.sects import (
    SectsCreate,
    SectsUpdate,
    SectsResponse,
    MessageResponse
)

router = APIRouter(
    prefix="/sects",
    tags=["sects"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_sects(sects: SectsCreate, db: Session = Depends(get_db)):
    try:
        existing_record = db.query(SectsScore).filter(SectsScore.user_id == sects.user_id).first()
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The record with id {sects.user_id} already exists"
            )
        
        new_sects = SectsScore(user_id=sects.user_id)
        
        for field in new_sects.__dict__:
            if isinstance(getattr(new_sects, field, None), bool):
                setattr(new_sects, field, False)
        
        setattr(new_sects, sects.sects, True)
        
        db.add(new_sects)
        db.commit()
        db.refresh(new_sects)
        
        return {"message": f"Sects for user {sects.user_id} created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("", response_model=List[SectsResponse])
def get_all_sects_preferences(db: Session = Depends(get_db)):
    try:
        sects = db.query(SectsScore).all()
        if not sects:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sects records found")
        return sects
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{user_id}", response_model=SectsResponse)
def get_user_sects(user_id: str, db: Session = Depends(get_db)):
    try:
        sects = db.query(SectsScore).filter(SectsScore.user_id == user_id).first()
        if not sects:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sects not found for user {user_id}")
        return sects
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{user_id}", response_model=MessageResponse)
def update_sects(user_id: str, sects: SectsUpdate, db: Session = Depends(get_db)):
    try:
        db_sects = db.query(SectsScore).filter(SectsScore.user_id == user_id).first()
        if not db_sects:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sects not found for user {user_id}")
        
        for field in db_sects.__dict__:
            if isinstance(getattr(db_sects, field, None), bool):
                setattr(db_sects, field, False)
        
        setattr(db_sects, sects.sects, True)
        
        db.commit()
        db.refresh(db_sects)
        return {"message": f"Sects for user {user_id} updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{user_id}", response_model=MessageResponse)
def delete_sects(user_id: str, db: Session = Depends(get_db)):
    try:
        db_sects = db.query(SectsScore).filter(SectsScore.user_id == user_id).first()
        if not db_sects:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sects not found for user {user_id}")
        
        db.delete(db_sects)
        db.commit()
        return {"message": f"Sects for user {user_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 