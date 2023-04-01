import psutil
import json
from selenium import webdriver
import requests
from flask import Flask, request, jsonify
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

request_number = []
BASE_URL = "http://{}:{}/{}"
hostName = "0.0.0.0"
serverPort = 9285

app = Flask(__name__)


def init_and_login():
    # Navigate to the router's web interface
    driver.get("http://192.168.0.1")

    # Find the username and password fields and fill them in
    username_field = driver.find_element(By.ID, "userName")
    username_field.send_keys(ADMIN_USERNAME)
    password_field = driver.find_element(By.ID, "pcPassword")
    password_field.send_keys(ADMIN_PASSWORD)

    # Find the login button and click it
    login_button = driver.find_element(By.ID, "loginBtn")
    login_button.click()

    # Wait for the page to load
    driver.implicitly_wait(10)


def limit_upload_download_speed(upload_speed, download_speed):
    # Find the router's information
    driver.switch_to.frame("bottomLeftFrame")
    driver.find_element(By.XPATH, '//*[@id="ol38"]').click()
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame")
    egress_bandwidth_field = driver.find_element(By.XPATH,
                                                 '/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[3]/td['
                                                 '2]/input')
    egress_bandwidth_field.clear()
    egress_bandwidth_field.send_keys(upload_speed)
    egress_bandwidth_field = driver.find_element(By.XPATH,
                                                 '/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[4]/td['
                                                 '2]/input')
    egress_bandwidth_field.clear()
    egress_bandwidth_field.send_keys(download_speed)
    router_info = egress_bandwidth_field
    print(router_info)


def print_general_packets_data():
    # Get the network interface for internet usage
    interface = psutil.net_io_counters(pernic=True)['WiFi']

    # Get the total number of bytes sent and received
    bytes_sent: int = interface.packets_sent
    bytes_recv: int = interface.packets_recv

    # Calculate the total amount of data used
    total_data_used: int = bytes_sent + bytes_recv

    # Print the result
    print("Total internet data used: ", total_data_used, " packets")


@app.route("/data_feed", methods=["GET"])
def get_wireless_customer_data():
    driver.switch_to.default_content()
    driver.switch_to.frame("bottomLeftFrame")
    driver.find_element(By.XPATH, '//*[@id="a7"]').click()
    driver.find_element(By.XPATH, '//*[@id="a12"]').click()
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame")
    amount_connected_devices = driver.find_element(By.XPATH, '//*[@id="autoWidth"]/tbody/tr[3]/td[2]').text
    amount_range = range(int(amount_connected_devices))
    result_usage_dict: dict = {}
    for connection in amount_range:
        connection_index: int = 2 + connection
        connection_recieved_packets = driver.find_element(By.XPATH, '//*[@id="autoWidth"]/tbody/tr['
                                                                    '5]/td/table/tbody/tr[{}]/td[4]'.
                                                          format(connection_index)).text

        connection_sent_packets = driver.find_element(By.XPATH,
                                                      '//*[@id="autoWidth"]/tbody/tr[5]/td/table/tbody/tr[{}]/td[5]'.
                                                      format(connection_index)).text
        result_usage_dict["{}".format(connection)] = [connection_recieved_packets, connection_sent_packets]
    return jsonify(result_usage_dict), 200


def create_output_json(data_usage):
    with open("users_data.json", "w") as outfile:
        json.dump(data_usage, outfile)


if __name__ == '__main__':
    init_and_login()
    app.run(host="0.0.0.0", port=serverPort)
    #limit_upload_download_speed(download_speed='2049', upload_speed='513')
    #print_general_packets_data()
    driver.quit()
