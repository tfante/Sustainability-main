import numpy as np
import pandas as pd
import glob
import re
import calendar
import mysql.connector
from sqlalchemy import create_engine
#create empty list
li = []
cons = []
#create months dictionary
path = './'
#use glob to accummulate a list of .xls files
all_files = glob.glob(path + "/*.xls")

#first for loop for each excel in excels
for filename in all_files:
	xls = pd.ExcelFile(filename)
	#get sheet names into a list
	sheets = xls.sheet_names
	#print(filename)
#iterate over the list to get each sheet
	for m in sheets:
		#use regular expression to find 4 digit year in file Name
		months = dict((month,index) for index, month in enumerate(calendar.month_abbr))
		#use regular expression to find 4 digit year in file Name
		year = re.findall(r"[0-9]{4}", filename)
		#dictionary lookup on each iteration of sheet
		#print(months)
		if "Index" in m:
			continue
		if (m.capitalize()[:3] not in months) or ('Alloc' in m) or (m=='June'):
			continue
		month = months[m.capitalize()[:3]]
		#create a variable of the newly constructed date
		formatted_date = year[-1] + "0" + str(month)
		#use conditional to skip date if needed
		if year in ['2004','2005', '2006', '2007']:
			df = pd.read_excel(xls, m, skiprows=1)
		else:
			df = pd.read_excel(xls, m)
			#print(m,df.columns)
		#insert new date into new dataframe column
		df['Date'] = formatted_date
		df.set_index('Date')
		#append sheet dataframe to li(list object of all dataframes)
		df = df[df.columns.drop(list(df.filter(regex='Unnamed')))]
		#print(filename, m, df.columns)
		li.append(df)
frame = pd.concat(li, axis=0,)
#print(frame.head())

cnx = mysql.connector.connect(user='root', password='$',host='localhost', database='sys')
cursor = cnx.cursor()
cols=df.columns
for k,v in zip(frame.index, frame.values):
	#generate mysql insert statement using value index (going over the list)
	insert = 'insert into sustainability (pse_account, rate, ups_account, physical_address, sub_account_title,therms_1,therms_2,cost, date) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8])
	#print(insert)
	res = cursor.execute(insert)
	#print(res)

select_cmd = 'select * from sustainability'
#execute the select via cursor
cursor.execute(select_cmd)
#fetch results
res = cursor.fetchall()


cnx.commit()
cnx.close()
