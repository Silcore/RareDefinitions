'''
Written by /u/Sillycore

This module is used as storage for the bot credentials when initializing a Reddit instance.
The necessary values are hidden from the Github repository to prevent external access to the bot.
'''

import praw

def login():
	reddit = praw.Reddit(
		user_agent = "HIDDEN_AGENT",
		client_id = "HIDDEN_ID",
		client_secret = "HIDDEN_SECRET",
		username = "HIDDEN_USERNAME",
		password = "HIDDEN_PASSWORD"
	)
	
	return reddit
