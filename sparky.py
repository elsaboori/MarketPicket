import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
import re
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer, Tokenizer
import jsonify


analyzer = SentimentIntensityAnalyzer()
Base = declarative_base()

engine = create_engine('postgresql://product:pr0dPwnz@redshift1.db.xignite.com:5439/xignite')
last_hour = (datetime.now() - timedelta(hours=3)).replace(microsecond=0)
now = datetime.now().replace(microsecond=0)
data=engine.execute(
    "select parameters from view_usage_hits_recent where identifier ='XigniteGlobalRealTime_V3.GetGlobalRealTimeQuote' and timestamp> '{}' and timestamp<'{}'order by timestamp desc limit 20000".format(last_hour, now)
).fetchall()

#get the symbols out of the text file
list_identifier=[]
for i in range(len(data)):
    symbol = re.search(r'\<N\>Identifier\<\/N\>\<V\>(.*?)\<', data[i][0]).group(1)
    item = (i, symbol)
    list_identifier.append(item)

def top_movers():

#Using Spark to find the most active symbols(the ones clients called the most)
	spark = SparkSession.builder.appName('topMover').getOrCreate()
	df = spark.createDataFrame(list_identifier, ["id", "symbol"])

	tokeizer = Tokenizer(inputCol="symbol", outputCol="tokens")
	tokenized = tokeizer.transform(df)

	contvertvectorizer = CountVectorizer(minTF=1.0 , minDF =1.0 , vocabSize=2, inputCol='tokens', outputCol='Vectors, [Indexes], [Frequencies]')
	model = contvertvectorizer.fit(tokenized)
	result = model.transform(tokenized)
	result['Vectors, [Indexes], [Frequencies]']['[Frequencies]']


	from pyspark.sql.types import StringType
	df_vocab = tokenized.select('tokens').rdd.\
	           flatMap(lambda x: x[0]).\
	           toDF(schema=StringType()).toDF('symbol')

	# stringindexer = StringIndexer(inputCol='symbol', outputCol='StringIndexer(index)')
	# ordered_list=stringindexer.fit(df_vocab).transform(df_vocab).\
	#    distinct().\
	#    orderBy('StringIndexer(index)')

	#finallist = ordered_list.select("symbol").rdd.flatMap(list).collect()

	from pyspark.ml.feature import StringIndexer
	stringindexer = StringIndexer(inputCol='symbol', outputCol ='StringIndexer(index)')
	top_movers=stringindexer.fit(df_vocab).transform(df_vocab).distinct().orderBy('StringIndexer(index)')
	finallist=list(top_movers.toPandas().set_index('symbol').T.to_dict('list'))
	return finallist
