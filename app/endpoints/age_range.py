from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.schemas.age_range import AgeRange
from app.dto.age_range import AgeRangeCreate, AgeRangeUpdate, AgeRangeResponse, MessageResponse

router = APIRouter(
    prefix="/age-range",
    tags=["age-range"],
    responses={404: {"description": "Not found"}},
)

def _calculate_age_range(birth_date_str: str):
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        if 18 <= age <= 24:
            return 'range_18_to_24'
        elif 25 <= age <= 34:
            return 'range_25_to_34'
        elif 35 <= age <= 44:
            return 'range_35_to_44'
        elif age > 44:
            return 'range_above_44'
        else:
            raise ValueError(f"Age {age} is not within valid range (must be 18 or older)")
    except ValueError as e:
        if "time data" in str(e):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD format")
        raise e

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_age_range(age_range: AgeRangeCreate, db: Session = Depends(get_db)):
    try:     
        existing_record = db.query(AgeRangeScore).filter(AgeRangeScore.user_id == age_range.user_id).first()
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Age range preference already exists for user {age_range.user_id}"
            )
            
        age_range_field = _calculate_age_range(age_range.date_of_birth)
        
        db_age_range = AgeRangeScore(
            user_id=age_range.user_id,
            range_18_to_24=False,
            range_25_to_34=False,
            range_35_to_44=False,
            range_above_44=False
        )
        
        setattr(db_age_range, age_range_field, True)
        
        db.add(db_age_range)
        db.commit()
        db.refresh(db_age_range)
        
        return {"message": f"Age range preference for user {age_range.user_id} created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("", response_model=List[AgeRangeResponse])
def get_all_age_ranges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        age_ranges = db.query(AgeRangeScore).offset(skip).limit(limit).all()
        if not age_ranges:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No age range records found")
        return age_ranges
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{user_id}", response_model=AgeRangeResponse)
def get_age_range(user_id: str, db: Session = Depends(get_db)):
    try:
        age_range = db.query(AgeRangeScore).filter(AgeRangeScore.user_id == user_id).first()
        if not age_range:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Age range not found for user {user_id}")
        return age_range
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{user_id}", response_model=MessageResponse)
def update_age_range(user_id: str, age_range: AgeRangeUpdate, db: Session = Depends(get_db)):
    try:
        db_age_range = db.query(AgeRangeScore).filter(AgeRangeScore.user_id == user_id).first()
        if not db_age_range:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Age range not found for user {user_id}")
        
        age_range_field = _calculate_age_range(age_range.date_of_birth)
        
        db_age_range.range_18_to_24 = False
        db_age_range.range_25_to_34 = False
        db_age_range.range_35_to_44 = False
        db_age_range.range_above_44 = False
        
        setattr(db_age_range, age_range_field, True)
        
        db.commit()
        db.refresh(db_age_range)
        
        return {"message": f"Age range preference for user {user_id} updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{user_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_age_range(user_id: str, db: Session = Depends(get_db)):
    try:
        db_age_range = db.query(AgeRangeScore).filter(AgeRangeScore.user_id == user_id).first()
        if not db_age_range:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Age range not found for user {user_id}")
        
        db.delete(db_age_range)
        db.commit()
        return {"message": f"Age range preference for user {user_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 