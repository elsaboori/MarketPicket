import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

url ='https://api.intrinio.com/news?identifier={}'
news_date=[]
news_summary=[]
yesterday=datetime.now()- timedelta(days=1)


def get_sentiment(summary):
    # Run Vader Analysis on each text
    compound = analyzer.polarity_scores(str(summary))["compound"]
    return compound



def sentamental_a(symbol):
	response = requests.get (url.format(symbol),auth=('user', 'pass'))
	data=response.json()['data']
	for news in data:
		news_date.append(pd.to_datetime(news['publication_date']))
		news_summary.append(news['summary'])
	df= pd.DataFrame({
		'date': news_date,
		'summary': news_summary,
		'sentimental_value' : [get_sentiment(news) for news in news_summary]
		})
	df = df[df['date']>yesterday]
	s_analys = df['sentimental_value'].std()
	return s_analys