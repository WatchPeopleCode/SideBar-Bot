from praw import *

import random
import os
import requests
import json

config_data = open('config.json')
config = json.load(config_data)

BOT_NAME = config["bot"]["username"]
BOT_PASSWORD = config["bot"]["password"]
SUBREDDIT = config["subreddit"] or "watchpeoplecode"

r = Reddit('Get the top 3 streams from r/WatchPeopleCode')
r.login(BOT_NAME, BOT_PASSWORD)

data = requests.get("http://www.watchpeoplecode.com/json").json()

live_streams = data["stream_urls"]
top_streams = []
if len(live_streams) >= 3:
	chosen = []
	for z in range(0, 3):
		i = 0
		while i not in chosen:
			i = random.randint(0, len(live_streams))
		
		top_streams.append(live_streams[i])
		chosen.append(i)
else:
	top_streams = live_streams

config_data.close()

