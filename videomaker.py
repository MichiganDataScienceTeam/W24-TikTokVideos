import click


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


if __name__ == "__main__":
    main()
