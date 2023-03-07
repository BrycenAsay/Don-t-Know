from sqlalchemy import create_engine
from config import HOST, USER, PASSWORD, DATABASE, _USERNAME
import logging
from API_Funcs import get_tweet_info, get_tweets, get_following, get_followers, get_private_tweet_info, token_retrieval
logging.basicConfig(level=logging.DEBUG)

def main():
   # retrive the user we are getting all the twitter info for
   USERNAME = _USERNAME
   engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')

   # process the public metrics for all given tweets and write to a SQL table
   TWEETS_AND_DATES = get_tweets()
   sample_info = get_tweet_info(TWEETS_AND_DATES[0], TWEETS_AND_DATES[1])
   sample_info.to_sql(f'twitter_data for user {USERNAME}', engine)

   # process the followers/following for the user and write to 2 seperate tables
   following = get_following()
   ing_and_ers = get_followers(following)
   following = ing_and_ers[0]
   followers = ing_and_ers[1]
   followers.to_sql(f'users following {USERNAME}', engine)
   following.to_sql(f'users {USERNAME} is following', engine)

   # process the private metrics for tweets within the past 30 days and write to a SQL table
   tweets = get_tweets(time_specific=True)
   USER_TOKENS = token_retrieval()
   USER_TOKEN = USER_TOKENS[0]
   TOKEN_SECRET = USER_TOKENS[1]
   private_metrics = get_private_tweet_info(tweets[0], tweets[1], USER_TOKEN, TOKEN_SECRET)
   private_metrics.to_sql(f'private twitter_data for user {USERNAME}', engine)

if __name__ == '__main__':
   main()