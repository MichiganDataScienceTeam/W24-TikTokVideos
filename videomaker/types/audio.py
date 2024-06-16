from moviepy.editor import AudioFileClip


class Audio:
    file: str
    timestamps: dict
    audio_object: AudioFileClip

    def __init__(self, file: str, timestamps: dict, audio_object: AudioFileClip):
        self.file = file
        self.timestamps = timestamps
        self.audio_object = audio_object
