MySQL_CREATE_USERS_TABLE_QUERY = (
    "CREATE TABLE IF NOT EXISTS users ("
    "full_name VARCHAR(255) NOT NULL,"
    "email VARCHAR(255) PRIMARY KEY,"
    "password VARCHAR(255) NOT NULL,"
    "created_at TIMESTAMP DEFAULT NOW()"
    ")"
)

MySQL_CREATE_CREDIT_CARD_TABLE_QUERY = (
    "CREATE TABLE IF NOT EXISTS credit_card ("
    "email VARCHAR(255),"
    "card_number VARCHAR(16) NOT NULL, "
    "expiration_month VARCHAR(2) NOT NULL, "
    "expiration_year VARCHAR(4) NOT NULL, "
    "cvv VARCHAR(255) NOT NULL, "
    "FOREIGN KEY (email) REFERENCES users(email) ON DELETE RESTRICT ON UPDATE RESTRICT"
    ");"
)

MySQL_CREATE_WIFI_SESSION_TABLE_QUERY = (
    "CREATE TABLE IF NOT EXISTS wifi_session ("
    "email VARCHAR(255) REFERENCES users(email),"
    "start_time BIGINT(20) NOT NULL, "
    "end_time BIGINT(20) NOT NULL, "
    "data_usage INTEGER NOT NULL, "
    "FOREIGN KEY (email) REFERENCES users(email) ON DELETE RESTRICT ON UPDATE RESTRICT"
    ");"
)

MYSQL_WIFI_SESSION_DELETE_EXPIRED_EVENT_QUERY = (
    "CREATE EVENT IF NOT EXISTS wifi_session_cleanup "
    "ON SCHEDULE EVERY 1 MINUTE "
    "DO "
    "DELETE FROM wifi_session WHERE end_time < unix_timestamp(now());"
)

INSERT_A_USER_QUERY = (
    "INSERT INTO users (full_name, email, password) " "VALUES (%s, %s, %s)"
)
INSERT_CREDIT_CARD_BY_USER_ID_QUERY = (
    "INSERT INTO credit_card "
    "(email, card_number, expiration_month, expiration_year, cvv)"
    "VALUES (%s, %s, %s, %s, %s)"
)
INSERT_WIFI_SESSION_QUERY = (
    "INSERT INTO wifi_session "
    "(email, start_time, end_time, data_usage)"
    "VALUES (%s, %s, %s, %s)"
)
IS_WIFI_SESSION_EXPIRED_QUERY = "SELECT email FROM wifi_session WHERE email = %s"
IS_USER_REGISTERED_QUERY = "SELECT * FROM users WHERE email = %s"
