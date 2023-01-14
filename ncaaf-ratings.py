import requests
import pandas as pd
import csv
import numpy as np
import openpyxl
import mysql.connector
from mysql.connector import connect, Error
from bs4 import BeautifulSoup, NavigableString, Tag
from datetime import datetime
import json
import os
import utils
from utils import generate_id, get_abbreviation, official_name, trueround, month_number

"""WebScraping Ratings"""

URL = input('Enter URL:')
URL = str(URL)
#URL = 'https://sagarin.usatoday.com/2022-2/college-football-team-ratings-2022/'
page = requests.get(URL)
html = page.text
#print(html)
soup = BeautifulSoup(html, 'html.parser')
d = soup.find_all('b')
date = str(d[2])
date = date.replace('<b>','').replace('COLLEGE FOOTBALL 2022 through results of ', '').replace('-', '').replace('</b>', '')
dates = date.split(' ')
year = dates[0]
month = month_number(dates[1])
day = dates[2]
date = year+month+day
date =date.replace('\r\n', '')
print(date)

"""Divide txt obtained from de webpage"""

textpage = soup.get_text()
date_input = input('Enter date game as appears on NFL webpage '
                   'e.g:"College Football 2022 through games of October 22 Saturday":')
split_by__ = textpage.split(str(date_input))
#print(split_by__)

dataframes = []
for i in split_by__:
    s = pd.Series(i)
    s = pd.DataFrame(s)
    dataframes.append(s)

_27_table = split_by__[27].split('_________________________________________________________________________________________________________________________________________________')
_27_dataframe = pd.Series(_27_table[0])
_27_dataframe = pd.DataFrame(_27_dataframe)

s = pd.concat(dataframes)
s = s.iloc[1:]
s = s.iloc[:26]
s = pd.concat([s,_27_dataframe] )
s.to_csv('out2.csv', sep=',')
rating_ = pd.read_fwf('out2.csv')

rating_ = pd.DataFrame(rating_['Unnamed: 1'])
new = rating_['Unnamed: 1'].str.split("=", n = 1, expand = True)

rating_["team"]= new[0]
rating_["rating"]= new[1]
rating_ =  rating_[rating_[ 'team' ].str.contains('HOME ADVANTAGE')==False ]
rating_ = rating_[rating_[ 'team' ].str.contains('RATING')==False ]
rating_ = rating_[rating_[ 'team' ].str.contains('UNRATED')==False ]
rating_ = rating_.drop(['Unnamed: 1'], axis=1)

q = rating_['team'].str.replace("AA",'A')
q = q .str.replace(" A ",'')
rating_['team'] = q

k = []
for i in rating_['rating']:
    s = trueround(float(i), places=1)
    k.append(s)


rating_['rating'] = k

"""Date to Datetime format"""

datecolumn = year+'-'+month+'-'+day
datecolumn =datecolumn.replace('\r\n', '')
rating_['date'] = datecolumn
rating_['date'] = rating_['date'].apply(lambda X:datetime.strptime(X, '%Y-%M-%d').date())

"""Exporting csv"""

csv_name = 'NCAAF' + '-' + date +'-'+ 'Ratings' +'.csv'
rating_.to_csv(str(csv_name), sep=',')

print(rating_)

#import sqlalchemy
#database_username = 'root'
#database_password = 'WEBscraping2022!'
#database_ip       = 'localhost'
#database_name     = 'games'
#database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               #format(database_username, database_password,
                                                #      database_ip, database_name))

#rating_.to_sql(con=database_connection, name='college-football-ratings', if_exists='append')










