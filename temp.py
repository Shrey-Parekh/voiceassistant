import datetime
import random
import pyttsx3
import requests
import speech_recognition as sr
import time


class VoiceAssistant:
    def __init__(self):
        self._setup_core_components()
        self._setup_apis()
        self._setup_responses()
        self._initialize_assistant()

    def _setup_core_components(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = None
        self.assistant_name = "DeepSphere"
        self._configure_voice()

    def _setup_apis(self):
        self.gemini_api_key = "AIzaSyBVbzio3hQ6-Vr69n1wO_KmKAavAyB7X1M"
        self.gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    def _setup_responses(self):
        self.responses = {
            "hello": ["Hello! How can I help you today?", "Hi there!", "Hello! Nice to meet you!"],
            "how are you": ["I'm doing great, thank you for asking!", "I'm fine, how about you?"],
            "what is your name": [f"I'm {self.assistant_name}, your personal voice assistant!", f"You can call me {self.assistant_name}.", f"I'm {self.assistant_name}."],
            "goodbye": ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"],
            "thank you": ["You're welcome!", "Happy to help!", "No problem!"],
        }

    def _initialize_assistant(self):
        print("DeepSphere initialized successfully!")
        self.speak(f"Hello! I'm {self.assistant_name}. How can I help you today?")
        self._test_gemini_connection()

    def _configure_voice(self):
        try:
            self.tts_engine = pyttsx3.init()
            
            voices = self.tts_engine.getProperty('voices')
            print(f"Found {len(voices)} voices available")
            
            if voices:
                print(f"Using default voice: {voices[0].name}")
            
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 1.0)
            
            print("Text-to-speech engine configured successfully!")
            
        except Exception as e:
            print(f"Warning: TTS initialization failed: {e}")
            print("Speech output will not be available")
            self.tts_engine = None

    def _test_gemini_connection(self):
        print("Testing Gemini API connection...")
        if self.ask_gemini("Say hello in one sentence"):
            print("Gemini API connected successfully!")
        else:
            print("Gemini API connection failed - check your API key")

    def speak(self, text):
        print(f"Assistant: {text}")
        
        if self.tts_engine is None:
            print("[TTS not available - text only]")
            return
            
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            time.sleep(0.1)
        except Exception as e:
            print(f"TTS Error: {e}")
            try:
                self.tts_engine.stop()
                time.sleep(0.5)
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 1.0)
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e2:
                print(f"TTS Recovery failed: {e2}")
                print("[Speaking text only in console]")

    def listen(self):
        timeout = 30
        phrase_limit = 60
        threshold = 200
        pause_threshold = 1.5
        try:
            with self.microphone as source:
                print("Listening for input...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                
                self.recognizer.energy_threshold = threshold
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = pause_threshold

                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

            print("Processing speech...")
            text = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text

        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            error_msg = "I couldn't understand that clearly. Please try again with clearer speech."
            print("Speech was unclear - please try again")
            self.speak(error_msg)
            return None
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            self.speak("Sorry, I'm having trouble with the speech recognition service.")
            return None
        except Exception as e:
            print(f"Error during listening: {e}")
            self.speak("Sorry, something went wrong while listening. Please try again.")
            return None

    def ask_gemini(self, prompt):
        try:
            full_prompt = f"You are a friendly voice assistant. Answer naturally and conversationally. Keep responses concise but helpful.\n\nUser: {prompt}\nAssistant:"
            payload = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {
                    "temperature": 0.6,
                    "maxOutputTokens": 500,
                    "topP": 0.7,
                    "topK": 30
                }
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                f"{self.gemini_api_url}?key={self.gemini_api_key}",
                json=payload,
                headers=headers,
                timeout=30
            )
            if response.ok:
                data = response.json()
                if "candidates" in data and data["candidates"]:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        answer = candidate["content"]["parts"][0]["text"].strip()
                        print(f"Gemini Response: {answer[:100]}...")
                        return answer
                else:
                    print(f"Gemini API error: {data}")
            else:
                print(f"Gemini API request failed: {response.status_code} - {response.text}")
            
            return None

        except Exception as e:
            print(f"Gemini API request failed: {e}")
            return None

    def process_command(self, command):
        if not command:
            return True

        command = command.lower().strip()

        if any(word in command for word in ["quit", "exit", "goodbye", "bye", "stop"]):
            self.speak("Goodbye! Have a great day!")
            return False

        basic_response = self._get_basic_response(command)
        if basic_response:
            self.speak(basic_response)
            return True

        if "time" in command and ("what" in command or "tell" in command):
            current_time = datetime.datetime.now().strftime("It's %I:%M %p")
            self.speak(current_time)
            return True

        if "date" in command or "day" in command:
            current_date = datetime.datetime.now().strftime("Today is %A, %B %d, %Y")
            self.speak(current_date)
            return True

        print("Sending query to Gemini AI...")
        answer = self.ask_gemini(command)
        if answer:
            print("Speaking Gemini response...")
            self.speak(answer)
        else:
            error_msg = "I'm having trouble getting a response right now. Please try again."
            print("Speaking error message...")
            self.speak(error_msg)
        return True

    def _get_basic_response(self, user_input):
        for key, responses in self.responses.items():
            if key in user_input:
                return random.choice(responses)
        
        return None

    def run(self):
        print("\n" + "="*60)
        print("DEEPSPHERE VOICE ASSISTANT STARTED")
        print("Connected to Gemini AI")
        print("Say 'quit', 'exit', or 'goodbye' to stop")
        print("Continuous listening mode enabled")
        print("I can answer your questions with Gemini AI!")
        if self.tts_engine is None:
            print("WARNING: Text-to-speech not available - text only mode")
        print("="*60 + "\n")

        while True:
            try:
                user_input = self.listen()

                if user_input:
                    result = self.process_command(user_input)

                    if result == False:
                        break

            except KeyboardInterrupt:
                print("\nShutting down...")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, something went wrong. Let's try again.")

def main():
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"Failed to start: {e}")
        print("Check your libraries and API key.")


if __name__ == "__main__":
    main()