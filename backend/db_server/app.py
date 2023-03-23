import os
from typing import Optional
import datetime
from flask import Flask, request

from backend.db_server.mysql.mysql_util import MysqlUtil
from exception import InvalidUsernameException
from validation import validate_register_request, validate_credit_card
from werkzeug.security import generate_password_hash
from utiles import make_db_server_response, HttpStatus

db_server = Flask(__name__)

RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_USERNAME = os.environ["RDS_USERNAME"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]
RDS_PORT = 3306
DATABASE = "wifix_db"

mysqlutil = MysqlUtil(RDS_USERNAME, RDS_PASSWORD, RDS_ENDPOINT, DATABASE, RDS_PORT)


@db_server.route("/register", methods=["POST"])
def register():
    # Get the user's registration information from the request
    data = request.get_json()

    full_name: str = data["full_name"]
    password: str = data["password"]
    email: str = data["email"]

    validate_register_request(full_name, password, email)

    hashed_password: str = generate_password_hash(password)

    mysqlutil.register(
        full_name=full_name, email=email, hashed_password=hashed_password
    )

    msg = "User registered successfully"
    response = make_db_server_response(HttpStatus.OK, msg, {})

    return response


@db_server.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email: str = data["email"]

    is_user_registered_response = mysqlutil.is_user_registered(email=email)

    if is_user_registered_response:
        response = make_db_server_response(
            HttpStatus.OK, "User registered", {"is_user_registered": True}
        )
    else:
        response = make_db_server_response(
            HttpStatus.OK, "User not registered", {"is_user_registered": False}
        )

    return response


@db_server.route("/add_card", methods=["POST"])
def add_card():
    # Get credit card information from form
    data = request.get_json()

    card_number: str = data["card_number"]
    expiration_month: str = data["exp_month"]
    expiration_year: str = data["exp_year"]
    cvv: str = data["cvv"]
    email: str = data["email"]

    validate_credit_card(card_number)

    # Hash CVV before storing in database
    hashed_cvv = generate_password_hash(str(cvv))

    mysqlutil.add_credit_card(
        card_number=card_number,
        expiration_month=expiration_month,
        expiration_year=expiration_year,
        hashed_cvv=hashed_cvv,
        email=email,
    )

    msg = "User added credit card successfully"
    response = make_db_server_response(HttpStatus.OK, msg, {})

    return response


@db_server.route("/wifi_session/start", methods=["POST"])
def start_wifi_session():
    data = request.get_json()

    email: str = data["email"]
    end_time_in_min: int = data["end_time_in_min"]
    data_usage: Optional[int] = data.get("data_usage") if data.get("data_usage") else 0

    is_user_registered_response = mysqlutil.is_user_registered(email)

    if not is_user_registered_response:
        raise InvalidUsernameException("User not registered")

    if not mysqlutil.is_wifi_session_expired(email):
        raise Exception("There is a wifi session for the user")

    if data.get("start_time"):
        date_start_str = data["start_time"]["date"]
        time_start_str = data["start_time"]["time"]
        start_time = datetime.datetime.strptime(
            f"{date_start_str} {time_start_str}", "%Y-%m-%d %H:%M:%S"
        )
    else:
        start_time: datetime = datetime.datetime.now()

    end_time: datetime = start_time + datetime.timedelta(minutes=end_time_in_min)

    start_time = start_time.timestamp()
    end_time = end_time.timestamp()

    mysqlutil.start_wifi_session(email, start_time, end_time, data_usage)

    msg = f"Added WiFi session to user: {email} successfully"
    response = make_db_server_response(HttpStatus.OK, msg, {})

    return response


@db_server.route("/wifi_session/is_expired", methods=["Get"])
def is_wifi_session_expired_endpoint():
    email = request.args["email"]

    is_expired = mysqlutil.is_wifi_session_expired(email)

    if is_expired:
        msg = f"Wifi session is expired for email: {email}"
    else:
        msg = f"Wifi session is not expired for email: {email}"

    data = {"is_expired": is_expired}

    response = make_db_server_response(HttpStatus.OK, msg, data)

    return response


def main():
    mysqlutil.create_tables()
    mysqlutil.create_events()
    db_server.run(debug=True, port=8080, host="0.0.0.0")


if __name__ == "__main__":
    main()



