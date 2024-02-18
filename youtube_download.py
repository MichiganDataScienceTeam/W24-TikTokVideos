from pytube import YouTube
yt = YouTube('https://www.youtube.com/watch?v=y0MHb7hIaHU&list=PLRPR8uJQx5tE8lpRYJeZ29wFYPAxptsdd&index=26')
print(yt.streams.filter(only_audio=True))
stream = yt.streams.get_by_itag(139)
stream.download()