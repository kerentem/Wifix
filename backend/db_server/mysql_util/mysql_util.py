import datetime
import logging

import mysql.connector

from mysql_util.mysql_query import *
from mysql_util.mysql_exception import *

logger = logging.getLogger(__name__)

from flask_bcrypt import check_password_hash


class MysqlUtil:
    def __init__(
            self,
            rds_username: str,
            rds_password: str,
            rds_endpoint: str,
            database: str,
            rds_port: int,
    ):
        logger.info("Connecting to MySQL database.")
        self.connection = mysql.connector.connect(
            user=rds_username,
            password=rds_password,
            host=rds_endpoint,
            database=database,
            port=rds_port,
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.connection:
            logger.info("Closing MySQL database connection.")
            self.cursor.close()
            self.connection.close()
            logger.info("MySQL connection is closed")

    def create_tables(self):
        if self.connection and self.cursor:
            self.cursor.execute(MySQL_CREATE_USERS_TABLE_QUERY)  # users table
            self.cursor.execute(MySQL_CREATE_ADMINS_TABLE_QUERY)  # admins table
            self.cursor.execute(MySQL_CREATE_CREDIT_CARD_TABLE_QUERY)  # credit card table
            self.cursor.execute(MySQL_CREATE_PAYMENT_TABLE_QUERY)  # payments table
            self.cursor.execute(MySQL_CREATE_WIFI_SESSION_TABLE_QUERY)  # wifi session table
            self.cursor.execute(MySQL_CREATE_COMPANIES_TOKENS_TABLE_QUERY)  # companies tokens table
            self.connection.commit()

    def create_events(self):
        if self.connection and self.cursor:
            # delete record every x min, users that ended their session
            self.cursor.execute(MYSQL_WIFI_SESSION_DELETE_EXPIRED_EVENT_QUERY)
            self.connection.commit()

    def is_email_registered(self, email: str) -> bool:
        try:
            self.cursor.execute(IS_EMAIL_REGISTERED_QUERY, [email])

            email = self.cursor.fetchone()

            if email:
                return True
            else:
                return False

        except Exception as error:
            raise Exception(
                f"Error while checking if a email registered, with MySQL,\n"
                f"Error: {error}"
            )


    def is_user_registered(self, email: str, password: str, admin: bool = False) -> bool:
        try:
            is_valid_password: bool = False

            query = IS_ADMIN_REGISTERED_QUERY if admin else IS_USER_REGISTERED_QUERY

            self.cursor.execute(query, [email])

            user_password = self.cursor.fetchone()

            if user_password:
                is_valid_password = check_password_hash(user_password[0], password)

            return is_valid_password


        except Exception as error:
            raise Exception(
                f"Error while checking if a user registered, with MySQL,\n"
                f"Error: {error}"
            )

    def is_wifi_session_expired(self, email: str) -> bool:
        try:
            self.cursor.execute(IS_WIFI_SESSION_EXPIRED_QUERY, [email])

            is_expired: bool = self.cursor.fetchone() is None
            return is_expired

        except mysql.connector.errors.IntegrityError:
            logger.error(
                f"Error while checking WiFi session with MySQL,\n" "Error: {error}"
            )
            raise InvalidUsernameException(f"Hi {email}," "\nPlease register first.")

        except Exception as error:
            f"Error while checking WiFi session with MySQL,\n" f"Error: {error}"
            raise error

    def register(self, full_name: str, email: str, hashed_password: str, admin: bool = False):
        try:
            query = INSERT_ADMIN_QUERY if admin else INSERT_USER_QUERY
            self.cursor.execute(
                query, [full_name, email, hashed_password]
            )

            self.connection.commit()

        except mysql.connector.errors.IntegrityError as error:
            self.connection.rollback()
            raise UniqueViolationException(error_msg=error.msg)

        except Exception as error:
            self.connection.rollback()
            raise Exception(
                f"Error while creating a new user with MySQL,\n" f"Error: {error.msg}"
            )

    def add_credit_card(
            self, card_number, expiration_month, expiration_year, hashed_cvv, email
    ):
        try:
            self.cursor.execute(
                INSERT_CREDIT_CARD_BY_USER_ID_QUERY,
                [email, card_number, expiration_month, expiration_year, hashed_cvv],
            )

            self.connection.commit()

        except Exception as error:
            self.connection.rollback()
            logger.error(
                f"Error while inserting credit card with MySQL, error: {error}"
            )
            raise InvalidUsernameException(f"Hi {email}," "\nPlease register first.")

    def start_wifi_session(
            self, email: str, start_time: float, end_time: float, data_usage: int
    ):
        try:
            self.cursor.execute(
                INSERT_WIFI_SESSION_QUERY, [email, start_time, end_time, data_usage]
            )

            self.connection.commit()

        except mysql.connector.IntegrityError as error:
            self.connection.rollback()
            logger.error(
                f"Error while starting WiFi session with MySQL, error: {error}"
            )
            raise InvalidUsernameException(f"Hi {email}," "\nPlease register first.")


        except Exception as error:
            self.connection.rollback()
            logger.error(
                f"Error while inserting WiFi session with MySQL,\n" f"Error: {error}"
            )
            raise error

    def remove_wifi_session(
            self, email: str, start_time: int, end_time: int
    ):
        try:
            self.cursor.execute(
                REMOVE_WIFI_SESSION_QUERY, [email, start_time, end_time]
            )

            self.connection.commit()

        except mysql.connector.IntegrityError as error:
            self.connection.commit()
            logger.error(
                f"Error while starting WiFi session with MySQL, error: {error}"
            )
            raise InvalidUsernameException(f"Hi {email}," "\nPlease register first.")

        except Exception as error:
            self.connection.rollback()
            logger.error(
                f"Error while inserting WiFi session with MySQL,\n" f"Error: {error}"
            )
            raise error

    def insert_payment(
            self, email: str, price: int
    ):
        created_at = datetime.datetime.now().timestamp()
        try:
            self.cursor.execute(
                INSERT_PAYMENT_QUERY, [email, price, created_at]
            )

            self.connection.commit()

        except mysql.connector.IntegrityError as error:
            self.connection.commit()
            logger.error(
                f"Error while adding payment with MySQL, error: {error}"
            )
            raise InvalidUsernameException(f"Hi {email}," "\nPlease register first.")

        except Exception as error:
            self.connection.rollback()
            logger.error(
                f"Error while inserting WiFi session with MySQL,\n" f"Error: {error}"
            )
            raise error

    def get_current_balance(self, from_date_timestamp: float, to_date_timestamp: float) -> int:
        try:
            self.cursor.execute(GET_CURRENT_BALANCE_QUERY, [from_date_timestamp, to_date_timestamp])

            balance = self.cursor.fetchone()[0]
            return int(balance) if balance else 0

        except Exception as error:
            f"Error while getting admin balance with MySQL,\n" f"Error: {error}"
            raise error

    def is_valid_company_token(self, company_name: str, hashed_token: str) -> bool:
        try:
            is_valid_token: bool = False

            self.cursor.execute(IS_VALID_COMPANY_TOKEN_QUERY, [company_name])

            table_token = self.cursor.fetchone()

            if table_token:
                is_valid_token = check_password_hash(table_token[0], hashed_token)

            return is_valid_token

        except Exception as error:
            raise Exception(
                f"Error while checking if a user registered, with MySQL,\n"
                f"Error: {error}"
            )

    def set_company_token(self, company_name: str, hashed_token: str,):
        try:

            self.cursor.execute(
                INSERT_COMPANY_TOKEN_QUERY, [company_name, hashed_token]
            )

            self.connection.commit()

        except Exception as error:
            self.connection.rollback()
            raise Exception(
                f"Error while creating a new token for the company with MySQL,\n" f"Error: {error}"
            )
