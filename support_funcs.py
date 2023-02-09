import requests

def get_user_id(USERNAME, bear_token):
    url = "https://api.twitter.com/2/users/by/username/" + USERNAME

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

def get_tweet_ids(list_of_tweets):
    list_of_tweet_ids = []
    for tweet in list_of_tweets:
        list_of_tweet_ids.append(tweet['id'])
    return list_of_tweet_ids