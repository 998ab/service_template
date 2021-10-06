from controllers import new_client, get_all_clients, append_book, new_book, get_all_books, update_book_price


def setup_routes(app):
    # Client
    app.router.add_post("/client/new", new_client)
    app.router.add_get("/client/all", get_all_clients)

    # Client's books
    app.router.add_post("/client/book/add", append_book)

    # Book
    app.router.add_post("/book/new", new_book)
    app.router.add_post("/book/update/price", update_book_price)
    app.router.add_get("/book/all", get_all_books)
