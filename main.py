from sqlalchemy import create_engine
from config import HOST, USER, PASSWORD, DATABASE, _USERNAME
import logging
from API_Calls import API_CALLS
from API_Funcs import get_tweet_info, get_tweets, get_user_id, get_following, get_followers, get_private_tweet_info, token_retrieval
logging.basicConfig(level=logging.DEBUG)

def main():
   # retrive the user we are getting all the twitter info for, and create database engine for mysql database
   USERNAME = _USERNAME
   engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')

   # process the public metrics for all given tweets and write to a SQL table
   for user in _USERNAME:
      User_ID = get_user_id(url = API_CALLS(username=user).get_user_id())
      TWEETS_AND_DATES = get_tweets(_user_id=User_ID)
      sample_info = get_tweet_info(_user_id=User_ID, list_of_tweets=TWEETS_AND_DATES[0], pre_retrived_dates=TWEETS_AND_DATES[1])
      sample_info.to_sql(f'twitter_data for user {user}', engine)


   # process the followers/following for the user and write to 2 seperate tables
   for user in _USERNAME:
      User_ID = get_user_id(url = API_CALLS(username=user).get_user_id())
      following = get_following(_user_id=User_ID)
      ing_and_ers = get_followers(_user_id=User_ID, following_info=following)
      following = ing_and_ers[0]
      followers = ing_and_ers[1]
      followers.to_sql(f'users following {USERNAME}', engine)
      following.to_sql(f'users {USERNAME} is following', engine)

   # process the private metrics for tweets within the past 30 days and write to a SQL table
   for user in _USERNAME:
      User_ID = get_user_id(url = API_CALLS(username=user).get_user_id())
      tweets = get_tweets(_user_id=User_ID, time_specific=True)
      USER_TOKENS = token_retrieval()
      USER_TOKEN = USER_TOKENS[0]
      TOKEN_SECRET = USER_TOKENS[1]
      private_metrics = get_private_tweet_info(User_ID, tweets[0], tweets[1], USER_TOKEN, TOKEN_SECRET)
      private_metrics.to_sql(f'private twitter_data for user {USERNAME}', engine)
   
if __name__ == '__main__':
   main()