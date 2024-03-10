import praw 
from praw.models import MoreComments

reddit = praw.Reddit(
    client_id="qO_E9x26ahBwZwt0E4C6gQ",
    client_secret="_DbAEWbLn8HtwkZafiU3KqW349Ae9g",
    user_agent="r/travelreddit comment extraction by u/MDSTBot",
    username="MDSTBot",
    password="Winter-2024"
    )

sub = reddit.subreddit("AskReddit")
print(reddit.user.me())
url = "https://www.reddit.com/r/travel/comments/1bbboif/would_your_husband_or_wife_approve_of_you_going/"
# print(sub.top(limit=2))
# for submission in sub.top(limit=2):
#     print(submission.title)
submission = reddit.submission(url=url)
for top_level_comment in submission.comments:
    if isinstance(top_level_comment, MoreComments):
        continue
    print(top_level_comment.body)