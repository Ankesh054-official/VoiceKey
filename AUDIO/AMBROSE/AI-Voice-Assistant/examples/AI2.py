import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os

# from yh import take_command
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voices', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("good morning!")
    if hour >= 12 and hour < 18:
        speak("good afternoon!")
    else:
        speak("good evening!")

    speak("I am jarvis sir. please tell how can i help you")


def take_Command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("recognizing....")
        query = r.recognize_google(audio)
        print(f"user said: {query}\n")
        return query

    except Exception as e:
        print("say that again....")
        return "none"


if __name__ == "__main__":
    wishMe()
    if 1:
        query = take_Command().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wekipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("accodring to wikipedia")
            print(results)
            speak(results)

        elif 'open code' in query:
            speak('opening vs code')
            codePath = "C:\\Users\\ankes\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
