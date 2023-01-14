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
from utils import generate_id, get_abbreviation, official_name, trueround, month_number

"""WebScraping Ratings"""


URL = input('Enter URL:')
URL = str(URL)
page = requests.get(URL)
html = page.text
#print(html)
soup = BeautifulSoup(html, 'html.parser')
d = soup.find_all('b')
date = str(d[2])
date = date.replace('<b>','').replace('NFL 2022 Ratings through results of', '').replace('-', '').replace('</b>', '')
dates = date.split(' ')
#print(dates)
year = dates[1]
month = month_number(dates[2])
day = dates[3]
week = dates[6] + dates[7]
week = week.replace('\r\n', '')
date = year+month+day


"""Divide txt obtained from de webpage"""

textpage = soup.get_text()
date_input = input('Enter date game as appears on NFL webpage '
                   'e.g:"NFL 2022 through games of October 17 Monday - Week #6   ":')

split_by__ = textpage.split(str(date_input))
print(len(split_by__))


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
rating_ = pd.read_fwf('out2.csv')
rating_ = pd.DataFrame(rating_['Unnamed: 1'])
new = rating_['Unnamed: 1'].str.split("=", n = 1, expand = True)
rating_["team"]= new[0]
rating_["rating"]= new[1]
rating_ =  rating_[rating_[ 'team' ].str.contains('HOME ADVANTAGE')==False ]
rating_ = rating_[rating_[ 'team' ].str.contains('RATING')==False ]
rating_ = rating_.drop(['Unnamed: 1'], axis=1)
rating_['date'] = date

"""Date to Datetime format"""

datecolumn = year+'-'+month+'-'+day
datecolumn =datecolumn.replace('\r\n', '')
rating_['date'] = datecolumn
rating_['date'] = rating_['date'].apply(lambda X:datetime.strptime(X, '%Y-%M-%d').date())

"""Round numbers"""

k = []
for i in rating_['rating']:
    s = trueround(float(i), places=1)
    k.append(s)
#print(k)
rating_['rating'] = k


"""Exporting csv"""

"""Exporting csv"""

csv_name = 'NFL' + '-' + date +'-'+ 'Ratings' +'.csv'
rating_.to_csv(str(csv_name), sep=',')

print(rating_)


"""Database Conection"""

import sqlalchemy
database_username = 'root'
database_password = 'WEBscraping2022!'
database_ip       = 'localhost'
database_name     = 'games'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password,
                                                      database_ip, database_name))

rating_.to_sql(con=database_connection, name='ratings', if_exists='append')






