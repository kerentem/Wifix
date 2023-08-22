import requests
import json
import time
import mysql.connector
import datetime

cnx = mysql.connector.connect(
    user="root", password="Harari76", host="localhost", database="usersdb"
)

SERVER_URL = "http://192.168.0.100:9285/get_live_data"  # Replace with the server URL


def send_get_request():
    response = requests.get(SERVER_URL)
    if response.status_code == 200:
        data = json.loads(response.text)
        print("Response:", data)
    else:
        print("Error:", response.status_code)

    # Extract the values from the JSON object
    router_id = data["routerId"]
    user_id = data["userId"]
    time = data["timestamp"]
    usage_per_sec = data["usagePerSec"]
    total_usage = data["totalUsage"]

    # Create a cursor object
    cnx.reconnect()
    cursor = cnx.cursor()

    # Insert the values into the MySQL database table
    add_data = (
        "INSERT INTO usage_data"
        "(router_id, user_id, time, usage_per_sec, total_usage) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    data_values = (router_id, user_id, time, usage_per_sec, total_usage)
    cursor.execute(add_data, data_values)

    # Commit the changes to the database
    cnx.commit()

    # Close the cursor and database connection
    cursor.close()
    cnx.close()


while True:
    send_get_request()
    time.sleep(120)
