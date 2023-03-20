import psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

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


# Find the router's information
text: str = "//*[@id=/'a38/']"
driver.switch_to.frame("bottomLeftFrame")
driver.find_element(By.XPATH, '//*[@id="ol38"]').click()
driver.switch_to.default_content()
driver.switch_to.frame("mainFrame")

egress_bandwidth_field = driver.find_element(By.XPATH,
                                             '//*[@id="t_up_band"]')
router_info = egress_bandwidth_field
print(router_info)

# Close the webdriver
driver.quit()

# Get the network interface for internet usage
interface = psutil.net_io_counters(pernic=True)['WiFi']

# Get the total number of bytes sent and received
bytes_sent: int = interface.packets_sent
bytes_recv: int = interface.packets_recv

# Calculate the total amount of data used
total_data_used: int = bytes_sent + bytes_recv

# Print the result
print("Total internet data used: ", total_data_used, " packets")

if __name__ == '__main__':
    print('PyCharm')
