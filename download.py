from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=hoLYnS2jOV8")

print(yt.streams)
