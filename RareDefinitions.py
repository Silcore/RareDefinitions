'''
Written by /u/Sillycore
Rare Definitions Bot
	1. Read Reddit comments.
	2. Check for words with low frequencies.
	3. Respond with definitions.
'''

# Custom module containing necessary login credentials.
import botConfig

import praw
import os
import re
import nltk
from wordfreq import zipf_frequency

# Initialize Reddit instance and other necessary variables.
reddit = botConfig.login()
hotThreads = reddit.subreddit("test").hot(limit = 25)

for thread in hotThreads:
	comments = thread.comments.list()

	if not os.path.isfile("repliedComments.txt"):
		repliedComments = []
		with open("repliedComments.txt", "a"): pass
	else:
		with open("repliedComments.txt", "r") as file:
			repliedComments = file.read()
			repliedComments = repliedComments.split()
			repliedComments = list(filter(None, repliedComments))

	botComments = reddit.redditor('RareDefinitions').comments.new()

	# Iterate through the comments in the designated subreddit(s).
	for comment in comments:
		# If the comment has not yet been replied to, attempt to do so.
		if comment.id not in repliedComments and comment.id not in botComments:
			text = comment.body.lower()
			message = ""
		
			# Remove unnecessary symbols to grab only words or fragments.
			re.sub('[^A-Za-z]+', ' ', text)
			
			# Iterate through each comment body checking for uncommon words.
			for word in text.split():
				frequency = zipf_frequency(word, "en", wordlist = "large")
				if frequency != 0 and frequency < 2:
					message += "> " + '[' + word + "](http://www.dictionary.com/browse/" + word + "?s=t)" + "\n\n"
					
					try:
						synSet = nltk.corpus.wordnet.synsets(word)
						definition = synSet[0].definition()
						message += "> " + definition + '\n'
					except IndexError:
						message = ""
						break
					
					message += "\n***\n"
			
			if len(message) > 0:
				message += "^^Beep! ^^I ^^define ^^rare ^^words. ^^| "
				message += "^^[Github](https://github.com/Silcore/RareDefinitionsBot) ^^| [^^Message ^^Creator](https://www.reddit.com/message/compose/?to=sillycore)"
				comment.reply(message)
				print("Bot replying to: " + comment.id + " ...")
				repliedComments.append(comment.id)
		else:
			print("Comment " + comment.id + " already processed. Skipping.")
			
	with open("repliedComments.txt", "w") as file:
		for commentID in repliedComments:
			file.write(commentID + '\n')
			
print("Δ Rare Definitions Bot has closed successfully. Δ")