import threading
import time
import click
import psutil
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
LIVE_USERS: int = 0
request_number = []
hostName = "0.0.0.0"
serverPort = 9285
LIM_UPLOAD_SPEED = 800
LIM_DOWNLOAD_SPEED = 8000
MAX_USERS: int = 30
ACTIVE_USERS: int = 0
app = Flask(__name__)
UNLIMITED_USERS: dict = {}


@app.route("/")
def hello():
    return "Hello!!"


def run_scheduler():
    while True:
        print("run")
        threading.Timer(30.0, limit_live_free_users).start()
        time.sleep(30)


@click.command(name='scheduler')
@click.pass_context
def activate_scheduler(ctx):
    thread = threading.Thread(target=run_scheduler)
    thread.start()


app.cli.add_command(activate_scheduler)


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    client_ip = request.environ.get("REMOTE_ADDR")
    return jsonify({"ip": client_ip}), 200


@app.route("/user_ip", methods=["GET"])
def get_ip():
    client_ip = request.environ.get("REMOTE_ADDR")
    return jsonify({"ip": client_ip}), 200


def init_and_login():
    # Navigate to the router's web interface
    try:
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
    except Exception as e:
        print(f"An error occurred while initializing and logging in: {e}")


@app.route("/remove_user", methods=["POST"])
def remove_user():
    global ACTIVE_USERS
    global UNLIMITED_USERS
    input_json_object: str = request.get_json(force=True)
    try:
        ip: str = input_json_object["ip"]
    except Exception as e:
        result = {"result": "Wrong IP"}
        return jsonify(result), 200
    UNLIMITED_USERS.pop(ip)
    result = {"result": "Success"}
    return jsonify(result), 200


@app.route("/change_speed", methods=["POST"])
def cancel_limit_user():
    global ACTIVE_USERS
    global UNLIMITED_USERS
    input_json_object: str = request.get_json(force=True)
    try:
        company_name: str = input_json_object["company_name"]
    except Exception as e:
        company_name: str = ""
    try:
        ip: str = input_json_object["ip"]
        upload_speed: str = input_json_object["upload_speed"]
        download_speed: str = input_json_object["download_speed"]
    except Exception as e:
        print(f"An error occurred while reading json data input: {e} + {input_json_object}")
        result = {"result": "Json Error"}
        return jsonify(result), 405
    ACTIVE_USERS += 1
    UNLIMITED_USERS[f'{ACTIVE_USERS}'] = ip
    driver.refresh()
    driver.switch_to.frame("bottomLeftFrame")
    driver.find_element(By.XPATH, '//*[@id="a38"]').click()
    driver.find_element(By.XPATH, '//*[@id="a40"]').click()
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame")
    for i in range(3, MAX_USERS):
        try:
            text = driver.find_element(By.XPATH,
                                       f'/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[{i}]/td[2]').text
            if ip in text:
                driver.find_element(By.XPATH, f'/html/body/form/center'
                                              f'/table/tbody/tr[3]/td/table/tbody/tr[{i}]/td[8]/a[2]').click()
                result = {"result": "SUCCESS"}
                driver.refresh()
                return jsonify(result), 200
        except Exception as e:
            result = {"result": "Wrong IP"}
            driver.refresh()
            return jsonify(result), 405


def limit_upload_download_speed(ip, upload_speed, download_speed, company_name):
    # Find the router's information
    driver.refresh()
    driver.switch_to.frame("bottomLeftFrame")
    driver.find_element(By.XPATH, '//*[@id="a38"]').click()
    driver.find_element(By.XPATH, '//*[@id="ol40"]').click()
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame")
    driver.find_element(
        By.XPATH, '//*[@id="autoWidth"]/tbody/tr[5]/td/input[1]'
    ).click()
    ip_range = driver.find_element(
        By.XPATH, '//*[@id="autoWidth"]/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/input[1]'
    )
    ip_range.clear()
    ip_range.send_keys(ip)
    port_range_from = driver.find_element(
        By.XPATH,
        "/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/input[1]",
    )
    port_range_from.clear()
    port_range_from.send_keys(1)
    port_range_to = driver.find_element(
        By.XPATH,
        "/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/input[2]",
    )
    port_range_to.clear()
    port_range_to.send_keys(8000)
    egress_bandwidth_from = driver.find_element(
        By.XPATH,
        "/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[6]/td[" "2]/input",
    )
    egress_bandwidth_from.clear()
    egress_bandwidth_from.send_keys(1)
    egress_bandwidth_to = driver.find_element(
        By.XPATH,
        "/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[6]/td[" "3]/input",
    )
    egress_bandwidth_to.clear()
    egress_bandwidth_to.send_keys(upload_speed)
    ingress_bandwidth_from = driver.find_element(
        By.XPATH,
        "/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[7]/td[" "2]/input",
    )
    ingress_bandwidth_from.clear()
    ingress_bandwidth_from.send_keys(1)
    ingress_bandwidth_to = driver.find_element(
        By.XPATH,
        "/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[7]/td[" "3]/input",
    )
    ingress_bandwidth_to.clear()
    ingress_bandwidth_to.send_keys(download_speed)
    driver.find_element(
        By.XPATH, '//*[@id="autoWidth"]/tbody/tr[5]/td/input[1]'
    ).click()
    driver.refresh()
    result = {"result": "SUCCESS"}
    return jsonify(result), 200


def print_general_packets_data():
    # Get the network interface for internet usage
    interface = psutil.net_io_counters(pernic=True)["WiFi"]

    # Get the total number of bytes sent and received
    bytes_sent: int = interface.packets_sent
    bytes_recv: int = interface.packets_recv

    # Calculate the total amount of data used
    total_data_used: int = bytes_sent + bytes_recv

    # Print the result
    print("Total internet data used: ", total_data_used, " packets")


@app.route("/routine_check", methods=["GET"])
def limit_live_free_users() -> tuple:
    global LIVE_USERS
    driver.switch_to.default_content()
    driver.switch_to.frame("bottomLeftFrame")
    driver.find_element(By.XPATH, '//*[@id="a15"]').click()
    driver.find_element(By.XPATH, '//*[@id="a17"]').click()
    driver.switch_to.default_content()
    driver.switch_to.frame("mainFrame")
    LIVE_USERS = 0
    for i in range(2, MAX_USERS):
        try:
            driver.find_element(By.XPATH, f'//*[@id="autoWidth"]/tbody/tr[3]/td/table/tbody/tr[{i}]/td[4]')
            LIVE_USERS += 1
        except Exception as e:
            break

    amount_range = range(int(LIVE_USERS))
    result_usage_dict: dict = {}
    # limit_upload_download_speed
    for connection in amount_range:
        connection_index: int = 2 + connection
        driver.switch_to.default_content()
        driver.switch_to.frame("bottomLeftFrame")
        driver.find_element(By.XPATH, '//*[@id="a15"]').click()
        driver.find_element(By.XPATH, '//*[@id="a17"]').click()
        driver.switch_to.default_content()
        driver.switch_to.frame("mainFrame")
        client_ip = driver.find_element(By.XPATH,
                                        f'//*[@id="autoWidth"]/tbody/tr[3]'
                                        f'/td/table/tbody/tr[{connection_index}]/td[4]').text
        if client_ip in UNLIMITED_USERS.values():
            continue
        else:
            limit_upload_download_speed(ip=client_ip, download_speed=LIM_DOWNLOAD_SPEED, upload_speed=LIM_UPLOAD_SPEED,
                                        company_name="Initial")

    driver.refresh()
    result = {"result": "SUCCESS"}
    return jsonify(result), 200


@app.route("/live_users", methods=["GET"])
def get_amount_users():
    result = {"result": LIVE_USERS}
    return jsonify(result), 200


if __name__ == "__main__":
    init_and_login()
    app.run(host="0.0.0.0", port=serverPort)
    driver.quit()
