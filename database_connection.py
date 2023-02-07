import pymysql
import logging
import time
from main import get_tweet_info, get_tweets, get_user_id
from config import BEARER_TOKEN as auth
logging.basicConfig(level=logging.DEBUG)
import simple_sql

def format_dates(date):
   year = date[0:10]
   time = date[11:19]
   return f'{year} {time}'

last_tweet_access_method = ['2022-12-18T19:08:47.000Z'] 

if __name__ == '__main__':
   for i in range(0,3):
      if last_tweet_access_method != []:
         access_last_tweet = last_tweet_access_method[-1]
      else:
         access_last_tweet = []
      sample_info = get_tweet_info(get_tweets(get_user_id('Jack', auth), access_last_tweet, auth), auth)
      last_tweet_access_method.append(sample_info['created_on'][-1])
      sql_info_to_upload = []
      colms = ['tweet_id','body','likes','views','created_on'] 
      for i in range(len(sample_info['tweet_id'])):
         DATA = []
         # the id of the tweet
         DATA.append(str(sample_info['tweet_id'][i]))
         # the main text of the data
         text = sample_info['text'][i]
         DATA.append(f'"{text}"')
         # the like count
         DATA.append(str(sample_info['likes'][i]))
         # the view/impression count
         DATA.append(str(sample_info['views'][i]))
         # the date the post was created
         date = format_dates(sample_info['created_on'][i])
         DATA.append(f'"{date}"')
         sql_info_to_upload.append(simple_sql.create_row('twitter_info.twitter_data', colms, DATA))
         print(sql_info_to_upload)
      conn = pymysql.connect(host='twitter-info-database.cdqr0hsklsgu.us-west-1.rds.amazonaws.com',
      user='admin',password='U8tIZayYVeCPXtKsJaAJ',database='twitter_info')
      with conn.cursor() as cursor: 
         for queries in sql_info_to_upload:
            try:
               # Executing the SQL command
               cursor.execute(queries)

               # Commit your changes in the database
               conn.commit()

            except Exception as e:
               # Rolling back in case of error
               conn.rollback()
               logging.error(e)
      # Closing the connection
      conn.close()
      time.sleep(900)