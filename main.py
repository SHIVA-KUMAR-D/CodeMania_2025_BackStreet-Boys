import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import time
import datetime
import webbrowser
import requests
import pywhatkit
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Configure Gemini
genai.configure(api_key="AIzaSyBOHXVPbBX2tHur1mPiP0Yspi-gCr-6y30")  # Replace if needed
model = genai.GenerativeModel('gemini-1.5-flash-latest')

session_memory = {
    "last_response": "",
    "history": []
}

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        text = response.text
        session_memory["last_response"] = text
        session_memory["history"].append({
            "prompt": prompt,
            "response": text
        })
        return text
    except Exception as e:
        return f"Something went wrong with Gemini: {e}"

# Listen to user's voice
recognizer = sr.Recognizer()
def listen():
    with sr.Microphone() as source:
        print("\nListening... ")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, phrase_time_limit=30)
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
            return ""
        except sr.RequestError:
            speak("Network error.")
            return ""
        except sr.WaitTimeoutError:
            speak("Timeout while waiting for speech.")
            return ""

# Get time and date
def get_time_date():
    now = datetime.datetime.now()
    date = now.strftime("%A, %d %B %Y")
    current_time = now.strftime("%I:%M %p")
    return f"Today is {date} and the time is {current_time}."

# Get weather using OpenWeatherMap
def get_weather(city):
    API_KEY = "70536283d539e4abdf43e6b09d211bcf"  # Replace with your OpenWeatherMap key
    try:
        city = city.strip().title()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            print("Weather API error:", data)
            return f"Sorry, I couldn't fetch weather data: {data.get('message', 'unknown error')}."

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        return (f"The current weather in {city} is {weather}, with a temperature of {temp}°C, "
                f"feels like {feels_like}°C, and humidity is {humidity} percent.")
    except Exception as e:
        return f"Failed to get the weather. Error: {e}"

# Timer feature
def set_timer(minutes):
    def countdown():
        time.sleep(minutes * 60)
        speak(f"{minutes} minute timer has ended.")
    threading.Thread(target=countdown).start()

# Get movie details using OMDb API
def get_movie_details(movie_name):
    API_KEY = "d1fdbdf2"  
    try:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if data["Response"] == "False":
            return f"Sorry, I couldn't find details for {movie_name}."

        title = data.get("Title", "N/A")
        year = data.get("Year", "N/A")
        genre = data.get("Genre", "N/A")
        director = data.get("Director", "N/A")
        plot = data.get("Plot", "N/A")
        imdb_rating = data.get("imdbRating", "N/A")

        return (f"{title} ({year}) is a {genre} film directed by {director}. "
                f"IMDb rating: {imdb_rating}/10. Here's a short plot: {plot}")
    except Exception as e:
        return f"Failed to fetch movie details. Error: {e}"

# Main loop
while True:
    try:
        command = listen().lower()
        if command:
            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                break

            elif "repeat last response" in command:
                last = session_memory.get("last_response", "")
                if last:
                    speak("Here's the last response.")
                    speak(last)
                else:
                    speak("No previous response to repeat.")

            elif "show history" in command:
                if session_memory["history"]:
                    for idx, item in enumerate(session_memory["history"], start=1):
                        print(f"{idx}. Prompt: {item['prompt']}\n   Response: {item['response']}\n")
                    speak("Displayed conversation history.")
                else:
                    speak("No history available yet.")

            elif "open" in command:
                query = command.replace("open", "").strip()
                speak(f"Opening {query} on Google.")
                webbrowser.open(f"https://www.google.com/search?q={query}")

            elif "time" in command or "date" in command:
                result = get_time_date()
                speak(result)

            elif "weather" in command:
                speak("Which city's weather would you like to know?")
                city = listen()
                if city:
                    print("City received:", city)
                    weather_info = get_weather(city)
                    speak(weather_info)
                else:
                    speak("I couldn't get the city name.")

            elif "play" in command:
                video = command.replace("play", "").strip()
                speak(f"Playing {video} on YouTube.")
                pywhatkit.playonyt(video)

            elif "set timer" in command:
                speak("For how many minutes?")
                response = listen()
                try:
                    minutes = int(response)
                    set_timer(minutes)
                    speak(f"Timer set for {minutes} minutes.")
                except:
                    speak("Sorry, I couldn't understand the duration.")

            elif "movie" in command or "film" in command:
                speak("Which movie would you like details about?")
                movie = listen()
                if movie:
                    details = get_movie_details(movie)
                    speak(details)
                else:
                    speak("I didn't catch the movie name.")

            else:
                reply = ask_gemini(command)
                speak(reply)
        else:
            speak("Please say something...")

        time.sleep(1)

    except KeyboardInterrupt:
        print("\nVoice assistant stopped manually.")
        break
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred. Restarting listening.")
        time.sleep(1)