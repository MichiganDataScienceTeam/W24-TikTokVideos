import json
import praw
import os
import re
from unidecode import unidecode
from praw.models import MoreComments
import pathlib
import html
from videomaker.utils.tts import text_to_speach
from videomaker.utils.screenshot import screenshot
from videomaker.types.audio import Audio
from videomaker.types.comment import Comment
from videomaker.types.video import Video
from moviepy.editor import *
import random
from typing import List
from copy import deepcopy

credentials = "client_secrets.json"
SAMPLE = 1
TIME_FILTERS = ["all", "day", "hour", "month", "week", "year"]


with open(credentials) as f:
    creds = json.load(f)


def main():
    """Automatically generate videos from Reddit posts."""
    # subreddit = input("Enter the subreddit: ")
    # time_filter = int(
    #     input(
    #         "Enter the time filter:\n 1. all\n 2. day\n 3. hour\n 4. month\n 5. week\n 6. year\n"
    #     )
    # )

    subreddit = "AskReddit"
    time_filter = 5

    reddit = praw.Reddit(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        user_agent=creds["user_agent"],
        redirect_uri=creds["redirect_uri"],
        refresh_token=creds["refresh_token"],
    )
    submissions = reddit.subreddit(subreddit).top(
        limit=SAMPLE, time_filter=TIME_FILTERS[time_filter - 1]
    )

    while True:
        for index, submission in enumerate(submissions):
            print(f"Post {index + 1}: {submission.title} {submission.fullname}")
            video = Video(
                submission.title,
                submission.url,
                submission.author.name,
                submission.fullname,
            )
            if input("Use post in video? (y/n): ") == "n":
                break

            screenshot(video.url, False, video.fullname + ".png")

            if os.path.exists("screenshot/" + video.fullname + ".png"):
                video.screen_shot = "screenshot/" + video.fullname + ".png"

            video.intro_audio = text_to_speach(
                "<speak>" + video.title + "</speak>",
                "audio/" + video.author + ".wav",
            )

            for comment in submission.comments:
                if isinstance(comment, MoreComments):
                    continue
                print(f"Comment: {comment.body}")
                include = input("Include in video? (y/n): ")
                if include == "y":
                    comment = Comment(
                        comment.body,
                        comment.author,
                    )
                    comment.audio = text_to_speach(
                        comment.ssml(),
                        "audio/" + video.fullname + comment.author.name + ".wav",
                    )
                    video.comments.append(comment)
                print(f"Video length: {video.video_length()}s")
                if input("Continue? (y/n): ") == "n":
                    video.edit_video()
                    break

        submissions = reddit.subreddit(subreddit).top(
            limit=SAMPLE,
            time_filter=TIME_FILTERS[time_filter - 1],
            params={"after": video.fullname},
        )


if __name__ == "__main__":
    # main()
    video = Video(
        "What's the grossest thing your partner does but you accept?",
        "url",
        "author",
        "t3_1bzisls",
    )
    with open("audio/egguchom.wav.json") as file:
        timestamps = json.load(file)

    video.intro_audio = Audio(
        "audio/egguchom.wav", timestamps, AudioFileClip("audio/egguchom.wav")
    )
    video.screen_shot = "screenshot/screenshot.png"

    video.comments.append(
        Comment(
            "Enterprise Rent-A-Car buys their cars straight from the manufacturers at a price lower than dealerships get. After they rent them for a year, they sell them to the public at a price higher than they originally paid.",
            "IsNoHeroes94",
        )
    )

    video.comments[0].audio = Audio(
        "audio/1bfblldw0rx4me.wav",
        json.load(open("audio/1bfblldw0rx4me.wav.json")),
        AudioFileClip("audio/1bfblldw0rx4me.wav"),
    )

    video.comments.append(video.comments[0])

    video.edit_video()
