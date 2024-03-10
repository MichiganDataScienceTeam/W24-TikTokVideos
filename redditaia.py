import praw 
from praw.models import MoreComments

reddit = praw.Reddit(
    client_id="qO_E9x26ahBwZwt0E4C6gQ",
    client_secret="_DbAEWbLn8HtwkZafiU3KqW349Ae9g",
    user_agent="testscript by u/MDSTBot",
    username="MDSTBot",
    password="Winter-2024"
    )


sub = reddit.subreddit("AmItheAsshole")
print(reddit.user.me())

for submission in sub.top(limit=2):
    print(submission.selftext)
