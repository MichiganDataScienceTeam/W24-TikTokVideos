# Import everything needed to edit video clips
from moviepy.editor import *

def videomaker():

    videoclip = VideoFileClip("backgroundvideos/minecraftdiamonds.mp4").subclip(0,36)
    audioclip = AudioFileClip("test0.mp3")
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile("minecraft_edited.mp4")

videomaker()
