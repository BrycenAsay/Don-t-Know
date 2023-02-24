# import required functions
import requests
import pandas as pd
import time
from IPython.display import display
from API_Calls import API_CALLS, HEADERS, PAYLOAD
from config import _USERNAME

# defines error handling for 429 api-limit-error
def error_handling(_data, _url, _headers):
    if 'status' in _data:
        if _data['status'] == 429:
            time.sleep(903)
            _response = requests.request("GET", _url, headers=_headers)
            return _response.json()
    else:
        return _data

# retrives the user_id given a username
def get_user_id(headers=HEADERS, payload=PAYLOAD, url = API_CALLS(username=_USERNAME).get_user_id()):
    response = requests.request("GET", url, headers=headers, data=payload)
    unchecked_data = response.json()
    data = error_handling(unchecked_data, url, headers)
    user_id = data['data']['id']
    return user_id

USER_ID = get_user_id()
next_token_list = ['']
list_of_tweets = []

# retrives a list of tweets for a given user
def get_tweets(headers=HEADERS, payload=PAYLOAD, url = API_CALLS(username=_USERNAME, user_id=USER_ID, pag_token=next_token_list[-1]).get_tweets()):
    next_token_exists = True
    while next_token_exists:
        response = requests.request("GET", url, headers=headers, data=payload)
        unchecked_data = response.json()
        data = error_handling(unchecked_data, url, headers)
        if 'next_token' not in data['meta']:
            list_of_tweets.append(data['data'])
            next_token_exists = False
        else:
            list_of_tweets.append(data['data'])
            next_token_list.append("&pagination_token=" + data['meta']['next_token'])
            url = API_CALLS(username=_USERNAME, user_id=USER_ID, pag_token=next_token_list[-1]).get_tweets()
    return list_of_tweets

# retrives some public metrics on the list of tweets from a given user
def get_tweet_info(list_of_tweets, headers=HEADERS, payload=PAYLOAD):
    # create a list of tweet_ids so that when can iterate through them that way
    list_of_tweet_ids = []
    for group_of_tweets in list_of_tweets:
        for tweet in group_of_tweets:
            list_of_tweet_ids.append(tweet['id'])

    # create a seperate list for every public metric
    likes = []
    views = []
    retweets = []
    replys = []
    quotes = []
    text = []
    dates = []

    # this will iterate through all the tweets and append the views, likes, and text metrics
    for TWEET_ID in list_of_tweet_ids:
        url = API_CALLS(_USERNAME, USER_ID, TWEET_ID).get_tweets_txt_likes_views()
        response = requests.request("GET", url, headers=headers, data=payload)
        unchecked_data = response.json()
        data = error_handling(unchecked_data, url, headers)
        like_count = int(data['data'][0]['public_metrics']['like_count'])
        view_count = int(data['data'][0]['public_metrics']['impression_count'])
        retweet_count = int(data['data'][0]['public_metrics']['retweet_count'])
        reply_count = int(data['data'][0]['public_metrics']['reply_count'])
        quote_count = int(data['data'][0]['public_metrics']['quote_count'])
        individual_text = data['data'][0]['text']
        likes.append(like_count)
        views.append(view_count)
        retweets.append(retweet_count)
        replys.append(reply_count)
        quotes.append(quote_count)
        text.append(individual_text)

    # this will iterate through all the tweets again and in a seperate API Call retrive the created date metric
    for TWEET_ID in list_of_tweet_ids:
        url = API_CALLS(_USERNAME, USER_ID, TWEET_ID).get_tweets_create_date()
        response = requests.request("GET", url, headers=headers, data=payload)
        unchecked_data = response.json()
        data = error_handling(unchecked_data, url, headers)
        create_dates = data['data'][0]['created_at']
        dates.append(create_dates)

    # once we are done using the string version of the IDs for the URL functionality change it back to integers for proper storage into a database/pandas dataframe
    for i in range(len(list_of_tweet_ids)):
        list_of_tweet_ids[i] = int(list_of_tweet_ids[i])

    # store public metrics into a dictionary for easy manipulation of data
    tweets_info = {'tweet_id':list_of_tweet_ids, 'text':text, 'likes':likes, 'views':views, 'retweets':retweets, 'replys':replys, 'quotes':quotes, 'created_on':dates}
    return pd.DataFrame(tweets_info)