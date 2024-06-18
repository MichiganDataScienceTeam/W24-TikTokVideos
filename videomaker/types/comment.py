from videomaker.types.audio import Audio
import textwrap
import re
from videomaker.config import config


class Comment:
    audio: Audio

    def __init__(self, body: str, author: str):
        self.body = body
        self.author = author

    def __str__(self):
        return f"Author: {self.author}\nComment: {self.body}"

    def word_segments(self):
        return textwrap.fill(
            re.sub(r"([.!?])", r"\1\n", self.body),
            width=config["tts"]["max_words_per_line"],
            replace_whitespace=False,
        ).split("\n")

    def ssml(self):
        marked = [
            words + f'<mark name="{i}"/>'
            for i, words in enumerate(self.word_segments())
        ]
        return f"<speak>{' '.join(marked)}</speak>"
