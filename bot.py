from praw import *

import random
import os
import requests
import json

# Open up the bots config.
config_data = open('config.json')
config = json.load(config_data)

# Set credentials for the bot.
BOT_NAME = config["bot"]["username"]
BOT_PASSWORD = config["bot"]["password"]
SUBREDDIT = config["subreddit"] or "watchpeoplecode"

r = Reddit('Get the top 3 streams from r/WatchPeopleCode')
r.login(BOT_NAME, BOT_PASSWORD)

# Get streams and convert them to JSON.
data = requests.get("http://www.watchpeoplecode.com/json").json()

# Choose 3 random streams to display in sidebar.
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

output = ""
for stream in top_streams:
	output += "Check out [{}]({}) streaming".format(stream["user"], stream["url"])

print(output)

# TODO: Set sidebar to output.

config_data.close()

