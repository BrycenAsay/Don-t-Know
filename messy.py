import requests
import pandas as pd
from IPython.display import display
from API_Calls import API_CALLS, HEADERS, PAYLOAD
# starter variables in order for functions to work
USERNAME = 'Jack'
# write functions

def get_user_id(headers=HEADERS, payload=PAYLOAD, url = API_CALLS(username=USERNAME).get_user_id()):
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    user_id = data['data']['id']
    return user_id

USER_ID = get_user_id()

def get_tweets(headers=HEADERS, payload=PAYLOAD, url = API_CALLS(username=USERNAME, user_id=USER_ID).get_tweets()):
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    print(data)
    list_of_tweets = data['data']
    return list_of_tweets

def get_tweet_info(list_of_tweets, headers=HEADERS, payload=PAYLOAD):
    list_of_tweet_ids = []
    for tweet in list_of_tweets:
        list_of_tweet_ids.append(tweet['id'])
    views = []
    likes = []
    text = []
    dates = []
    for TWEET_ID in list_of_tweet_ids:
        url = API_CALLS(USERNAME, USER_ID, TWEET_ID).get_tweets_txt_likes_views()
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        like_count = data['data'][0]['public_metrics']['like_count']
        view_count = data['data'][0]['public_metrics']['impression_count']
        individual_text = data['data'][0]['text']
        text.append(individual_text)
        likes.append(like_count)
        views.append(view_count)

    for TWEET_ID in list_of_tweet_ids:
        url = API_CALLS(USERNAME, USER_ID, TWEET_ID).get_tweets_create_date()
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        create_dates = data['data'][0]['created_at']
        dates.append(create_dates)

    for i in range(len(list_of_tweet_ids)):
        list_of_tweet_ids[i] = int(list_of_tweet_ids[i])

    for i in range(len(likes)):
        likes[i] = int(likes[i])

    for i in range(len(views)):
        views[i] = int(views[i])

    tweets_info = {'tweet_id':list_of_tweet_ids, 'text':text, 'likes':likes, 'views':views, 'created_on':dates}
    return tweets_info