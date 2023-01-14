"""Libraries imported to webscraping and db connect"""
import requests
import pandas as pd
import csv
import numpy as np
import openpyxl
import mysql.connector
from mysql.connector import connect, Error
from bs4 import BeautifulSoup, NavigableString, Tag
from datetime import datetime
from utils import generate_id, get_abbreviation, official_name, trueround


""" Connection to DB"""


"""WebScraping Ratings"""

URL = input('Enter URL:')
URL = str(URL)
page = requests.get(URL)
html = page.text
#print(html)
soup = BeautifulSoup(html, 'html.parser')
d = soup.find_all('b')
date = str(d[2])
week_input = input("enter Week Game as 'WEEK #_':")
date = date.replace('<b>','').replace('NFL 2022 Ratings through results of', '').replace('-', '').replace(str(week_input), '').replace('</b>', '')
date = date.split()

print(date)

"""Divide txt obtained from de webpage"""

textpage = soup.get_text()
#Year = input('Enter year:')
#Month = input('Write month name E.g: Octuber:')
#Day = input('Enter day:')
#Week = input('Week number:')
#date_input = "NFL " +Year + ' through games of ' + ' ' + Month + ' '+ Day +' Monday - Week #'+Week
date_imput = input('Enter date game as appears on NFL webpage '
                   'e.g:"NFL 2022 through games of October 17 Monday - Week #6:')

split_by__ = textpage.split(str(date_imput))
#print(split_by__[1])

"""convert to dataframe"""

dataframes = []
for i in split_by__:
    s = pd.Series(i)
    s = pd.DataFrame(s)
    dataframes.append(s)

four_table = split_by__[4].split('_________________________________________________________________________________________________________________________________________________')
four_dataframe = pd.Series(four_table[0])
four_dataframe = pd.DataFrame(four_dataframe)

ratingdataframe = pd.concat([dataframes[1], dataframes[2], dataframes[3], four_dataframe])


ratingdataframe.to_csv('out2.csv', sep=',')
df = pd.read_fwf('out2.csv')
df = pd.DataFrame(df['Unnamed: 1'])
new = df['Unnamed: 1'].str.split("=", n = 1, expand = True)
df["team"]= new[0]
df["rating"]= new[1]
df =  df[df[ 'team' ].str.contains('HOME ADVANTAGE')==False ]
df = df[df[ 'team' ].str.contains('RATING')==False ]



df = df.drop(['Unnamed: 1'], axis=1)


df['year'] = date[0]
df['month'] = date[1].lower()
df['day'] = date[2]
df['date'] = df['year'] + ' ' + df['month'] + ' ' + df['day']


k = []
for i in df['rating']:
    s = trueround(float(i), places=1)
    k.append(s)
print(k)



df['date'] = df['date'].apply(lambda X:datetime.strptime(X, '%Y %B %d').date())
name_csv = input('How want to name youe csv file (use .csv at end):')
df.to_csv(str(name_csv), sep=',')
print(df)


"""Conexion y base de datos"""

#import sqlalchemy
#database_username = 'root'
#database_password = 'WEBscraping2022!'
#database_ip       = 'localhost'
#database_name     = 'games'
#database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
#                                               format(database_username, database_password,
#                                                      database_ip, database_name))

#df.to_sql(con=database_connection, name='ratings', if_exists='append')