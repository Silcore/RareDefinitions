'''
Written by /u/SIllycore
Rare Definitions Bot
	1. Read Reddit comments.
	2. Check for words with low frequencies.
	3. Respond with definitions.
'''

# Custom module containing necessary login credentials.
import botConfig

import praw
import os
from wordfreq import zipf_frequency
from vocabulary.vocabulary import Vocabulary as vocab

# Initialize Reddit instance and other necessary variables.
reddit = botConfig.login()
subreddit = reddit.subreddit("test")
comments = subreddit.stream.comments()

# Iterate through the comments in the designated subreddit(s).
for comment in comments:
	if not os.path.isfile("repliedComments.txt"):
		repliedComments = []
		with open("repliedComments.txt", "a"): pass
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