import praw
from praw.models import MoreComments

reddit = praw.Reddit(
    client_id="hxKUZEKETgOc--A26clqtA",
    client_secret="RBAwnYgLtVrlnzJkud7VKmrhYb1G6Q",
    user_agent="Subreddit extraction by u/snootdoots",
    username="snootdoots",
    password="Yucheng0423!"
)

# url = "https://www.reddit.com/r/AmItheAsshole/comments/1bgctcv/aita_for_asking_my_fianc%C3%A9_to_tell_my_mil_i_dont/"
for submission in reddit.subreddit("AmItheAsshole").hot(limit=1):
    print(submission.title)
    print(submission.selftext)