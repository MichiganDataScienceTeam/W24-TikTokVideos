import google.cloud.texttospeech_v1beta1 as tts
import os
import json
from moviepy.editor import AudioFileClip
from videomaker.types.audio import Audio

GOOGLE_VOICE_TYPE = "en-US-Neural2-D"


def text_to_speach(ssml: str, filename: str, speaking_rate=1.25, pitch=-8) -> Audio:
    if os.path.exists(filename) and os.path.exists(filename + ".json"):
        print("Cached audio")
        with open(filename + ".json") as file:
            timestamps = json.load(file)
        return Audio(
            file=filename, timestamps=timestamps, audio_object=AudioFileClip(filename)
        )
    language_code = "-".join(GOOGLE_VOICE_TYPE.split("-")[:2])
    text_input = tts.SynthesisInput(ssml=ssml)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=GOOGLE_VOICE_TYPE
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    client = tts.TextToSpeechClient()
    # print(filename)
    # print(ssml)
    # print()
    request = tts.SynthesizeSpeechRequest(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
        enable_time_pointing=[tts.SynthesizeSpeechRequest.TimepointType.SSML_MARK],
    )

    response = client.synthesize_speech(request=request)

    output = Audio
    output.timestamps = [
        dict(sec=t.time_seconds, name=t.mark_name) for t in response.timepoints
    ]

    with open(filename, "wb") as out:
        out.write(response.audio_content)
    with open(filename + ".json", "w") as out:
        json.dump(output.timestamps, out)
    output.file = filename
    output.audio_object = AudioFileClip(filename)
    return output
