from pydantic import BaseModel, Field , validator
from typing import Union


class PartnerHeightBase(BaseModel):
    partner_height: Union[int, float] = Field(..., description="Height in centimeters (140-220)")

    @validator('partner_height')
    def validate_height(cls, v):
        height_float = float(v)
        if not (140.0 <= height_float <= 220.0):
            raise ValueError("Height must be between 140 and 220 cm")
        return v


class PartnerHeightCreate(PartnerHeightBase):
    user_id: str = Field(..., description="User ID")


class PartnerHeightUpdate(PartnerHeightBase):
    pass


class PartnerHeightResponse(BaseModel):
    user_id: str
    partner_range_140_to_145: bool
    partner_range_146_to_150: bool
    partner_range_151_to_155: bool
    partner_range_156_to_160: bool
    partner_range_161_to_165: bool
    partner_range_166_to_170: bool
    partner_range_171_to_175: bool
    partner_range_176_to_180: bool
    partner_range_181_to_185: bool
    partner_range_186_to_190: bool
    partner_range_191_to_195: bool
    partner_range_196_to_200: bool
    partner_range_201_to_205: bool
    partner_range_206_to_210: bool
    partner_range_211_to_215: bool
    partner_range_216_to_220: bool

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str 