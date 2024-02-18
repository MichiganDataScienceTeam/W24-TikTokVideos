import click
import shutil
from pytube import YouTube
from moviepy.editor import *
#

@click.command()
@click.option(
    "--videos", "videos", default=1, help="Number of videos to make.", type=int
)
@click.option(
    "--subreddit",
    "subreddit",
    default="AskReddit",
    help="Subreddit to get videos from.",
    type=str,
)
def main(videos: int, subreddit: str):
    """Automatically generate videos from Reddit posts."""
    print(f"Generating {videos} videos from r/{subreddit}.")
    downloadVideos()

def downloadVideos():
    #yt = YouTube('https://www.youtube.com/watch?v=Q5KtBKk4hC0')
    # video name - Subway Surfers - First 30 Minutes Gameplay (Vertical Video).mp4
    yt = YouTube('https://www.youtube.com/watch?v=Q5KtBKk4hC0')
    str = yt.streams[0].title + ".mp4"
    yt.streams.filter(res="720p").first().download(output_path = 'videos')
    #video = VideoFileClip("Subway Surfers - First 30 Minutes Gameplay (Vertical Video).mp4").subclip(1622, 1682) # from 27:02 to 28:02
    video = VideoFileClip(str).subclip(1622, 1682) # from 27:02 to 28:02
    video.write_videofile("videos/background_edited.mp4",fps=25) #was a .webm

   

if __name__ == "__main__":
    main()

