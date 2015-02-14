from praw import *
from urllib import request
import os
import requests

BOT_NAME = os.environ.get('BOT_NAME')
BOT_PASSWORD = os.environ.get('BOT_PASSWORD')
SUBREDDIT = os.getenv('SUBREDDIT', 'WatchPeopleCode')

r = Reddit('Get the top 3 streams from r/WatchPeopleCode')
r.login(BOT_NAME, BOT_PASSWORD)

data = requests.get("http://www.watchpeoplecode.com/json").json()

print(data)

r.close()

