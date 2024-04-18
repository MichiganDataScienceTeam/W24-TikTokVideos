from moviepy.editor import *
import assemblyai as aai
from PIL import Image

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
generator = lambda txt: TextClip(txt, font='Arial', fontsize=100, color='white', method= "caption")
vertical_offset = 100
sub = SubtitlesClip("subtitle_example.srt", generator)

sub = sub.set_position((0.3,0.3), relative=True)

myvideo = VideoFileClip("minecraft_edited2.mp4")




desired_width = 1080
desired_height = 1920

# Calculate the aspect ratios
original_aspect_ratio = myvideo.aspect_ratio
desired_aspect_ratio = desired_width / desired_height

# Calculate new dimensions and crop/pad as needed
if original_aspect_ratio > desired_aspect_ratio:
    # Video is wider than desired aspect ratio
    # Resize to fit height and pad sides
    new_clip = myvideo.resize(height=desired_height)
    # Calculate padding on the sides
    pad_size = (new_clip.w - desired_width) // 2
    # Crop the sides to achieve desired width
    final_clip = new_clip.crop(x1=pad_size, x2=new_clip.w - pad_size)
elif original_aspect_ratio < desired_aspect_ratio:
    # Video is taller than desired aspect ratio
    # Resize to fit width and pad top and bottom
    new_clip = myvideo.resize(width=desired_width)
    # Calculate padding on the top and bottom
    pad_size = (new_clip.h - desired_height) // 2
    # Crop the top and bottom to achieve desired height
    final_clip = new_clip.crop(y1=pad_size, y2=new_clip.h - pad_size)
else:
    # Aspect ratios are equal, just resize
    final_clip = myvideo.resize(width=desired_width, height=desired_height)

# Save the final resized and cropped video
final_clip = CompositeVideoClip([final_clip, sub])
final_clip.write_videofile("vertical_video.mp4")