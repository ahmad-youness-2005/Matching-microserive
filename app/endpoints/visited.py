from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any, Dict
import logging

from app.db.database import get_db
from app.models.visited import VisitedScore
from app.schemas.visited import VisitedCreate, VisitedUpdate

router = APIRouter(prefix="/visited", tags=["visited"])
logger = logging.getLogger(__name__)


@router.post("", response_model=Dict[str, str], status_code=status.HTTP_201_CREATED)
def create_visited(
    *,
    db: Session = Depends(get_db),
    visited_in: VisitedCreate
) -> Any:
    try:
        existing_record = db.query(VisitedScore).filter(
            VisitedScore.user_id == visited_in.user_id,
            VisitedScore.visited_user_id == visited_in.visited_user_id
        ).first()
        
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Visit record already exists for user {visited_in.user_id} and visited user {visited_in.visited_user_id}"
            )
        
        db_obj = VisitedScore(
            user_id=visited_in.user_id,
            visited_user_id=visited_in.visited_user_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return {"message": "Visit record created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating visited record: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create visited record: {str(e)}"
        )


@router.put("", response_model=Dict[str, str])
def update_visited(
    *,
    db: Session = Depends(get_db),
    visited_in: VisitedUpdate
) -> Any:

    try:
        record = db.query(VisitedScore).filter(
            VisitedScore.user_id == visited_in.user_id,
            VisitedScore.visited_user_id == visited_in.visited_user_id
        ).first()
        
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Visit record not found for user {visited_in.user_id} and visited user {visited_in.visited_user_id}"
            )
        
        return {"message": "Visit record confirmed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating visited record: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update visited record: {str(e)}"
        ) 