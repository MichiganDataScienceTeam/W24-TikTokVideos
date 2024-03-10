from pytube import YouTube

def Download(link):
    youtubeObject = YouTube('https://www.youtube.com/watch?v=VUfvRciny_Y&ab_channel=AnimatedSoundEffects')
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(output_path= 'backgroundvideos')
    except:
        print("An error has occurred")
    print("Download is completed successfully")
    # print(youtubeObject.streams)

link = input("Enter the YouTube video URL: ")
Download(link)