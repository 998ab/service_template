from sqlalchemy import Integer, String, Column, DateTime, func, Numeric


from database.entities import Base


class DbBook(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String(63))
    author = Column(String(63))
    price = Column(Numeric())
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

