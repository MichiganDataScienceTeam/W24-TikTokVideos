from typing import List
from random import shuffle
from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
import os
from videomaker.types.audio import Audio
from videomaker.types.comment import Comment
import random
from videomaker.config import config
from videomaker.utils.console import *


class Video:
    comments: List[Comment] = []
    intro_audio: Audio
    background_video: VideoFileClip = None
    screen_shot: str

    def __init__(self, title, url, author, fullname):
        self.title = title
        self.url = url
        self.author = author
        self.fullname = fullname

    def __str__(self):
        return f"Title: {self.title}\nURL: {self.url}\nAuthor: {self.author}"

    def video_length(self):
        return (
            sum(obj.audio.audio_object.duration for obj in self.comments)
            + config["video"]["clip_gap"] * (len(self.comments) + 1)
            + self.intro_audio.audio_object.duration
        )

    def get_background_video(self):
        if self.background_video is None:
            if "background_video" in config["video"] and os.path.isfile(
                config["video"]["background_video"]
            ):
                try:
                    self.background_video = VideoFileClip(
                        config["video"]["background_video"]
                    )
                except Exception as e:
                    pass
                file = config["video"]["background_video"]
                print_step(f"Video file: {file}")
            else:
                files = os.listdir("backgrounds")
                shuffle(files)
                found = False
                for file in files:
                    if not file.startswith("resize-"):
                        continue
                    file_path = os.path.join("backgrounds", file)
                    if os.path.isfile(file_path):
                        try:
                            self.background_video = VideoFileClip(file_path)
                        except Exception as e:
                            continue
                    if self.background_video.duration > self.video_length():
                        found = True
                        break
                if not found:
                    raise FileExistsError  # probably not right one to raise
                if self.background_video.duration < self.video_length():
                    print_error("Video file shorter than audio")
                    raise ValueError
                print_step(f"Video file: {file}")

    def edit_video(self):
        print_step("Editing video...")

        def animate_in(t):
            return min(1, 200 * (t - 0.075) ** 3 + 1)

        video_length = self.video_length()
        self.get_background_video()

        if (
            "start_time" in config["video"]
            and video_length + config["video"]["start_time"]
            < self.background_video.duration
        ):
            start_time = config["video"]["start_time"]
        else:
            start_time = (
                float(
                    random.randint(
                        0, int((self.background_video.duration - video_length) * 100)
                    )
                )
                / 100
            )

        intro_segment = self.background_video.subclip(
            start_time,
            start_time
            + self.intro_audio.audio_object.duration
            + config["video"]["clip_gap"],
        ).set_audio(self.intro_audio.audio_object)

        image: ImageClip = (
            ImageClip(self.screen_shot)
            .set_start(0)
            .set_duration(self.intro_audio.audio_object.duration)
            .set_pos(("center", "center"))
        )

        image = image.resize((700, image.h / image.w * 700)).resize(animate_in)
        intro = CompositeVideoClip([intro_segment, image])

        segments = [intro]
        offset = intro.duration

        for comment in self.comments:
            clip_start_time = start_time + offset
            timestamps = sorted([item["sec"] for item in comment.audio.timestamps])
            word_segments = comment.word_segments()
            prev_timestamp = 0

            subtitles = []
            for index, timestamp in enumerate(timestamps):

                caption_text_stroke = (
                    TextClip(
                        word_segments[index],
                        stroke_width=config["video"]["stroke_width"],
                        stroke_color=config["video"]["stroke_color"],
                        fontsize=config["video"]["font_size"],
                        color="white",
                        font=config["video"]["font_path"],
                        method="label",
                        size=self.background_video.size,
                    )
                    .set_position("center")
                    .set_start(prev_timestamp)
                    .set_end(timestamp)
                    .resize(animate_in)
                )

                caption_text = (
                    TextClip(
                        word_segments[index],
                        fontsize=config["video"]["font_size"],
                        color=config["video"]["text_color"],
                        font=config["video"]["font_path"],
                        method="label",
                        size=self.background_video.size,
                    )
                    .set_position("center")
                    .set_start(prev_timestamp)
                    .set_end(timestamp)
                    .resize(animate_in)
                )

                subtitles.append(caption_text_stroke)
                subtitles.append(caption_text)

                prev_timestamp = timestamp

            segment = CompositeVideoClip(
                [
                    self.background_video.subclip(
                        clip_start_time,
                        clip_start_time
                        + comment.audio.audio_object.duration
                        + config["video"]["clip_gap"],
                    ),
                    *subtitles,
                ]
            ).set_audio(comment.audio.audio_object)

            segments.append(segment)
            offset += comment.audio.audio_object.duration + config["video"]["clip_gap"]

        final_video = concatenate_videoclips(segments)

        if abs(video_length - final_video.duration) < 1:
            final_video.write_videofile(self.fullname + ".mp4", codec="libx264")
        else:
            print_error("error in video creation")
