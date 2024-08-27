import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
from datetime import datetime
from client_api import send_tweets

PATH="C:\Program Files\Drivers\chromedriver.exe"
service=Service(PATH)
driver=webdriver.Chrome(service=service)
driver.get("https://x.com/explore")

sleep(5)
user_name=driver.find_element(By.XPATH,"//input[@name='text']")
user_name.clear()
#user_name.send_keys("Debasish8384887")
user_name.send_keys("debasish_n60898")

sleep(5)
next_button=driver.find_element(By.XPATH, "//span[contains(text(),'Next')]")
next_button.click()

sleep(5)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
)
password.clear()
# password.send_keys('debu@720584')
password.send_keys('debu720584')
sleep(5)
login_button=driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
login_button.click()


#search button
sleep(5)
subject="#pumadive"
search_button=driver.find_element(By.XPATH,"//input[@placeholder='Search']")
search_button.clear()
sleep(4)
search_button.send_keys(subject)
search_button.send_keys(Keys.ENTER)

#click on Latest 
sleep(5)
latest=driver.find_element(By.XPATH,"//span[contains(text(),'Latest')]")
latest.click()

# usertags=[]
# timestamps=[]
# tweets=[]
# no_of_likes=[]
# no_of_comments=[]
# no_of_retweets=[]
seen_tweets=set()


#articles=driver.find_elements(By.XPATH,"//article[@data-testid='tweet']")

def is_today(tweet_time):
    try:
        tweet_date = datetime.strptime(tweet_time, '%Y-%m-%dT%H:%M:%S.%fZ').date()
        print("tweet date :",tweet_date)
    except ValueError:
        return False  # Handle parsing errors gracefully
    return tweet_date == datetime.today().date()

refresh_interval = 60  # Time interval for refreshing the page (in seconds)
last_refresh_time = time.time()

while True:
    # Wait for articles to be present
    #WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']")))
    try:
        usertags=[]
        current_time=time.time()
        
        if current_time - last_refresh_time > refresh_interval:
            driver.refresh()
            last_refresh_time = current_time
            print("Page refreshed")
            time.sleep(5)  # Allow time for the page to reload
            
        articles = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
        )
        if not articles:
            print("No articles found.")
            break
        
        for article in articles:
            try:
                #find usertag,tmestamp,liikes,comments,retwetes
                Usertag = article.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
                Timestamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
                
                unique_id = f"{Usertag}_{Timestamp}"
                print("unique id:", unique_id)
                
                if unique_id in seen_tweets:
                    continue
                #adding to seen_tweets tuple to avoid duplicates 
                seen_tweets.add(unique_id)
                
                if not is_today(Timestamp):
                    continue
                
                tweets = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                Likes = article.find_element(By.XPATH, ".//button[@data-testid='like']").text
                Comments = article.find_element(By.XPATH, ".//button[@data-testid='reply']").text
                Retweets = article.find_element(By.XPATH, ".//button[@data-testid='retweet']").text

                usertags.append(Usertag)
                
                #sending data to database through api
                send_tweets(Usertag,Timestamp,tweets,Likes,Comments,Retweets)
                
                if len(usertags) > 20:
                    break

            except Exception as e:
                print(f"An error occurred: {e}")
                continue
        # Scroll down to load more tweets
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)
    
    except Exception as e:
        print(f"An error occure during scraping  : {e}")
        break
    
    
        
   

        
        

