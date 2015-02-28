# SideBar-Bot
A bot for WPC to get the "top 3 streams" (currently these streams are chosen at random) and place them in the sidebar.

# Configuration
There are two methods of configuring the SideBar-Bot, first using a JSON file, second using environment variables.

## JSON Configuration
In order to get started with JSON configuration, copy the ```example_config.json``` file to a new ```config.json``` file. Inside your new ```config.json``` you will be able to find basic documentation on how to use each available setting.

## Environment Variable Configuration
Environment variables are the recommended production setup. Translation between JSON configuration and environment variable configuration is relatively simple: replace ```_``` instead of ```.```'s and changeall letters to upper-case.

***note:*** if you are going to use environment variables, **ALWAYS** set ```ENV_MODE``` to anything other than None to enable it.

* ENV_MODE
* BOT_USERNAME
* BOT_PASSWORD
* MODE
* SUBREDDIT
* DEBUG
* TIMER
* DESCRIPTION_PRE
* DESCRIPTION_VIEWERS_TEMPLATE
* DESCRIPTION_TEMPLATE
* DESCRIPTION_POST

# Running
Once you have filled out the ```config.json``` with a valid reddit account with moderator access to the wanted subreddit, you can safely execute the bot with ```python3 bot.py```.

