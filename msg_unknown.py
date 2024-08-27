import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("user-data-dir=C:/Users/madhu/AppData/Local/Google/Chrome/User Data")
options.add_argument("profile-directory=Profile 1")

PATH="C:\Program Files\Drivers\chromedriver.exe"
service=Service(PATH)
driver=webdriver.Chrome(service=service,options=options)
sleep(10)
driver.get("https://web.whatsapp.com")
driver.maximize_window()

wait=WebDriverWait(driver,100)

sleep(10)
# Message to send
msg = "Hello! Don't reply to this message!"
try:

    contact_name=["8969-941-567","7000770007"]
    # Re-locate contact
    for contact in contact_name:
        plus_icon_path='//*[@id="app"]/div/div[2]/div[3]/header/header/div/span/div/span/div[1]/div/span'
        
        plus_icon=WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, plus_icon_path))
        )
        plus_icon.click()
        sleep(2)
        while True:
            try:
                search_box_xpath = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div/p'
                search_box = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, search_box_xpath))
                )
                search_box.click()
                search_box.send_keys(contact)
                sleep(3)
                search_box.send_keys(Keys.ENTER)
                break
            except Exception as e:
                print(f"Failed to locate search box {e}")
                sleep(3)
    
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
        # for msg in msg_list:
        #     try:
        #         msg_box = WebDriverWait(driver, 10).until(
        #             EC.presence_of_element_located((By.XPATH, msg_path))
        #         )
        #         msg_box.click()  # Ensure the input box is focused
                
        #         # Send message
        #         msg_box.send_keys(msg)
        #         msg_box.send_keys(Keys.ENTER)
        #         sleep(1)  # Adding a slight dela
        #     except Exception as e:
        #         print(f"Error sending message: {e}")
        #         break
        msg_box.click()  # Ensure the input box is focused
                
        # Send message
        msg_box.send_keys(msg)
        sleep(0.5)
        msg_box.send_keys(Keys.ENTER)
        sleep(1)  # Adding a slight dela
        # search_box.click()
        # search_box.clear()
        sleep(3)
    sleep(30)
            
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
    sleep(30)

except Exception as e:
    print(f"An error occurred: {e}")




        

