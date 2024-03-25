"""
Main file for simple_one app.

Steps:

1. When run, grab post and comment from reddit.

1a. Create a fake "post image" from the title

2. Take the post and comment from reddit and generate speech from both as separate files.

3. Grab the parkour video. Overlay the speech on it, with a 2 second delay between title and answer

4. Use the Leapord model from picovoice to generate two .srt timed caption files

5. Use pymovie to insert the captions onto the video

6. trim the parkour video 1 second after the last caption is said.

"""
from src.settings import settings
import praw
from praw.models import Subreddit, Submission, Comment

reddit = praw.Reddit(
    client_id=settings.REDDIT_CLIENT_APP_ID,
    client_secret=settings.REDDIT_CLIENT_SECRET,
    user_agent=settings.REDDIT_CLIENT_ACC_NAME,
)

subreddit: Subreddit = reddit.subreddit("AmItheAsshole")

num_posts = 2

# Return type Submission
for item in subreddit.hot(limit=num_posts):
    assert isinstance(item, Submission)
    if item.stickied:
        continue
    # print(item.title)
    the_title = item.title
    item.comment_limit = 2
    item.comment_sort = "confidence"
    item.comments.replace_more(limit=0)
    comment: Comment = item.comments.list()[1]
    the_body = comment.body
    # print(comment, repr(comment.body))
    # print(type(comment.body))
    # print([comment.body for comment in item.comments.list() if not comment.stickied])

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 120)
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[2].id)
#engine.say('Sally sells seashells by the seashore.')
#engine.say('The quick brown fox jumped over the lazy dog.')
engine.save_to_file(the_body, "first_file.mp3")
engine.runAndWait()


from moviepy.editor import *

# Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
clip = VideoFileClip("./videos/video.mp4")

# Reduce the audio volume (volume x 0.8)
clip = clip.volumex(0)

audioclip = AudioFileClip("first_file.mp3")

clip: VideoFileClip = clip.set_audio(audioclip)

clip.write_videofile("output_video.mp4",codec="libx264")