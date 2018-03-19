# Written by /u/Sillycore

# Custom module containing necessary login credentials.
import botConfig

import praw
import os
import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from wordfreq import zipf_frequency

# Initialize Reddit instance and other necessary variables.
reddit = botConfig.login()
hotThreads = reddit.subreddit("InforMe").hot(limit = 25)

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

	# Iterate through the comments in the designated subreddit(s).
	for comment in comments:
		# If the comment has not yet been replied to, attempt to do so.
		if comment.id not in repliedComments and comment.author != botConfig.getUsername():		
			# Remove unnecessary symbols to grab only words or fragments.
			text = re.sub('[^A-Za-z]+', ' ', comment.body.lower())
			message = ""
			wordList = []
			
			# Iterate through each comment body checking for uncommon words.
			for word in text.split():
				frequency = zipf_frequency(word, "en", wordlist = "large")
				
				# Upper bound of word appearance rate is once per ten million words.
				if frequency != 0 and frequency < 2 and word not in wordList:
					# Add each word to wordList to prevent duplicate definitions per reply.
					wordList.append(word)
					message += "> " + '[' + word + "](http://www.dictionary.com/browse/" + word + "?s=t)"
					
					if word != WordNetLemmatizer().lemmatize(word, 'v'):
						word = WordNetLemmatizer().lemmatize(word, 'v')
						message += " → " + '[' + word + "](http://www.dictionary.com/browse/" + word + "?s=t)"
						
					try:
						synSet = nltk.corpus.wordnet.synsets(word)
						definition = synSet[0].definition()
						message += "\n\n> → " + definition
					except IndexError:
						message = ""
						break
					
					message += "\n\n***\n"
			
			if len(message) > 0:
				message += "^^Beep! ^^I ^^define ^^uncommon ^^words. ^^| "
				message += "^^[Github](https://github.com/Silcore/RareDefinitions) ^^| [^^Message ^^Creator](https://www.reddit.com/message/compose/?to=sillycore)"
				comment.reply(message)
				print("Bot replying to: " + comment.id + " ...")
				repliedComments.append(comment.id)
			else:
				print("Comment " + comment.id + " does not contain rare words. Skipping.")
		else:
			print("Comment " + comment.id + " already processed. Skipping.")
			
	with open("repliedComments.txt", "w") as file:
		for commentID in repliedComments:
			file.write(commentID + '\n')
			
print("Δ Rare Definitions Bot has closed successfully. Δ")