from global_models.error import Error
from global_models.service_template.book import BookCreate, BookInDb
from global_models.status import Status
from global_models.service_response import ServiceResponse

from controllers.controller_base import controller_middleware
from database.database_base import scoped_session
from database.entities import DbBook
from services.model_parser import parse_book_create, parse_book_update_price
from logger import log


@controller_middleware
async def new_book(queries, headers, body, request):
    new_book = parse_book_create(queries)
    with scoped_session() as session:
        db_book = DbBook(name=new_book.name,
                         author=new_book.author,
                         price=new_book.price)
        session.add(db_book)
        session.flush()
        new_book = BookInDb.from_orm(db_book)
    service_response = ServiceResponse(payload=new_book,
                                       status_code=200,
                                       status=Status.OK)
    return service_response


@controller_middleware
async def get_all_books(queries, headers, body, request):
    with scoped_session() as session:
        books = []
        db_books = session.query(DbBook).all()
        for book in db_books:
            books.append(BookInDb.from_orm(book))

    service_response = ServiceResponse(payload=books,
                                       status_code=200,
                                       status=Status.OK)
    return service_response


@controller_middleware
async def update_book_price(queries, headers, body, request):
    update_book = parse_book_update_price(queries)
    with scoped_session() as session:
        db_book = session.query(DbBook).filter(DbBook.id == update_book.id).one_or_none()
        if db_book:
            db_book.price = update_book.price
            session.flush()
            result = BookInDb.from_orm(db_book)
        else:
            result = Error(message='No such book',
                           code='No such book')

    service_response = ServiceResponse(payload=result,
                                       status_code=200,
                                       status=Status.OK)
    return service_response
