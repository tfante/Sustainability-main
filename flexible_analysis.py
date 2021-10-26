#/opt/anaconda3/bin/python3
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import numpy as np
import scipy as stats
#Import label encoder to convert categorical columns
from sklearn.preprocessing import LabelEncoder
#import visualization tools
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())
from utils import *



def get_address_data(address):
    df = get_water_df()
    #create a sql statement to reqeust data
    test = sqldf(f"select * from df where full_address like '%{address}%'")
    #match = sqldf('select * from df where id like "%{}%"'.format(3),locals)
    print(test.head())
    #execute the select via cursor
    #cursor.execute(select_cmd)
    #fetch results  & store in a res named variable
    #res = cursor.fetchall()

#get_address_data(address)
