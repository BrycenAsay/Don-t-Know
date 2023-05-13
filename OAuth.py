"""
This file exists to automate the OAuth handshake process by having a user sign in using their twitter credentials
And then saves those credentials into a table that can be read from the main file to get private metrics for a compliant user
"""
from config import API_KEY, API_SECRET, USER, PASSWORD, HOST, DATABASE
from requests_oauthlib import OAuth1
from sqlalchemy import create_engine, text
import logging
import requests

# Part where we define nessicary variables when making an API call
OAUTH_ACCESS_TOKENS_HEADERS = {
  'Cookie': '_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLmYfYSGAToMY3NyZl9p%250AZCIlNGMyZWMwN2Y0YzUwOTgwYzRjNWY5YWQ5MGMwOGNjMmY6B2lkIiU2YzM5%250ANjgzYmI5MTJiNDUwM2RlYmEwMDkyMjAxYThlNA%253D%253D--1cf2c36413e28fe1726e2ff12287c59076045c07; guest_id=v1%3A167354671801418520; guest_id_ads=v1%3A167354671801418520; guest_id_marketing=v1%3A167354671801418520; personalization_id="v1_Yg76iBwLIOAcAZZ145rAAA=="'
}

PAYLOAD = {}

# class for OAuth specific API calls
class API_CALLS:
    def __init__(self, oauth_token='', oauth_verifier=''):
        self.oauth_token = oauth_token
        self.oauth_verifier = oauth_verifier
    def get_OAuth_Tokens(self):
        return f'https://api.twitter.com/oauth/request_token'
    def access_OAuth_Tokens(self):
        return f'https://api.twitter.com/oauth/access_token?oauth_token={self.oauth_token}&oauth_verifier={self.oauth_verifier}&oauth_consumer_key={API_KEY}'

# functions that runs the OAuth handshake process
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
    user_OAuth_Creds['user_oauth_token'] = "'" + data[0] + "'"
    user_OAuth_Creds['user_oauth_secret'] = "'" + data[1] + "'"
    user_OAuth_Creds['user_id'] = data[2]
    user_OAuth_Creds['screen_name'] = "'" + data[3] + "'"
    return user_OAuth_Creds

def create_row(table_name, columns, data):
    columns = ','.join(columns)
    data = ','.join(data)
    query = text(f'INSERT INTO {table_name}({columns}) VALUES ({data});')
    return query

# where all the files run from
def main():
    # automation of the 3-legged OAuth process for getting more permanent tokens for a user (at least as much as I could automate the process)
    COLUMNS = []
    DATA = []
    OAuth_Tokens = get_OAuth_Tokens()
    User_OAuth_Tokens = Access_Token(OAuth_Tokens)
    for key in User_OAuth_Tokens:
        COLUMNS.append(key)
        DATA.append(str(User_OAuth_Tokens[key]))
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    with engine.connect() as conn:
        sql = create_row('User_OAuth_Info', COLUMNS, DATA)
        try:
            conn.execute(sql)
            conn.commit()
        except Exception as e:
            logging.error('did not work: ', e)
            conn.rollback()
        conn.close()
        
if __name__ == '__main__':
    main()