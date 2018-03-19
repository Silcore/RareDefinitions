# Written by /u/Sillycore

# Custom module containing necessary login credentials.
import botConfig

import praw
import os
import re
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from wordfreq import zipf_frequency

def defineWords(reddit, threads):
	for thread in threads:
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
							synSet = wordnet.synsets(word)
							definition = synSet[0].definition()
							message += "\n\n> → " + definition
						except IndexError:
							message = ""
							break
						
						message += "\n\n***\n"
				
				if len(message) > 0:
					message += "^^Beep! ^^I ^^define ^^uncommon ^^words. ^^| "
					message += "^^[Github](https://github.com/Silcore/RareDefinitions) ^^| "
					message += "[^^Message ^^Creator](https://www.reddit.com/message/compose/?to=sillycore)"
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

'''
def checkMessages(reddit):
	for message in reddit.inbox.unread():
		if isinstance(message, Comment):

'''
def getThreads(reddit):
	# User-defined list of subreddits for the bot to check.
	subreddits = ["InforMe"]
	threads = []
	
	for name in subreddits:
		threads.extend(reddit.subreddit(name).hot(limit = 25))
	
	return threads
	
def main():
	# Initialize Reddit instance and other necessary variables.
	reddit = botConfig.login()
	defineWords(reddit, getThreads(reddit))
	# checkMessages(reddit)
	
	print("Δ The bot has closed successfully. Δ")
	
if __name__ == "__main__":
	main()