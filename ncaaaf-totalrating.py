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
#"day_input = input("enter Date Game as e.g: '2022-10-22':")
date = date.replace('<b>','').replace('COLLEGE FOOTBALL 2022 through results of ', '').replace('-', '').replace('</b>', '')
dates = date.split(' ')
year = dates[0]
month = month_number(dates[1])
day = dates[2]
date = year+month+day
date =date.replace('\r\n', '')
print(date)

"""webscraping"""

textpage = soup.get_text()
split_by__ = textpage.split('======================================================================================================')
split_by__ = split_by__[1].split('EIGENVECTOR Analysis            eigen MONEY=odds to 100  EPCT%=confidence')

"""Dataframe cration with rating data"""

split_by__ = pd.Series(split_by__[0])
split_by__ = pd.DataFrame(split_by__)
split_by__.to_csv('out.csv', sep=',')
df = pd.read_fwf('out.csv')
df = pd.DataFrame(df.iloc[:,1:])
df = df.rename(columns={'Unnamed: 1':'home_team', 'Unnamed: 2':'Rating', 'Unnamed: 3':'Predict',
                        'Unnamed: 4':'Golden', 'Unnamed: 5':'Recent',
                        'Unnamed: 6':'team_away', 'Unnamed: 7':'ODDS', 'Unnamed: 8':'PCT%', 'Unnamed: 9':'TOTAL'})
df = df.dropna()
df['date'] =date

"""Adjusting format to record on DB"""

off_name_home_team = []
for i in df['home_team']:
    s = official_name(name = i, sport = 'ncaaf')
    off_name_home_team.append(s)
df['home_team'] = off_name_home_team


off_name_team_away = []
for i in df['team_away']:
    s = official_name(name = i, sport = 'ncaaf')
    off_name_team_away.append(s)
df['team_away'] = off_name_team_away

home_team = []
for i in off_name_home_team:
    s = get_abbreviation(name = i, sport='ncaaf')
    home_team.append(s)

away_team = []
for i in off_name_team_away:
    s = get_abbreviation(name = i, sport='ncaaf')
    away_team.append(s)

"""Unique ID generation"""

df['game_number'] = 1
df['sport'] = 'ncaaf'
s = map(generate_id, df['date'],away_team, home_team, df['game_number'], df['sport'])
s = pd.Series(list(s))
s = pd.DataFrame(s)
df = df.reset_index()
df['id'] = s
df = df.iloc[:,1:]

"""Date to Datetime format"""
datecolumn = year+'-'+month+'-'+day
datecolumn =datecolumn.replace('\r\n', '')
df['date'] = datecolumn
df['date'] = df['date'].apply(lambda X:datetime.strptime(X, '%Y-%M-%d').date())

"""Round numbers"""

df['places'] = 1
a = map(trueround, df['Rating'], df['places'])
a = pd.Series(list(a))
a = pd.DataFrame(a)
df['Rating'] = a

b = map(trueround, df['Predict'], df['places'])
b = pd.Series(list(b))
b = pd.DataFrame(b)
df['Predict'] = b

c = map(trueround, df['Golden'], df['places'])
c = pd.Series(list(c))
c = pd.DataFrame(c)
df['Golden'] = c

d = map(trueround, df['ODDS'], df['places'])
d = pd.Series(list(d))
d = pd.DataFrame(d)
df['ODDS'] = d

e = map(trueround, df['Recent'], df['places'])
e = pd.Series(list(e))
e = pd.DataFrame(e)
df['Recent'] = e

f = map(trueround, df['TOTAL'], df['places'])
f = pd.Series(list(f))
f = pd.DataFrame(f)
df['TOTAL'] = f

""" csv exportation """

#Rating_or_Totals = input('Rating or Totals:')
csv_name = 'NCAAF' + '-' + date +'-'+ 'Totals' +'.csv'
df.to_csv(str(csv_name), sep=',')

print(df)

"""Database record"""


#import sqlalchemy
#database_username = 'root'
#database_password = 'WEBscraping2022!'
#database_ip       = 'localhost'
#database_name     = 'games'
#database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
#                                               format(database_username, database_password,
#                                                     database_ip, database_name))

#df.to_sql(con=database_connection, name='ncaafratingwithtotals', if_exists='append')
#database_connection .execute('ALTER TABLE games.ncaafratingwithtotals MODIFY COLUMN id VARCHAR(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL;')
#database_connection .execute('ALTER TABLE games.ncaafratingwithtotals ADD CONSTRAINT ncaafratingwithtotals_un UNIQUE KEY (id);')

