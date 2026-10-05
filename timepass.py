import pyttsx3
import speech_recognition as sr
import webbrowser
import musicLibrary
import requests
from google import genai
from gtts import gTTS
import pygame ,os
from dotenv import load_dotenv

recognizer = sr.Recognizer()

newsapi = "1339c40a98cb4397ab46071325df18de" 

def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def speak(text):
    tts = gTTS(text)
    tts.save('tempo.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('tempo.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove('tempo.mp3')

load_dotenv()
def aiProcess(command):
    client = genai.Client(
      api_key=os.environ["GEMINI_API_KEY"])

    interaction = client.interactions.create(
      agent="antigravity-preview-09-2026",
      input=command,
      environment="remote"
)
    print(f"Interaction ID: {interaction.id}")
    print(f"Environment ID: {interaction.environment_id}")
    print(f"Output: {interaction.output_text}")
    return interaction.output_text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open('https://google.com')

    elif "open skyfall" in c.lower():
        webbrowser.open("https://www.youtube.com/shorts/EzYRorLpn0U")

    elif "open dollar" in c.lower():
        webbrowser.open("https://www.youtube.com/shorts/kDhFYO_5sa8")

    elif c.lower().startswith('play'):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        try:
            r = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={"country": "in", "apiKey": newsapi},
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