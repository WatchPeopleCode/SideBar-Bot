"""
@author Harrison Shoebridge <@paked/@hcwool>

The r/WatchPeopleCode sidebar updater script/bot!

In order to use the bot you will need a config.json file, following the format of the provided example_config.json
"""

from praw import *

import random
import os
import requests
import json
import time
from urllib.parse import urlparse, parse_qs

class Bot:
	"""
	Bot represents a basic bot, with a reddit username, password and subreddit
	"""
	def __init__(self, username, password, subreddit="watchpeoplecode", debug=False):
		self._username = username
		self._password = password
		self._subreddit = subreddit
		self.debug = debug

		self.r = Reddit("{0} a bot for /r/{1} to set top WPC streams!".format(self._username, self._subreddit))

		self.login()

	def login(self):
		self.log("I'm logging in now!")
		self.r.login(self._username, self._password)

	def log(self, message):
		if not self.debug:
			return
		print("[{}] {}".format(self._username, message))


class SidebarBot(Bot):
	"""
	Sidebar bot, a bot to update your sidebar!
	"""
	def __init__(self, username, password, description, subreddit="watchpeoplecode", mode="live", debug=False):
		super().__init__(username, password, subreddit, debug)

		self.description = description
		self.mode = mode

	def update(self):
		self.log("Just about to start making that sweet description of yours!")
		description = self.generate_description(self.choose_streams())

		self.log("Whew! Just gonna get that specified subreddit for you!")
		subreddit = self.r.get_subreddit(self._subreddit)
		self.log("Updating your sidebar now...")
		subreddit.update_settings(description=description.encode('utf8'))
		self.log("Updated your sidebar")

	def generate_description(self, streams):
		output = self.description["pre"] + "\n\n"
		output += self.description["viewers_template"].format(str(self._get_total_viewers())) + "\n\n"
		for stream in streams:
			output += self.description["template"].format(stream["username"], stream["title"], stream["url"], self._get_viewers(stream)) + "\n\n"

		output += "\n\n" + self.description["post"]
		return output

	def choose_streams(self):
		streams = self._get_streams()
		live_streams = streams[self.mode]
		if len(live_streams) <= 3:
			return live_streams
		else:
			return random.sample(live_streams, 3)
		
	def _get_total_viewers(self):
		streams = self._get_streams()
		live_streams = streams[self.mode]
		viewers = 0
		if len(live_streams) == 0:
			return viewers
		else:
			for stream in live_streams:
				viewers += self._get_viewers(stream)
			return viewers
			
	def _get_viewers(self, stream):
		if "twitch.tv" in stream["url"]:
			twitch_name = stream["url"].split("/")
			if twitch_name[-1] == "":
				twitch_name = twitch_name[-2]
			else:
				twitch_name = twitch_name[-1]
			stream_json = requests.get("https://api.twitch.tv/kraken/streams?channel=" + twitch_name).json()
			return stream_json["streams"][0]["viewers"]
		elif "youtube.com" in stream["url"]:
			# WARNING - Only accepts Youtube urls in the yt.com/watch?v=... format.
			url_data = urlparse(stream["url"])
			video_id = parse_qs(url_data.query)["v"][0]
			stream_viewers = requests.get("https://www.youtube.com/live_stats?v=" + video_id)
			return int(stream_viewers.text)
	
	def _get_streams(self):
		return requests.get("http://www.watchpeoplecode.com/json").json()

if __name__ == '__main__':
	if not os.environ.get('ENV_MODE'):
		print("In JSON mode")
		config_data = open('config.json')
		config = json.load(config_data)

		username = config["bot"]["username"]
		password = config["bot"]["password"]
		description = config["description"]
		subreddit = config["subreddit"]
		timer = int(config["timer"])
		mode = config["mode"]
		debug = config["debug"]

		config_data.close()
	else:
		username = os.environ['BOT_USERNAME']
		password = os.environ['BOT_PASSWORD']
		mode = os.environ['MODE']
		description = {"pre": os.environ['DESCRIPTION_PRE'],
					   "viewers_template": os.environ['DESCRIPTION_VIEWERS_TEMPLATE'],
					   "template": os.environ['DESCRIPTION_TEMPLATE'],
					   "post": os.environ['DESCRIPTION_POST']}
		subreddit = os.environ['SUBREDDIT']
		debug = os.environ['DEBUG']
		timer = int(os.environ['TIMER'])

	sb = SidebarBot(username,
					password,
					description,
					subreddit=subreddit,
					mode=mode,
					debug=debug)
	while True:
		try:
			sb.update()
		except errors.InvalidCaptcha:
			print("WARNING: No Captcha Supplied\nIt worked anyway though...\nSuppress this message by getting 2 link karma.")
		except Exception as e:
			print("FAILED: todo mail harrison and aaron")
			print(e)
			# mail harrison, and aaron.
		time.sleep(timer)
