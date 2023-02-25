# creating a dictionary to store all twitter APIs and respective headers
from config import BEARER_TOKEN as bear_token, API_KEY

# headers for all API Calls
HEADERS = {
    'Authorization': 'Bearer ' + bear_token,
    'Cookie': 'guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
    }
OAUTH_HEADERS = {
    'Cookie': '_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLmYfYSGAToMY3NyZl9p%250AZCIlNGMyZWMwN2Y0YzUwOTgwYzRjNWY5YWQ5MGMwOGNjMmY6B2lkIiU2YzM5%250ANjgzYmI5MTJiNDUwM2RlYmEwMDkyMjAxYThlNA%253D%253D--1cf2c36413e28fe1726e2ff12287c59076045c07; guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
}

# payload for all API Calls
PAYLOAD = {}

# create a class called API_Calls which stores all urls and proper peramaters to make the format the API urls properly when called upon
class API_CALLS:
    def __init__(self, username=None, user_id=None, tweet_id=None, pag_token=''):
        self.username = username
        self.user_id = user_id
        self.tweet_id = tweet_id
        self.pag_token = pag_token
    def get_user_id(self):
        return 'https://api.twitter.com/2/users/by/username/' + self.username
    def get_tweets(self):
        return f"https://api.twitter.com/2/users/" + self.user_id + "/tweets?tweet.fields=created_at&max_results=5" + self.pag_token
    def get_tweets_txt_likes_views(self):
        return "https://api.twitter.com/2/tweets?ids=" + self.tweet_id + "&tweet.fields=public_metrics&expansions=attachments.media_keys&media.fields=public_metrics"
    def get_OAuth_Tokens(self):
        return f'https://api.twitter.com/oauth/request_token?oauth_consumer_key={API_KEY}&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1677300609&oauth_nonce=7QHNopWh1zp&oauth_version=1.0&oauth_signature=b2FjalXERzHbGVwzWnwIPN2Jf%2Fg%3D"'