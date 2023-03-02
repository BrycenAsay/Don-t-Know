from sqlalchemy import create_engine
from config import HOST, USER, PASSWORD, DATABASE, _USERNAME
import logging
from API_Funcs import get_tweet_info, get_tweets, get_user_id, get_following, get_followers
logging.basicConfig(level=logging.DEBUG)

def main_one():
   # define starting variables
   USERNAME = _USERNAME
   USER_ID = get_user_id()
   TWEETS_AND_DATES = get_tweets()
   print(TWEETS_AND_DATES)
   sample_info = get_tweet_info(TWEETS_AND_DATES[0], TWEETS_AND_DATES[1])
   engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
   sample_info.to_sql(f'twitter_data for user {USERNAME}', engine)

def main_two():
   USERNAME = _USERNAME
   USER_ID = get_user_id
   following = get_following()
   ing_and_ers = get_followers(following)
   following = ing_and_ers[0]
   followers = ing_and_ers[1]
   engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
   followers.to_sql(f'users following {USERNAME}', engine)
   following.to_sql(f'users {USERNAME} is following', engine)

if __name__ == '__main__':
   main_two()