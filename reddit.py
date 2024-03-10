import praw 

reddit = praw.Reddit(
    client_id="qO_E9x26ahBwZwt0E4C6gQ",
    client_secret="	_DbAEWbLn8HtwkZafiU3KqW349Ae9g",
    user_agent="r/AskReddit comment extraction by u/MDSTBot",
    username="MDSTBot",
    password="Winter-2024"
    )

url = "https://www.reddit.com/r/AskReddit/comments/1bb49z1/what_was_cool_in_2014_but_isnt_cool_in_2024/"
submission = reddit.submission(url=url)
for top_level_comment in submission.comments:
    print(top_level_comment.body)