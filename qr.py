import logging
import pandas as pd
import numpy as np
import mysql.connector
import qrcode
logger = logging.getLogger(__name__)
#create a connection to SQL database
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
df = pd.DataFrame(res,columns=['id','ups_account_number','tpu_account_number','street_number','street_name','kwh_consumption','electricity_cost','water_ccf','water_cost','wastewater_cost','solid_waste','surface_water','rental','recycle','late_fees','total','date'])
#an attempt to clear nans in month dataframe
df.replace('nan', np.nan)

df['full_address'] = df['street_number'].str[:-2] + ' ' + df['street_name']

def qrify(address):
    addy = address.replace(" ", '_')
    url = "http://127.0.0.1:5000/{}".format(addy)
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
        )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save('../QR/{}.png'.format(addy))
    logger.info("Image saved! ../QR/{}.png".format(addy))
    return

addresses = df.full_address.unique()
for addy in addresses:
    logger.info(addy)
    qrify(addy)
