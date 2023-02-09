import requests
import pandas as pd
from IPython.display import display

# write functions

def get_user_id(username, bear_token):
    url = "https://api.twitter.com/2/users/by/username/" + username

    payload={}

    # make it easier to change token for current user
    # error logic for recieving a response (response status code 429)
    # run multiple instances

    headers = {
    'Authorization': 'Bearer ' + bear_token,
    'Cookie': 'guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    user_id = data['data']['id']
    return user_id

def get_tweets(user_id, last_date, bear_token):

    if last_date == []:
        start_filter = ''
    else:
        last_tweet = last_date
        start_filter = f'&end_time={last_tweet}'
    url = f"https://api.twitter.com/2/users/" + user_id + "/tweets?tweet.fields=created_at&max_results=69" + '&start_time=2010-11-09T19:08:47.000Z' + start_filter

    payload={}
    headers = {
    'Authorization': 'Bearer ' + bear_token,
    'Cookie': 'guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    print(data)
    list_of_tweets = data['data']
    return list_of_tweets

def get_tweet_info(list_of_tweets, bear_token):
    list_of_tweet_ids = []
    for tweet in list_of_tweets:
        list_of_tweet_ids.append(tweet['id'])

    views = []
    likes = []
    text = []
    dates = []
    for tweet_id in list_of_tweet_ids:

        url = "https://api.twitter.com/2/tweets?ids=" + tweet_id + "&tweet.fields=public_metrics&expansions=attachments.media_keys&media.fields=public_metrics"

        payload={}
        headers = {
        'Authorization': 'Bearer ' + bear_token,
        'Cookie': 'guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        print(data)
        like_count = data['data'][0]['public_metrics']['like_count']
        view_count = data['data'][0]['public_metrics']['impression_count']
        individual_text = data['data'][0]['text']
        text.append(individual_text)
        likes.append(like_count)
        views.append(view_count)

    for tweet_id in list_of_tweet_ids:
        url = "https://api.twitter.com/2/tweets?ids=" + tweet_id + "&tweet.fields=attachments,author_id,context_annotations,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld&expansions=referenced_tweets.id"

        payload={}
        headers = {
        'Authorization': 'Bearer ' + bear_token,
        'Cookie': 'guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
        }

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