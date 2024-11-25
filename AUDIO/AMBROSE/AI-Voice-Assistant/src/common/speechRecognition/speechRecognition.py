from . import sr


class SpeechRecognizer:

    def __init__(self, name=""):
        self.ASSISTANT = name
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        print("Initilizing")

    def recognize(self, audio):

        try:
            if(str(type(audio)) == "<class 'speech_recognition.audio.AudioData'>"):
                __recognized_text = self.recognizer.recognize_google(audio)
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
            try:
                print("Listning")
                return self.recognizer.listen(source)
            except sr.RequestError as e:
                print(f"Error requesting results; {e}")
