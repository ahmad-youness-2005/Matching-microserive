from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db
from app.schemas.partner_ethnics_score import PartnerEthnicsScore
from app.dto.partner_ethnics_score import (
    PartnerEthnicsBase,
    PartnerEthnicsCreate,
    PartnerEthnicsUpdate,
    PartnerEthnicsResponse,
    MessageResponse
)

router = APIRouter(
    prefix="/partner-ethnics",
    tags=["Partner Ethnics"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_partner_ethnics(partner_ethnics: PartnerEthnicsCreate, db: Session = Depends(get_db)):
    try:
        existing_record = db.query(PartnerEthnicsScore).filter(PartnerEthnicsScore.user_id == partner_ethnics.user_id).first()
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Partner ethnics preference for user {partner_ethnics.user_id} already exists"
            )
        
        new_partner_ethnics = PartnerEthnicsScore(user_id=partner_ethnics.user_id)
        
        for ethnicity in partner_ethnics.partner_ethnic_origins:
            if hasattr(new_partner_ethnics, ethnicity):
                setattr(new_partner_ethnics, ethnicity, True)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid ethnicity: {ethnicity}"
                )
        
        db.add(new_partner_ethnics)
        db.commit()
        
        return {"message": f"Partner ethnics preferences for user {partner_ethnics.user_id} created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("", response_model=List[PartnerEthnicsResponse])
def get_all_partner_ethnics(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        partner_ethnics_list = db.query(PartnerEthnicsScore).offset(skip).limit(limit).all()
        if not partner_ethnics_list:
            raise HTTPException(status_code=404, detail="No partner ethnics preferences found")
        
        result = []
        for ethnics in partner_ethnics_list:
            active_ethnicities = [field for field in dir(ethnics) 
                               if not field.startswith('_') and 
                               field != 'user_id' and
                               not callable(getattr(ethnics, field)) and
                               getattr(ethnics, field, False) is True]
            result.append({
                "user_id": ethnics.user_id,
                "partner_ethnic_origins": active_ethnicities
            })
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/available", response_model=List[str])
def get_available_ethnicities():
    return get_all_available_ethnicities()

@router.get("/{user_id}", response_model=PartnerEthnicsResponse)
def get_partner_ethnics(user_id: str, db: Session = Depends(get_db)):
    try:
        partner_ethnics = db.query(PartnerEthnicsScore).filter(PartnerEthnicsScore.user_id == user_id).first()
        if not partner_ethnics:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Partner ethnics preference not found for user {user_id}")
        
        active_ethnicities = [field for field in dir(partner_ethnics) 
                           if not field.startswith('_') and 
                           field != 'user_id' and
                           not callable(getattr(partner_ethnics, field)) and
                           getattr(partner_ethnics, field, False) is True]
        
        return {
            "user_id": partner_ethnics.user_id,
            "partner_ethnic_origins": active_ethnicities
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{user_id}", response_model=MessageResponse)
def update_partner_ethnics(user_id: str, partner_ethnics: PartnerEthnicsUpdate, db: Session = Depends(get_db)):
    try:
        db_partner_ethnics = db.query(PartnerEthnicsScore).filter(PartnerEthnicsScore.user_id == user_id).first()
        if not db_partner_ethnics:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Partner ethnics preference not found for user {user_id}")
        
        ethnicity_fields = [field for field in dir(db_partner_ethnics) 
                          if not field.startswith('_') and 
                          field != 'user_id' and
                          not callable(getattr(db_partner_ethnics, field))]
        
        for field in ethnicity_fields:
            setattr(db_partner_ethnics, field, False)
        
        for ethnicity in partner_ethnics.partner_ethnic_origins:
            if hasattr(db_partner_ethnics, ethnicity):
                setattr(db_partner_ethnics, ethnicity, True)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid ethnicity: {ethnicity}"
                )
        
        db.commit()
        
        return {"message": f"Partner ethnics preferences for user {user_id} updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{user_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_partner_ethnics(user_id: str, db: Session = Depends(get_db)):
    try:
        db_partner_ethnics = db.query(PartnerEthnicsScore).filter(PartnerEthnicsScore.user_id == user_id).first()
        if not db_partner_ethnics:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Partner ethnics preference not found for user {user_id}")
        
        db.delete(db_partner_ethnics)
        db.commit()
        return {"message": f"Partner ethnics preferences for user {user_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 