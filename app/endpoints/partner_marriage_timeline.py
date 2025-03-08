from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.db.session import get_db
from app.schemas.partner_marriage_timeline import PartnerMarriageTimelineScore
from app.dto.partner_marriage_timeline import (
    PartnerMarriageTimelineCreate,
    PartnerMarriageTimelineUpdate,
    PartnerMarriageTimelineResponse,
    MessageResponse
)

router = APIRouter(prefix="/partner-marriage-timeline", tags=["Partner Marriage Timeline"])
logger = logging.getLogger(__name__)


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_partner_marriage_timeline(
    timeline: PartnerMarriageTimelineCreate, 
    db: Session = Depends(get_db)
):

    try:
        existing_record = db.query(PartnerMarriageTimelineScore).filter_by(
            user_id=timeline.user_id
        ).first()
        
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Record already exists for user_id {timeline.user_id}"
            )
        
        new_record = PartnerMarriageTimelineScore(user_id=timeline.user_id)
        
        new_record.partner_agree_together = False
        new_record.partner_within_1_year = False
        new_record.partner_within_2_year = False
        new_record.partner_within_3_year = False
        new_record.partner_within_5_year = False
        
        setattr(new_record, timeline.partner_marriage_timeline, True)
        
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        return {"message": f"Partner marriage timeline for user {timeline.user_id} created successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating partner marriage timeline: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating partner marriage timeline: {str(e)}"
        )


@router.get("", response_model=List[PartnerMarriageTimelineResponse])
def get_all_partner_marriage_timelines(db: Session = Depends(get_db)):
    try:
        records = db.query(PartnerMarriageTimelineScore).all()
        if not records:
            return []
        return records
    
    except Exception as e:
        logger.error(f"Error retrieving partner marriage timelines: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving partner marriage timelines: {str(e)}"
        )


@router.get("/{user_id}", response_model=PartnerMarriageTimelineResponse)
def get_partner_marriage_timeline(user_id: str, db: Session = Depends(get_db)):
    try:
        record = db.query(PartnerMarriageTimelineScore).filter_by(user_id=user_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner marriage timeline not found for user_id: {user_id}"
            )
        
        return record
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error retrieving partner marriage timeline for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving partner marriage timeline: {str(e)}"
        )


@router.put("/{user_id}", response_model=MessageResponse)
def update_partner_marriage_timeline(
    user_id: str, 
    timeline: PartnerMarriageTimelineUpdate, 
    db: Session = Depends(get_db)
):
    try:
        record = db.query(PartnerMarriageTimelineScore).filter_by(user_id=user_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner marriage timeline not found for user_id: {user_id}"
            )
        
        record.partner_agree_together = False
        record.partner_within_1_year = False
        record.partner_within_2_year = False
        record.partner_within_3_year = False
        record.partner_within_5_year = False
        
        setattr(record, timeline.partner_marriage_timeline, True)
        
        db.commit()
        db.refresh(record)
        
        return {"message": f"Partner marriage timeline for user {user_id} updated successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating partner marriage timeline for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating partner marriage timeline: {str(e)}"
        )


@router.delete("/{user_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_partner_marriage_timeline(user_id: str, db: Session = Depends(get_db)):
    try:
        record = db.query(PartnerMarriageTimelineScore).filter_by(user_id=user_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner marriage timeline not found for user_id: {user_id}"
            )
        
        db.delete(record)
        db.commit()
        
        return {"message": "Partner marriage timeline deleted successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting partner marriage timeline for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting partner marriage timeline: {str(e)}"
        ) 