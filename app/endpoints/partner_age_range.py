from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.schemas.partner_age_range import PartnerAgeRange
from app.dto.partner_age_range import PartnerAgeRangeCreate, PartnerAgeRangeUpdate, PartnerAgeRangeResponse, MessageResponse

router = APIRouter(
    prefix="/partner-age-range",
    tags=["partner-age-range"],
    responses={404: {"description": "Not found"}},
)

def _calculate_age_range(birth_date_str: str):
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        if 18 <= age <= 24:
            return 'partner_range_18_to_24'
        elif 25 <= age <= 34:
            return 'partner_range_25_to_34'
        elif 35 <= age <= 44:
            return 'partner_range_35_to_44'
        elif age > 44:
            return 'partner_range_above_44'
        else:
            raise ValueError(f"Age {age} is not within valid range (must be 18 or older)")
    except ValueError as e:
        if "time data" in str(e):
            raise ValueError("Invalid date format. Please use YYYY-MM-DD format")
        raise e

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_partner_age_range(
    partner_age_range: PartnerAgeRangeCreate, 
    db: Session = Depends(get_db)
):
    try:
        user_id = partner_age_range.user_id
        
        existing = db.query(PartnerAgeRange).filter(PartnerAgeRange.user_id == user_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Partner age range already exists for this user")
        
        age_range_field = _calculate_age_range(partner_age_range.date_of_birth)
        
        db_partner_age_range = PartnerAgeRange(
            user_id=user_id,
            partner_range_18_to_24=False,
            partner_range_25_to_34=False,
            partner_range_35_to_44=False,
            partner_range_above_44=False
        )
        
        setattr(db_partner_age_range, age_range_field, True)
        
        db.add(db_partner_age_range)
        db.commit()
        db.refresh(db_partner_age_range)
        
        return {"message": f"Partner age range preference for user {user_id} created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/{user_id}", response_model=PartnerAgeRangeResponse)
def get_partner_age_range(user_id: str, db: Session = Depends(get_db)):
    partner_age_range = db.query(PartnerAgeRange).filter(PartnerAgeRange.user_id == user_id).first()
    if not partner_age_range:
        raise HTTPException(status_code=404, detail="Partner age range not found for this user")
    return partner_age_range

@router.put("/{user_id}", response_model=MessageResponse)
def update_partner_age_range(
    user_id: str,
    partner_age_range: PartnerAgeRangeUpdate,
    db: Session = Depends(get_db)
):
    try:
        db_partner_age_range = db.query(PartnerAgeRange).filter(PartnerAgeRange.user_id == user_id).first()
        if not db_partner_age_range:
            raise HTTPException(status_code=404, detail="Partner age range not found for this user")
        
        age_range_field = _calculate_age_range(partner_age_range.date_of_birth)
        
        db_partner_age_range.partner_range_18_to_24 = False
        db_partner_age_range.partner_range_25_to_34 = False
        db_partner_age_range.partner_range_35_to_44 = False
        db_partner_age_range.partner_range_above_44 = False
        
        setattr(db_partner_age_range, age_range_field, True)
        
        db.add(db_partner_age_range)
        db.commit()
        db.refresh(db_partner_age_range)
        
        return {"message": f"Partner age range preference for user {user_id} updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/{user_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_partner_age_range(user_id: str, db: Session = Depends(get_db)):
    try:
        db_partner_age_range = db.query(PartnerAgeRange).filter(PartnerAgeRange.user_id == user_id).first()
        if not db_partner_age_range:
            raise HTTPException(status_code=404, detail="Partner age range not found for this user")
        
        db.delete(db_partner_age_range)
        db.commit()
        
        return {"message": f"Partner age range preference for user {user_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("", response_model=List[PartnerAgeRangeResponse])
def get_all_partner_age_ranges(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    partner_age_ranges = db.query(PartnerAgeRange).offset(skip).limit(limit).all()
    return partner_age_ranges 