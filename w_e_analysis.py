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

#create a connection to SQL database
cnx = mysql.connector.connect(user='root', password='tinofante',host='127.0.0.1', database='sys')
# name a variable to manage the connection
cursor = cnx.cursor()

#create a sql statement to reqeust data
select_cmd = 'select * from water_2 where total !=0'
#execute the select via cursor
cursor.execute(select_cmd)
#fetch results  & store in a res named variable
res = cursor.fetchall()


#create a dataframe with the res variable and our desired column names
month = pd.DataFrame(res,columns=['id','ups_account_number','tpu_account_number','street_number','street_name','kwh_consumption','electricity_cost','water_ccf','water_cost','wastewater_cost','solid_waste','surface_water','rental','recycle','late_fees','total','date'])
#an attempt to clear nans in month dataframe
month.replace('nan', np.nan)

#print(month.dtypes)
#my_conn = create_engine("mysql:MySQLdb//root:tinofante@127.0.0.1/water")
#my_data = pd.read_sql('select * from water',my_conn)
#print(res)
#print(month)
total_null = month.isnull().sum().sort_values(ascending=False)
#print(total_null)

def calc_percent_missing():
    '''define a function to get the percent missing of the dataframe'''
    percent_missing = (month.isnull().sum()/month.isnull().count()).sort_values(ascending=False)
    return percent_missing
percent_missing = calc_percent_missing()

missing_data = pd.concat([total_null,percent_missing], axis = 1, keys = ['total', 'percent'])
#print(missing_data)

new = month[['total','date']].copy()
#new = pd.DataFrame([month.total, month.date]).transpose()
#print(new.head)
def build_Prophet():
    df = new
    df = df.rename(columns={'date':'ds','total': 'y'})
    df['y'] = [x for x in df['y']]
    df['ds'] = [pd.to_datetime(x, format='%Y%m', errors='coerce', infer_datetime_format=True) for x in df['ds']]
    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    df=df.mask(df==0).fillna(df.mean())
    df['y'] = pd.to_numeric(df['y'])
    df = df.replace([np.inf, -np.inf], np.nan)
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    m.plot(forecast)

    m.plot_components(forecast)

    df['y'] = np.log(df['y'].astype('float64'))

    df['cap'] = 5
    m = Prophet(growth='logistic')
    m.fit(df)

    future = m.make_future_dataframe(periods=365)
    future['cap'] = 5
    forecast = m.predict(future)
    m.plot(forecast)

    #second section
    df['y'] = 10 - df['y']
    df['cap'] = 9
    df['floor'] = 1
    future['cap'] = 9
    future['floor'] = 1
    m = Prophet(growth='logistic')
    m.fit(df)
    fcast = m.predict(future)
    m.plot(fcast)

    m = Prophet(weekly_seasonality=False)
    m.add_seasonality(name='weekly_', period=7, fourier_order=3,)
    forecast = m.fit(df).predict(future)
    m.plot_components(forecast)

build_Prophet()

def run_analysis():
    categorical_cols = ['ups_account_number','tpu_account_number','street_number','street_name','kwh_consumption','electricity_cost','water_ccf','water_cost','wastewater_cost','solid_waste','surface_water','rental','recycle','late_fees','total','date']
    labelEncoder = LabelEncoder()
    for col in categorical_cols:
        month[col]=labelEncoder.fit_transform(month[col])

    #calculate z scores:
    zscore=np.abs(stats.stats.zscore(month))
    # taking out zscores greater than 3 or 3 std deviaitons away from the mean - think normal dist.
    month=month[(zscore<3)]
    sns.displot(month['water_cost'], kind='hist', stat='density')
    print(zscore)

    var = 'water_ccf'
    df = pd.concat([month['water_cost'], month[var]], axis=1)
    f, ax = plt.subplots(figsize=(4,4))
    fig = sns.boxplot(x=var, y='water_cost', data=df)
    fig.axis(ymin=1000, ymax=10000)
    print(fig)

    #correlation matrix
    correlation_matrix = df.corr()
    f, ax = plt.subplots(figsize=(20,10))
    sns.heatmap(correlation_matrix, cmap="YlGnBu", vmax=9, square=True)
    print(correlation_matrix)

    #Linaear Regression
    from sklearn.model_selection import train_test_split
    X = df.drop('water_ccf', axis=1)
    y = df['water_cost']
    xtrain, xtest, ytrain, ytest = train_test_split(X,y,test_size=0.50, random_state=80, shuffle=True)

    from sklearn.linear_model import LinearRegression
    LR = LinearRegression(copy_X=True)
    LR.fit(xtrain,ytrain)
    print(LR)
    #lr model trained ^

    yhat = LR.predict(xtest)
    from sklearn.metrics import mean_squared_error
    print("Mean square error of LR model:", mean_squared_error(ytest, yhat))

    #calculate z scores:
    zscore=np.abs(stats.stats.zscore(month))
    # taking out zscores greater than 3 or 3 std deviaitons away from the mean - think normal dist.
    month=month[(zscore<3)]
    sns.displot(month['kwh_consumption'], kind='hist', stat='density')
    print(zscore)

    var = 'kwh_consumption'
    df = pd.concat([month['electricity_cost'], month[var]], axis=1)
    f, ax = plt.subplots(figsize=(4,4))
    fig = sns.boxplot(x=var, y='electricity_cost', data=df)
    fig.axis(ymin=1000, ymax=10000)
    print(fig)

    #correlation matrix
    correlation_matrix = df.corr()
    f, ax = plt.subplots(figsize=(20,10))
    sns.heatmap(correlation_matrix, cmap="YlGnBu", vmax=9, square=True)
    print(correlation_matrix)

    #Linaear Regression
    from sklearn.model_selection import train_test_split
    X = df.drop('kwh_consumption', axis=1)
    y = df['electricity_cost']
    xtrain, xtest, ytrain, ytest = train_test_split(X,y,test_size=0.50, random_state=80, shuffle=True)
    #print(X, y)

    from sklearn.linear_model import LinearRegression
    LR = LinearRegression(copy_X=True)
    LR.fit(xtrain,ytrain)
    #lr model trained ^
    print(LR)

    yhat = LR.predict(xtest)
    from sklearn.metrics import mean_squared_error
    print("Mean square error of LR model:", mean_squared_error(ytest, yhat))

#print(month.columns)


cnx.commit()
#close DB connection
cnx.close()
