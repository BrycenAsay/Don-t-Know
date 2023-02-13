import pymysql
from sqlalchemy import create_engine, URL
import logging
import time
from messy import get_tweet_info, get_tweets, get_user_id
from config import BEARER_TOKEN as auth
logging.basicConfig(level=logging.DEBUG)
import simple_sql

def format_dates(date):
   year = date[0:10]
   time = date[11:19]
   return f'{year} {time}'

if __name__ == '__main__':
   # define starting variables
    USERNAME = 'Jack'
    USER_ID = get_user_id()
    sample_info = get_tweet_info(get_tweets())
    engine = create_engine('mysql+pymysql://admin:U8tIZayYVeCPXtKsJaAJ@twitter-info-database.cdqr0hsklsgu.us-west-1.rds.amazonaws.com/twitter_info')
    sample_info.to_sql('twitter_data', engine)