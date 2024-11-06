from . import speak

class Speak:

    def __init__(self):
        self.speaker = speak.init()

    def say(self, text):
        print("say: ", text)
        self.speaker.say(text)
        self.speaker.runAndWait()