# RareDefinitionsBot
### Purpose
The Rare Definitions Bot is intended to define words that have uncommon usage in the English language. It accomplishes this by scanning through recent Reddit comments in the designated subreddit(s), passing words from comments into a [Zipf frequency function](https://en.wikipedia.org/wiki/Zipf%27s_law), and posting definitions of those words with frequencies under the designated threshold.

### Languages and Dependencies
* Python
  * [PRAW](https://github.com/praw-dev/praw)
  * [NLTK](https://www.nltk.org/)
  * [WordFreq](https://github.com/LuminosoInsight/wordfreq)
