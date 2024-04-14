from moviepy.editor import *
import assemblyai as aai
from PIL import Image

# import moviepy.config as conf  
# conf.change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI"})

# If the API key is not set as an environment variable named
# ASSEMBLYAI_API_KEY, you can also set it like this:
aai.settings.api_key = "5dd9e6ecb8f1476b804c9c0d62cacc30"
transcriber = aai.Transcriber()
transcript = transcriber.transcribe("minecraft_edited2.mp4")
srt = transcript.export_subtitles_srt()
# Save it to a file
with open("subtitle_example.srt", "w") as f:
    f.write(srt)
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
generator = lambda txt: TextClip(txt, font='Georgia-Regular', fontsize=24, color='white')
sub = SubtitlesClip("subtitle_example.srt", generator)
myvideo = VideoFileClip("minecraft_edited2.mp4")
myvideo_resized = myvideo.resize((1080, 1920))
final = CompositeVideoClip([myvideo_resized, sub])
final.write_videofile("final_resized.mp4", fps=myvideo_resized.fps)