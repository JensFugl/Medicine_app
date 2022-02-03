# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 11:03:19 2022

@author: jensr
"""
# pip install webdriver-manager
# conda install -c conda-forge selenium


from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import pandas as pd


#application.py
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

url = "https://www.medicinpriser.dk/default.aspx"
driver.get(url)

#element_text = driver.page_source
#element = driver.execute_script("return document.documentElement.outerHTML")
#user_agent = driver.execute_script("return navigator.userAgent;")
#print(element_text)
#print(user_agent)
#select search box
search = driver.find_element(By.ID,"ctl00_ctl07_simpleForm_LaegemiddelBox")
search.send_keys("Pulmicort")
search.send_keys(Keys.RETURN)
print(search)

#select All rows
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element(By.ID, "ctl00_ctl07_Results_PagerTop_ResultsCountList"))
select.select_by_visible_text('Alle')

table = driver.find_element(By.ID, "mainContainer")
print(table)

soup = BeautifulSoup(driver.page_source, 'lxml')
# Obtain information from tag table id
table1 = soup.find(id="mainContainer")
# Obtain every title of columns with tag <th>
headers = []
for i in table1.find_all('th'):
 title = i.text
 headers.append(title)


# Create a dataframe
df = pd.DataFrame(columns = headers)


# Create a for loop to fill mydata
df = pd.DataFrame(columns = ['Lægemiddel/varenummer', 'Styrke', 'Pakning'])
table_left = table1.find(id="ctl00_ctl07_Results_LeftGridDiv")

for j in table_left.find_all("tr")[1:]:
    row_data = j.find_all("td")
    row = [i.text for i in row_data]
    length = len(df)
    df.loc[length] = row

df2 = pd.DataFrame(columns = ['Virksomt stof', 'Firma', 'Tilskud beregnes af  (kr.)', 'Pris pr. enhed (kr.)', 'Pris pr.pakning (kr.)'])
table_right = table1.find(id="ctl00_ctl07_Results_RightGridDiv")

for j in table_right.find_all("tr")[1:]:
    row_data = j.find_all("td")
    row = [i.text for i in row_data]
    length = len(df2)
    df2.loc[length] = row

driver.quit()

df = df.merge(df2, how ='outer', right_index = True, left_index = True)
df.convert_dtypes().dtypes


df = df[df['Tilskud beregnes af  (kr.)'] != 'Udgået']
df['Varenummer'] = df['Lægemiddel/varenummer'].apply( lambda x: x[-6:])
df['Navn'] = df['Lægemiddel/varenummer'].apply( lambda x: x[:-6])
df['Stof'] = df.apply(lambda x: (float(x.Pakning[:2])*float(x.Styrke[:2])), axis=1)

def to_float(key):
    df[key] = pd.to_numeric(df[key].str.replace("," , "."))
    return df
to_numeric = ['Tilskud beregnes af  (kr.)', 'Pris pr. enhed (kr.)','Pris pr.pakning (kr.)']

list(map(to_float, to_numeric))

df.rename(columns={'Tilskud beregnes af  (kr.)' : 'Tilskud', 
                   'Pris pr. enhed (kr.)': 'Enhedspris', 
                   'Pris pr.pakning (kr.)' : 'Pakkepris'}, inplace=True)


print(df)
'''
from sqlalchemy import create_engine, types
import sqlalchemy
import pandas as pd
from sqlalchemy.sql.sqltypes import INTEGER


db = create_engine('mysql://jens:gj2PWWhCTw2GSH8@test-db.cu0mjlmttufo.eu-central-1.rds.amazonaws.com:3306/db_medicine_app')

data = df.drop(columns = ['Lægemiddel/varenummer', 'Styrke', 'Pakning'])
from datetime import date

data['date'] = date.today() 

#text = data[data['Enhedspris'] == data['Enhedspris'].min()].set_index('Enhedspris').replace("b'", '').to_html().replace('\n', '').encode('utf-8')

text = data[data['Enhedspris'] == data['Enhedspris'].min()].iloc[0].to_frame().to_html().replace('\n', '').replace("b'", '').encode('utf-8')

import smtplib
from creds import gmail_user, gmail_password

sent_from = "Kill big pharma.dk"
to = ['jensringsholm@gmail.com']


# subject could be defined as buy or wait depending on criteria
subject = 'Best medicine price'


# should be a couple of graphs as background for det desicion
# Linechart w new price shown
# % increase decrease

TEXT=f"""
{text}
""" #Your Message (Even Supports HTML Directly)




email_text = f"Subject: {subject}\nFrom: {sent_from}\nTo: {to}\nContent-Type: text/html\n\n{TEXT}" #This is where the stuff happens


try:
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print ("Email sent successfully!")
except Exception as ex:
    print ("Something went wrong….",ex)



data.to_sql(con=db, name='med', if_exists='append', index=False)

lol = pd.read_sql_query("SELECT * FROM med", con=db)
'''



