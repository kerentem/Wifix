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
            self.cursor.execute(MySQL_CREATE_USERS_TABLE_QUERY)
            self.cursor.execute(MySQL_CREATE_CREDIT_CARD_TABLE_QUERY)
            self.cursor.execute(MySQL_CREATE_WIFI_SESSION_TABLE_QUERY)
            self.connection.commit()

    def create_events(self):
        if self.connection and self.cursor:
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

        except mysql.connector.errors as error:
            raise Exception(
                f"Error while checking if a email registered, with MySQL,\n"
                f"Error: {error}"
            )
        except Exception as error:
            logger.error(error)
            raise error

    def is_user_registered(self, email: str, password: str) -> bool:
        try:
            is_valid_password: bool = False

            self.cursor.execute(IS_USER_REGISTERED_QUERY, [email])

            user_password = self.cursor.fetchone()

            if user_password:
                is_valid_password = check_password_hash(user_password[0], password)

            return is_valid_password

        except mysql.connector.errors as error:
            raise Exception(
                f"Error while checking if a user registered, with MySQL,\n"
                f"Error: {error}"
            )

        except Exception as error:
            logger.error(error)
            raise error

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

        except mysql.connector.errors as error:
            logger.error(
                f"Error while checking WiFi session with MySQL,\n" f"Error: {error}"
            )
            raise error
        except Exception as error:
            logger.error(error)
            raise error

    def register(self, full_name: str, email: str, hashed_password: str):
        try:
            self.cursor.execute(
                INSERT_A_USER_QUERY, [full_name, email, hashed_password]
            )

            self.connection.commit()

        except mysql.connector.errors.IntegrityError as error:
            self.connection.commit()
            raise UniqueViolationException(error_msg=error.msg)

        except mysql.connector.errors as error:
            self.connection.commit()
            raise Exception(
                f"Error while creating a new user with MySQL,\n" f"Error: {error.msg}"
            )
        except Exception as error:
            logger.error(error)
            raise error

    def add_credit_card(
        self, card_number, expiration_month, expiration_year, hashed_cvv, email
    ):
        try:
            self.cursor.execute(
                INSERT_CREDIT_CARD_BY_USER_ID_QUERY,
                [email, card_number, expiration_month, expiration_year, hashed_cvv],
            )

            self.connection.commit()

        except mysql.connector.errors.IntegrityError as error:
            self.connection.commit()
            logger.error(
                f"Error while inserting credit card with MySQL, error: {error}"
            )
            raise InvalidUsernameException(f"Hi {email}," "\nPlease register first.")

        except mysql.connector.errors as error:
            self.connection.commit()
            logger.error(
                f"Error while inserting credit card with MySQL,\n" f"Error: {error}"
            )
            raise error
        except Exception as error:
            logger.error(error)
            raise error

    def start_wifi_session(
        self, email: str, start_time: float, end_time: float, data_usage: int
    ):
        try:
            self.cursor.execute(
                INSERT_WIFI_SESSION_QUERY, [email, start_time, end_time, data_usage]
            )

            self.connection.commit()

        except mysql.connector.IntegrityError as error:
            self.connection.commit()
            logger.error(
                f"Error while starting WiFi session with MySQL, error: {error}"
            )
            raise InvalidUsernameException(f"Hi {email}," "\nPlease register first.")

        except mysql.connector.errors as error:
            self.connection.commit()
            logger.error(
                f"Error while inserting WiFi session with MySQL,\n" f"Error: {error}"
            )
            raise error
        except Exception as error:
            logger.error(error)
            raise error
