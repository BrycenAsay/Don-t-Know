# creating a dictionary to store all twitter APIs and respective headers
from config import BEARER_TOKEN as bear_token, API_KEY
from datetime import datetime, date, timedelta

# headers for all public API Calls
HEADERS = {
    'Authorization': 'Bearer ' + bear_token,
    'Cookie': 'guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
    }
OAUTH_GET_TOKENS_HEADERS = {
    'Cookie': '_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLmYfYSGAToMY3NyZl9p%250AZCIlNGMyZWMwN2Y0YzUwOTgwYzRjNWY5YWQ5MGMwOGNjMmY6B2lkIiU2YzM5%250ANjgzYmI5MTJiNDUwM2RlYmEwMDkyMjAxYThlNA%253D%253D--1cf2c36413e28fe1726e2ff12287c59076045c07; guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
}
OAUTH_ACCESS_TOKENS_HEADERS = {
  'Cookie': '_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLmYfYSGAToMY3NyZl9p%250AZCIlNGMyZWMwN2Y0YzUwOTgwYzRjNWY5YWQ5MGMwOGNjMmY6B2lkIiU2YzM5%250ANjgzYmI5MTJiNDUwM2RlYmEwMDkyMjAxYThlNA%253D%253D--1cf2c36413e28fe1726e2ff12287c59076045c07; guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
}

# payload for all API Calls
PAYLOAD = {}

# create a class called API_Calls which stores all urls and proper peramaters to make the format the API urls properly when called upon
class API_CALLS:
    def __init__(self, username=None, user_id=None, tweet_id=None, pag_token='', oauth_token='', oauth_verifier=''):
        self.username = username
        self.user_id = user_id
        self.tweet_id = tweet_id
        self.pag_token = pag_token
        self.oauth_token = oauth_token
        self.oauth_verifier = oauth_verifier
        current_time = datetime.now()
        self.end_time = f'{str(current_time)[0:10]}T{str(current_time)[11:20]}000Z'
        thirty_days_back = str(date.today()-timedelta(days=30))
        self.start_time = f'{thirty_days_back}T{str(current_time)[11:20]}000Z'
    def get_user_id(self):
        return 'https://api.twitter.com/2/users/by/username/' + self.username
    def get_tweets(self):
        return f"https://api.twitter.com/2/users/" + self.user_id + "/tweets?tweet.fields=created_at&max_results=5" + self.pag_token
    def get_tweets_time_specific(self):
        return f"https://api.twitter.com/2/users/{self.user_id}/tweets?tweet.fields=created_at&max_results=100&start_time={self.start_time}&end_time={self.end_time}"
    def get_tweets_txt_likes_views(self):
        return "https://api.twitter.com/2/tweets?ids=" + self.tweet_id + "&tweet.fields=public_metrics&expansions=attachments.media_keys&media.fields=public_metrics"
    def get_following(self):
        return f"https://api.twitter.com/2/users/{self.user_id}/following?max_results=100" + self.pag_token
    def get_followers(self):
        return f"https://api.twitter.com/2/users/{self.user_id}/followers?max_results=100" + self.pag_token
    def get_OAuth_Tokens(self):
        return f'https://api.twitter.com/oauth/request_token?oauth_consumer_key={API_KEY}&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1677427442&oauth_nonce=wVsQ2P8nTbb&oauth_version=1.0&oauth_signature=3BSY1kX9DuLKypRMfc4%2Fn3nHgJE%3D'
    def access_OAuth_Tokens(self):
        return f'https://api.twitter.com/oauth/access_token?oauth_token={self.oauth_token}&oauth_verifier={self.oauth_verifier}&oauth_consumer_key={API_KEY}'