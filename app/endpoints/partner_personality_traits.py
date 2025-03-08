from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

from app.db.database import get_db
from app.schemas.partner_personality_traits import PartnerPersonalityTraitsScore
from app.dto.partner_personality_traits import (
    PartnerPersonalityTraitsCreate,
    PartnerPersonalityTraitsUpdate,
    PartnerPersonalityTraitsResponse,
    MessageResponse
)

router = APIRouter(
    prefix="/partner-personality-traits", 
    tags=["partner-personality-traits"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)

def _traits_to_dict(user: PartnerPersonalityTraitsScore) -> Dict[str, Any]:
    traits = []
    for column in user.__table__.columns:
        if column.name != 'user_id' and getattr(user, column.name) is True:
            traits.append(column.name)
    return {"user_id": user.user_id, "partner_personality_traits": traits}

@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_partner_personality_traits(partner_traits: PartnerPersonalityTraitsCreate, db: Session = Depends(get_db)):
    try:
        db_partner_traits = db.query(PartnerPersonalityTraitsScore).filter(
            PartnerPersonalityTraitsScore.user_id == partner_traits.user_id
        ).first()
        
        if db_partner_traits:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {partner_traits.user_id} already has partner personality traits preferences"
            )
        
        db_user = PartnerPersonalityTraitsScore(user_id=partner_traits.user_id)
        
        for trait in partner_traits.partner_personality_traits:
            if hasattr(db_user, trait):
                setattr(db_user, trait, True)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {"message": f"Partner personality traits for user {partner_traits.user_id} created successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating partner personality traits: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.get("", response_model=List[PartnerPersonalityTraitsResponse])
def get_all_partner_personality_traits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        users = db.query(PartnerPersonalityTraitsScore).offset(skip).limit(limit).all()
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No partner personality traits preferences found"
            )
        
        return [_traits_to_dict(user) for user in users]
    except Exception as e:
        logger.error(f"Error retrieving all partner personality traits: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.get("/{user_id}", response_model=PartnerPersonalityTraitsResponse)
def get_partner_personality_traits(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(PartnerPersonalityTraitsScore).filter(
            PartnerPersonalityTraitsScore.user_id == user_id
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner personality traits preferences for user {user_id} not found"
            )
        
        return _traits_to_dict(user)
    except Exception as e:
        logger.error(f"Error retrieving partner personality traits for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )

@router.put("/{user_id}", response_model=MessageResponse)
def update_partner_personality_traits(user_id: str, partner_traits: PartnerPersonalityTraitsUpdate, db: Session = Depends(get_db)):
    try:
        user = db.query(PartnerPersonalityTraitsScore).filter(
            PartnerPersonalityTraitsScore.user_id == user_id
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner personality traits preferences for user {user_id} not found"
            )
        
        # Reset all traits to False
        for column in user.__table__.columns:
            if column.name != 'user_id':
                setattr(user, column.name, False)
        
        # Set the specified traits to True
        for trait in partner_traits.partner_personality_traits:
            if hasattr(user, trait):
                setattr(user, trait, True)
        
        db.commit()
        db.refresh(user)
        
        # Return success message
        return {"message": f"Partner personality traits for user {user_id} updated successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating partner personality traits for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )


@router.delete("/{user_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_partner_personality_traits(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(PartnerPersonalityTraitsScore).filter(
            PartnerPersonalityTraitsScore.user_id == user_id
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Partner personality traits preferences for user {user_id} not found"
            )
        
        db.delete(user)
        db.commit()
        
        return {"message": f"Partner personality traits for user {user_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting partner personality traits for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        ) 