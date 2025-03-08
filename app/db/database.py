import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable not found. Please check your .env file.")
    raise ValueError("DATABASE_URL environment variable not found")

try:
    if '@' in DATABASE_URL:
        logger.info(f"Using database URL: {DATABASE_URL.split('@')[0].split(':')[0]}:***@{DATABASE_URL.split('@')[1]}")
    else:
        logger.info(f"Using database URL: {DATABASE_URL}")
except Exception as e:
    logger.info(f"Using database URL: [URL parsing error - showing truncated] {DATABASE_URL.split('://')[0]}://...")

try:
    engine = create_engine(DATABASE_URL)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base = declarative_base()
    
    logger.info("Database connection established successfully")
except Exception as e:
    logger.error(f"Error connecting to database: {str(e)}")
    raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 