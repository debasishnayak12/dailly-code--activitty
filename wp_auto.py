import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time

PATH="C:\Program Files\Drivers\chromedriver.exe"
service=Service(PATH)
driver=webdriver.Chrome(service=service)
driver.get("https://web.whatsapp.com")
driver.maximize_window()

wait=WebDriverWait(driver,100)

sleep(40)
contact_name='Bijendra bhai'
try:
      # Message to send
    #msg = "Hello! This is testing for automation."
    msg_list=[
        "Hi,Buddy",
        "Good afternoon!",
        "How are you doing ?",
        "Lets plan for a tour.",
        "This is for automation testing.",
        "Please don't reply to this message!",
        
    ]
    # Re-locate contact
    search_box_xpath = '//div[@contenteditable="true" and @data-tab="3"]'
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, search_box_xpath))
    )
    search_box.click()
    search_box.send_keys(contact_name)
    search_box.send_keys(Keys.ENTER)
    sleep(3)
    #contact_path = f"//span[contains(@title , '{contact_name}')]"
    
    # while True:
    #     try:
    #         contact = WebDriverWait(driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, contact_path))
    #         )
    #         contact.click()
    #         break
    #     except Exception as e:
    #         print(f"Failed to locate contact: {e}")
    #         sleep(2)  # Wait a bit before retrying

    # Re-locate the message input box
    msg_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
    
    while True:
        try:
            msg_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, msg_path))
            )
            msg_box.click()  # Ensure the input box is focused
            break
        except Exception as e:
            print(f"Failed to locate message box: {e}")
            sleep(2)  # Wait a bit before retrying
        


  

    # Send the message multiple times
    for msg in msg_list:
        try:
            msg_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, msg_path))
            )
            msg_box.click()  # Ensure the input box is focused
            
            # Send message
            msg_box.send_keys(msg)
            msg_box.send_keys(Keys.ENTER)
            sleep(1)  # Adding a slight dela
        except Exception as e:
            print(f"Error sending message: {e}")
            break
    sleep(40)
        
    # This is for single message 
    # for i in range(5):
    #     try:
    #         msg_box = WebDriverWait(driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, msg_path))
    #         )
    #         msg_box.click()  # Ensure the input box is focused
            
    #         # Send message
    #         msg_box.send_keys(msg)
    #         msg_box.send_keys(Keys.ENTER)
    #         sleep(0.3)  # Adding a slight dela
    #     except Exception as e:
    #         print(f"Error sending message: {e}")
    #         break
    # sleep(10)

except Exception as e:
    print(f"An error occurred: {e}")


