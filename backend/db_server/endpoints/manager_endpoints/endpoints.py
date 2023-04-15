import uuid
from datetime import datetime
from flask_bcrypt import generate_password_hash

from utiles import make_db_server_response, HttpStatus, Const
from validation import validate_register_request, validate_datetime


class Admin:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def register(self, data):
        full_name: str = data["full_name"]
        password: str = data["password"]
        email: str = data["email"]

        validate_register_request(full_name=full_name, password=password, email=email)

        hashed_password: str = generate_password_hash(password)

        try:
            self.db_handler.register(
                full_name=full_name, email=email, hashed_password=hashed_password
            )

            msg = "Admin registered successfully"
            response = make_db_server_response(HttpStatus.OK, msg, {})
            return response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def login(self, data):
        email: str = data["email"]
        password: str = data["password"]

        try:
            is_user_registered_response: bool = self.db_handler.is_user_registered(
                email=email, password=password
            )

            if is_user_registered_response:
                response = make_db_server_response(
                    HttpStatus.OK, "Admin registered", {"is_email_registered": True}
                )
            else:
                response = make_db_server_response(
                    HttpStatus.OK,
                    "Admin not registered",
                    {"is_email_registered": False},
                )

            return response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def get_current_balance(self, data):
        from_date: str = data["from_date"]
        to_date: str = data["to_date"]

        validate_datetime(from_date)
        validate_datetime(to_date)

        from_date_timestamp = datetime.strptime(
            from_date, Const.DATE_FORMAT
        ).timestamp()
        to_date_timestamp = datetime.strptime(to_date, Const.DATE_FORMAT).timestamp()

        try:
            current_balance = self.db_handler.get_current_balance(
                from_date_timestamp, to_date_timestamp
            )

            data = {
                "current_balance: ": current_balance,
                "from_timestamp: ": from_date_timestamp,
                "to_timestamp: ": to_date_timestamp,
            }

            response = make_db_server_response(HttpStatus.OK, "", data)

            return response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def is_valid_token(self, data) -> bool:
        company_name: str = data["company_name"]
        token: str = data["token"]

        try:
            is_valid_token_response: bool = self.db_handler.is_valid_company_token(
                company_name=company_name, hashed_token=token
            )

            return is_valid_token_response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def set_new_token(self, data):
        username: str = data["username"]
        password: str = data["password"]
        company_name: str = data["company_name"]

        def is_manager(username: str, password: str):
            return False if username != "wifix" or password != "12345" else True

        if not is_manager(username, password):
            raise Exception("You are not a service manager, please contact BarSe")

        token: str = str(uuid.uuid4())
        hashed_token: str = generate_password_hash(token)

        try:
            self.db_handler.set_company_token(
                company_name=company_name, hashed_token=hashed_token
            )

            response = make_db_server_response(HttpStatus.OK, "", {"token": token})
            return response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response
