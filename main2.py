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
from client_api2 import send_tweets

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

seen_tweets=set()

while True:
    try:
            
        articles = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.XPATH, "//article[@data-testid='tweet']"))
        )
        if not articles:
            print("No articles found.")
            break
        
        for article in articles:
            try:
                tweet_link=article.find_element(By.XPATH,".//a[@href and contains(@href ,('/status/'))]")
                tweet_url=tweet_link.get_attribute('href')
                tweet_id=tweet_url.split('/')[-1]
                
                time.sleep(1)
                
                #find usertag,tmestamp,liikes,comments,retwetes
                # Usertag = article.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
                Timestamp = article.find_element(By.XPATH, ".//time").get_attribute('datetime')
                
                try:
                    
                    image_element=article.find_element(By.XPATH,".//img[contains(@src , 'twimg.com/media')]")
                    # image_element=article.find_element(By.XPATH,".//div[@class='css-175oi2r r-1kqtdi0 r-1phboty r-rs99b7 r-1867qdf r-1udh08x r-o7ynqc r-6416eg r-1peqgm7 r-1ny4l3l']//img[@alt='Image']")
                    
                    image_url=image_element.get_attribute('src')
                    
                except Exception:
                    iamge_url=None
                
              
                if tweet_id in seen_tweets:
                    continue
                #adding to seen_tweets tuple to avoid duplicates 
            
                seen_tweets.add(tweet_id)
                print(len(seen_tweets))
                
                Tweets = article.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                
                
                print("Tweet :",Tweets)
                print("Tweet_id :",tweet_id)
                print("image url :",image_url)
                send_tweets(tweet_id,Tweets,image_url,Timestamp)
                #sending data to database through api
                #send_tweets(Usertag,Timestamp,tweets,Likes,Comments,Retweets)
                if len(seen_tweets) > 5:
                    break

            except Exception as e:
                print(f"An error occurred: {e}")
                break
            
        if len(seen_tweets) > 20:
            break
        # Scroll down to load more tweets
        
        
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(20)
    
    except Exception as e:
        print(f"An error occure during scraping  : {e}")
        break

    
    
        
   

        
        

