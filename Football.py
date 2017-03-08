#!/bin/python

import RedditFuncs as RF

reddit = RF.config_reddit_readonly()
SCORE_MIN	= 50												#Minimum comment score
thisSubreddit = RF.choose_subreddit()					#Choose the subreddit to be used

	
#print the body of the highest comment
def title_and_top_com(sub):
	topComments = {}
	for top_level in sub.comments:
		if top_level.score > SCORE_MIN:
			topComments[top_level.id] = [top_level.score, top_level.body]
	print("Number of comments above " + str(SCORE_MIN) + ":  " +str(len(topComments)))
#assert lenth is greater than 0?
	comMax = [0,'none']
	for com in topComments.keys():
		if topComments[com][0] > comMax[0]:
			comMax = [topComments[com][0], com]
	return("***" + sub.title + "***" +'\n' +topComments[comMax[1]][1] + '\n\n')

# Take submission and return an average length response.
submissionIds = RF.top_posts(2, thisSubreddit)

for postId in submissionIds:
	submission = reddit.submission(id = postId)
	submission.comments.replace_more(limit=0)
	print(title_and_top_com(submission))
	
	
