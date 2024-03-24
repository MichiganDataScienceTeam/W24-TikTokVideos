# Import everything needed to edit video clips
from moviepy.editor import VideoFileClip, AudioFileClip

# # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
# clip = VideoFileClip("minecraft_background.mp4").subclip(0,60)

# # Reduce the audio volume (volume x 0.8)
# clip = clip.volumex(0.8)

# # Generate a text clip. You can customize the font, color, etc.
# txt_clip = TextClip("My Holidays 2013",fontsize=70,color='white')

# # Say that you want it to appear 10s at the center of the screen
# txt_clip = txt_clip.set_pos('center').set_duration(10)

# # Overlay the text clip on the first video clip
# video = CompositeVideoClip([clip, txt_clip])

# # Write the result to a file (many options available !)
# video.write_videofile("myHolidays_edited.webm")

video_path = "videos/minecraft_background.mp4"
audio_path = "hello.mp3"

# Load video and audio clips
video_clip = VideoFileClip(video_path)
audio_clip = AudioFileClip(audio_path)

# Set the duration of the video to match the duration of the audio
video_clip = video_clip.set_duration(audio_clip.duration)

# Combine video and audio
final_clip = video_clip.set_audio(audio_clip)

# Export the combined video with audio
final_clip.write_videofile("combined_video.mp4", codec="libx264", fps=24)

# Close the clips
video_clip.close()
audio_clip.close()