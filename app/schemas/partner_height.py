from sqlalchemy import Column, Boolean, Text
from app.db.database import Base


class PartnerHeightScore(Base):
    __tablename__ = "partner_height_score"
    
    user_id = Column(Text, primary_key=True, nullable=False)
    
    partner_range_140_to_145 = Column(Boolean, default=False)
    partner_range_146_to_150 = Column(Boolean, default=False) 
    partner_range_151_to_155 = Column(Boolean, default=False) 
    partner_range_156_to_160 = Column(Boolean, default=False) 
    partner_range_161_to_165 = Column(Boolean, default=False) 
    partner_range_166_to_170 = Column(Boolean, default=False) 
    partner_range_171_to_175 = Column(Boolean, default=False) 
    partner_range_176_to_180 = Column(Boolean, default=False) 
    partner_range_181_to_185 = Column(Boolean, default=False) 
    partner_range_186_to_190 = Column(Boolean, default=False) 
    partner_range_191_to_195 = Column(Boolean, default=False) 
    partner_range_196_to_200 = Column(Boolean, default=False) 
    partner_range_201_to_205 = Column(Boolean, default=False) 
    partner_range_206_to_210 = Column(Boolean, default=False) 
    partner_range_211_to_215 = Column(Boolean, default=False) 
    partner_range_216_to_220 = Column(Boolean, default=False) 