from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.db.session import get_db
from app.schemas.partner_children_expectations import PartnerChildrenExpectations
from app.dto.partner_children_expectations import (
    PartnerChildrenExpectationsCreate,
    PartnerChildrenExpectationsUpdate,
    PartnerChildrenExpectationsResponse,
    MessageResponse
)

router = APIRouter(prefix="/partner-children-expectations", tags=["Partner Children Expectations"])
logger = logging.getLogger(__name__)


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_partner_children_expectations(
    expectations: PartnerChildrenExpectationsCreate, 
    db: Session = Depends(get_db)
):
    try:
        existing_record = db.query(PartnerChildrenExpectationsScore).filter_by(
            user_id=expectations.user_id
        ).first()
        
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Record already exists for user_id {expectations.user_id}"
            )
        
        new_record = PartnerChildrenExpectationsScore(user_id=expectations.user_id)
        
        new_record.partner_wants_children = False
        new_record.partner_open_to_have_children = False
        new_record.partner_does_not_want_children = False
        
        if expectations.partner_children_expectation == "wants_children":
            new_record.partner_wants_children = True
        elif expectations.partner_children_expectation == "open_to_have_children":
            new_record.partner_open_to_have_children = True
        elif expectations.partner_children_expectation == "does_not_want_children":
            new_record.partner_does_not_want_children = True
        
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        return {"message": f"Partner children expectations for user {expectations.user_id} created successfully"}
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating partner children expectations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating partner children expectations: {str(e)}"
        )


@router.get("", response_model=List[PartnerChildrenExpectationsResponse])
def get_all_partner_children_expectations(db: Session = Depends(get_db)):
    try:
        records = db.query(PartnerChildrenExpectationsScore).all()
        return records
    
    except Exception as e:
        logger.error(f"Error retrieving partner children expectations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving partner children expectations: {str(e)}"
        )


@router.get("/{user_id}", response_model=PartnerChildrenExpectationsResponse)
def get_partner_children_expectations(user_id: str, db: Session = Depends(get_db)):
    try:
        record = db.query(PartnerChildrenExpectationsScore).filter_by(user_id=user_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner children expectations not found for user_id: {user_id}"
            )
        
        return record
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error retrieving partner children expectations for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving partner children expectations: {str(e)}"
        )


@router.put("/{user_id}", response_model=MessageResponse)
def update_partner_children_expectations(
    user_id: str, 
    expectations: PartnerChildrenExpectationsUpdate, 
    db: Session = Depends(get_db)
):
    try:
        record = db.query(PartnerChildrenExpectationsScore).filter_by(user_id=user_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner children expectations not found for user_id: {user_id}"
            )
        
        record.partner_wants_children = False
        record.partner_open_to_have_children = False
        record.partner_does_not_want_children = False
        
        if expectations.partner_children_expectation == "wants_children":
            record.partner_wants_children = True
        elif expectations.partner_children_expectation == "open_to_have_children":
            record.partner_open_to_have_children = True
        elif expectations.partner_children_expectation == "does_not_want_children":
            record.partner_does_not_want_children = True
        
        db.commit()
        db.refresh(record)
        
        return {"message": f"Partner children expectations for user {user_id} updated successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating partner children expectations for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating partner children expectations: {str(e)}"
        )


@router.delete("/{user_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_partner_children_expectations(user_id: str, db: Session = Depends(get_db)):
    try:
        record = db.query(PartnerChildrenExpectationsScore).filter_by(user_id=user_id).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner children expectations not found for user_id: {user_id}"
            )
        
        db.delete(record)
        db.commit()
        
        return {"message": f"Partner children expectations for user {user_id} deleted successfully"}
    
    except HTTPException:
        raise
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting partner children expectations for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting partner children expectations: {str(e)}"
        ) 