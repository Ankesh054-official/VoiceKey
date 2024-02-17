from . import Recognizer

def start():
    SR = Recognizer()
    SR.get_audio()
    SR.recognize()
