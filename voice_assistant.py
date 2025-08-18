import datetime
import math
import os
import random
import re
import threading
import time
import json
import webbrowser
import platform
import psutil

import pyttsx3
import requests
import speech_recognition as sr


class VoiceAssistant:
    def __init__(self):
        self._setup_core_components()
        self._setup_apis()
        self._setup_responses()
        self._initialize_assistant()

    def _setup_core_components(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.assistant_name = "AI Voice Assistant"
        self.memory = []
        self.max_memory = 50
        self.active_timers = []
        self._configure_voice()

    def _setup_apis(self):
        # Use the provided Gemini API key
        self.gemini_api_key = "AIzaSyBVbzio3hQ6-Vr69n1wO_KmKAavAyB7X1M"
        self.gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        # Weather API (OpenWeatherMap - free tier)
        self.weather_api_key = os.getenv("OPENWEATHER_API_KEY")
        self.weather_api_url = "https://api.openweathermap.org/data/2.5/weather"
        
        # News API (optional)
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.news_api_url = "https://newsapi.org/v2/top-headlines"

    def _setup_responses(self):
        self.responses = {
            "hello": ["Hello! How can I help you today?", "Hi there!", "Hello! Nice to meet you!"],
            "how are you": ["I'm doing great, thank you for asking!", "I'm fine, how about you?"],
            "what is your name": [f"I'm {self.assistant_name}, your personal voice assistant!", f"You can call me {self.assistant_name}.", f"I'm {self.assistant_name}."],
            "goodbye": ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"],
            "thank you": ["You're welcome!", "Happy to help!", "No problem!"],
        }

    def _initialize_assistant(self):
        print("AI Voice Assistant initialized successfully!")
        self.speak(f"Hello! I'm {self.assistant_name}.  How can I assist you today?")
        self._test_gemini_connection()

    def _configure_voice(self):
        voices = self.tts_engine.getProperty('voices')
        print(f"🔍 Found {len(voices)} voices")

        # Try to find a good quality voice
        priority_voices = ['zira', 'samantha', 'hazel', 'david', 'mark', 'alex', 'victoria']
        
        for voice in voices:
            name = (voice.name or "").lower()
            if any(priority in name for priority in priority_voices):
                self.tts_engine.setProperty('voice', voice.id)
                print(f"🎯 Using: {voice.name}")
                break

        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 1.0)

    def _test_gemini_connection(self):
        print("🧪 Testing Gemini API connection...")
        if self.ask_gemini("Say hello in one sentence"):
            print("✅ Gemini API connected successfully!")
        else:
            print("❌ Gemini API connection failed - check your API key")

    def speak(self, text):
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        timeout = 30
        phrase_limit = 60
        threshold = 200
        pause_threshold = 1.5

        try:
            with self.microphone as source:
                print("🎤 Listening for input...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                
                self.recognizer.energy_threshold = threshold
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = pause_threshold

                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {text}")
            return text

        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            error_msg = "I couldn't understand that clearly. Please try again with clearer speech." if continuous_mode else "Sorry, I didn't understand that. Could you speak more clearly and try again?"
            print("❌ Speech was unclear - please try again")
            self.speak(error_msg)
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            self.speak("Sorry, I'm having trouble with the speech recognition service.")
            return None
        except Exception as e:
            print(f"❌ Error during listening: {e}")
            self.speak("Sorry, something went wrong while listening. Please try again.")
            return None

    def ask_gemini(self, prompt, context=""):
        """Send any question to Gemini AI"""
        try:
            full_prompt = f"You are a helpful AI assistant. {context}\nQuestion: {prompt}\nPlease provide a clear, helpful, and natural response:"
            
            payload = {
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 500,
                    "topP": 0.8,
                    "topK": 40
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
                        print(f"🤖 Gemini Response: {answer[:100]}...")
                        return answer
                else:
                    print(f"❌ Gemini API error: {data}")
            else:
                print(f"❌ Gemini API request failed: {response.status_code} - {response.text}")
            
            return None

        except Exception as e:
            print(f"❌ Gemini API request failed: {e}")
            return None

    def handle_math(self, command):
        """Handle mathematical calculations"""
        try:
            expr = command.lower().strip()
            print(f"🔢 Processing math command: {expr}")

            # Handle special functions first
            # Square root
            if "square root" in expr or "root" in expr:
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)
                if numbers:
                    number = float(numbers[0])
                    result = math.sqrt(number)
                    return f"The square root of {number} is {result:.4f}"

            # Cube root
            if "cube root" in expr:
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)
                if numbers:
                    number = float(numbers[0])
                    result = number ** (1/3)
                    return f"The cube root of {number} is {result:.4f}"

            # Factorial
            if "factorial" in expr:
                numbers = re.findall(r'\d+', expr)
                if numbers:
                    number = int(numbers[0])
                    if number < 0:
                        return "Factorial is not defined for negative numbers"
                    if number > 20:
                        return f"Factorial of {number} is too large to calculate"
                    result = math.factorial(number)
                    return f"The factorial of {number} is {result}"

            # Power/Exponent
            if any(word in expr for word in ["power", "raised to", "to the power"]):
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)
                if len(numbers) >= 2:
                    base = float(numbers[0])
                    exponent = float(numbers[1])
                    result = base ** exponent
                    return f"{base} to the power of {exponent} is {result}"

            # Basic arithmetic operations
            # Addition
            if any(word in expr for word in ["plus", "add", "addition"]):
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)
                if len(numbers) >= 2:
                    num1 = float(numbers[0])
                    num2 = float(numbers[1])
                    result = num1 + num2
                    return f"{num1} plus {num2} equals {result}"

            # Subtraction
            if any(word in expr for word in ["minus", "subtract", "subtraction"]):
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)
                if len(numbers) >= 2:
                    num1 = float(numbers[0])
                    num2 = float(numbers[1])
                    result = num1 - num2
                    return f"{num1} minus {num2} equals {result}"

            # Multiplication
            if any(word in expr for word in ["times", "multiply", "multiplication"]):
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)
                if len(numbers) >= 2:
                    num1 = float(numbers[0])
                    num2 = float(numbers[1])
                    result = num1 * num2
                    return f"{num1} times {num2} equals {result}"

            # Division
            if any(word in expr for word in ["divided by", "divide", "division"]):
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)
                if len(numbers) >= 2:
                    num1 = float(numbers[0])
                    num2 = float(numbers[1])
                    if num2 == 0:
                        return "Cannot divide by zero"
                    result = num1 / num2
                    return f"{num1} divided by {num2} equals {result:.4f}"

            # Modulo
            if any(word in expr for word in ["modulo", "mod", "remainder"]):
                numbers = re.findall(r'\d+', expr)
                if len(numbers) >= 2:
                    num1 = int(numbers[0])
                    num2 = int(numbers[1])
                    if num2 == 0:
                        return "Cannot divide by zero"
                    result = num1 % num2
                    return f"The remainder when {num1} is divided by {num2} is {result}"

            # Try to extract simple expressions with operators
            # Look for patterns like "5 + 3" or "10 * 2"
            if any(op in expr for op in ["+", "-", "*", "/", "**", "%"]):
                # Clean up the expression
                clean_expr = re.sub(r'[^\d+\-*/.()%]', '', expr)
                if clean_expr:
                    try:
                        result = eval(clean_expr)
                        if isinstance(result, (int, float)):
                            if result == int(result):
                                result = int(result)
                            return f"The answer is {result}"
                    except:
                        pass

            # If no specific operation found, try to extract numbers and suggest operations
            numbers = re.findall(r'\d+(?:\.\d+)?', expr)
            if numbers:
                return f"I found the numbers: {', '.join(numbers)}. Please specify an operation like 'plus', 'minus', 'times', or 'divided by'."

            return "I couldn't understand the math operation. Please try phrases like '5 plus 3' or '10 times 2'."

        except Exception as e:
            print(f"Math calculation error: {e}")
            return f"Sorry, I couldn't calculate that. Error: {str(e)}"

    def handle_weather(self, command):
        """Get weather information"""
        if not self.weather_api_key:
            return "Weather information requires an OpenWeather API key. Set OPENWEATHER_API_KEY environment variable and ask me again."

        city = self._extract_location(command)
        if not city:
            return "Please specify a city, like 'weather in New York' or 'what's the weather in London'."

        weather_data = self._fetch_weather(city)
        if weather_data:
            return self._format_weather(weather_data)
        return "Sorry, I couldn't fetch the weather right now. Please try again later."

    def handle_timer(self, command):
        """Set timers and stopwatch"""
        if "stopwatch" in command or "start timing" in command:
            self.speak("Stopwatch started. Say 'stop stopwatch' to stop.")
            start_time = time.time()
            self.stopwatch_start = start_time
            return None

        if "stop stopwatch" in command and hasattr(self, 'stopwatch_start'):
            elapsed = time.time() - self.stopwatch_start
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            result = f"Stopwatch stopped. Time elapsed: {minutes} minutes and {seconds} seconds"
            delattr(self, 'stopwatch_start')
            return result

        # Extract duration from command
        duration = self._extract_duration(command)
        if duration and 1 <= duration <= 3600:  # 1 second to 1 hour
            minutes = duration // 60
            seconds = duration % 60
            time_str = f"{minutes} minutes {seconds} seconds" if minutes > 0 else f"{seconds} seconds"
            
            self.speak(f"Timer set for {time_str}. I'll notify you when it's done!")
            
            timer_id = len(self.active_timers)
            timer_thread = threading.Thread(target=self._run_timer, args=(duration, timer_id), daemon=True)
            timer_thread.start()
            
            self.active_timers.append({
                'id': timer_id,
                'duration': duration,
                'start_time': time.time(),
                'thread': timer_thread
            })
            
            return None
        return "Please specify a duration between 1 second and 1 hour."

    def handle_system_commands(self, command):
        """Handle system-related commands"""
        if "volume" in command:
            if "up" in command or "increase" in command:
                # This would require additional libraries on Windows
                return "Volume control requires additional setup. You can use your system volume controls."
            elif "down" in command or "decrease" in command:
                return "Volume control requires additional setup. You can use your system volume controls."
            else:
                return "You can say 'volume up' or 'volume down' to control system volume."

        if "system info" in command or "computer info" in command:
            system_info = f"Operating System: {platform.system()} {platform.release()}"
            system_info += f"\nMachine: {platform.machine()}"
            system_info += f"\nProcessor: {platform.processor()}"
            
            # Memory info
            memory = psutil.virtual_memory()
            system_info += f"\nMemory: {memory.total // (1024**3)} GB total, {memory.percent}% used"
            
            # Disk info
            disk = psutil.disk_usage('/')
            system_info += f"\nDisk: {disk.total // (1024**3)} GB total, {disk.free // (1024**3)} GB free"
            
            return system_info

        if "open browser" in command or "open web browser" in command:
            try:
                webbrowser.open("https://www.google.com")
                return "Opening web browser"
            except:
                return "Could not open web browser"

        return None

    def handle_news(self, command):
        """Get news headlines"""
        if not self.news_api_key:
            return "News requires a News API key. Set NEWS_API_KEY environment variable and ask me again."

        try:
            # Extract topic if specified
            topic = ""
            if "about" in command:
                topic = command.split("about")[-1].strip()
            
            params = {
                "apiKey": self.news_api_key,
                "country": "us",
                "pageSize": 5
            }
            
            if topic:
                params["q"] = topic
                
            response = requests.get(self.news_api_url, params=params, timeout=10)
            
            if response.ok:
                data = response.json()
                articles = data.get("articles", [])
                
                if articles:
                    news_text = f"Here are the top {len(articles)} news headlines"
                    if topic:
                        news_text += f" about {topic}"
                    news_text += ":\n\n"
                    
                    for i, article in enumerate(articles[:3], 1):
                        title = article.get("title", "").split(" - ")[0]  # Remove source
                        news_text += f"{i}. {title}\n"
                    
                    return news_text
                else:
                    return "No news articles found."
            else:
                return "Could not fetch news at the moment."
                
        except Exception as e:
            print(f"News API error: {e}")
            return "Sorry, I couldn't fetch the news right now."

    def process_command(self, command):
        """Main command processor - redirects all questions to Gemini"""
        if not command:
            return True

        command = command.lower().strip()

        # Exit commands
        if any(word in command for word in ["quit", "exit", "goodbye", "bye", "stop"]):
            self.speak("Goodbye! Have a great day!")
            return False



        # Time and date
        if "time" in command and ("what" in command or "tell" in command):
            current_time = datetime.datetime.now().strftime("It's %I:%M %p")
            self.speak(current_time)
            return True

        if "date" in command or "day" in command:
            current_date = datetime.datetime.now().strftime("Today is %A, %B %d, %Y")
            self.speak(current_date)
            return True

        # Math calculations
        math_indicators = ["plus", "minus", "times", "multiply", "divide", "divided by", "add", "subtract", 
                          "addition", "subtraction", "multiplication", "division", "power", "raised to", 
                          "square root", "root", "cube root", "factorial", "modulo", "mod", "remainder", "calculate", 
                          "solve", "compute", "find", "result", "answer", "what is", "how much is", "equals"]
        
        # Check for math operations or numbers
        if (any(indicator in command for indicator in math_indicators) or 
            any(char in command for char in "+-*/%**") or
            re.search(r'\d+', command)):  # Check if command contains numbers
            
            result = self.handle_math(command)
            if result:
                self.speak(result)
                return True

        # Weather
        if any(word in command for word in ["weather", "forecast", "temperature"]):
            result = self.handle_weather(command)
            self.speak(result)
            return True

        # Timer and stopwatch
        if any(word in command for word in ["timer", "stopwatch", "countdown"]):
            result = self.handle_timer(command)
            if result:
                self.speak(result)
            return True

        # System commands
        if any(word in command for word in ["volume", "system", "computer", "browser"]):
            result = self.handle_system_commands(command)
            if result:
                self.speak(result)
            return True

        # News
        if any(word in command for word in ["news", "headlines", "current events"]):
            result = self.handle_news(command)
            if result:
                self.speak(result)
            return True

        # Memory commands
        if "memory" in command:
            result = self._get_memory_stats()
            self.speak(result)
            return True

        # Clear memory
        if "clear memory" in command or "forget" in command:
            self.memory.clear()
            self.speak("I've cleared my memory.")
            return True

        # All other questions go to Gemini AI
        if any(word in command for word in ["what", "who", "when", "where", "why", "how", "explain", 
                                          "define", "tell me", "can you", "could you", "would you", 
                                          "in detail", "more about", "information", "details", 
                                          "explanation", "describe", "elaborate", "what is", "how to"]):
            
            answer = self.ask_gemini(command)
            
            if answer:
                self._remember(command, answer)
                self.speak(answer)
            else:
                self.speak("I'm having trouble getting a response right now. Please try again.")
            return True

        # Basic responses for greetings and simple commands
        basic_response = self._get_basic_response(command)
        if basic_response:
            self.speak(basic_response)
            return True

        # If nothing else matches, ask Gemini AI
        answer = self.ask_gemini(command)
        
        if answer:
            self._remember(command, answer)
            self.speak(answer)
        else:
            self.speak("I couldn't get a response. Could you try rephrasing your question?")
        
        return True

    def _remember(self, question, answer):
        """Remember interactions for context"""
        interaction = {
            "question": question,
            "answer": answer,
            "topic": self._get_topic(question),
            "timestamp": datetime.datetime.now()
        }
        self.memory.append(interaction)
        if len(self.memory) > self.max_memory:
            self.memory.pop(0)
        print(f"💾 Remembered: {interaction['topic']}")

    def _get_topic(self, question):
        """Categorize questions by topic"""
        question_lower = question.lower()
        topics = {
            "technology": ["computer", "software", "ai", "programming", "code", "app", "website"],
            "science": ["physics", "chemistry", "biology", "math", "experiment", "research"],
            "health": ["medical", "fitness", "nutrition", "exercise", "health", "diet"],
            "finance": ["money", "investment", "budget", "savings", "stock", "bank"],
            "weather": ["weather", "temperature", "forecast", "climate", "rain", "sunny"],
            "entertainment": ["movie", "music", "game", "book", "show", "joke", "fun"],
            "education": ["learn", "study", "school", "university", "course", "teach"],
            "news": ["news", "current events", "headlines", "politics", "world"]
        }
        
        for topic, keywords in topics.items():
            if any(keyword in question_lower for keyword in keywords):
                return topic
        return "general"

    def _extract_location(self, command):
        """Extract city name from weather command"""
        try:
            # Look for patterns like "weather in London", "temperature at New York"
            matches = re.search(r"(?:in|at|for)\s+([a-zA-Z\s\-]+)", command)
            if matches:
                city_raw = matches.group(1).strip()
                # Remove common words
                city_raw = re.sub(r"\b(today|now|right now|please|forecast|weather|temperature)\b", "", city_raw, flags=re.IGNORECASE).strip()
                city = re.sub(r"\s+", " ", city_raw).title()
                return city if city else ""
            return ""
        except Exception:
            return ""

    def _extract_duration(self, command):
        """Extract duration from timer command"""
        try:
            # Look for time patterns
            time_patterns = {
                r"(\d+)\s*seconds?": 1,
                r"(\d+)\s*minutes?": 60,
                r"(\d+)\s*hours?": 3600
            }
            
            for pattern, multiplier in time_patterns.items():
                match = re.search(pattern, command)
                if match:
                    number = int(match.group(1))
                    return number * multiplier
            
            # Look for just numbers (assume seconds)
            match = re.search(r"(\d+)", command)
            if match:
                return int(match.group(1))
                
            return None
        except Exception:
            return None

    def _fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        try:
            params = {"q": city, "appid": self.weather_api_key, "units": "metric"}
            response = requests.get(self.weather_api_url, params=params, timeout=10)
            
            if response.ok:
                data = response.json()
                cod = str(data.get("cod", "200"))
                if cod.startswith("2"):
                    return data
            return None
        except Exception:
            return None

    def _format_weather(self, data):
        """Format weather data into readable text"""
        try:
            name = data.get("name")
            main = data.get("main", {})
            wind = data.get("wind", {})
            weather_list = data.get("weather", [])
            desc = weather_list[0].get("description") if weather_list else None
            temp = main.get("temp")
            feels = main.get("feels_like")
            humidity = main.get("humidity")
            wind_speed = wind.get("speed")
            
            parts = []
            if name:
                parts.append(f"In {name}")
            if temp is not None:
                parts.append(f"it's {round(float(temp))}°C")
            if desc:
                parts.append(f"with {desc}")
            if feels is not None:
                parts.append(f"(feels like {round(float(feels))}°C)")
            if humidity is not None:
                parts.append(f"humidity {int(humidity)}%")
            if wind_speed is not None:
                parts.append(f"wind {round(float(wind_speed))} m/s")
            
            if not parts:
                return "I couldn't parse the weather details."
            
            response = ", ".join(parts[:3])
            if len(parts) > 3:
                response += ", " + ", ".join(parts[3:])
            return response
        except Exception:
            return "I couldn't parse the weather details."

    def _run_timer(self, duration, timer_id):
        """Run a timer in background"""
        remaining = duration
        while remaining > 0:
            time.sleep(1)
            remaining -= 1
            
            # Give updates every 30 seconds for longer timers
            if remaining % 30 == 0 and remaining > 0 and remaining > 60:
                print(f"⏱️ Timer {timer_id}: {remaining} seconds remaining")
        
        print(f"⏰ Timer {timer_id} finished!")
        self.speak("Time's up! Your timer has finished.")
        
        # Remove from active timers
        self.active_timers = [t for t in self.active_timers if t['id'] != timer_id]

    def _get_memory_stats(self):
        """Get statistics about remembered conversations"""
        if not self.memory:
            return "I haven't had any conversations yet to remember."

        topic_counts = {}
        for m in self.memory:
            topic = m["topic"]
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        response = f"I remember {len(self.memory)} conversations. "
        if topic_counts:
            topics = [f"{topic} ({count})" for topic, count in topic_counts.items()]
            response += "Topics: " + ", ".join(topics)
        return response

    def _get_basic_response(self, user_input):
        """Get basic responses for simple commands"""
        for key, responses in self.responses.items():
            if key in user_input:
                return random.choice(responses)

        return random.choice([
            "That's interesting! Tell me more.",
            "I'm here to help! What would you like to know?",
            "I'm connected to Gemini AI, so I can help with almost any question!",
            "Could you rephrase that or ask me something else?"
        ])

    def run(self):
        """Main run loop"""
        print("\n" + "="*60)
        print("🤖 AI VOICE ASSISTANT STARTED")
        print("🔑 Connected to Gemini AI")
        print("📝 Say 'quit', 'exit', or 'goodbye' to stop")
        print("🧮 I can do math, weather, timers, and answer any questions!")
        print("="*60 + "\n")

        while True:
            try:
                user_input = self.listen()

                if user_input:
                    result = self.process_command(user_input)

                    if result == False:
                        break

            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.speak("Sorry, something went wrong. Let's try again.")


def main():
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        print("Check your libraries and API key.")


if __name__ == "__main__":
    main()