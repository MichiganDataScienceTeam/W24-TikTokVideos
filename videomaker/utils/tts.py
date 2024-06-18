import google.cloud.texttospeech_v1beta1 as tts
import os
import json
from moviepy.editor import AudioFileClip
from videomaker.types.audio import Audio
from videomaker.config import config
from videomaker.utils.console import print_step, print_substep


def text_to_speach(ssml: str, filename: str, speaking_rate=1.25, pitch=-8) -> Audio:
    print_step("Generating audio...")
    if os.path.exists(filename) and os.path.exists(filename + ".json"):
        print_substep("Using cached audio...")
        with open(filename + ".json") as file:
            timestamps = json.load(file)
        return Audio(
            file=filename, timestamps=timestamps, audio_object=AudioFileClip(filename)
        )
    language_code = "-".join(config["tts"]["google_voice_type"].split("-")[:2])
    text_input = tts.SynthesisInput(ssml=ssml)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=config["tts"]["google_voice_type"]
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    client = tts.TextToSpeechClient()

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
