"""
Originally written by Harrison Shoebridge (@paked/@hcwool), now property of the WPC community!

The r/WatchPeopleCode sidebar updater script/bot!

Configuration is required, and can be done through the config.json or corresponding environment variables.
"""

from praw import *

import random
import os
import requests
import json
import time
import logging
from urllib.parse import urlparse, parse_qs

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s')

class Bot:
	"""
	Bot represents a basic bot, with a reddit username, password and subreddit
	"""
	def __init__(self, username, password, subreddit="watchpeoplecode"):
		self._username = username
		self._password = password
		self._subreddit = subreddit

		self.r = Reddit("{0} a bot for /r/{1} to set top WPC streams!".format(self._username, self._subreddit))

		self.login()

	def login(self):
		logging.info("I'm logging in now!")
		self.r.login(self._username, self._password)


class SidebarBot(Bot):
	"""
	Sidebar bot, a bot to update your sidebar!
	"""
	def __init__(self, username, password, description, subreddit="watchpeoplecode", mode="live"):
		super().__init__(username, password, subreddit)
		if mode != 'live':
			raise Exception("Only 'live' mode is supported")

		self.description = description

	def update(self):
		logging.info("Just about to start making that sweet description of yours!")
		description = self.generate_description(self.choose_streams())

		logging.info("Whew! Just gonna get that specified subreddit for you!")
		subreddit = self.r.get_subreddit(self._subreddit)
		logging.info("Updating your sidebar now...")
		subreddit.update_settings(description=description.encode('utf8'))
		logging.info("Updated your sidebar")

	def generate_description(self, streams):
		output = self.description["pre"] + "\n\n"
		output += self.description["viewers_template"].format(str(self._get_total_viewers())) + "\n\n"
		for stream in streams:
			output += self.description["template"].format(stream["user"], stream["title"], stream["url"], self._get_viewers(stream)) + "\n\n"

		output += "\n\n" + self.description["post"]
		return output

	def choose_streams(self):
		streams = self._get_streams()
		return random.sample(streams, 3) if len(streams) >= 3 else streams
		
	def _get_total_viewers(self):
		live_streams = self._get_streams()
		viewers = 0
		if len(live_streams) == 0:
			return viewers
		else:
			for stream in live_streams:
				viewers += self._get_viewers(stream)
			return viewers
			
	def _get_viewers(self, stream):
		return stream["viewers"]
	
	def _get_streams(self):
		return requests.get("http://www.watchpeoplecode.com/api/v1/streams/live").json()["data"]

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
		timer = int(os.environ['TIMER'])

	sb = SidebarBot(username,
					password,
					description,
					subreddit=subreddit,
					mode=mode)
	while True:
		try:
			sb.update()
		except errors.InvalidCaptcha:
			logging.warning("No Captcha Supplied\nIt worked anyway though...\nSuppress this message by getting 2 link karma.")
		except Exception as e:
			logging.error("todo mail harrison and aaron")
			logging.exception(e)
			# mail harrison, and aaron.
		time.sleep(timer)
