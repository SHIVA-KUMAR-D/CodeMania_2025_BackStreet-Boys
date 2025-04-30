# STUDENT_AI_ASSITANT
This Python AI voice assistant uses Google's Gemini for intelligent replies. It listens via speech_recognition, speaks with pyttsx3, fetches time, weather (OpenWeatherMap), movie info (OMDb), plays YouTube videos (pywhatkit), sets timers, and maintains conversational memory for dynamic interactions.



# 🎙️ AI Voice Assistant with Gemini

This Python project is a multifunctional AI voice assistant that uses voice recognition and Google Gemini (Generative AI) to respond intelligently to user commands. It handles tasks like answering questions, checking the weather, setting timers, fetching movie info, and more — all through voice.

---

## 🚀 Features

- 🎤 **Voice Recognition** using `speech_recognition`
- 🗣️ **Text-to-Speech** with `pyttsx3`
- 🤖 **Smart Conversations** via Google's Gemini AI
- 🕒 **Time and Date** announcements
- 🌦️ **Weather Reports** using OpenWeatherMap API
- 📺 **YouTube Playback** via `pywhatkit`
- ⏱️ **Timer Setting** using multithreading
- 🎬 **Movie Details** via OMDb API
- 🧠 **Session Memory** for prompt-response history

---

## 📦 Requirements

Install dependencies using pip:

```bash
pip install speechrecognition pyttsx3 google-generativeai requests pywhatkit
```

---

## 🔑 API Keys Required

To run the assistant, you'll need API keys:

- **Google Gemini AI** (replace in `genai.configure(api_key=...)`)
- **OpenWeatherMap API** (replace in `get_weather()`)
- **OMDb API** (replace in `get_movie_details()`)

---

## 🧠 How It Works

1. Listens to your voice input via microphone.
2. Recognizes speech and converts it into text.
3. If it's a general query, sends it to Gemini AI.
4. For specific tasks (e.g., weather, YouTube, movie info), uses appropriate APIs.
5. Replies using text-to-speech.

---

## 🛠️ How to Run

```bash
python your_script_name.py
```

Say commands like:

- "What’s the weather in London?"
- "Set timer for 5 minutes"
- "Play lo-fi music on YouTube"
- "Tell me about the movie Inception"

To stop the assistant, say: **"exit"** or **"quit"**.

---

## ⚠️ Troubleshooting

### Module not found: `google.generativeai`

Run:

```bash
pip install google-generativeai
```

Make sure your API key is valid.

---

## 📝 License

This project is open-source and available under the MIT License.

---

## 🙌 Credits

Built using Python, Google Gemini, and open APIs.
```
