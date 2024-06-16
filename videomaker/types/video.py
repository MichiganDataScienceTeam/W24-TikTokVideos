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

VIDEO_GAP = 1
font_path = os.path.join(os.getcwd(), "fonts", "Roboto", "Roboto-Bold.ttf")


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
            + VIDEO_GAP * (len(self.comments) + 1)
            + self.intro_audio.audio_object.duration
        )

    def get_background_video(self):
        if self.background_video is None:
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
                print("Video file shorter than audio")
                raise ValueError
            print("Video file:", file)

    def edit_video(self):

        video_length = self.video_length()
        self.get_background_video()

        start_time = (
            float(
                random.randint(
                    0, int((self.background_video.duration - video_length) * 100)
                )
            )
            / 100
        )

        intro_segment = self.background_video.subclip(
            start_time, start_time + self.intro_audio.audio_object.duration + VIDEO_GAP
        ).set_audio(self.intro_audio.audio_object)

        image: ImageClip = (
            ImageClip(self.screen_shot)
            .set_start(0)
            .set_duration(self.intro_audio.audio_object.duration)
            .set_pos(("center", "center"))
        )

        image = image.resize((700, image.h / image.w * 700))
        intro = CompositeVideoClip([intro_segment, image])

        segments = [intro]
        offset = intro.duration

        for comment in self.comments:
            clip_start_time = start_time + offset
            timestamps = sorted([item["sec"] for item in comment.audio.timestamps])
            word_segments = comment.word_segments()
            prev_timestamp = 0
            subtitle_clips = []
            # print("Comment", comment.body)
            # print(len(timestamps), len(word_segments))

            for index, timestamp in enumerate(timestamps):
                # print(
                #     timestamp,
                #     word_segments[index],
                # )
                caption_text_stroke = (
                    TextClip(
                        word_segments[index],
                        stroke_width=20,
                        stroke_color="black",
                        fontsize=74,
                        color="white",
                        font=font_path,
                        size=self.background_video.size,
                        method="caption",
                    )
                    .set_duration(timestamp - prev_timestamp)
                    .set_position("center")
                )

                caption_text = (
                    TextClip(
                        word_segments[index],
                        fontsize=74,
                        color="white",
                        font=font_path,
                        size=self.background_video.size,
                        method="caption",
                    )
                    .set_duration(timestamp - prev_timestamp)
                    .set_position("center")
                )

                subtitle_clips.append(
                    CompositeVideoClip(
                        [caption_text_stroke, caption_text],
                    )
                )
                prev_timestamp = timestamp

            subtitles = concatenate_videoclips(subtitle_clips)

            segment = CompositeVideoClip(
                [
                    self.background_video.subclip(
                        clip_start_time,
                        clip_start_time
                        + comment.audio.audio_object.duration
                        + VIDEO_GAP,
                    ),
                    subtitles,
                ]
            ).set_audio(comment.audio.audio_object)

            # subtitles.set_fps(24).write_videofile("test.mp4", codec="libx264")
            # break
            segments.append(segment)
            offset += comment.audio.audio_object.duration + VIDEO_GAP

        final_video = concatenate_videoclips(segments)
        # print(final_self.duration, video_length, abs(video_length - final_video.duration))
        if abs(video_length - final_video.duration) < 1:
            final_video.write_videofile(self.fullname + ".mp4", codec="libx264")
            pass
        else:
            print("error in video creation")
