MySQL_SELECT_QUERY = "select * from users"

MySQL_CREATE_USERS_TABLE_QUERY = \
    "CREATE TABLE IF NOT EXISTS users (" \
    "full_name VARCHAR(255) NOT NULL," \
    "email VARCHAR(255) PRIMARY KEY," \
    "password VARCHAR(255) NOT NULL," \
    "created_at TIMESTAMP DEFAULT NOW()" \
    ")"

MySQL_CREATE_CREDIT_CARD_TABLE_QUERY = \
    "CREATE TABLE IF NOT EXISTS credit_card (" \
    "email VARCHAR(255)," \
    "card_number VARCHAR(16) NOT NULL, " \
    "expiration_month VARCHAR(2) NOT NULL, " \
    "expiration_year VARCHAR(4) NOT NULL, " \
    "cvv VARCHAR(255) NOT NULL, " \
    "FOREIGN KEY (email) REFERENCES users(email) ON DELETE RESTRICT ON UPDATE RESTRICT" \
    ");"

MySQL_CREATE_WIFI_SESSION_TABLE_QUERY = \
    "CREATE TABLE IF NOT EXISTS wifi_session (" \
    "email VARCHAR(255) REFERENCES users(email)," \
    "start_time TIMESTAMP NOT NULL, " \
    "end_time TIMESTAMP NOT NULL, " \
    "data_usage INTEGER NOT NULL, " \
    "FOREIGN KEY (email) REFERENCES users(email) ON DELETE RESTRICT ON UPDATE RESTRICT" \
    ");"

INSERT_A_USER_QUERY = "INSERT INTO users (full_name, email, password) " \
                      "VALUES (%s, %s, %s)"
INSERT_CREDIT_CARD_BY_USER_ID_QUERY = "INSERT INTO credit_card " \
                                      "(email, card_number, expiration_month, expiration_year, cvv)" \
                                      "VALUES (%s, %s, %s, %s, %s)"
INSERT_WIFI_SESSION_QUERY = "INSERT INTO wifi_session " \
                                      "(email, start_time, end_time, data_usage)" \
                                      "VALUES (%s, %s, %s, %s)"
GET_WIFI_SESSION_END_TIME_QUERY = "SELECT end_time FROM wifi_session WHERE email = %s"
IS_USER_EXISTS_QUERY = "SELECT * FROM users WHERE email = %s AND password = %s"