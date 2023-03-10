POSTGRESQL_SELECT_QUERY = "select * from users"

POSTGRESQL_CREATE_USERS_TABLE_QUERY = \
    "CREATE TABLE IF NOT EXISTS users " \
    "(id SERIAL PRIMARY KEY,name VARCHAR(255) NOT NULL," \
    "email VARCHAR(255) UNIQUE NOT NULL," \
    "username VARCHAR(255) UNIQUE NOT NULL," \
    "password VARCHAR(255) UNIQUE NOT NULL," \
    "created_at TIMESTAMP DEFAULT NOW()" \
    ")"

POSTGRESQL_CREATE_CREDIT_CARD_TABLE_QUERY = \
    "CREATE TABLE IF NOT EXISTS credit_card (" \
    "id SERIAL PRIMARY KEY, " \
    "user_id INTEGER REFERENCES users(id)," \
    "number VARCHAR(16) NOT NULL, " \
    "expiration_month INTEGER NOT NULL, " \
    "expiration_year INTEGER NOT NULL, " \
    "cvv VARCHAR(4) NOT NULL" \
    ");"

POSTGRESQL_CREATE_WIFI_SESSION_TABLE_QUERY = \
    "CREATE TABLE IF NOT EXISTS wifi_sessions (" \
    "id SERIAL PRIMARY KEY, " \
    "user_id INTEGER REFERENCES users(id)," \
    "start_time TIMESTAMP NOT NULL, " \
    "end_time TIMESTAMP NOT NULL, " \
    "data_usage INTEGER" \
    ");"


ADD_A_USER_QUERY = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
GET_A_USER_ID_BY_USERNAME_QUERY = "SELECT id FROM users WHERE username = %s"
INSERT_CREDIT_CARD_BY_USER_ID_QUERY = "INSERT INTO credit_cards (card_number, exp_month, exp_year, cvv, user_id) VALUES (%s, %s, %s, %s, %s)"