POSTGRESQL_SELECT_QUERY = "select * from users"

POSTGRESQL_CREATE_USERS_TABLE_QUERY = \
    "CREATE TABLE IF NOT EXISTS users " \
    "(username VARCHAR(255) PRIMARY KEY," \
    "email VARCHAR(255) UNIQUE NOT NULL," \
    "password VARCHAR(255) NOT NULL," \
    "created_at TIMESTAMP DEFAULT NOW()" \
    ")"

POSTGRESQL_CREATE_CREDIT_CARD_TABLE_QUERY = \
    "CREATE TABLE IF NOT EXISTS credit_card (" \
    "username VARCHAR(255) REFERENCES users(username)," \
    "card_number VARCHAR(16) NOT NULL, " \
    "expiration_month VARCHAR(2) NOT NULL, " \
    "expiration_year VARCHAR(4) NOT NULL, " \
    "cvv VARCHAR(255) NOT NULL" \
    ");"

POSTGRESQL_CREATE_WIFI_SESSION_TABLE_QUERY = \
    "CREATE TABLE IF NOT EXISTS wifi_session (" \
    "username VARCHAR(255) REFERENCES users(username)," \
    "start_time TIMESTAMP NOT NULL, " \
    "end_time TIMESTAMP NOT NULL, " \
    "data_usage INTEGER NOT NULL" \
    ");"

INSERT_A_USER_QUERY = "INSERT INTO users (username, password, email) " \
                      "VALUES (%s, %s, %s)"
INSERT_CREDIT_CARD_BY_USER_ID_QUERY = "INSERT INTO credit_card " \
                                      "(username, card_number, expiration_month, expiration_year, cvv)" \
                                      "VALUES (%s, %s, %s, %s, %s)"
INSERT_WIFI_SESSION_QUERY = "INSERT INTO wifi_session " \
                                      "(username, start_time, end_time, data_usage)" \
                                      "VALUES (%s, %s, %s, %s)"
GET_WIFI_SESSION_END_TIME_QUERY = "SELECT end_time FROM wifi_session WHERE username = %s"
IS_USER_EXISTS_QUERY = "SELECT * FROM users WHERE username = %s AND password = %s"