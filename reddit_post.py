import praw
import pyttsx3
from gtts import gTTS


from io import BytesIO
reddit = praw.Reddit(
    client_id="-e_5SNLpeJsBl8yVe-fxtA",
    client_secret="Ub_dCex2QTb9LSrWtPa5r9BWKAnvMA",
    user_agent="SubstantialYak6282",
)
#engine = pyttsx3.init(driverName='nsss')
# for submission in reddit.subreddit("cats").hot(limit=10):
#     print(submission.title)

engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id)
#engine.setProperty('voice', 'en_GB')
subreddit = reddit.subreddit("AmItheAsshole")

# Print available voices

print(subreddit.display_name)
# Output: redditdev
#print(subreddit.title)
# Output: reddit development
#print(subreddit.description)
# Output: a subreddit for discussion
first_iteration = True

# for submission in subreddit.hot(limit=2):
#     if first_iteration:
#         first_iteration = False
#         continue
#     # Output: the submission's title
#     #print(submission.score)
#     # Output: the submission's score
#     #print(submission.id)
#     # Output: the submission's ID
#     #print(submission.url)
#     #top_level_comments = list(submission.comments)
    
#     #print(top_level_comments)

#     # engine.say(submission.selftext)
#     # engine.runAndWait()
#     print("-"*150)
#     print(submission.author.name)   
#     print(submission.title)
#     # # Output: the URL the submi
#     #engine.say(submission.selftext)
#     engine.say(submission.title)
#     print(submission.selftext)
#     engine.runAndWait()


for submission in subreddit.hot(limit=2):
    text = submission




tts = gTTS(text.selftext, lang='en')
tts.save('hello.mp3')