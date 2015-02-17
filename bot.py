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

class Bot:
	"""
	Bot represents a basic bot, with a reddit username, password and subreddit
	"""
	def __init__(self, username, password, subreddit="watchpeoplecode", debug=False):
		self._username = username
		self._password = password
		self._subreddit = subreddit
		self.debug = debug

		self.r = Reddit("{0} a bot for /r/{1} to set top WPC streams!".format(self._username, self._password))

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

		self.log("Whew! About to update your subreddits sidebar!")
		subreddit = self.r.get_subreddit(self._subreddit)
		subreddit.update_settings(description=description.encode('utf8'))

	def generate_description(self, streams):
		output = self.description["pre"] + "\n\n"
		for stream in streams:
			output += self.description["template"].format(stream["username"], stream["title"], stream["url"]) + "\n\n"

		output += "\n\n" + self.description["post"]
		return output

	def choose_streams(self):
		streams = self._get_streams()
		live_streams = streams[self.mode]
		top_streams = []
		if len(live_streams) > 3:
			chosen = []
			for z in range(0, 3):
				i = random.randint(0, len(live_streams)) 
				while i in chosen:
					i = random.randint(0, len(live_streams))
				
				top_streams.append(live_streams[i])
				chosen.append(i)
		else:
			top_streams = live_streams

		return top_streams

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
		except:
			print("FAILED: todo mail harrison and aaron")
			# mail harrison, and aaron.

		time.sleep(int(config["timer"]))
