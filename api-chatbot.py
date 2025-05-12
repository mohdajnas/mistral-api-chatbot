import os
import requests
import speech_recognition as sr
from transformers import pipeline
from gtts import gTTS
import tempfile
import playsound

# Set your Mistral API key and endpoint
MISTRAL_API_KEY = "3htzo0NaQBmzvjpgkyOZ3tkB6He0up8E"  # Replace with your actual key
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"  # Confirm endpoint with your Mistral provider

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
        "model": "mistral-medium",  # Or "mistral-small", etc.
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
