import json
from datetime import datetime, timedelta
import numpy as np
from newsapi import NewsApiClient
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time

yesterday=datetime.now()- timedelta(hours=5)


def get_sentiment(text):
    # Run Vader Analysis on each text
    compound = analyzer.polarity_scores(str(text))["compound"]
    return compound

def sentamental_analyst(symbol):
	sentamental_a='There is no related news in my database!'
    executable_path = {'executable_path': '/Users/elham/Desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = f'https://www.bloomberg.com/quote/{symbol}:US'
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #time.sleep(5)
    headlines_scraped = soup.findAll("div", {"class": "headline__07dbac92"})
    headlines = [things.text for things in headlines_scraped]
    time_headlines= soup.findAll("div", {"class": "publishedAt__4009bb4f "})
    time_for_headlines = [things.text for things in time_headlines]
    headlines = [things.text for things in headlines_scraped]
    df_headlines = pd.DataFrame({
                'time': time_for_headlines,
                'headlines': headlines,
                'sentimental_value' : [get_sentiment(headline) for headline in headlines]
    })
    df_headlines['time']=pd.to_datetime(df_headlines['time'])
    df_headlines=df_headlines[df_headlines['time']>=yesterday]
    sentamental_a=df_headlines['sentimental_value'].mean()
    browser.quit()
    return sentamental_a
    
