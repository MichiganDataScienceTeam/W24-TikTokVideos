import pytube
import pathlib

video_ids = [
    "rKif1aPl30A",
    "2VpG0WS4uCo",
    "TTdtMqKajws",
    "SUi-H3Zjp3s",
    "JlPEb6WNuDI",
]


def check_dowloaded(video_id):
    if pathlib.Path(f"backgrounds/{video_id}.mp4").exists():
        return True
    return False


def download_videos():
    for video_id in video_ids:
        if check_dowloaded(video_id):
            continue
        yt = pytube.YouTube(f"https://www.youtube.com/watch?v={video_id}")
        streams = (
            yt.streams.filter(progressive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
        )
        streams.first().download(output_path="backgrounds", filename=video_id)


if __name__ == "__main__":
    download_videos()
