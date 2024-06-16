from videomaker.types.audio import Audio


class Comment:
    audio: Audio

    def __init__(self, body: str, author: str):
        self.body = body
        self.author = author

    def __str__(self):
        return f"Author: {self.author}\nComment: {self.body}"

    def word_segments(self):
        return [
            " ".join(self.body.split()[i : i + 3])
            for i in range(0, len(self.body.split()), 3)
        ]

    def ssml(self):
        marked = [
            words + f'<mark name="{i}"/>'
            for i, words in enumerate(self.word_segments())
        ]
        return f"<speak>{' '.join(marked)}</speak>"
