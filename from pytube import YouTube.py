from pytube import YouTube

def Download(link):
    youtubeObject = YouTube('https://youtu.be/f8mL0_4GeV0?feature=shared')
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(output_path= 'backgroundvideos')
    except:
        print("An error has occurred")
    print("Download is completed successfully")
    print(youtubeObject.streams)

link = input("Enter the YouTube video URL: ")
Download(link)