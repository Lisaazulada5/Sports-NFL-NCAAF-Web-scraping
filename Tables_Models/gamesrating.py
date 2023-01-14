import datetime as datetime
from mysql.connector import Column, Numeric, Integer, String, Date, Time, DateTime

class gamesrating():
    __tablename__ = "gamesrating"

    id = Column(char(50), primary_key=True, unique=True, autoincrement=True)
    gamedate = Column(DateTime)
    teamname = Column(char(50))
    rating = Column(double)
    ratingtotals = Column(double)

class Meta:
    database = connectdb
    table_name = 'gamesrating'