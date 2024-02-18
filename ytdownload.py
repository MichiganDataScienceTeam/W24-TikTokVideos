from pytube import YouTube

if __name__ == "__main__":
    yt = YouTube('https://www.youtube.com/watch?v=Q5KtBKk4hC0')

    print(yt.streams)