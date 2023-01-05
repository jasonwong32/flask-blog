def handle_bad_request(e):
    return 'bad request', 400


def handle_page_not_found(e):
    return 'page not found', 404


def handle_internal_server_error(e):
    return 'internal server error', 500
