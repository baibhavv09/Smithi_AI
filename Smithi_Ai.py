# Import necessary libraries
import pyttsx3  # For text-to-speech functionality
import speech_recognition as sr  # For speech recognition
import datetime as dt  # For working with dates and times
import wikipedia  # For fetching summaries from Wikipedia
import pyjokes  # For retrieving jokes
import webbrowser as wb  # For opening websites in the browser
import os  # For interacting with the operating system
import random  # For random selection
import pyautogui  # For GUI automation (e.g., taking screenshots)
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML and web scraping
from PIL import Image #for image generation
from io import BytesIO


#Initialization: Configures the speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    """Tells the current time."""
    current_time = dt.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date():
    """Tells the current date."""
    now = dt.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")


def wishme():
    """Greets the user based on the time of day."""
    speak("Welcome back, sir!")
    print("Welcome back, sir!")

    hour = dt.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
        print("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
        print("Good afternoon!")
    else:
        speak("Good evening!")
        print("Good evening!")

    speak("Smithy at your service. Please tell me how may I assist you.")
    print("smithy at your service. Please tell me how may I assist you.")

def generateImage(category):
    # Temporarily hardcode to test a known valid category
    test_category = category # Replace with an actual known category from the documentation
    api_url = f'https://api.api-ninjas.com/v1/randomimage?category={test_category}'
    headers = {
        'X-Api-Key': 'uaIez1toU6a8boIoGQc7nA==doIWxj8RYZEZqkXW',
        'Accept': 'image/jpg'
    }
    response = requests.get(api_url, headers=headers, stream=True)
    if response.status_code == requests.codes.ok:
        image = Image.open(BytesIO(response.content))
        image.show()  # Opens in the default image viewer
        speak(f"Here is a picture of {test_category}")
    else:
        speak("I couldn't generate an image. Please try again.")
        print("Error:", response.status_code, response.text)

def play_music(song_name=None):
    """
    Plays music from the user's Music directory.
    If a song name is specified, it searches for that song.
    If no song name is provided, it plays a random song.
    """
    # Define the music directory
    music_dir =  r"C:\Users\varsh\OneDrive\Desktop\python & ML\smithy\songs"

    # Check if the directory exists
    if not os.path.exists(music_dir):
        speak("Music directory not found.")
        print("Music directory not found.")
        return

    # Get the list of songs in the directory
    songs = os.listdir(music_dir)

    # If the directory is empty
    if not songs:
        speak("No songs found in the Music directory.")
        print("No songs found in the Music directory.")
        return

    # If a song name is provided, search for it
    if song_name:
        filtered_songs = [song for song in songs if song_name.lower() in song.lower()]
        if filtered_songs:
            song_to_play = random.choice(filtered_songs)
        else:
            speak("No matching song found. Playing a random song instead.")
            print("No matching song found. Playing a random song instead.")
            song_to_play = random.choice(songs)
    else:
        # If no song name is provided, play a random song
        song_to_play = random.choice(songs)

    # Construct the full path and play the song
    song_path = os.path.join(music_dir, song_to_play)
    os.startfile(song_path)
    speak(f"Playing {song_to_play}.")
    print(f"Playing: {song_to_play}")


def screenshot() -> None:
    """Takes a screenshot and saves it."""
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(img_path)
    speak(f"Screenshot saved as {img_path}.")
    print(f"Screenshot saved as {img_path}.")


def takecommand() -> str:
    """Takes microphone input from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)  # Listen with a timeout
        except sr.WaitTimeoutError:

            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Speech recognition service is unavailable.")
        return None
    except Exception as e:

        print(f"Error: {e}")
        return None




def search_wikipedia(query):
    """Searches Wikipedia and returns a summary."""
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")

def temp(query):
    url=f"https://www.google.com/search?q={query}"
    r=requests.get(url)
    data=BeautifulSoup(r.text,"html.parser")
    temp=data.find("div",class_="BNeawe").text
    speak(f"current temperature is {temp}")


if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand()
        if not query:
            continue

        if "time" in query:
            time()

        elif "date" in query:
            date()

        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)

        elif "play music" in query:
            play_music()

        elif "open youtube" in query:
            wb.open("youtube.com")

        elif "open google" in query:
            wb.open("google.com")

        elif "screenshot" in query:
            screenshot()
            speak("I've taken screenshot, please check it")

        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif "shutdown" in query:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break

        elif "restart" in query:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break

        elif "offline" in query or "exit" in query:
            speak("Going offline. Have a good day!")
            break
        elif "temperature" in query:
            temp(query)

        elif "generate a picture of" in query:
            prompt = query.replace("generate a picture of", "").strip()
            speak(f"Generating a picture of {prompt}")
            generateImage(prompt)
