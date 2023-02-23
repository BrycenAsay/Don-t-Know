# creating a dictionary to store all twitter APIs and respective headers
from config import BEARER_TOKEN as bear_token

# headers for all API Calls
HEADERS = {
    'Authorization': 'Bearer ' + bear_token,
    'Cookie': 'guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
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
    def get_tweets_create_date(self):
        return "https://api.twitter.com/2/tweets?ids=" + self.tweet_id + "&tweet.fields=attachments,author_id,context_annotations,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld&expansions=referenced_tweets.id"