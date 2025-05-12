
# 🎙️ Voice Chatbot with Mistral LLM, Sentiment Analysis & TTS

This Python project enables real-time voice interaction using the [Mistral LLM API](https://docs.mistral.ai), with built-in sentiment analysis via Hugging Face and voice response using gTTS.

---

## 🧠 Features

- 🎤 Voice input via microphone using `SpeechRecognition`
- 🧪 Sentiment analysis using Hugging Face Transformers
- 🤖 LLM response from Mistral API (`mistral-medium`, etc.)
- 🔊 Voice output via `gTTS` + `playsound`
- 🗨️ Say "exit" to end the conversation

---

## 📦 Requirements

Install required packages:

```bash
pip install speechrecognition transformers gtts playsound requests
````

You also need:

* A working microphone
* Internet connection (for STT, gTTS, and Mistral API)

---

## 🔑 Setup

1. **Get your Mistral API key:** [https://console.mistral.ai](https://console.mistral.ai)
2. Replace this line in the code:

```python
MISTRAL_API_KEY = "your-mistral-api-key"
```

Optionally, confirm or update the MISTRAL API URL:

```python
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
```

---

## ▶️ How to Run

```bash
python mistral_voice_chatbot.py
```

Speak your message, wait for a sentiment response and LLM reply, and hear the bot talk back.

Say **"exit"** to stop the program.

---

## 💻 Full Source Code

```python
import os
import requests
import speech_recognition as sr
from transformers import pipeline
from gtts import gTTS
import tempfile
import playsound

# Set your Mistral API key and endpoint
MISTRAL_API_KEY = "your-mistral-api-key"  # Replace with your actual key
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Initialize sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except:
            print("Speech Recognition failed.")
            return ""

def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    label = result['label']
    score = result['score']
    print(f"Sentiment: {label} ({score:.2f})")
    return f"Sentiment: {label} ({score:.2f})"

def generate_llm_response(prompt):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-medium",  # Or "mistral-small"
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(MISTRAL_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()

def text_to_speech(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
        tts.save(fp.name)
        playsound.playsound(fp.name)

# === MAIN INTERACTION ===
while True:
    user_input = speech_to_text()

    if user_input.lower() == "exit":
        print("Exiting the program.")
        break

    if user_input:
        sentiment = analyze_sentiment(user_input)
        print(sentiment)

        llm_response = generate_llm_response(user_input)
        print("LLM says:", llm_response)

        text_to_speech(llm_response)
```

---

## 📁 File Structure

```
mistral_voice_chatbot.py  # Main script
README.md                 # Documentation
```

---

## 📝 Notes

* gTTS requires internet access (uses Google Translate TTS)
* Hugging Face will download the sentiment model on first run
* This is a console-based app with no GUI

---

## 📜 License

MIT License

```

Let me know if you'd like to add offline STT or use a different TTS engine.
```
