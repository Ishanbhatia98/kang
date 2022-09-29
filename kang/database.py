from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from kang.custom_logger import GetLogger
from kang.base_domain_sql import Base
from  kang.conf import settings

logger = GetLogger(__name__)




#MYSQL DB SETTINGS
SQLALCHEMY_DATABASE_URL = f"mysql+mysqldb://{settings.MYSQL_USERNAME}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOSTNAME}/{settings.MYSQL_DBNAME}" 
# SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'

logger.info(f"connecting to db on {SQLALCHEMY_DATABASE_URL}")
#connect_args={"check_same_thread": False}
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base(cls=Base)
mysqldb = SessionLocal()

#flush
#mysqldb.flush()

