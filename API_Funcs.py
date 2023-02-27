# import required functions
import requests
import pandas as pd
import time
from datetime import date
import logging
logging.basicConfig(level=logging.DEBUG)
from IPython.display import display
from API_Calls import API_CALLS, OAUTH_GET_TOKENS_HEADERS, OAUTH_ACCESS_TOKENS_HEADERS, HEADERS, PAYLOAD
from config import _USERNAME, API_KEY

# defines error handling for 429 api-limit-error, can handle other errors too if you want it to though
def error_handling(_data, _url, _headers):
    if 'status' in _data:
        if _data['status'] == 429:
            time.sleep(903)
            _response = requests.request("GET", _url, headers=_headers)
            return _response.json()
    else:
        return _data

# retrives OAuth Tokens
def get_OAuth_Tokens(headers=OAUTH_GET_TOKENS_HEADERS, payload=PAYLOAD, url = API_CALLS().get_OAuth_Tokens()):
    O_Auth_Tokens = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.text
    print(data)
    O_Auth_Tokens['OAuth_Token'] = data[12:39]
    O_Auth_Tokens['OAuth_Secret'] = data[59:91]
    print('The user must visit THIS URL for Authorization purposes: ' + 'https://api.twitter.com/oauth/authorize?oauth_token=' + O_Auth_Tokens['OAuth_Token'])
    O_Auth_Verifier = input('Look in the URL for the verifier and enter here: ')
    O_Auth_Tokens['OAuth_Verifier'] = O_Auth_Verifier
    return O_Auth_Tokens

def Access_Token(O_AUTH_TOKENS, headers=OAUTH_ACCESS_TOKENS_HEADERS, payload=PAYLOAD):
    user_OAuth_Creds = {}
    url = API_CALLS(oauth_token=O_AUTH_TOKENS['OAuth_Token'], oauth_verifier=O_AUTH_TOKENS['OAuth_Verifier']).access_OAuth_Tokens()
    response = requests.request("POST", url, headers=headers, data=payload)
    data = (response.text).split('&')
    for i in range(len(data)):
        seperated_data = data[i].split('=')
        data[i] = seperated_data[1]
    user_OAuth_Creds['user_oauth_token'] = data[0]
    user_OAuth_Creds['user_oauth_secret'] = data[1]
    user_OAuth_Creds['user_id'] = data[2]
    user_OAuth_Creds['screen_name'] = data[3]
    return user_OAuth_Creds

# retrives the user_id given a username
def get_user_id(headers=HEADERS, payload=PAYLOAD, url = API_CALLS(username=_USERNAME).get_user_id()):
    response = requests.request("GET", url, headers=headers, data=payload)
    unchecked_data = response.json()
    data = error_handling(unchecked_data, url, headers)
    user_id = data['data']['id']
    return user_id

# global variables for user_id and pagination tokens used by functions below
USER_ID = get_user_id()
next_token_list = ['']

# retrives a list of tweets for a given user
def get_tweets(headers=HEADERS, payload=PAYLOAD, time_specific=False):
    if time_specific:
        url = API_CALLS(username=_USERNAME, user_id=USER_ID, pag_token=next_token_list[-1]).get_tweets_time_specific()
    else:
        url = API_CALLS(username=_USERNAME, user_id=USER_ID, pag_token=next_token_list[-1]).get_tweets()
    list_of_tweets = []
    list_of_dates = []
    next_token_exists = True
    while next_token_exists:
        response = requests.request("GET", url, headers=headers, data=payload)
        unchecked_data = response.json()
        data = error_handling(unchecked_data, url, headers)
        print(data)
        if 'next_token' not in data['meta']:
            list_of_tweets.append(data['data'])
            group_of_tweets = list_of_tweets[-1]
            for tweet in group_of_tweets:
                list_of_dates.append(tweet['created_at'])
            next_token_exists = False
        else:
            list_of_tweets.append(data['data'])
            group_of_tweets = list_of_tweets[-1]
            for tweet in group_of_tweets:
                list_of_dates.append(tweet['created_at'])
            next_token_list.append("&pagination_token=" + data['meta']['next_token'])
            url = API_CALLS(username=_USERNAME, user_id=USER_ID, pag_token=next_token_list[-1]).get_tweets()
    return list_of_tweets, list_of_dates

# retrives some public metrics on the list of tweets from a given user
def get_tweet_info(list_of_tweets, pre_retrived_dates, headers=HEADERS, payload=PAYLOAD):
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
    dates = pre_retrived_dates

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
        
    # once we are done using the string version of the IDs for the URL functionality change it back to integers for proper storage into a database/pandas dataframe
    for i in range(len(list_of_tweet_ids)):
        list_of_tweet_ids[i] = int(list_of_tweet_ids[i])

    # store public metrics into a dictionary for easy manipulation of data
    tweets_info = {'tweet_id':list_of_tweet_ids, 'text':text, 'likes':likes, 'views':views, 'retweets':retweets, 'replys':replys, 'quotes':quotes, 'created_on':dates}
    return pd.DataFrame(tweets_info)