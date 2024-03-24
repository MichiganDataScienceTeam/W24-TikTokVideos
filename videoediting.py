# pip install moviepy
# pip install ez_setup

from moviepy.editor import *

clip = VideoFileClip("rKif1aPl30A.mp4").subclip(50,60) #video
clip = clip.volumex(0.7) #volume
txt_clip = TextClip("hello", fontsize = 40, color = "white") #text, size, color
txt_clip = txt_clip.set_pos('center').set_duration(10) #position, duration of text
video = CompositeVideoClip([clip, txt_clip]) #making the video!
video.ipython_display(width = 480) #display video
video.write_videofile("rKif1aPl30A_edited.webm") #creating the video file


#audioclip = AudioFileClip("some_audiofile.mp3")
#audioclip = AudioFileClip("some_video.avi")

