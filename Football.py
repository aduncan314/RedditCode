#!/bin/python

import RedditFuncs as RF

reddit = RF.config_reddit_readonly()
SCORE_MIN	= 50												#Minimum comment score
thisSubreddit = choose_subreddit()					#Choose the subreddit to be used

#Choose subreddit for later use
def choose_subreddit():
	return 'nfl'
	
#print the body of the highest comment
def title_and_top_com(sub):
	topComments = {}
	for top_level in sub.comments:
		if top_level.score > SCORE_MIN:
			topComments[top_level.id] = [top_level.score, top_level.body]
	print len(topComments)
#assert lenth is greater than 0?
	comMax = [0,'none']
	for com in topComments.keys():
		if topComments[com][0] > comMax[0]:
			comMax = [topComments[com][0], com]
	return(sub.title +'\n' +topComments[comMax[1]][1])

# Take submission and return an average length response.
submissionIds = RF.top_posts(2, thisSubreddit)
print submissionIds

#print submissionIds
for postId in submissionIds:
	submission = reddit.submission(id = postId)
	submission.comments.replace_more(limit=0)
	print( title_and_top_com(submission))
	
	
