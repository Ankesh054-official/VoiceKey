from . import Recognizer
from . import Speak

from . import thread


class Assistant:

    def __init__(self):
        super().__init__()
        self._SR = Recognizer()
        self._speaker = Speak()

        self._text_to_speak = None

    def say(self):
        while True:
            if(self._text_to_speak != None):
                self._speaker.say(self._text_to_speak)
                self._text_to_speak = None

    def listen(self):
        self._SR.get_audio()
        
        
    def text_initlizer(self):
        print("Recognizing...")
        while True:
            self._text_to_speak = self._SR.recognize()

    def recognize_audio(self):
        
        self.text_initlizer()
        

    

def start():
    ambrose = Assistant()
    
    listen = thread.Thread(target=ambrose.listen)
    
    text_init = thread.Thread(target=ambrose.recognize_audio)
    
    speaker = thread.Thread(target=ambrose.say)
    
    listen.start()
    text_init.start()
    speaker.start()

    listen.join()
    text_init.join()
    speaker.join()