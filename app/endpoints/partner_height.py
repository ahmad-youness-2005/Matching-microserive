from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.db.session import get_db
from app.schemas.partner_height import PartnerHeightScore
from app.dto.partner_height import (
    PartnerHeightCreate,
    PartnerHeightUpdate,
    PartnerHeightResponse,
    MessageResponse
)

router = APIRouter(prefix="/partner-height", tags=["Partner Height"])
logger = logging.getLogger(__name__)


def _get_range_field(height):
    """Helper method to determine which height range field to set"""
    try:
        height_float = float(height)
        
        rounded_height = round(height_float)
        
        height_ranges = {
            (140, 145): 'partner_range_140_to_145',
            (146, 150): 'partner_range_146_to_150',
            (151, 155): 'partner_range_151_to_155',
            (156, 160): 'partner_range_156_to_160',
            (161, 165): 'partner_range_161_to_165',
            (166, 170): 'partner_range_166_to_170',
            (171, 175): 'partner_range_171_to_175',
            (176, 180): 'partner_range_176_to_180',
            (181, 185): 'partner_range_181_to_185',
            (186, 190): 'partner_range_186_to_190',
            (191, 195): 'partner_range_191_to_195',
            (196, 200): 'partner_range_196_to_200',
            (201, 205): 'partner_range_201_to_205',
            (206, 210): 'partner_range_206_to_210',
            (211, 215): 'partner_range_211_to_215',
            (216, 220): 'partner_range_216_to_220'
        }

        for (min_height, max_height), field_name in height_ranges.items():
            if min_height <= rounded_height <= max_height:
                return field_name
                
        raise ValueError(f"Height {height} is not within valid range (140-220 cm)")
    except Exception as e:
        raise ValueError(f"Invalid height value: {height}. Please provide a valid number between 140 and 220 cm")


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_partner_height(
    height_data: PartnerHeightCreate, 
    db: Session = Depends(get_db)
):
    try:
        existing_record = db.query(PartnerHeightScore).filter_by(
            user_id=height_data.user_id
        ).first()
        
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Record already exists for user_id {height_data.user_id}"
            )
        
        new_record = PartnerHeightScore(user_id=height_data.user_id)
        
        ranges = [
            (140, 145), (146, 150), (151, 155), (156, 160),
            (161, 165), (166, 170), (171, 175), (176, 180),
            (181, 185), (186, 190), (191, 195), (196, 200),
            (201, 205), (206, 210), (211, 215), (216, 220)
        ]
        for start, end in ranges:
            field_name = f'partner_range_{start}_to_{end}'
            setattr(new_record, field_name, False)
        
        try:
            range_field = _get_range_field(height_data.partner_height)
            setattr(new_record, range_field, True)
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
        
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        return {"message": f"Partner height for user {height_data.user_id} created successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating partner height: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating partner height: {str(e)}"
        )


@router.get("", response_model=List[PartnerHeightResponse])
def get_all_partner_heights(db: Session = Depends(get_db)):
    try:
        partner_heights = db.query(PartnerHeightScore).all()
        return partner_heights
    except Exception as e:
        logger.error(f"Error retrieving partner heights: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{user_id}", response_model=PartnerHeightResponse)
def get_partner_height(user_id: str, db: Session = Depends(get_db)):
    try:
        record = db.query(PartnerHeightScore).filter_by(user_id=user_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner height not found for user_id: {user_id}"
            )
        
        return record
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error retrieving partner height for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving partner height: {str(e)}"
        )


@router.put("/{user_id}", response_model=MessageResponse)
def update_partner_height(
    user_id: str, 
    height_data: PartnerHeightUpdate, 
    db: Session = Depends(get_db)
):
    try:
        record = db.query(PartnerHeightScore).filter_by(user_id=user_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner height not found for user_id: {user_id}"
            )
        
        ranges = [
            (140, 145), (146, 150), (151, 155), (156, 160),
            (161, 165), (166, 170), (171, 175), (176, 180),
            (181, 185), (186, 190), (191, 195), (196, 200),
            (201, 205), (206, 210), (211, 215), (216, 220)
        ]
        for start, end in ranges:
            field_name = f'partner_range_{start}_to_{end}'
            setattr(record, field_name, False)
        
        try:
            range_field = _get_range_field(height_data.partner_height)
            setattr(record, range_field, True)
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
        
        db.commit()
        db.refresh(record)
        
        return {"message": f"Partner height for user {user_id} updated successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating partner height for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating partner height: {str(e)}"
        )


@router.delete("/{user_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_partner_height(user_id: str, db: Session = Depends(get_db)):
    try:
        record = db.query(PartnerHeightScore).filter_by(user_id=user_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner height not found for user_id: {user_id}"
            )
        
        db.delete(record)
        db.commit()
        
        return {"message": "Partner height deleted successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting partner height for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting partner height: {str(e)}"
        ) 