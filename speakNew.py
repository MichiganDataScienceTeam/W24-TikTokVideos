from gtts import gTTS
# put the text here
tts = gTTS('hello')
tts.save('hello.mp3')