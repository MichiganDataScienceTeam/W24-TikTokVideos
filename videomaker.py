import praw
import os
from videomaker.utils.sanitize import sanitize_text
from praw.models import MoreComments
from videomaker.utils.tts import text_to_speach
from videomaker.utils.screenshot import screenshot
from videomaker.types.audio import Audio
from videomaker.types.comment import Comment
from videomaker.types.video import Video
from moviepy.editor import *
from videomaker.config import config, creds
from videomaker.utils.console import *
import json

credentials = "client_secrets.json"
SAMPLE = 1


def main():
    """Automatically generate videos from Reddit posts."""

    reddit = praw.Reddit(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        user_agent=creds["user_agent"],
        redirect_uri=creds["redirect_uri"],
        refresh_token=creds["refresh_token"],
    )
    submissions = reddit.subreddit(config["reddit"]["subreddit"]).top(
        limit=SAMPLE, time_filter=config["reddit"]["time_filter"]
    )

    while True:
        for index, submission in enumerate(submissions):
            print_markdown(submission.title)
            video = Video(
                submission.title,
                submission.url,
                submission.author.name,
                submission.fullname,
            )

            if not yes_no_prompt("Use post in video?"):
                break

            screenshot(video.url, False, video.fullname + ".png")
            video.screen_shot = "screenshot/" + video.fullname + ".png"

            video.intro_audio = text_to_speach(
                "<speak>" + video.title + "</speak>",
                "audio/" + video.author + ".wav",
            )

            for comment in submission.comments:
                if isinstance(comment, MoreComments):
                    continue
                cleaned = sanitize_text(comment.body)
                print_markdown(f"### Comment\n {cleaned}")

                if yes_no_prompt("Include in video?"):
                    comment = Comment(
                        cleaned,
                        comment.author,
                    )
                    comment.audio = text_to_speach(
                        comment.ssml(),
                        "audio/" + video.fullname + comment.author.name + ".wav",
                    )
                    video.comments.append(comment)
                print_step(f"Video length: {video.video_length()}s")

                if video.video_length() > config["video"]["target_length"]:
                    print_step("Target length reached.")
                    break
                if yes_no_prompt("Done with video?"):
                    break

        video.edit_video()

        submissions = reddit.subreddit(config["reddit"]["subreddit"]).top(
            limit=SAMPLE,
            time_filter=config["reddit"]["time_filter"],
            params={"after": video.fullname},
        )


if __name__ == "__main__":
    # main()
    video = Video(
        "What crazy stuff happened in the year 2001 that got overshadowed by 9/11?",
        "url",
        "author",
        "bet",
    )
    with open("audio/NightNo423.wav.json") as file:
        timestamps = json.load(file)

    video.intro_audio = Audio(
        "audio/NightNo423.wav", timestamps, AudioFileClip("audio/NightNo423.wav")
    )
    video.screen_shot = "screenshot/t3_1dcy3pi.png"

    video.comments.append(
        Comment(
            "American Airlines Flight 587 An Airbus A-300 crashed in Queens, NY two months after 9/11. It was the second-deadliest aviation accident in US history, and not well remembered.",
            "IsNoHeroes94",
        )
    )

    video.comments[0].audio = Audio(
        "audio/t3_1dcy3piCheesy_Discharge.wav",
        json.load(open("audio/t3_1dcy3piCheesy_Discharge.wav.json")),
        AudioFileClip("audio/t3_1dcy3piCheesy_Discharge.wav"),
    )

    # video.comments.append(video.comments[0])

    video.edit_video()
