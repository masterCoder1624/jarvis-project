import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import subprocess
import pyautogui


recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "<Your Key Here>"


def shutdown_pc():
    os.system("shutdown /s /f /t 0") 

def restart_pc():
    os.system("shutdown /r /f /t 0")  
    
def log_off():
    os.system("shutdown /l") 



def adjust_volume(command):
    if "volume up" in command.lower():
        pyautogui.press('volumeup')
    elif "volume down" in command.lower():
        pyautogui.press('volumedown')
    elif "mute" in command.lower():
        pyautogui.press('volumemute')
    else:
        print("Unknown volume command.")



def open_application(app_name):
    if 'notepad' in app_name.lower():
        os.system("onenote.exe")
    elif 'calculator' in app_name.lower():
        os.system("calc.exe")
    elif 'browser' in app_name.lower():
        os.system("microsoft edge")  # or use the path for any other browser
    else:
        print(f"Sorry, I don't know how to open {app_name}")



def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="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",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://whatsapp.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 





if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("sun rha hu bol")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("haa bol kya hua ")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
