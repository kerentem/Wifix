import os
from flask import Flask, request, Response

from sqlalchemy_handler.db_client import DBHandler
from endpoints.manager_endpoints.endpoints import Admin
from endpoints.user_endpoints.endpoints import User
from utiles import ADMIN_ENDPOINTS, USER_ENDPOINTS
from mysql_util.mysql_exception import InvalidUsernameException
from flask_cors import CORS

db_server = Flask(__name__)

CORS(db_server)

RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_USERNAME = os.environ["RDS_USERNAME"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]
RDS_PORT = 3306
DATABASE = "wifix_db"


@db_server.before_request
def is_valid_request():
    if request.path != ADMIN_ENDPOINTS.SET_NEW_TOKEN:
        if request.method.lower() == "options":
            return Response()
        elif request.method == "POST":
            email: str = request.json["email"]
        elif request.method == "GET":
            email: str = request.args["email"]
        else:
            raise Exception("We are supporting GET/POST methods")

        is_admin: bool = ADMIN_ENDPOINTS.ADMIN in request.path

        if is_admin:
            is_valid = admin.is_valid_token(request.json)
            if not is_valid:
                raise Exception("Please insert the right company token")

        if request.path not in [USER_ENDPOINTS.REGISTER,
                                USER_ENDPOINTS.LOGIN,
                                ADMIN_ENDPOINTS.REGISTER,
                                ADMIN_ENDPOINTS.LOGIN,]:

            _is_email_registered: bool = db_handler.is_email_registered(email, is_admin)
            if not _is_email_registered:
                raise InvalidUsernameException("User not registered")

@db_server.route(USER_ENDPOINTS.REGISTER, methods=["POST"])
def user_register():
    data = request.get_json()
    response = user.register(data)
    return response


@db_server.route(USER_ENDPOINTS.LOGIN, methods=["POST"])
def user_login():
    data = request.get_json()
    response = user.login(data)
    return response


@db_server.route(USER_ENDPOINTS.ADD_CARD, methods=["POST"])
def add_card():
    data = request.get_json()
    response = user.add_card(data)
    return response


@db_server.route(USER_ENDPOINTS.START_WIFI_SESSION, methods=["POST"])
def start_wifi_session():
    data = request.get_json()
    response = user.start_wifi_session(data)
    return response


@db_server.route(USER_ENDPOINTS.IS_EXPIRED_WIFI_SESSION, methods=["Get"])
def is_wifi_session_expired_endpoint(self, data):
    data = request.get_json()
    response = admin.register(data)
    return response


@db_server.route(ADMIN_ENDPOINTS.REGISTER, methods=["POST"])
def admin_register():
    data = request.get_json()
    response = admin.register(data)
    return response


@db_server.route(ADMIN_ENDPOINTS.LOGIN, methods=["POST"])
def admin_login():
    data = request.get_json()
    response = admin.login(data)
    return response


@db_server.route(ADMIN_ENDPOINTS.GET_CURRENT_BALANCE, methods=["POST"])
def admin_get_current_balance():
    data = request.get_json()
    response = admin.get_current_balance(data)
    return response


@db_server.route(ADMIN_ENDPOINTS.SET_NEW_TOKEN, methods=["POST"])
def set_new_token():
    data = request.get_json()
    response = admin.set_new_token(data)
    return response


db_handler = DBHandler(RDS_USERNAME, RDS_PASSWORD, RDS_ENDPOINT, DATABASE, RDS_PORT)

user = User(db_handler)
admin = Admin(db_handler)


def main():
    db_handler.create_all()
    db_handler.create_events()
    db_server.run(debug=True, port=8080, host="0.0.0.0")


if __name__ == "__main__":
    main()
