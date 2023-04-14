import psutil
import json
from selenium import webdriver
from flask import Flask, request, jsonify
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
LIVE_USERS: int = 0
request_number = []
BASE_URL = "http://{}:{}/{}"
hostName = "0.0.0.0"
serverPort = 9285

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello Geeks!!"


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    client_ip = request.environ.get('REMOTE_ADDR')
    # return ['Your IP is: {}'.format(client_ip)]
    return jsonify({'ip': client_ip}), 200


@app.route("/user_ip", methods=["GET"])
def get_ip():
    client_ip = request.environ.get('REMOTE_ADDR')
    return jsonify({'ip': client_ip}), 200


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


@app.route("/change_speed", methods=['POST'])
def limit_upload_download_speed():
    input_json_object = request.get_json(force=True)
    client_ip = input_json_object['client_ip']
    upload_speed = input_json_object['upload_speed']
    download_speed = input_json_object['download_speed']
    # Find the router's information
    driver.switch_to.frame("bottomLeftFrame")
    driver.find_element(By.XPATH, '//*[@id="a38"]').click()
    driver.find_element(By.XPATH, '//*[@id="ol40"]').click()
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame")
    driver.find_element(By.XPATH, '//*[@id="autoWidth"]/tbody/tr[5]/td/input[1]').click()
    ip_range = driver.find_element(By.XPATH,
                                   '//*[@id="autoWidth"]/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/input[1]')
    ip_range.clear()
    ip_range.send_keys(client_ip)
    port_range_from = driver.find_element(By.XPATH,
                                          '/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/input[1]')
    port_range_from.clear()
    port_range_from.send_keys(1)
    port_range_to = driver.find_element(By.XPATH,
                                        '/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/input[2]')
    port_range_to.clear()
    port_range_to.send_keys(8000)
    egress_bandwidth_from = driver.find_element(By.XPATH,
                                                '/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[6]/td['
                                                '2]/input')
    egress_bandwidth_from.clear()
    egress_bandwidth_from.send_keys(1)
    egress_bandwidth_to = driver.find_element(By.XPATH,
                                              '/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[6]/td['
                                              '3]/input')
    egress_bandwidth_to.clear()
    egress_bandwidth_to.send_keys(upload_speed)
    ingress_bandwidth_from = driver.find_element(By.XPATH,
                                                 '/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[7]/td['
                                                 '2]/input')
    ingress_bandwidth_from.clear()
    ingress_bandwidth_from.send_keys(1)
    ingress_bandwidth_to = driver.find_element(By.XPATH,
                                               '/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[7]/td['
                                               '3]/input')
    ingress_bandwidth_to.clear()
    ingress_bandwidth_to.send_keys(download_speed)
    driver.find_element(By.XPATH, '//*[@id="autoWidth"]/tbody/tr[5]/td/input[1]').click()
    result = {"result": "SUCCESS"}
    return jsonify(result), 200


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
    global LIVE_USERS
    driver.switch_to.default_content()
    driver.switch_to.frame("bottomLeftFrame")
    driver.find_element(By.XPATH, '//*[@id="a7"]').click()
    driver.find_element(By.XPATH, '//*[@id="a12"]').click()
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame")
    LIVE_USERS = driver.find_element(By.XPATH, '//*[@id="autoWidth"]/tbody/tr[3]/td[2]').text
    amount_range = range(int(LIVE_USERS))
    result_usage_dict: dict = {}
    for connection in amount_range:
        connection_index: int = 2 + connection
        connection_received_packets = driver.find_element(By.XPATH, '//*[@id="autoWidth"]/tbody/tr['
                                                                    '5]/td/table/tbody/tr[{}]/td[4]'.
                                                          format(connection_index)).text

        connection_sent_packets = driver.find_element(By.XPATH,
                                                      '//*[@id="autoWidth"]/tbody/tr[5]/td/table/tbody/tr[{}]/td[5]'.
                                                      format(connection_index)).text
        result_usage_dict["{}".format(connection)] = [connection_received_packets, connection_sent_packets]
    return jsonify(result_usage_dict), 200


@app.route("/live_users", methods=["GET"])
def get_amount_users():
    result = {"result": LIVE_USERS}
    return jsonify(result), 200


def create_output_json(data_usage):
    with open("users_data.json", "w") as outfile:
        json.dump(data_usage, outfile)


if __name__ == '__main__':
    res = get_ip()
    init_and_login()
    app.run(host="0.0.0.0", port=serverPort)
    driver.quit()
