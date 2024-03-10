import pyttsx3

def read():
    engine = pyttsx3.init()
    engine.save_to_file('this is a test. I\'m talking' , 'test.mp3')
    # engine.say("I will speak this text")
    engine.runAndWait()
    



read()