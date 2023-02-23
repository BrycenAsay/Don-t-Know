from sqlalchemy import create_engine
from config import HOST, USER, PASSWORD, DATABASE
import logging
from API_Funcs import get_tweet_info, get_tweets, get_user_id
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
   # define starting variables
    USERNAME = 'RobTopGames'
    USER_ID = get_user_id()
    sample_info = get_tweet_info(get_tweets())
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    sample_info.to_sql('twitter_data', engine)