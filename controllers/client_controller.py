from pydantic.utils import deep_update

from global_models.service_template.book import BookInDb, BookCreate
from global_models.service_template.client import Client
from global_models.status import Status
from global_models.service_response import ServiceResponse

from controllers.controller_base import controller_middleware
from database.database_base import scoped_session
from database.entities import DbClient, DbBook
from services.model_parser import parse_client, parse_req_append_book
from logger import log


@controller_middleware
async def new_client(queries, headers, body, request):
    client = parse_client(queries)
    with scoped_session() as session:
        db_client = DbClient(name=client.name,
                             role=client.role)
        session.add(db_client)
        session.flush()
        created_client = Client.from_orm(db_client)

    service_response = ServiceResponse(status_code=200,
                                       payload=created_client,
                                       status=Status.OK)
    return service_response


@controller_middleware
async def get_all_clients(queries, headers, body, request):
    payload = []
    with scoped_session() as session:
        db_clients = session.query(DbClient).all()
        for db_client in db_clients:
            books = []
            for book in db_client.books:
                book_res = BookInDb.from_orm(book)
                book_res = BookCreate.parse_obj(book_res)
                books.append(book_res)
                # books.append(BookInDb.from_orm(book))
            merged = deep_update(Client.from_orm(db_client).dict(), {"books": books})
            payload.append(merged)

    service_response = ServiceResponse(payload=payload,
                                       status_code=200,
                                       status=Status.OK)
    return service_response


@controller_middleware
async def append_book(queries, headers, body, request):
    req_append_book = parse_req_append_book(body)
    with scoped_session() as session:
        db_client: DbClient = session.query(DbClient).filter(DbClient.id == req_append_book.client_id).one_or_none()
        db_book = session.query(DbBook).filter(DbBook.id == req_append_book.book_id).one_or_none()
        if db_client and db_book:
            db_client.books.add(db_book)
        session.commit()

        books = []
        for book in db_client.books:
            books.append(BookInDb.from_orm(book))
        payload = deep_update(Client.from_orm(db_client).dict(), {"books": books})
    service_response = ServiceResponse(status_code=200,
                                       payload=payload,
                                       status=Status.OK)
    return service_response
