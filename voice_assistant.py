#!/usr/bin/env python3
"""
Personal Voice Assistant - Workshop Project
A beginner-friendly voice assistant that can:
- Answer simple questions
- Play music
- Tell time and date
- Respond to basic voice commands

Required libraries: speech_recognition, pyttsx3, pygame, requests
"""

import speech_recognition as sr
import pyttsx3
import datetime
import os
import random
import pygame
import requests
import json
from pathlib import Path

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with speech recognition and text-to-speech"""
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.setup_voice()
        
        # Initialize pygame for music playback
        pygame.mixer.init()
        
        # Music folder path (create if doesn't exist)
        self.music_folder = Path("music")
        self.music_folder.mkdir(exist_ok=True)
        
        # Assistant identity
        self.assistant_name = "IET"
        
        # LLM (Gemma) configuration - uses Google's Gemma 3N API
        self.llm_enabled = True
        self.llm_backend = "gemma_api"  # Only Gemma API supported
        # Google AI Studio Gemma 3N API configuration
        self.gemma_api_key = os.getenv("GEMMA_API_KEY", "AIzaSyDK5zS9iaaL72QzxzneOJYshwCj73e6Xik")
        self.gemma_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemma-1.5-flash-exp:generateContent"
        
        # Simple knowledge base for chatbot responses
        self.responses = {
            "hello": ["Hello! How can I help you today?", "Hi there!", "Hello! Nice to meet you!"],
            "how are you": ["I'm doing great, thank you for asking!", "I'm fine, how about you?"],
            "what is your name": ["I'm IET, your personal voice assistant!", "You can call me IET.", "I'm IET."],
            "goodbye": ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"],
            "thank you": ["You're welcome!", "Happy to help!", "No problem!"],
        }
        
        print("Voice Assistant initialized successfully!")
        self.speak(f"Hello! I'm {self.assistant_name}, your personal voice assistant. How can I help you today?")

    def setup_voice(self):
        """Configure the text-to-speech voice settings"""
        voices = self.tts_engine.getProperty('voices')
        # Prefer more natural-sounding voices across platforms
        preferred_names = [
            'zira',      # Windows female (en-US)
            'samantha',  # macOS female (en-US)
            'hazel',     # Windows female (en-GB)
            'david',     # Windows male (en-US)
            'mark',      # common neural naming
            'daniel',    # macOS male (en-GB)
            'alex',      # macOS default
            'victoria',  # macOS female
        ]
        selected_voice_id = None
        try:
            for voice in voices:
                name = (voice.name or "").lower()
                if any(pref in name for pref in preferred_names):
                    selected_voice_id = voice.id
                    break
            if selected_voice_id:
                self.tts_engine.setProperty('voice', selected_voice_id)
        except Exception:
            # Fallback to default voice silently
            pass
        
        # Tune rate/volume for a less robotic sound
        self.tts_engine.setProperty('rate', 165)
        self.tts_engine.setProperty('volume', 1.0)

    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio input
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("Processing...")
            # Convert speech to text using Google's speech recognition
            text = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            self.speak("Sorry, I didn't understand that. Could you repeat?")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            self.speak("Sorry, I'm having trouble with speech recognition.")
            return None

    def ask_llm(self, prompt):
        """Ask Gemma 3N API for a response. Returns text or None on failure."""
        if not self.llm_enabled:
            return None
        try:
            # Google AI Studio Gemma 3N API
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"You are IET, a helpful voice assistant. Answer this question concisely and naturally: {prompt}"
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 150,
                }
            }
            headers = {"Content-Type": "application/json"}
            url = f"{self.gemma_api_url}?key={self.gemma_api_key}"
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            if resp.ok:
                data = resp.json()
                # Extract response from Google AI Studio format
                if "candidates" in data and len(data["candidates"]) > 0:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts = candidate["content"]["parts"]
                        if len(parts) > 0 and "text" in parts[0]:
                            answer = parts[0]["text"].strip()
                            return answer or None
            print(f"Unexpected API response format: {data}")
            return None
        except Exception as e:
            print(f"LLM request failed: {e}")
        return None

    def get_current_time(self):
        """Get and speak the current time"""
        now = datetime.datetime.now()
        time_string = now.strftime("It's %I:%M %p")
        return time_string

    def get_current_date(self):
        """Get and speak the current date"""
        now = datetime.datetime.now()
        date_string = now.strftime("Today is %A, %B %d, %Y")
        return date_string

    def play_music(self, query=""):
        """Play music from local folder or handle music commands"""
        music_files = list(self.music_folder.glob("*.mp3")) + list(self.music_folder.glob("*.wav"))
        
        if not music_files:
            self.speak("I don't have any music files in the music folder. Please add some MP3 or WAV files.")
            return
        
        # Stop any currently playing music
        pygame.mixer.music.stop()
        
        # Select a random song if no specific request
        selected_song = random.choice(music_files)
        
        try:
            pygame.mixer.music.load(str(selected_song))
            pygame.mixer.music.play()
            self.speak(f"Now playing {selected_song.stem}")
        except pygame.error as e:
            self.speak("Sorry, I couldn't play that music file.")
            print(f"Music error: {e}")

    def stop_music(self):
        """Stop currently playing music"""
        pygame.mixer.music.stop()
        self.speak("Music stopped.")

    def get_weather(self, city=""):
        """Get weather information (requires internet)"""
        # This is a simple example - in a real app, you'd need an API key
        try:
            # Using a free weather API (you'd need to sign up for a real API key)
            self.speak("I would need an API key to get real weather data. This is a demo feature.")
        except:
            self.speak("Sorry, I can't get weather information right now.")

    def simple_chatbot(self, user_input):
        """Respond to simple questions and conversations"""
        user_input = user_input.lower().strip()
        
        # Check for exact matches first
        for key, responses in self.responses.items():
            if key in user_input:
                return random.choice(responses)
        
        # Handle some common question patterns
        if "what" in user_input and "time" in user_input:
            return self.get_current_time()
        elif "what" in user_input and "date" in user_input:
            return self.get_current_date()
        elif "play music" in user_input or "play song" in user_input:
            self.play_music()
            return "Playing music for you!"
        elif "stop music" in user_input:
            self.stop_music()
            return "Music stopped."
        elif "weather" in user_input:
            self.get_weather()
            return "Weather feature is in demo mode."
        
        # Default responses for unrecognized input
        default_responses = [
            "That's interesting! Tell me more.",
            "I'm still learning. Can you ask me something else?",
            "I'm not sure about that, but I'm here to help!",
            "Could you rephrase that question?",
        ]
        return random.choice(default_responses)

    def process_command(self, command):
        """Process voice commands and determine appropriate response"""
        if not command:
            return
        
        command = command.lower().strip()
        
        # Exit commands
        if any(word in command for word in ["quit", "exit", "goodbye", "bye"]):
            self.speak("Goodbye! Have a great day!")
            return False
        
        # Time commands
        elif "time" in command:
            response = self.get_current_time()
            self.speak(response)
        
        # Date commands
        elif "date" in command:
            response = self.get_current_date()
            self.speak(response)
        
        # Music commands
        elif "play music" in command or "play song" in command:
            self.play_music()
        elif "stop music" in command:
            self.stop_music()
        
        # Weather commands
        elif "weather" in command:
            self.get_weather()
        
        # General chatbot response
        else:
            # Try LLM for open-ended questions before falling back
            try_llm = any(k in command for k in [
                "what", "who", "when", "where", "why", "how", "explain", "define", "tell me about"
            ]) or ("?" in command)
            if try_llm:
                llm_answer = self.ask_llm(command)
                if llm_answer:
                    self.speak(llm_answer)
                    return True
            response = self.simple_chatbot(command)
            self.speak(response)
        
        return True

    def run(self):
        """Main loop to run the voice assistant"""
        print("\n" + "="*50)
        print("IET VOICE ASSISTANT STARTED")
        print("Say 'quit', 'exit', or 'goodbye' to stop")
        print("="*50 + "\n")
        
        while True:
            try:
                # Listen for user input
                user_input = self.listen()
                
                # Process the command
                if user_input:
                    continue_running = self.process_command(user_input)
                    if not continue_running:
                        break
                
            except KeyboardInterrupt:
                print("\nShutting down...")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                self.speak("Sorry, something went wrong. Let's try again.")

def main():
    """Main function to start the voice assistant"""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"Failed to start voice assistant: {e}")
        print("Make sure all required libraries are installed.")

if __name__ == "__main__":
    main()