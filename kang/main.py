from fastapi import FastAPI
from kang.custom_logger import GetLogger
from kang.database import Base, engine
from routers import file_parser

Base.metadata.create_all(bind=engine)

app = FastAPI()

logger = GetLogger(__name__)
logger.info('starting the project....')

app.include_router(file_parser.router)