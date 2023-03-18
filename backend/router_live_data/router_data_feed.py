import psutil
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the webdriver to use Firefox
driver = webdriver.Chrome()

# Navigate to the router's web interface
driver.get("http://192.168.0.1")

# Find the username and password fields and fill them in
username_field = driver.find_element(By.ID, "userName")
username_field.send_keys("admin")
password_field = driver.find_element(By.ID, "pcPassword")
password_field.send_keys("admin")

# Find the login button and click it
login_button = driver.find_element(By.ID, "loginBtn")
login_button.click()

# Wait for the page to load
driver.implicitly_wait(10)

# Find the router's information

text = "//*[@id=/'a38/']"
driver.switch_to.frame("bottomLeftFrame")
driver.find_element(By.XPATH, '//*[@id="ol38"]').click()
#/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/input
driver.find_element(By.XPATH, '//*[@id="a39"]')
driver.switch_to.frame("mainFrame")
router_info = driver.find_element(By.XPATH, '/html/body/form/center/table/tbody/tr[3]/td/table/tbody/tr[3]/td[1]').text
print(router_info)

# Close the webdriver
driver.quit()

# Get the network interface for internet usage
interface = psutil.net_io_counters(pernic=True)['WiFi']  # Replace 'Ethernet' with your interface name

# Get the total number of bytes sent and received
bytes_sent = interface.packets_sent
bytes_recv = interface.packets_recv

# Calculate the total amount of data used
total_data_used = bytes_sent + bytes_recv

# Print the result
print("Total internet data used: ", total_data_used, " packets")

if __name__ == '__main__':
    print('PyCharm')
