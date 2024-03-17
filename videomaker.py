import click
import praw
import shutil
from pytube import YouTube
from moviepy.editor import *
import pyttsx3
from gtts import gTTS
#
# client ID: hfs2HBUHyxqvKhgZGMBfuQ
# client sectrt: upIiQlIX9rNlXIohlw7NEsEt3KYElQ
#python videomaker.py --videos 1 --subreddit askReddit

@click.command()
@click.option(
    "--videos", "videos", default=1, help="Number of videos to make.", type=int
)
@click.option(
    "--subreddit",
    "subreddit",
    default="AmItheAsshole", #default="AskReddit"
    help="Subreddit to get videos from.",
    type=str,
)
def main(videos: int, subreddit: str):
    """Automatically generate videos from Reddit posts."""
    print(f"Generating {videos} videos from r/{subreddit}.")
    #downloadVideos()
    downloadReddit(subreddit)

def downloadVideos():
    print('Downloading video')
    #yt = YouTube('https://www.youtube.com/watch?v=Q5KtBKk4hC0')
    # video name - Subway Surfers - First 30 Minutes Gameplay (Vertical Video).mp4
    yt = YouTube('https://www.youtube.com/watch?v=Q5KtBKk4hC0')
    str = yt.streams[0].title + ".mp4"
    yt.streams.filter(res="720p").first().download(output_path = 'videos')
    #video = VideoFileClip("Subway Surfers - First 30 Minutes Gameplay (Vertical Video).mp4").subclip(1622, 1682) # from 27:02 to 28:02
    video = VideoFileClip(str).subclip(1622, 1682) # from 27:02 to 28:02
    video.write_videofile("videos/background_edited.mp4",fps=25) #was a .webm

def downloadReddit(subredditStr : str):
    client_id = "hfs2HBUHyxqvKhgZGMBfuQ"
    client_secret = "upIiQlIX9rNlXIohlw7NEsEt3KYElQ"
    user_agent = "TikTok generated videos - u/Nearby-Counter-5848"
    
    # reddit read only login
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    print('Downloading reddit posts')

    # loop through the posts
    #for submission in reddit.subreddit("Python").hot(limit=10):
        #print(submission.title)

    subreddit = reddit.subreddit(subredditStr)
    #print(subreddit.display_name)
    #print(subreddit.title)
    #print(subreddit.description)

    postList = []
    top_level_comments = []
    for submission in subreddit.hot(limit=5):
        postList.append(submission)
        submission.comment_sort = "best"
        #print(submission.title)
        top_level_comments.append(list(submission.comments))
    
    

    #for j in range(5):
        #print(postList[j].title)
        #for i in range(5):
         #   print("Comment: #" + str(i+1))
          #  print(top_level_comments[j][i].body)
           # print("-----------------------------------")
    titleAndText = postList[4].title + postList[4].selftext
    createAudio(titleAndText, 'audio.mp3')


def createAudio(text : str, audioFileName : str):
    print('Creating TTS audio.')
    #BELOW IS USING PYTTSX3
    engine = pyttsx3.init()
    engine.save_to_file(text, audioFileName)
    engine.runAndWait()

    

    #print(text)
    #print(audioFileName)

if __name__ == "__main__":
    main()

