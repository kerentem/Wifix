from enum import Enum
from typing import Dict, Any

from flask import jsonify


class HttpStatus(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


def make_db_server_response(
    status_code: HttpStatus, message: str, data: Dict[Any, Any]
):
    response = {"message": message, "data": data}
    return jsonify(response), status_code.value
