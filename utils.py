from flask import Flask, request, render_template
from pprint import pprint
import logging
import mysql.connector
import pandas as pd
import numpy as np
import os
import sys
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# import things
from flask_table import Table, Col



def get_water_df():
    '''
    Function to get basic dataframe of water table back
    -->
    returns a df object
    '''
    cnx = mysql.connector.connect(user='root', password='$',host='127.0.0.1', database='sys')
    # name a variable to manage the connection
    cursor = cnx.cursor()

    #create a sql statement to reqeust data
    select_cmd = 'select * from water_2 where total !=0'
    #execute the select via cursor
    cursor.execute(select_cmd)
    #fetch results  & store in a res named variable
    res = cursor.fetchall()
    #create a dataframe with the res variable and our desired column names
    df = pd.DataFrame(res,columns=['id','ups_account_number','tpu_account_number','street_number','street_name','kwh_consumption','electricity_cost','water_ccf','water_cost','wastewater_cost','solid_waste','surface_water','rental','recycle','late_fees','total','date', 'full_address'])
    #an attempt to clear nans in month dataframe
    df.replace('nan', np.nan)
    return df

h2odf = get_water_df()

def df_to_html_table(df):
    '''
    takes in an df and --> returns an html object
    '''
    html = df.to_html(header="true", table_id='table', classes=['table table-striped table-sm'])
    return html

def get_all_uniq_addresses_by_date():
    '''
    get uniq addy df w/ year
    '''
    df = get_water_df()
    #create a sql statement to reqeust data
    test = sqldf(f"select distinct date,full_address from df")
    html = df_to_html_table(test)
    return html

def get_all_uniq_addresses():
    '''
    get uniq addy df
    '''
    df = get_water_df()
    #create a sql statement to reqeust data
    test = sqldf(f"select distinct full_address from df")
    html = df_to_html_table(test)
    return html

def get_all_uniq_addresses_list():
    '''
    get uniq addy list
    '''
    df = get_water_df()
    #create a sql statement to reqeust data
    test = sqldf(f"select distinct full_address from df")
    addy_list = list(test['full_address'])
    return addy_list

def get_address_data(address):
    '''
    dynamic selects to minimize the data selections
    '''
    #create a sql statement to reqeust data
    address_df = sqldf(f"select * from h2odf where full_address like '%{address}%'")
    #match = sqldf('select * from df where id like "%{}%"'.format(3),locals)
    return address_df

def home_descriptions():
    '''
    home page descriptions
    '''
    desc = {
        "Purpose": "The intentions of this project was to create campus awareness around sustainability in energy, water, & natrual gas",
        "Goals": "Spread awareness, get direct experiece with python, data science, flask based applications, and web deployments",
        "Methods": "Data collection, data cleansing, statistical modeling, linear regression, kmeans algorithms, and machine learning modeling"
    }
    return desc

def team_page():
    '''
    Sustainability Team descriptions
    '''

    about_us = {
            "Agostino Fante": {"About" :"Manager of on campus sustainability team, Political Science major with a passion for sports, technology, breakfast burritos, fishing and dogs", "Image": "Tino.png", "LinkedIn": "https://www.linkedin.com/in/tino-fante-9785b81a2"},
            "Kaylynn O'Curran": {"About" :"I use she/her pronouns. I will be graduating in 2023! I have worked for sustainability for roughly three years now and am a Field Lead. I am a Gender Queer Studies and Environmental Policy double major with a minor in Education and maybe Geology. In my free time I love to hike, camp, backpack, skateboard, surf, drink triple shot lattes, and read books. I've had a passion for protecting the environment for as long I can remember so this job is something I love!", "Image": "Kaylynn.png", "LinkedIn":"https://www.linkedin.com/in/kaylynn-o%E2%80%99curran-06719820b"},
            "Alden Robert": {"About" :"My name is Alden Robert and I use he/him pronouns. Class of ‘23. I use He/Him pronouns. I’m the student manager for sustainability services and a religious studies and IPE double major. Fun Fact: I speak danish", "Image": "Alden.png"},
            "Gerogia": {"About" :"My name is Georgia, and I use she/her pronouns. I am a Sociology/Anthropology and Environmental Policy and Decision Making double major with a minor in Education. I have been a part of the Sustainability team for 2 years now. I also compete on the varsity Women’s Basketball and Women’s Golf teams. I am also a member of Gamma Phi Beta. In my free time, I enjoy hiking, camping, and a good cup of coffee.", "Image": "Georgia.png"},

    }
    return about_us

def kmeans_clustering():
    '''
    intro to machine learning
    '''
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    import tkinter as tk
    df = get_water_df()
    kmeans = KMeans(n_clusters=3).fit(df)
    centroids = kmeans.cluster_centers_
    print(centroids,df.head())
    root = tk.Tk()

    plt.scatter(df['x'], df['y'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
    plt.show()
