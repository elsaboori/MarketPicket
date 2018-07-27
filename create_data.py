from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import requests
Base = declarative_base()
from datetime import datetime, timedelta
import pandas as pd
import api_SA

engine = create_engine('mysql+pymysql://root:fghtmn504@localhost:3306/StockPredictor')

Base.metadata.create_all(engine)

from sqlalchemy.orm import Session
session = Session(engine)
last_hour = (datetime.now() - timedelta(hours=10)).replace(microsecond=0)
now = datetime.now().replace(microsecond=0)

columns=['timestamp', 'stock', 'volume', 'newsSA','price', 'price_15min']
url = 'https://globalrealtime.xignite.com/v3/xGlobalRealTime.json/GetChartBars?IdentifierType=Symbol&Identifier={}&StartTime={}&EndTime={}&Precision=Minutes&Period=5&AdjustmentMethod=All&IncludeExtended=False&_token=ElhamAccess'
def stock_info(symbol, start_time, end_time):
	api = requests.get(url.format(symbol,start_time, end_time)).json()
	#bars = reponse['ChartBars']
	return api

def create_data(symbol, start_time, end_time):
	sentament = api_SA.sentamental_a(symbol)
	reponse = requests.get(url.format(symbol,start_time, end_time)).json()
	bars = reponse['ChartBars']
	df= pd.DataFrame(columns=columns)
	ls=[]
	#(if bars !=None) skips the bars if the API doesn't return any results
	if bars !=None:
		for i in range(0,len(bars)):
		    if i < len(bars)-1:
		        ls.append({
		        'timestamp':datetime.strptime("{}, {}".format(bars[i]['StartDate'], bars[i]['StartTime']), "%m/%d/%Y, %I:%M:%S %p"),
		        'stock':symbol,
		        'volume':bars[i]['Volume'],
		        'newsSA':sentament,
		        'price':bars[i]['Close'],
		        'price_15min':bars[i+1]['TWAP']
		        })
		    else:
		        ls.append({
		        'timestamp':datetime.strptime("{}, {}".format(bars[i]['StartDate'], bars[i]['StartTime']), "%m/%d/%Y, %I:%M:%S %p"),
		        'stock':symbol,
		        'volume':bars[i]['Volume'],
		        'newsSA':sentament,
		        'price':bars[i]['Close'],
		        'price_15min':bars[i]['TWAP']
		        })
    
		df = df.append(ls)
		df.loc[df.newsSA.isnull(),'no_news']=1
		df.loc[df.newsSA.notnull(),'no_news']=0
		data=df.to_json(orient='records')
        #df.to_sql('stock', con=engine,if_exists='append', index=False)
	else:
	    return None

	return data