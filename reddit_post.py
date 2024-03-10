import praw
import pyttsx3
reddit = praw.Reddit(
    client_id="-e_5SNLpeJsBl8yVe-fxtA",
    client_secret="Ub_dCex2QTb9LSrWtPa5r9BWKAnvMA",
    user_agent="SubstantialYak6282",
)
#engine = pyttsx3.init(driverName='nsss')
# for submission in reddit.subreddit("cats").hot(limit=10):
#     print(submission.title)

engine = pyttsx3.init()
engine.setProperty('rate', 80)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
subreddit = reddit.subreddit("AmItheAsshole")

print(subreddit.display_name)
# Output: redditdev
#print(subreddit.title)
# Output: reddit development
#print(subreddit.description)
# Output: a subreddit for discussion 

for submission in subreddit.hot(limit=10):
    print(submission.title)
    # Output: the submission's title
    #print(submission.score)
    # Output: the submission's score
    #print(submission.id)
    # Output: the submission's ID
    #print(submission.url)
    #top_level_comments = list(submission.comments)
    print(submission.author.name)
    #print(top_level_comments)

    # engine.say(submission.selftext)
    # engine.runAndWait()
    print("-"*150)
    # #for comment in submission.comments.list():
    # print(submission.comments.body)
    # # Output: the URL the submi
    engine.say(submission.selftext)
    engine.runAndWait()




