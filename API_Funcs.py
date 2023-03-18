# import required functions
import requests
import pandas as pd
import time
from sqlalchemy import create_engine
import logging
logging.basicConfig(level=logging.DEBUG)
from IPython.display import display
from API_Calls import API_CALLS, OAUTH_ACCESS_TOKENS_HEADERS, HEADERS, PAYLOAD
from config import _USERNAME, API_KEY, API_SECRET, USER, HOST, PASSWORD, DATABASE
from requests_oauthlib import OAuth1

def error_handling(_data, _url, _headers=False, _auth=False):
    # defines error handling for 429 api-limit-error, can handle other errors too if you want it to though
    if 'status' in _data:
        if _data['status'] == 429:
            time.sleep(903)
            if _headers != False:
                _response = requests.request("GET", _url, headers=_headers)
                return _response.json()
            else:
                _response = requests.get(_url, auth=_auth)
                return _response.json()
    else:
        return _data

def get_OAuth_Tokens(payload=PAYLOAD, url = API_CALLS().get_OAuth_Tokens()):
    # retrives OAuth Tokens
    O_Auth_Tokens = {}
    auth = OAuth1(API_KEY, API_SECRET)
    response = requests.request("POST", url, auth=auth, data=payload)
    data = response.text
    O_Auth_Tokens['OAuth_Token'] = data[12:39]
    O_Auth_Tokens['OAuth_Secret'] = data[59:91]
    print('The user must visit THIS URL for Authorization purposes: ' + 'https://api.twitter.com/oauth/authorize?oauth_token=' + O_Auth_Tokens['OAuth_Token'])
    O_Auth_Verifier = input('Look in the URL for the verifier and enter here: ')
    O_Auth_Tokens['OAuth_Verifier'] = O_Auth_Verifier
    return O_Auth_Tokens

def Access_Token(O_AUTH_TOKENS, headers=OAUTH_ACCESS_TOKENS_HEADERS, payload=PAYLOAD):
    # accesses user OAuth tokens
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

def token_retrieval():
    # retrives user OAuth tokens for getting private metrics from SQL table
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    User_Auth = pd.DataFrame()
    with engine.connect() as conn:
        User_Auth = (pd.read_sql_table('User_OAuth_Info', conn)).to_dict()
    found_name = False
    i = 0
    while found_name == False:
        if i not in User_Auth['screen_name']:
            print('ERROR, ENTER A VALID USERNAME FOR PRIVATE METRICS')
            found_name = True
            return
        name = (User_Auth['screen_name'][i]).lower()
        if name == _USERNAME.lower():
            users_number_id = i
            found_name == True
            break
        i += 1
    user_oauth_token = User_Auth['user_oauth_token'][users_number_id]
    user_oauth_secret = User_Auth['user_oauth_secret'][users_number_id]
    return user_oauth_token, user_oauth_secret

def get_user_id(headers=HEADERS, payload=PAYLOAD, url = API_CALLS(username=_USERNAME).get_user_id()):
    # retrives the user_id given a username
    response = requests.request("GET", url, headers=headers, data=payload)
    unchecked_data = response.json()
    data = error_handling(unchecked_data, url, headers)
    user_id = data['data']['id']
    return user_id

# global variables for user_id and pagination tokens used by functions below
USER_ID = get_user_id()
next_token_list = ['']

def get_tweets(headers=HEADERS, payload=PAYLOAD, time_specific=False):
    # retrives a list of tweets for a given user, you can choose the past 30 days or all tweets depending on wether you are getting public or private metrics
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
        if 'next_token' not in data['meta']:
            if data['meta']['result_count'] != 0:
                list_of_tweets.append(data['data'])
                group_of_tweets = list_of_tweets[-1]
                for tweet in group_of_tweets:
                    list_of_dates.append(tweet['created_at'])
                next_token_exists = False
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
    includes_media = []
    media_key = []
    media_views = []
    media_type = []
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
        if 'includes' in data:
            if 'media' in data['includes']:
                includes_media.append('True')
                media_key.append(data['includes']['media'][0]['media_key'])
                if 'public_metrics' in data['includes']['media'][0]:
                    media_views.append(data['includes']['media'][0]['public_metrics']['view_count'])
                else:
                    media_views.append('N/A')
                media_type.append(data['includes']['media'][0]['type'])
        else:
            includes_media.append('False')
            media_key.append('N/A')
            media_views.append('N/A')
            media_type.append('N/A')
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
    tweets_info = {'tweet_id':list_of_tweet_ids, 'text':text, 'likes':likes, 'views':views, 
                   'retweets':retweets, 'replys':replys, 'quotes':quotes, 
                   'includes_media':includes_media, 'media_key':media_key, 'media_views':media_views,
                    'media_type':media_type, 'created_on':dates}
    return pd.DataFrame(tweets_info)

def get_private_tweet_info(list_of_tweets, pre_retrived_dates, USER_T, TOKEN_S, API_K=API_KEY, API_S=API_SECRET, payload=PAYLOAD):
    # create a list of tweet_ids so that when can iterate through them that way
    list_of_tweet_ids = []
    for group_of_tweets in list_of_tweets:
        for tweet in group_of_tweets:
            list_of_tweet_ids.append(tweet['id'])

    auth = OAuth1(API_K, API_S, USER_T, TOKEN_S)

    # create a seperate list for every public metric
    user_profile_clicks = []
    impression_count = []
    url_link_clicks = []
    text = []
    dates = pre_retrived_dates

    # this will iterate through all the tweets and append the views, likes, and text metrics
    for TWEET_ID in list_of_tweet_ids:
        url = API_CALLS(_USERNAME, USER_ID, TWEET_ID).get_private_tweet_info()
        response = requests.request("GET", url, auth=auth, data=payload)
        unchecked_data = response.json()
        data = error_handling(unchecked_data, url, auth)
        if 'errors' not in data:
            _user_profile_clicks = data['data']['non_public_metrics']['user_profile_clicks']
            _impression_count = data['data']['non_public_metrics']['impression_count']
            if 'url_link_clicks' in data['data']['non_public_metrics']:
                url_link_clicks.append(data['data']['non_public_metrics']['url_link_clicks'])
            else:
                url_link_clicks.append('N/A')
            _text = data['data']['text']
            user_profile_clicks.append(_user_profile_clicks)
            impression_count.append(_impression_count)
            text.append(_text)
        else:
            user_profile_clicks.append('N/A')
            impression_count.append('N/A')
            url_link_clicks.append('N/A')
            text.append('N/A')

    # once we are done using the string version of the IDs for the URL functionality change it back to integers for proper storage into a database/pandas dataframe
    for i in range(len(list_of_tweet_ids)):
        list_of_tweet_ids[i] = int(list_of_tweet_ids[i])

    # store public metrics into a dictionary for easy manipulation of data
    tweets_info = {'tweet_id':list_of_tweet_ids, 'text':text, 'impression_count':impression_count, 'user_profile_clicks':user_profile_clicks, 'url_link_clicks':url_link_clicks, 'created_on':dates}

    return pd.DataFrame(tweets_info)

def get_following(headers=HEADERS, payload=PAYLOAD):
    # retrives a list of users the specified user is following
    next_token_list = ['']
    url = API_CALLS(username=_USERNAME, user_id=USER_ID, pag_token=next_token_list[-1]).get_following()
    list_of_following = []
    list_of_ids = []
    list_of_names = []
    list_of_usernames = []
    next_token_exists = True
    while next_token_exists:
        response = requests.request("GET", url, headers=headers, data=payload)
        unchecked_data = response.json()
        data = error_handling(unchecked_data, url, headers)
        if 'next_token' not in data['meta']:
            list_of_following.append(data['data'])
            group_of_tweets = list_of_following[-1]
            for tweet in group_of_tweets:
                list_of_ids.append(tweet['id'])
                list_of_names.append(tweet['name'])
                list_of_usernames.append(tweet['username'])
            next_token_exists = False
        else:
            list_of_following.append(data['data'])
            group_of_tweets = list_of_following[-1]
            for tweet in group_of_tweets:
                list_of_ids.append(tweet['id'])
                list_of_names.append(tweet['name'])
                list_of_usernames.append(tweet['username'])
            next_token_list.append("&pagination_token=" + data['meta']['next_token'])
            url = API_CALLS(username=_USERNAME, user_id=USER_ID, pag_token=next_token_list[-1]).get_following()
    following_info = {'id': list_of_ids, 'name': list_of_names, 'username': list_of_usernames}
    return following_info

def get_followers(following_info, headers=HEADERS, payload=PAYLOAD):
    # define next_token_list to store pagination tokens for paginating purposes, also empty lists for data needing to be stored
    next_token_list = ['']
    url = API_CALLS(username=_USERNAME, user_id=USER_ID, pag_token=next_token_list[-1]).get_followers()
    list_of_following = []
    list_of_ids = []
    list_of_names = []
    list_of_usernames = []
    next_token_exists = True

    # while the pagniation token exists, append data. Once you reach the end, stop.
    while next_token_exists:
        response = requests.request("GET", url, headers=headers, data=payload)
        unchecked_data = response.json()
        data = error_handling(unchecked_data, url, headers)
        if 'next_token' not in data['meta']:
            list_of_following.append(data['data'])
            group_of_tweets = list_of_following[-1]
            for tweet in group_of_tweets:
                list_of_ids.append(tweet['id'])
                list_of_names.append(tweet['name'])
                list_of_usernames.append(tweet['username'])
            next_token_exists = False
        else:
            list_of_following.append(data['data'])
            group_of_tweets = list_of_following[-1]
            for tweet in group_of_tweets:
                list_of_ids.append(tweet['id'])
                list_of_names.append(tweet['name'])
                list_of_usernames.append(tweet['username'])
            next_token_list.append("&pagination_token=" + data['meta']['next_token'])
            url = API_CALLS(username=_USERNAME, user_id=USER_ID, pag_token=next_token_list[-1]).get_followers()
    followers_info = {'id': list_of_ids, 'name': list_of_names, 'username': list_of_usernames}

    # create a mutal following list that will either append true or false depending on if a given user is both a follower and you are following
    mutal_following = []
    for following_id in following_info['id']:
        if following_id in followers_info['id']:
            mutal_following.append('True')
        else:
            mutal_following.append('False')
    following_info['mutal'] = mutal_following
    mutal_followers = []
    for followers_id in followers_info['id']:
        if followers_id in following_info['id']:
            mutal_followers.append('True')
        else:
            mutal_followers.append('False')
    followers_info['mutal'] = mutal_followers
    return_value = []
    return_value.append(pd.DataFrame(following_info))
    return_value.append(pd.DataFrame(followers_info))
    return return_value