import os

from flask import Flask, jsonify, request
import psycopg2
import logging
from werkzeug.security import generate_password_hash

from postgresql_query import *

app = Flask(__name__)
RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_USERNAME = os.environ["RDS_USERNAME"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]
RDS_PORT = 5432
DATABASE = "wifix-db"
connection = None
cursor = None


@app.route('/register', methods=['POST'])
def register():
    # Get the user's registration information from the request
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    # Generate a hash of the password
    hashed_password = generate_password_hash(password)

    # Insert the user into the users table
    cursor.execute(
        ADD_A_USER_QUERY,
        (username, hashed_password, email)
    )

    # Get the user's ID
    cursor.execute(GET_A_USER_ID_BY_USERNAME_QUERY, (username,))
    user_id = cursor.fetchone()[0]

    # Commit changes and close connection
    cursor.commit()

    # Return success message
    return user_id, 200, 'User registered successfully'


@app.route('/add_card', methods=['POST'])
def add_card():
    # Get credit card information from form
    card_number = request.form['card_number']
    exp_month = request.form['exp_month']
    exp_year = request.form['exp_year']
    cvv = request.form['cvv']
    user_id = request.form['user_id']

    # Hash CVV before storing in database
    hashed_cvv = generate_password_hash(cvv)

    # Insert credit card information into database
    cursor.execute(
        INSERT_CREDIT_CARD_BY_USER_ID_QUERY,
        (card_number, exp_month, exp_year, hashed_cvv, user_id))

    # Commit changes and close connection
    cursor.commit()

    # Return success message to user
    return "Credit card added successfully!"


if __name__ == '__main__':
    try:
        logging.info('PostgreSQL is connecting')
        connection = psycopg2.connect(user=RDS_USERNAME,
                                      password=RDS_PASSWORD,
                                      host=RDS_ENDPOINT,
                                      port=RDS_PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        app.run(debug=True, port=8080)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            logging.info('closing PostgreSQL database connection.')
            cursor.close()
            connection.close()
            logging.info("PostgreSQL connection is closed")
