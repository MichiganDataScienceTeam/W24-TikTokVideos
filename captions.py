from moviepy.editor import *
import assemblyai as aai

# If the API key is not set as an environment variable named
# ASSEMBLYAI_API_KEY, you can also set it like this:
aai.settings.api_key = "1f6c11325d414c648902ca605da37cb2"

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
final = CompositeVideoClip([myvideo, sub])
final.write_videofile("final.mp4", fps=myvideo.fps)