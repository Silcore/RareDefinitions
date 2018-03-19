# Written by /u/Sillycore

# Custom module containing necessary login credentials.
import botConfig

import praw
import os
import re
import random
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from wordfreq import zipf_frequency

# Parses through comments in the designated list of threads. Replies to comments with uncommon words and definitions.
def defineWords(reddit, threads):
	print("± Word Definitions Begin ±")
	
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
					message += getFooter()
					comment.reply(message)
					print("\t× Sending definitions to: " + comment.id + " ...")
					repliedComments.append(comment.id)
				
		with open("repliedComments.txt", "w") as file:
			for commentID in repliedComments:
				file.write(commentID + '\n')
				
	print("± Word Definitions End ±")

# Checks inbox for "good bot" or "bad bot" messages/replies and responds accordingly.
def checkMessages(reddit):
	print("± Message Checking Begin ±")
	
	unread_messages = []
	
	for item in reddit.inbox.unread():
		# Remove unnecessary symbols to grab only words or fragments.
		text = re.sub('[^A-Za-z]+', ' ', item.body.lower())
		
		if text.find("good bot") != -1 and text.find("bad bot") == -1:
			item.reply(getResponse("POSITIVE") + "\n\n***\n" + getFooter())
			print("\t× Sending happy reply to: " + item.id + " ...")
		elif text.find("bad bot") != -1 and text.find("good bot") == -1:
			item.reply(getResponse("NEGATIVE") + "\n\n***\n" + getFooter())
			print("\t× Sending sad reply to: " + item.id + " ...")
		
		unread_messages.append(item)
	
	reddit.inbox.mark_read(unread_messages)
	
	print("± Message Checking End ±")

# Returns the standard footer for all outgoing bot messages.	
def getFooter():
	message = "^^Beep! ^^I'm ^^a ^^friendly ^^robot. ^^| "
	message += "^^[Github](https://github.com/Silcore/RareDefinitions) ^^| "
	message += "[^^Message ^^Creator](https://www.reddit.com/message/compose/?to=sillycore)"
	
	return message

# Provides a randomized response to "good bot" or "bad bot" messages/replies.
def getResponse(sentiment):
	positiveResponses = ["It was my pleasure to serve you. ", "I'm happy to help. ", "You're very welcome! ", "You're very sweet! ",
						"I'll keep it up! ", "I love to see happy humans! "]
	negativeResponses = ["I'm sorry to disappoint. ", "I'll be sure to do better next time. ", "I'll try my best to improve. ", "I apologize profusely. ",
						"Please forgive me, for I'll never forgive myself. ", "Give me a second chance. I'll make it up to you. "]
	positiveEmojis = ["( ◞･౪･)", "(*\^▽\^*)", "(/\^▽\^)/", "o(≧∇≦o)", "(\^ _ \^)/", "(\*＾ワ＾\*)", "(⊙ヮ⊙)", "＼(\^ω\^＼)"]
	negativeEmojis = ["(︶︹︺)", "(oꆤ︵ꆤo)", "(▰︶︹︺▰)", "(つ﹏<)･ﾟ｡", "｡ﾟ･（>﹏<）･ﾟ｡", "(´•ω•̥`)", "(•̥́_•ૅू˳)", "(˘̩̩̩ε˘̩ƪ)"]
	
	if sentiment == "POSITIVE":
		return random.choice(positiveResponses) + random.choice(positiveEmojis) + "\n\n"
	elif sentiment == "NEGATIVE":
		return random.choice(negativeResponses) + random.choice(negativeEmojis) + "\n\n"
	
# Provides a list of top 25 hottest threads from designated subreddit list.
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
	checkMessages(reddit)
	
	print("Δ The bot has closed successfully. Δ")
	
if __name__ == "__main__":
	main()