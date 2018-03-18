'''
Written by Dexter Ketchum
Rare Definitions Bot
	1. Read Reddit comments.
	2. Check for words with low frequencies.
	3. Respond with definitions.
'''

import praw
import os
from wordfreq import zipf_frequency
from configparser import SafeConfigParser
from vocabulary.vocabulary import Vocabulary as vb

config = SafeConfigParser()
config.read("credentials.config")

# Initialize Reddit instance and other necessary variables.
reddit = praw.Reddit(config.get("bot_values", "user_agent"), config.get("bot_values", "client_id"),
					config.get("bot_values", "client_secret"), config.get("bot_values", "username"),
					config.get("bot_values", "password"))
subreddit = reddit.subreddit("test")
comments = subreddit.stream.comments()

# Iterate through the comments in the designated subreddit(s).
for comment in comments:
	if not os.path.isfile("repliedComments.txt"):
		repliedComments = []
		with open("repliedComments.txt", "w+"): pass
	else:
		with open("repliedComments.txt", "r") as file:
			repliedComments = file.read()
			repliedComments = repliedComments.split()
			repliedComments = list(filter(None, repliedComments))
	
	if comment.id not in repliedComments:
		text = comment.body.lower()
	
		# Iterate through each comment body checking for uncommon words.
		for word in text.split():
			frequency = zipf_frequency(word, "en", wordlist = "large")
			if frequency != 0 and frequency < 1.5:
				# Begin replying to comment here... TO DO