from sqlalchemy import create_engine
from config import HOST, USER, PASSWORD, DATABASE, _USERNAME
import logging
from API_Funcs import get_tweet_info, get_tweets, get_user_id
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
   # define starting variables
   USERNAME = _USERNAME
   USER_ID = get_user_id()
   TWEETS_AND_DATES = get_tweets()
   print(TWEETS_AND_DATES)
   sample_info = get_tweet_info(TWEETS_AND_DATES[0], TWEETS_AND_DATES[1])
   engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
   sample_info.to_sql(f'twitter_data for user {USERNAME}', engine)