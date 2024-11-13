from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import shutil
from PIL import Image
from io import BytesIO



def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
            return query
        except Exception as e:
            return "Some error occurred"


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
        say(f"Here is a picture of {test_category}")
    else:
        say("I couldn't generate an image. Please try again.")
        print("Error:", response.status_code, response.text)


def tellWeather(city):
    api_key = 'YOUR_API_KEY'  # Replace with your WeatherAPI key
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temp_c']
        condition = data['current']['condition']['text']

        weather_report = f"The current weather in {city} is {temperature}°C with {condition}."
        say(weather_report)
    else:
        say("Sorry, I couldn't fetch the weather.")


if __name__ == '__main__':
    say("Hello, I am Smithi AI")
    while True:
        print("listening...")
        query = takeCommand()
        if "open youtube" in query.lower():
            say("Opening YouTube, sir")
            webbrowser.open("https://youtube.com")

        elif "hello" in query.lower():
            say("Hello sir, how can I help you?")

        elif "hay" in query.lower():
            say("hay sir, how can I help you?")

        elif "love" in query.lower():
            say("i love you 2 sir")

        elif "Smriti" in query.lower():
            say("Yes sir, say")

        elif "open lead code" in query.lower():
            say("Opening LeetCode, sir")
            webbrowser.open("https://leetcode.com/")

        elif "open google" in query.lower():
            say("Opening Google, sir")
            webbrowser.open("https://google.com")

        elif "sleep" in query.lower():
            say("Ok sir, I am going to sleep. Have a good day.")
            break

        elif "date" in query.lower():
            current_date = datetime.now().strftime("%A, %d %B %Y")
            say(f"Today is {current_date}")

        elif "open chat gpt" in query.lower():
            say("Opening ChatGPT, sir")
            webbrowser.open("https://chat.openai.com")

        elif "search for" in query.lower():
            search_term = query.split("search for", 1)[1].strip()
            say(f"Searching for {search_term}")
            webbrowser.open(f"https://www.google.com/search?q={search_term}")

        elif "generate a picture of" in query.lower():
            prompt = query.replace("generate a picture of", "").strip()
            say(f"Generating a picture of {prompt}")
            generateImage(prompt)

        elif  "weather in" in query:
          city = query.split("weather in", 1)[1].strip()
          say(f"Fetching the weather for {city}. Please wait.")
          tellWeather(city)
           
