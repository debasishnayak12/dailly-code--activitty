from ntscraper import Nitter
import pandas as pd

scraper=Nitter(log_level=1,skip_instance_check=False)

def scraping_tweets(user,num_of_tweets):
    tweets=scraper.get_tweets(user,mode="user",number=num_of_tweets)
    print(tweets)