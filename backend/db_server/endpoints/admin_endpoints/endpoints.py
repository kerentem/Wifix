from datetime import datetime

from flask_bcrypt import generate_password_hash

from utiles import make_db_server_response, HttpStatus, Const
from validation import validate_register_request, validate_datetime, validate_ip

class Admin:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def register(self, data):
        full_name: str = data["full_name"]
        password: str = data["password"]
        email: str = data["email"]

        validate_register_request(password=password, email=email)

        hashed_password: str = generate_password_hash(password)

        try:
            self.db_handler.register(
                full_name=full_name, email=email, hashed_password=hashed_password, is_admin=True
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
                email=email, password=password, is_admin=True
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
