from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to chromedriver
PATH = "C:/Program Files/Drivers/chromedriver.exe"
service = Service(PATH)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Navigate to WhatsApp Web
driver.get("https://web.whatsapp.com")

# Wait for WhatsApp Web to fully load
time.sleep(40)  # Adjust this as necessary based on how long it takes to log in

wait = WebDriverWait(driver, 30)

# Locate the search box for contacts
search_box_xpath = '//div[@contenteditable="true" and @data-tab="3"]'
search_box = wait.until(
    EC.presence_of_element_located((By.XPATH, search_box_xpath))
)

# Interact with the chat
contact_name = "Bijendra bhai"  # Change to your contact name
search_box.send_keys(contact_name)
search_box.send_keys(Keys.ENTER)

# Click the attachment button (paperclip icon)
attachment_button_xpath = '//span[@data-icon="clip"]'
attachment_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, attachment_button_xpath))
)
attachment_button.click()

# Upload the image using the file input
image_input = wait.until(
    EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
)
image_path = "C:/Users/madhu/Pictures/3.jpg"  # Replace with the correct path to your image
image_input.send_keys(image_path)

# Send the image by pressing the send button
send_button_xpath = '//span[@data-icon="send"]'
send_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, send_button_xpath))
)
send_button.click()

# Wait a bit to ensure the image is sent
time.sleep(8)

# Close the browser
driver.quit()
