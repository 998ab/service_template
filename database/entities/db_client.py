from global_models.service_template.client_role import ClientRole
from sqlalchemy import Integer, String, Column, DateTime, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedSet

from .db_client_book import DbClientBook

from database.entities import Base


class DbClient(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(63))
    role = Column(ENUM(ClientRole, name="client_roles"))
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    books = relationship("DbBook",
                         secondary=DbClientBook,
                         backref="clients",
                         collection_class=InstrumentedSet)
