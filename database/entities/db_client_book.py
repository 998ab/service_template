from sqlalchemy import Integer, Column, DateTime, func, ForeignKey, Table, UniqueConstraint

from database.entities import Base

# class DbClientBook(Base):
#     __tablename__ = 'clients_books'
#     client_id = Column(Integer, primary_key=True)
#     book_id = Column(Integer, primary_key=True)
#     creation_date = Column(DateTime(timezone=True), server_default=func.now())

# class DbClientBook(Base):
#     __table__ = Table('client_book',
#                       Base.metadata,
#                       Column('client_id', Integer, ForeignKey('clients.id')),
#                       Column('book_id', Integer, ForeignKey('books.id')),
#                       Column('creation_date', DateTime(timezone=True), server_default=func.now()),
#                       UniqueConstraint('client_id', 'book_id', name='uix_1'))

DbClientBook = Table('client_book',
                     Base.metadata,
                     Column('client_id', Integer, ForeignKey('clients.id'), primary_key=True),
                     Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
                     Column('creation_date', DateTime(timezone=True), server_default=func.now()),
                     # UniqueConstraint('client_id', 'book_id', name='uix_1')
                     )
