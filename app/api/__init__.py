from fastapi import APIRouter

# Import all routers from endpoints
from app.endpoints.age_range import router as age_range_router
from app.endpoints.gender import router as gender_router
from app.endpoints.match import router as match_router
from app.endpoints.partner_age_range import router as partner_age_range_router
from app.endpoints.partner_children_expectations import router as partner_children_expectations_router
from app.endpoints.partner_ethnics import router as partner_ethnics_router
from app.endpoints.partner_height import router as partner_height_router
from app.endpoints.partner_marriage_timeline import router as partner_marriage_timeline_router
from app.endpoints.partner_personality_traits import router as partner_personality_traits_router
from app.endpoints.prayer_frequency import router as prayer_frequency_router
from app.endpoints.religious_level import router as religious_level_router
from app.endpoints.sects import router as sects_router
from app.endpoints.smoking_status import router as smoking_status_router
from app.endpoints.visited import router as visited_router

api_router = APIRouter()

# Include all routers
api_router.include_router(age_range_router, prefix="/age-range", tags=["age-range"])
api_router.include_router(gender_router, prefix="/gender", tags=["gender"])
api_router.include_router(match_router, prefix="/match", tags=["match"])
api_router.include_router(partner_age_range_router, prefix="/partner-age-range", tags=["partner-age-range"])
api_router.include_router(partner_children_expectations_router, prefix="/partner-children-expectations", tags=["partner-children-expectations"])
api_router.include_router(partner_ethnics_router, prefix="/partner-ethnics", tags=["partner-ethnics"])
api_router.include_router(partner_height_router, prefix="/partner-height", tags=["partner-height"])
api_router.include_router(partner_marriage_timeline_router, prefix="/partner-marriage-timeline", tags=["partner-marriage-timeline"])
api_router.include_router(partner_personality_traits_router, prefix="/partner-personality-traits", tags=["partner-personality-traits"])
api_router.include_router(prayer_frequency_router, prefix="/prayer-frequency", tags=["prayer-frequency"])
api_router.include_router(religious_level_router, prefix="/religious-level", tags=["religious-level"])
api_router.include_router(sects_router, prefix="/sects", tags=["sects"])
api_router.include_router(smoking_status_router, prefix="/smoking-status", tags=["smoking-status"])
api_router.include_router(visited_router, prefix="/visited", tags=["visited"]) 