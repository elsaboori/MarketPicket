from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
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
#from newsapi import NewsApiClient
import requests
import time
from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer, Tokenizer
from pyspark.ml.feature import StringIndexer
import sparky
import api_SA
import create_data
import getData

app = Flask(__name__)
last_hour = (datetime.now() - timedelta(hours=5)).replace(microsecond=0)
now = datetime.now().replace(microsecond=0)

@app.route('/')
def index():
    data = getData.dummy_func()
    # final = sparky.top_movers()
    return render_template('index.html', data=data)
    # return jsonify(final[:15])

    
@app.route('/data/<symbol>')
def data(symbol):
    last_hour = (datetime.now() - timedelta(hours=5)).replace(microsecond=0)
    now = datetime.now().replace(microsecond=0)
    last_hour_data=create_data.create_data(symbol, last_hour, now)
    return last_hour_data


@app.route('/top_movers')
def top_movers():
    final = sparky.top_movers()
    return jsonify(final[:15])

@app.route('/stock_info/<symbol>')
def stock_info(symbol):
    last_hour = (datetime.now() - timedelta(hours=5)).replace(microsecond=0)
    now = datetime.now().replace(microsecond=0)
    info=create_data.stock_info(symbol, last_hour, now)
    return jsonify(info)



@app.route('/sentamental/<symbol>')
def sentamental(symbol):
    sentament = api_SA.sentamental_a(symbol)
    return jsonify(sentament)



    #return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)