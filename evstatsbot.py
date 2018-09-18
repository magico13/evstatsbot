import praw


useragent = "linux:evstatsbot:v0.1.0 (by /u/magico13)"


reddit = praw.Reddit('evstatsbot', user_agent=useragent)


submission = reddit.submission(id='9dzaie')
#print(submission.author)
#print(vars(submission))
print('{}: "{}"'.format(submission.author, submission.selftext))
#submission.comments.replace_more(limit=0)
#for comment in submission.comments.list():
#    print('{}: "{}"'.format(comment.author, comment.body))
