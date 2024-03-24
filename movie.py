# Import everything needed to edit video clips
from moviepy.editor import *

def videomaker():

    # need to match the timings
    for i in range(3):
        audioclip = AudioFileClip('test' + str(i) + '.mp3')
        videoclip = VideoFileClip("backgroundvideos/minecraftdiamonds.mp4").subclip(0,audioclip.duration)
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile("minecraft_edited" + str(i) + ".mp4")

videomaker()
