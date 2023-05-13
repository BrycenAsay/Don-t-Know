# Twitter Data Project
This project includes a collection of files that help to collect, store, and analyze data from one or a list of twitter users, and also includes helper files such as OAuth.py which automates the OAuth handshake process for retrieving private metrics. Below includes all of the important information in order for the files to work properly.

# Required Third Party Depencies/Libraries
requests_oauthlib - used to complete the OAuth1.0 handshake
sqlalchemy - used for updating into/reading from the database
requests - used to make API calls to Twitter
pandas - used mostly as a middle man for converting from a dictionary to a database table

# config.py File and it's Contents
For virtually every file there is a config.py file depency. Since I obviously don't want to expose my own private information, you will have to construct your own config.py file. Below are the variable names and what you will need to set them to in order for the files to work properly:
API_KEY = {your api key}
API_SECRET = {your api secret}
BEARER_TOKEN = {your bearer token}
HOST = {the host for your database}
USER = {the user for your database}
PASSWORD = {the password for said user/database}
DATABASE = {the database you want to use to store all of the tables}
\_USERNAME = {the usernames you want to collect data from, inside of a list (ex: \['jeremy'] or \['hello234', 'lizzyg35', 'usnewstoday'])}
