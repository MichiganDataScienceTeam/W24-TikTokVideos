import pyttsx3

engine = pyttsx3.init()
engine.save_to_file("I will speak this text", "ttstest.mp3")
engine.runAndWait()