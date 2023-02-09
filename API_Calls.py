# creating a dictionary to store all twitter APIs and respective headers
from config import BEARER_TOKEN as bear_token
from support_funcs import get_user_id
HEADERS = {
    'Authorization': 'Bearer ' + bear_token,
    'Cookie': 'guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
    }
PAYLOAD = {}
class API_Calls:
    def __init__(self, username=None, user_id=None, tweet_id=None):
        self.username = username
        self.user_id = user_id
        self.tweet_id = tweet_id
    def get_user_id(self):
        return 'https://api.twitter.com/2/users/by/username/' + self.username
    def get_tweets(self):
        return f"https://api.twitter.com/2/users/" + self.user_id + "/tweets?tweet.fields=created_at&max_results=100"
    def get_tweets_info(self):
        return "https://api.twitter.com/2/tweets?ids=" + self.tweet_id + "&tweet.fields=public_metrics&expansions=attachments.media_keys&media.fields=public_metrics"