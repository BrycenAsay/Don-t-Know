from sqlalchemy import create_engine
import logging
from messy import get_tweet_info, get_tweets, get_user_id
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
   # define starting variables
    USERNAME = 'Jack'
    USER_ID = get_user_id()
    sample_info = get_tweet_info(get_tweets())
    engine = create_engine('mysql+pymysql://admin:U8tIZayYVeCPXtKsJaAJ@twitter-info-database.cdqr0hsklsgu.us-west-1.rds.amazonaws.com/twitter_info')
    sample_info.to_sql('twitter_data', engine)