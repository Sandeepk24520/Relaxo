import pyttsx3
import speech_recognition as sr
import webbrowser
import musicLibrary
import requests
from google import genai
from gtts import gTTS
import pygame ,os
from dotenv import load_dotenv
from google.genai import types

recognizer = sr.Recognizer()

newsapi = "1339c40a98cb4397ab94c071325df18de" 

def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('hello.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('hello.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove('hello.mp3')

load_dotenv()
def aiProcess(command):
    client = genai.Client(
      api_key="Your_APIkey_here")

    response = client.models.generate_content(
      model = "gemini-3.5-flash-lite",
      contents = command,
      config=types.GenerateContentConfig(
            system_instruction="You are Relaxo,a friendly assistant. Answer in one or two short sentences. No markdown.",
            max_output_tokens=100,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)
    )
    return (response.text or "").strip()


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open('https://google.com')

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        
    elif "play backbone" in c.lower():
        webbrowser.open("https://www.youtube.com/shorts/EzYRorLpn0U")

    elif c.lower().startswith('play'):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        try:
            r = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={"country": "us", "apiKey": newsapi},
                timeout=10,
            )
            r.raise_for_status()
            articles = r.json().get("articles", [])
            if not articles:
                speak("I couldn't find any news right now.")
            else:
                for article in articles[:5]:
                    print(article["title"])
                    speak(article["title"])
        except Exception as e:
            print("News error:", e)
            speak("Sorry, I couldn't fetch the news.")
    # Let Google.Genai handle the request
    else:
        output = aiProcess(c)
        print(f"Output:{output}")
        if output:
            speak(output)


if __name__ == "__main__":
    speak("Initializing Relaxo...")

    while True:
        r = sr.Recognizer()
        print("......")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)

            word = r.recognize_google(audio)

            if word.lower() == "relaxo":
                continue
            speak('ya')

            with sr.Microphone() as source:
                print('Relaxo Active')
                audio = r.listen(source)
                command = r.recognize_google(audio)

            processCommand(command)

        except Exception as e:
            print("Error:", e)