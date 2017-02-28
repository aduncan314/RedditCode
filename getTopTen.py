#!/bin/python

import praw, ConfigParser, datetime
import matplotlib.pyplot as plt

#import information to access Reddit API
config = ConfigParser.ConfigParser()
config.read('config')
configValues = config.items('data-collector-personal')

#f = open('attributes', 'a')

for item in configValues:
	exec('%s = %s' % (item[0],item[1]))
	
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)
#                     username='my username',
#                     password='my password')


plot = []
time = []
score = []

for submission in reddit.subreddit('Funny').hot(limit=1000):
	plot.append([1486680348-submission.created_utc,  submission.score])


#plot
plot =sorted(plot, key=lambda tup: tup[0])
for i in plot:
	time.append(i[0])
	score.append(i[1])
	
plt.plot(time, score)
plt.show()
#(datetime.datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'))
#	for entry in vars(submission):
#		f.write(str(entry)+"\n")
#f.close()
