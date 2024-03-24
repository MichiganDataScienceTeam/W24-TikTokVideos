# Import everything needed to edit video clips
from moviepy.editor import *

def videomaker():

    # need to match the timings
    audioclip = AudioFileClip("test0.mp3")
    videoclip = VideoFileClip("backgroundvideos/minecraftdiamonds.mp4").subclip(0,audioclip.duration)
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile("minecraft_edited.mp4")

videomaker()
