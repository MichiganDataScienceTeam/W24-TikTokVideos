import click
from pytube import YouTube

@click.command()
@click.option(
    "--videos", "videos", default=1, help="Number of videos to make.", type=int
)
@click.option(
    "--subreddit",
    "subreddit",
    default="AskReddit",
    help="Subreddit to get videos from.",
    type=str,
)
def main(videos: int, subreddit: str):
    """Automatically generate videos from Reddit posts."""
    print(f"Generating {videos} videos from r/{subreddit}.")
yt = YouTube('http://youtube.com/watch?v=2lAe1cqCOXo')

if __name__ == "__main__":
    main()
