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
                
                _recognized_text = self.recognizer.recognize_google(self.audio)
                self.audio = None
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
            self.recognizer.adjust_for_ambient_noise(source)
            
            print("Listning")
            while True:
                try:
                    self.audio = self.recognizer.listen(source)
                except sr.RequestError as e:
                    print("Error requesting results; {0}".format(e))

