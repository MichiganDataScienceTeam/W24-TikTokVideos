from pytube import YouTube
import os
from pathlib import Path

# hour-long video of subway surfers
yt = YouTube('https://www.youtube.com/watch?v=QFzfgB34cCk')

# shows what resolutions/birates are available
print("downloading....")

video = yt.streams.get_highest_resolution()

path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))

video.download(path_to_download_folder)
print("Downloaded! :)")