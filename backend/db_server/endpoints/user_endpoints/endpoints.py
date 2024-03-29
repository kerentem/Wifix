from typing import Optional
import datetime
from flask_bcrypt import generate_password_hash
from utiles import make_db_server_response, HttpStatus
from validation import validate_register_request, validate_credit_card, validate_ip

from welcome_email.email_client import EmailClient

from sqlalchemy_handler.db_models import WifiSession

from endpoints.manager_endpoints.endpoints import Manager

from backend.db_server.pricing.pricing_helper import DynamicPricing

EMAIL: bool = False


class User:
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.pricing_ml = DynamicPricing()
        if EMAIL:
            self.email_client = EmailClient()

    def register(self, data):
        # Get the user's registration information from the request
        full_name: str = data["full_name"]
        password: str = data["password"]
        email: str = data["email"]
        ip: str = data["ip"]
        company_name: str = data["company_name"]

        validate_register_request(password, email, ip)

        hashed_password: str = generate_password_hash(password)

        try:
            self.db_handler.register(
                full_name=full_name,
                email=email,
                hashed_password=hashed_password,
                ip=ip,
                company_name=company_name,
            )

            if EMAIL:
                self.email_client.send_email(to=email)

            msg = "User registered successfully"
            response = make_db_server_response(HttpStatus.OK, msg, {})

            return response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def login(self, data):
        email: str = data["email"]
        password: str = data["password"]
        ip: str = data["ip"]
        company_name: str = data["company_name"]

        validate_ip(ip)

        try:
            is_user_registered_response: bool = self.db_handler.is_user_registered(
                email=email, password=password, company_name=company_name
            )

            self.db_handler.set_user_ip(email=email, user_ip=ip)

            if is_user_registered_response:
                response = make_db_server_response(
                    HttpStatus.OK, "User registered", {"is_email_registered": True}
                )
            else:
                response = make_db_server_response(
                    HttpStatus.OK, "User not registered", {"is_email_registered": False}
                )

            return response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def add_card(self, data):
        card_number: str = data["card_number"]
        expiration_month: str = data["exp_month"]
        expiration_year: str = data["exp_year"]
        cvv: str = data["cvv"]
        email: str = data["email"]

        validate_credit_card(card_number)

        # Hash CVV before storing in database
        hashed_cvv = generate_password_hash(str(cvv))

        try:
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

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def start_wifi_session(self, data):
        email: str = data["email"]
        price: int = data["price"]
        ip: str = data["ip"]
        company_name: str = data["company_name"]

        end_time_in_min: int = data["end_time_in_min"]
        data_usage: Optional[int] = (
            data.get("data_usage") if data.get("data_usage") else 0
        )

        if not self.db_handler.is_wifi_session_expired(email, company_name):
            error_msg = "There is a wifi session for the user"
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

        if data.get("start_time"):
            date_start_str = data["start_time"]["date"]
            time_start_str = data["start_time"]["time"]
            start_time = datetime.datetime.strptime(
                f"{date_start_str} {time_start_str}", "%Y-%m-%d %H:%M:%S"
            )
        else:
            start_time: datetime = datetime.datetime.now()

        end_time: datetime = start_time + datetime.timedelta(minutes=end_time_in_min)

        start_time = int(start_time.timestamp())
        end_time = int(end_time.timestamp())

        # Inserting the data to the wifi_session table and payment table
        try:
            self.db_handler.set_user_ip(email, ip)
            self.db_handler.start_wifi_session(
                email, start_time, end_time, data_usage, company_name
            )
            try:
                self.db_handler.insert_payment(email, price)
            except Exception as e:
                self.db_handler.remove_wifi_session(
                    email, start_time, end_time, company_name
                )

                error_response = make_db_server_response(HttpStatus.OK, "", {}, str(e))
                return error_response

            company_speeds = Manager.get_company_speeds(company_name, self.db_handler)
            Manager.change_user_speed(
                ip=ip,
                upload_speed=company_speeds.premium_upload_speed,
                download_speed=company_speeds.premium_download_speed,
                is_cron=False,
                company=company_name,
            )

            msg = f"Added WiFi session to user: {email} successfully"
            response = make_db_server_response(HttpStatus.OK, msg, {})

            return response

        except Exception as e:
            error_response = make_db_server_response(HttpStatus.OK, "", {}, str(e))
            return error_response

    def is_wifi_session_expired_endpoint(self, data):
        email: str = data["email"]
        company_name: str = data["company_name"]

        try:
            is_expired = self.db_handler.is_wifi_session_expired(email, company_name)

            if is_expired:
                msg = f"Wifi session is expired for email: {email}, company_name: {company_name}"
            else:
                msg = f"Wifi session is not expired for email: {email}, company_name: {company_name}"

            data = {"is_expired": is_expired}

            response = make_db_server_response(HttpStatus.OK, msg, data)

            return response

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def get_end_session_time(self, data) -> float:
        email: str = data["email"]
        company_name: str = data["company_name"]

        try:
            wifi_session: WifiSession = self.db_handler.get_wifi_session_expired(
                email, company_name
            )

            if wifi_session:
                response = {"end_session_time_timestamp": wifi_session.end_time}
                return make_db_server_response(
                    HttpStatus.OK,
                    "",
                    response,
                )
            else:
                error_msg: str = "There isn't wifi session for the user"
                return make_db_server_response(HttpStatus.OK, "", {}, error_msg)

        except Exception as e:
            error_msg = str(e)
            error_response = make_db_server_response(HttpStatus.OK, "", {}, error_msg)
            return error_response

    def get_pricing(self, data) -> float:
        payment_method: str = data["plan"]
        current_hour = datetime.datetime.now().hour

        # TODO: need to get the number of users in the system dynamically
        current_input = [15, current_hour]

        final_price: float = self.pricing_ml.calculate_price(
            payment_method, current_input
        )
        return final_price
