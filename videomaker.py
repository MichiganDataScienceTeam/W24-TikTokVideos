import click
import praw
import shutil
from pytube import YouTube
from moviepy.editor import *
import pyttsx3
from gtts import gTTS
from moviepy.video.io import ffmpeg_writer

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
    videos = input("How many videos would you like:  ")
    if (videos == ""):
        videos = 1
    subreddit = input("Which subreddit would you like to use:  ")
    if (subreddit == ""):
        subreddit = "AmITheAsshole"
    """Automatically generate videos from Reddit posts."""
    print(f"Generating {videos} videos from r/{subreddit}.")
    #downloadVideos()
    videosInt = int(videos)
    downloadReddit(subreddit, videosInt)
    


def downloadVideos():
    # Subway Surfer: https://www.youtube.com/watch?v=Q5KtBKk4hC0
    # Minecraft https://www.youtube.com/watch?v=u7kdVe8q5zs
    # Car https://www.youtube.com/watch?v=VS3D8bgYhf4
    # Cake https://www.youtube.com/watch?v=88cgUkqH_x4
    print("Choose video option:")
    print("1: SubwaySurfer  2: Minecraft Parkour  3: GTA CAR   4: Cake Cutting")

    print('Downloading video')
    yt = YouTube('https://www.youtube.com/watch?v=yCI_iK3THF8')
    st = yt.streams[0].title + ".mp4"
    yt.streams.filter(res="720p").first().download(output_path = 'bgVideos')# (output_path = 'videos')
    

    

def downloadReddit(subredditStr : str, videos : int):
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
    for submission in subreddit.top(limit=videos):
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
       
    for submission in postList:
        title_full = submission.title
        title = "finalVids/" + title_full[:30] + ".mp4"
   
        titleAndText = submission.title + submission.selftext
        createAudio(titleAndText, 'audio.mp3', title)


def createAudio(text : str, audioFileName : str, title : str):
    print('Creating TTS audio.')
    engine = pyttsx3.init()
    engine.save_to_file(text, audioFileName)
    engine.runAndWait()

    print("0: Subway Surfers")
    print("1: Minecraft Parkour")
    print("2: Cake cutting")
    print("3: GTA Ramp")
    inputNum = input("Which background video would you like to use: ")
    
    if(inputNum == "0" or inputNum == ""):
        combineComponents(audioFileName, "bgVideos/SubwaySurfer.mp4", title)
    elif(inputNum == "1"):
        combineComponents(audioFileName, "bgVideos/MinecraftParkour.mp4", title)
    elif(inputNum == "2"):
        combineComponents(audioFileName, "bgVideos/CakeCut.mp4", title)
    elif(inputNum == "3"):
        combineComponents(audioFileName, "bgVideos/gtamegaramp.mp4", title)
    else:
        print("Error: incorrect input provided")


def combineComponents(audioFileName : str, videoFileName : str, title : str):
    '''videoclip = VideoFileClip(videoFileName)
    audioclip = AudioFileClip(audioFileName)

    #new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = audioclip
    videoclip.write_videofile("finalVids/" + "finalVid.mp4")'''

    # Load the video file
    video_clip = VideoFileClip(videoFileName)
    

    # Load the background audio
    background_audio = AudioFileClip(audioFileName)

    video_clip = video_clip.set_duration(background_audio.duration)

    # Set the background audio to the video clip
    new_video_clip = video_clip.set_audio(background_audio)

    # Write the combined video with the background audio
    new_video_clip.write_videofile(title, codec="libx264", audio_codec="aac")
    print("Created video called " + title)
    if os.path.exists("audio.mp3"):
    
        os.remove("audio.mp3")

if __name__ == "__main__":
    main()


#Fix GTA Ramp video

#Google TTS
#Subtitles?