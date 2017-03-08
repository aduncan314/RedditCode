# Functions for interacting with Reddit API through PRAW
# Andrew Duncan
# February 2017

import praw, ConfigParser


# Returns a read only reddit instance
def config_reddit_readonly():
	config = ConfigParser.ConfigParser()
	config.read('config')
	configValues = config.items('data-collector-personal')
	for item in configValues:
		exec('%s = %s' % (item[0],item[1]))
	reddit = praw.Reddit(client_id=client_id,
										  client_secret=client_secret,
										  user_agent=user_agent)
	return reddit


# Returns an authorized reddit instance
def config_reddit_auth():
	config = ConfigParser.ConfigParser()
	config.read('config')
	configValues = config.items('data-collector-personal')
	for item in configValues:
		exec('%s = %s' % (item[0],item[1]))	
	reddit = praw.Reddit(client_id=client_id,
										  client_secret=client_secret,
										  user_agent=user_agent,
										  username=username,
										  password=password)
	return reddit


# Returns list of ids of the top %n posts to %subreddit
def top_posts(n,subreddit):
	reddit = config_reddit_readonly()
#	idsNums = [submission.id for submission in reddit.subreddit(subreddit).top(limit=n)]
	idNums = []
	for submission in reddit.subreddit(subreddit).hot(limit=n*2): # Change to check number of stickies and return n non stickied posts
		if not submission.stickied and len(idNums) < n+1:
			idNums.append(submission.id)
	return idNums


# Returns a list of all word sequences of length *length* in *text*
def length_n_sec(n, text):
	words = text.split()
	strings = []
	textLength = len(words)
	for start in range(textLength - n):
		strings.append(words[start: start+n])
	return strings
	
	
# Choose subreddit:		TODO
def choose_subreddit():
	return 'nfl'


