# import required functions
import requests
import pandas as pd
from IPython.display import display
from API_Calls import API_CALLS, HEADERS, PAYLOAD

# starter variables in order for functions to work
USERNAME = 'Jack'

# retrives the user_id given a username
def get_user_id(headers=HEADERS, payload=PAYLOAD, url = API_CALLS(username=USERNAME).get_user_id()):
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    user_id = data['data']['id']
    return user_id

USER_ID = get_user_id()

# retrives a list of tweets for a given user
def get_tweets(headers=HEADERS, payload=PAYLOAD, url = API_CALLS(username=USERNAME, user_id=USER_ID).get_tweets()):
    tweets_and_token = []
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    print(data)
    input('STOP')
    list_of_tweets = data['data']
    next_token = data['meta']['next_token']
    tweets_and_token.append(list_of_tweets)
    tweets_and_token.append(next_token)
    return tweets_and_token

# retrives some public metrics on the list of tweets from a given user
def get_tweet_info(list_of_tweets, headers=HEADERS, payload=PAYLOAD):
    # create a list of tweet_ids so that when can iterate through them that way
    list_of_tweet_ids = []
    print(list_of_tweets[0])
    for tweet in list_of_tweets:
        list_of_tweet_ids.append(tweet['id'])

    # create a seperate list for every public metric
    views = []
    likes = []
    text = []
    dates = []

    # this will iterate through all the tweets and append the views, likes, and text metrics
    for TWEET_ID in list_of_tweet_ids:
        url = API_CALLS(USERNAME, USER_ID, TWEET_ID).get_tweets_txt_likes_views()
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        like_count = int(data['data'][0]['public_metrics']['like_count'])
        view_count = int(data['data'][0]['public_metrics']['impression_count'])
        individual_text = data['data'][0]['text']
        text.append(individual_text)
        likes.append(int(like_count))
        views.append(int(view_count))

    # this will iterate through all the tweets again and in a seperate API Call retrive the created date metric
    for TWEET_ID in list_of_tweet_ids:
        url = API_CALLS(USERNAME, USER_ID, TWEET_ID).get_tweets_create_date()
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        create_dates = data['data'][0]['created_at']
        dates.append(create_dates)

    # once we are done using the string version of the IDs for the URL functionality change it back to integers for proper storage into a database/pandas dataframe
    for i in range(len(list_of_tweet_ids)):
        list_of_tweet_ids[i] = int(list_of_tweet_ids[i])

    # store public metrics into a dictionary for easy manipulation of data
    tweets_info = {'tweet_id':list_of_tweet_ids, 'text':text, 'likes':likes, 'views':views, 'created_on':dates}
    return pd.DataFrame(tweets_info)