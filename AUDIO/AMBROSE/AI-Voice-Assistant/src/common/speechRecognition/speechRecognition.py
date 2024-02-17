from . import sr

class SpeechRecognizer:
    

    def __init__(self, name="ambrose"):
        self.ASSISTANT = name
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()


    def recognize(self):

        try:
            _recognized_text = self.recognizer.recognize_google(self.audio)
            print(f"user said: {_recognized_text}")
            return _recognized_text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except sr.WaitTimeoutError:
            print("Timeout occurred while waiting for microphone input.")
        except Exception as e:
            print("An unexpected error occurred:", e)

        return None


    def get_audio(self):

        with self.microphone as source:
            print("Listen ...")
            self.recognizer.adjust_for_ambient_noise(source)
            self.audio = self.recognizer.listen(source)

