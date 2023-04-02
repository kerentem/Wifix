from typing import Optional
import datetime
from flask_bcrypt import generate_password_hash

from backend.db_server.mysql_util.mysql_exception import InvalidUsernameException
from backend.db_server.utiles import make_db_server_response, HttpStatus
from backend.db_server.validation import validate_register_request, validate_credit_card


class User:

    def __init__(self, db_handler):
        self.db_handler = db_handler

    def register(self, data):
        # Get the user's registration information from the request
        full_name: str = data["full_name"]
        password: str = data["password"]
        email: str = data["email"]

        validate_register_request(full_name, password, email)

        hashed_password: str = generate_password_hash(password)

        self.db_handler.register(
            full_name=full_name, email=email, hashed_password=hashed_password
        )

        msg = "User registered successfully"
        response = make_db_server_response(HttpStatus.OK, msg, {})

        return response

    def login(self, data):
        email: str = data["email"]
        password: str = data["password"]

        is_user_registered_response: bool = self.db_handler.is_user_registered(
            email=email, password=password
        )

        if is_user_registered_response:
            response = make_db_server_response(
                HttpStatus.OK, "User registered", {"is_email_registered": True}
            )
        else:
            response = make_db_server_response(
                HttpStatus.OK, "User not registered", {"is_email_registered": False}
            )

        return response

    def add_card(self, data):
        card_number: str = data["card_number"]
        expiration_month: str = data["exp_month"]
        expiration_year: str = data["exp_year"]
        cvv: str = data["cvv"]
        email: str = data["email"]

        validate_credit_card(card_number)

        # Hash CVV before storing in database
        hashed_cvv = generate_password_hash(str(cvv))

        self.db_handler.add_credit_card(
            card_number=card_number,
            expiration_month=expiration_month,
            expiration_year=expiration_year,
            hashed_cvv=hashed_cvv,
            email=email,
        )

        msg = "User added credit card successfully"
        response = make_db_server_response(HttpStatus.OK, msg, {})

        return response

    def start_wifi_session(self, data):
        email: str = data["email"]
        price: int = data["price"]
        end_time_in_min: int = data["end_time_in_min"]
        data_usage: Optional[int] = data.get("data_usage") if data.get("data_usage") else 0

        if not self.db_handler.is_wifi_session_expired(email):
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

        # Inserting the data to the wifi_session table and payment table
        self.db_handler.start_wifi_session(email, start_time, end_time, data_usage)
        try:
            self.db_handler.insert_payment(email, price)
        except Exception as e:
            self.db_handler.remove_wifi_session(email, int(start_time), int(end_time))
            raise e

        msg = f"Added WiFi session to user: {email} successfully"
        response = make_db_server_response(HttpStatus.OK, msg, {})

        return response

    def is_wifi_session_expired_endpoint(self, data):
        email = data["email"]

        _is_email_registered: bool = self.db_handler.is_email_registered(email)
        if not _is_email_registered:
            raise InvalidUsernameException("User not registered")

        is_expired = self.db_handler.is_wifi_session_expired(email)

        if is_expired:
            msg = f"Wifi session is expired for email: {email}"
        else:
            msg = f"Wifi session is not expired for email: {email}"

        data = {"is_expired": is_expired}

        response = make_db_server_response(HttpStatus.OK, msg, data)

        return response
