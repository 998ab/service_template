# For migrations
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from database.entities.db_client import DbClient
from database.entities.db_book import DbBook
from database.entities.db_client_book import DbClientBook
