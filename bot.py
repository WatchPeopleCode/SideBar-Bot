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
			output += "You should check out [{0}](http://reddit.com/r/{0}) streaming [{1}]({2})\n\n".format(stream["username"], stream["title"], stream["url"])

		output += "\n\n" + self.description["post"]
		return output

	def choose_streams(self):
		streams = self._get_streams()
		live_streams = streams[self.mode]
		top_streams = []
		if len(live_streams) > 3:
			chosen = []
			for z in range(0, 3):
				i = 0
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
	# Open up the bots config.
	config_data = open('config.json')
	config = json.load(config_data)

	sb = SidebarBot(config["bot"]["username"],
					config["bot"]["password"],
					config["description"],
					subreddit=config["subreddit"],
					mode=config["mode"],
					debug=True)

	sb.update()
	config_data.close()
