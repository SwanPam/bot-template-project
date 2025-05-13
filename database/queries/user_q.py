from typing import Optional
from sqlalchemy import select
from database.engine import async_session
from utils.logger import setup_logger
from database.queries import *

logger = setup_logger(__name__)
