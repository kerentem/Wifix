import os
from typing import Optional
from datetime import datetime
from flask import Flask, request
import logging

from exception import UniqueViolationException, InvalidUsernameException
from validation import validate_register_request, validate_credit_card
from werkzeug.security import generate_password_hash
from MySQL_query import *
from utiles import make_db_server_response, HttpStatus
import mysql.connector

db_server = Flask(__name__)

RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_USERNAME = os.environ["RDS_USERNAME"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]
RDS_PORT = 3306
DATABASE = "wifix_db"

logger = logging.getLogger(__name__)


@db_server.route('/register', methods=['POST'])
def register():
    # Get the user's registration information from the request
    data = request.get_json()

    full_name: str = data['full_name']
    password: str = data['password']
    email: str = data['email']

    validate_register_request(full_name, password, email)

    hashed_password: str = generate_password_hash(password)

    try:
        cursor.execute(
            INSERT_A_USER_QUERY,
            (full_name, email, hashed_password)
        )

        connection.commit()

        # send_welcome_email(mail, email, username)

        msg = 'User registered successfully'
        response = make_db_server_response(HttpStatus.OK, msg, {})

        return response

    except mysql.connector.errors.IntegrityError as error:
        connection.commit()
        raise UniqueViolationException(error_msg=error.msg)

    except mysql.connector.errors as error:
        connection.commit()
        raise Exception(f"Error while creating a new user with MySQL,\n"
                        f"Error: {error.msg}")


@db_server.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email: str = data['email']
    password: str = data['password']

    hashed_password: str = generate_password_hash(password)

    try:
        cursor.execute(
            IS_USER_EXISTS_QUERY,
            (email, hashed_password)
        )

        user = cursor.fetchone()

        # (BarSe) need to talk with Keren on it !!!
        if user is not None:
            response = make_db_server_response(HttpStatus.OK, "", {})
            return response
        else:
            raise Exception

    except mysql.connector.errors as error:
        raise Exception(f"Error while creating a new user with MySQL,\n"
                        f"Error: {error}")


@db_server.route('/add_card', methods=['POST'])
def add_card():
    # Get credit card information from form
    data = request.get_json()

    card_number: str = data['card_number']
    expiration_month: str = data['exp_month']
    expiration_year: str = data['exp_year']
    cvv: str = data['cvv']
    email: str = data['email']

    validate_credit_card(card_number)

    # Hash CVV before storing in database
    hashed_cvv = generate_password_hash(str(cvv))

    try:
        cursor.execute(
            INSERT_CREDIT_CARD_BY_USER_ID_QUERY,
            (email, card_number, expiration_month, expiration_year, hashed_cvv))

        connection.commit()

        msg = 'User added credit card successfully'
        response = make_db_server_response(HttpStatus.OK, msg, {})

        return response

    except mysql.connector.errors.IntegrityError as error:
        connection.commit()
        logger.error(f"Error while inserting credit card with MySQL, error: {error}")
        raise InvalidUsernameException(f"Hi {email},"
                                       "\nPlease register first.")

    except mysql.connector.errors as error:
        connection.commit()
        logger.error(f"Error while inserting credit card with MySQL,\n"
                     f"Error: {error}")
        raise error


@db_server.route('/start_wifi_session', methods=['POST'])
def start_wifi_session():
    data = request.get_json()

    email: str = data['email']
    data_usage: Optional[int] = data.get('data_usage') if data.get('data_usage') else 0

    if data.get('start_time'):
        date_start_str = data["start_time"]['date']
        time_start_str = data["start_time"]['time']
        start_time = datetime.strptime(f"{date_start_str} {time_start_str}", '%Y-%m-%d %H:%M:%S')
    else:
        start_time = datetime.now()

    date_end_str = data["end_time"]['date']
    time_end_str = data["end_time"]['time']
    end_time: datetime = datetime.strptime(f"{date_end_str} {time_end_str}", '%Y-%m-%d %H:%M:%S')

    try:
        cursor.execute(
            INSERT_WIFI_SESSION_QUERY,
            (email, start_time, end_time, data_usage))

        connection.commit()

        msg = f'Added WiFi session to user: {email} successfully'
        response = make_db_server_response(HttpStatus.OK, msg, {})

        return response

    except mysql.connector.IntegrityError as error:
        connection.commit()
        logger.error(f"Error while inserting credit card with MySQL, error: {error}")
        raise InvalidUsernameException(f"Hi {email},"
                                       "\nPlease register first.")

    except mysql.connector.errors as error:
        connection.commit()
        logger.error(f"Error while inserting WiFi session with MySQL,\n"
                     f"Error: {error}")
        raise error


@db_server.route('/get_wifi_session/end_time', methods=['Get'])
def get_wifi_session_end_time():
    email = request.args['email']

    try:
        cursor.execute(
            GET_WIFI_SESSION_END_TIME_QUERY, (email,)
        )

        results = cursor.fetchall()[0]

        wifi_session_end_time: datetime = results[0]

        date = wifi_session_end_time.strftime('%Y-%m-%d')
        time = wifi_session_end_time.strftime('%H:%M:%S')

        data = {"wifi_session_end_time": {"date": date, "time": time}}
        response = make_db_server_response(HttpStatus.OK, "", data)

        return response

    except mysql.connector.errors.IntegrityError as error:
        logger.error(f"Error while inserting credit card with MySQL, error: {error}")
        raise InvalidUsernameException(f"Hi {email},"
                                       "\nPlease register first.")

    except mysql.connector.errors as error:
        logger.error(f"Error while inserting WiFi session with MySQL,\n"
                     f"Error: {error}")
        raise error


def creates_tables(connection, cursor):
    if connection and cursor:
        cursor.execute(MySQL_CREATE_USERS_TABLE_QUERY)
        cursor.execute(MySQL_CREATE_CREDIT_CARD_TABLE_QUERY)
        cursor.execute(MySQL_CREATE_WIFI_SESSION_TABLE_QUERY)
        connection.commit()


connection = None
cursor = None
try:
    logger.info('MySQL is connecting')
    connection = mysql.connector.connect(user=RDS_USERNAME, password=RDS_PASSWORD,
                                         host=RDS_ENDPOINT, database=DATABASE, port=RDS_PORT)
    cursor = connection.cursor()

except Exception as error:
    logger.error(f"Generic error: {error}")


def main():
    try:
        creates_tables(connection, cursor)
        db_server.run(debug=True, port=8080, host='0.0.0.0')
    finally:
        # closing database connection.
        if connection:
            logger.info('Closing MySQL database connection.')
            cursor.close()
            connection.close()
            logger.info("MySQL connection is closed")


if __name__ == "__main__":
    main()
