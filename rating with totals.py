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
from utils import generate_id, get_abbreviation, official_name, trueround


"""Game Date"""
#URL = "https://sagarin.usatoday.com/2022-2/nfl-team-ratings-2022/"
#page = requests.get(URL)
#html = page.text
#print(html)
soup = BeautifulSoup(html, 'html.parser')
d = soup.find_all('b')
date = str(d[2])
date = date.replace('<b>','').replace('NFL 2022 Ratings through results of', '').replace('- WEEK #6', '').replace('</b>', '')
date = date.split()


"""webscraping"""

URL = "https://sagarin.usatoday.com/2022-2/nfl-team-ratings-2022/"
page = requests.get(URL)
html = page.text
#print(html)
soup = BeautifulSoup(html, 'html.parser')
textpage = soup.get_text()
split_by__ = textpage.split('======================================================================================================')
split_by__ = split_by__[1].split('EIGENVECTOR Analysis            eigen MONEY=odds to 100  EPCT%=confidence')
split_by__ = pd.Series(split_by__[0])
split_by__ = pd.DataFrame(split_by__)
split_by__.to_csv('out.csv', sep=',')
df = pd.read_fwf('out.csv')
df = pd.DataFrame(df.iloc[:,1:])
df = df.rename(columns={'Unnamed: 1':'home_team', 'Unnamed: 2':'Rating', 'Unnamed: 3':'Predict',
                        'Unnamed: 4':'Golden', 'Unnamed: 5':'Recent',
                        'Unnamed: 6':'team_away', 'Unnamed: 7':'ODDS', 'Unnamed: 8':'PCT%', 'Unnamed: 9':'TOTAL'})
df = df.dropna()

df['year'] = date[0]
df['month'] = date[1].lower()
df['day'] = date[2]
df['date'] = df['year'] + ' ' + df['month'] + ' ' + df['day']

df['date'] = df['date'].apply(lambda X:datetime.strptime(X, '%Y %B %d').date())
#dt= datetime.strptime(dt, '%y, %b, %d')


#print(df)


#away_team = df['UNDERDOG']
#home_team= df['FAVORITE']
#game_number = 1
date = df['date']

off_name_home_team = []
for i in df['home_team']:
    s = official_name(name = i, sport = 'nfl')
    off_name_home_team.append(s)

df['home_team'] = off_name_home_team
#print(off_name_home_team)

off_name_team_away = []
for i in df['team_away']:
    s = official_name(name = i, sport = 'nfl')
    off_name_team_away.append(s)

df['team_away'] = off_name_team_away

#print(off_name_away)

home_team = []
for i in off_name_home_team:
    s = get_abbreviation(name = i, sport='nfl')
    home_team.append(s)

away_team = []
for i in off_name_team_away:
    s = get_abbreviation(name = i, sport='nfl')
    away_team.append(s)


#unique_id = []
#for i in date:
#    for i in away_team:
#        for i in home_team:
#            a = generate_id(date= i, away_team= i, home_team= i, game_number='1', sport='nfl')
#unique_id.append(a)

#print(unique_id)

df['game_number'] = 1
df['sport'] = 'nfl'
s = map(generate_id, date,away_team, home_team, df['game_number'], df['sport'])
s = pd.Series(list(s))
s = pd.DataFrame(s)
df = df.reset_index()
df['id'] = s
df = df.iloc[:,1:]



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

print(df)

""" csv exportation """

df.to_csv('ratingswithtotals.csv', sep=',')

"""Database record"""


import sqlalchemy
database_username = 'root'
database_password = 'WEBscraping2022!'
database_ip       = 'localhost'
database_name     = 'games'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password,
                                                      database_ip, database_name))

df.to_sql(con=database_connection, name='ratingwithtotals') #if_exists='replace')

