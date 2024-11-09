from . import sr


class SpeechRecognizer:

    def __init__(self, name="ambrose"):
        self.ASSISTANT = name
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.audio = None

        print("Initilizing")

    def recognize(self):

        try:
            if(str(type(self.audio)) == "<class 'speech_recognition.audio.AudioData'>"):

                __recognized_text = self.recognizer.recognize_google(self.audio)
                self.audio = None
                print(f"user said: {__recognized_text}")
                return __recognized_text
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.WaitTimeoutError:
            print("Timeout occurred while waiting for microphone input.")
        except Exception as e:
            print("An unexpected error occurred:", e)

        return None

    def get_audio(self):

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

            print("Listning")
            while True:
                try:
                    self.audio = self.recognizer.listen(source)
                except sr.RequestError as e:
                    self.audio = None
                    print(f"Error requesting results; {e}")
