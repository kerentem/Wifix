from enum import Enum
from typing import Dict, Any, Optional

from flask import jsonify
import re


class HttpStatus(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class Const:
    DATE_FORMAT = "%d/%m/%Y"


class USER_ENDPOINTS:
    LOGIN = "/login"
    REGISTER = "/register"
    ADD_CARD = "/add_card"
    START_WIFI_SESSION = "/wifi_session/start"
    IS_EXPIRED_WIFI_SESSION = "/wifi_session/is_expired"
    GET_END_SESSION_TIME = "/wifi_session/time_left"


class ADMIN_ENDPOINTS:
    ADMIN = "/admin"
    LOGIN = f"{ADMIN}/login"
    REGISTER = f"{ADMIN}/register"
    GET_CURRENT_BALANCE = f"{ADMIN}/get_current_balance"
    START_WIFI_SESSION = f"{ADMIN}/wifi_session/start"
    IS_EXPIRED_WIFI_SESSION = f"{ADMIN}/wifi_session/is_expired"


class MANAGER_ENDPOINTS:
    MANAGER = "/manager"
    SET_NEW_TOKEN = f"{MANAGER}/set_new_token"


def make_db_server_response(
        status_code: HttpStatus,
        message: str,
        data: Dict[Any, Any],
        error: Optional[str] = None,
):
    response = {
        "message": message,
        "data": data,
        "error": True if error else False,
        "error_message": error,
    }

    return jsonify(response), status_code.value
