---
title: "DeepSphere: Build a Voice Assistant"
author: "IET MPSTME ~ Rushabh"
format: revealjs
embed-resources: true
---

## Introduction
- This project is a Python-based voice assistant that listens to the microphone, converts speech into text, and interacts with users through natural language.
- It performs quick tasks such as telling the time and date, handling simple math operations, and answering general questions by querying the Gemini AI HTTP API.
- The assistant uses speech recognition for input, calls the Gemini AI for complex queries, and responds aloud using a text-to-speech engine, providing a conversational experience.


## Imports
```python
import datetime  # Provides date and time utilities
import math  # Provides mathematical functions and constants
import random  # Used to randomly choose from response lists
import re  # Regular expression operations for parsing text
import pyttsx3  # Text-to-speech engine for local voice output
import requests  # HTTP client for calling the Gemini API
import speech_recognition as sr  # Speech recognition for listening and transcription
```


## Class Definition & Docstring
```python
class VoiceAssistant:
    """A simple voice assistant that listens, understands, and speaks back.

    Responsibilities:
    - Convert microphone speech to text
    - Handle quick commands (time, date, math)
    - Ask Gemini AI for answers to general questions
    - Speak responses aloud via text-to-speech
    """
```


## Initialization
```python
    def __init__(self):
        self._setup_core_components()
        self._setup_apis()
        self._setup_responses()
        self._initialize_assistant()
```


## Core Component Setup
```python
    def _setup_core_components(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.assistant_name = "DeepSphere"
        self._configure_voice()
```


## API Setup
```python
    def _setup_apis(self):
        self.gemini_api_key = "AIzaSyBVbzio3hQ6-Vr69n1wO_KmKAavAyB7X1M"
        self.gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
```


## Responses Setup
```python
    def _setup_responses(self):
        self.responses = {
            "hello": ["Hello! How can I help you today?", "Hi there!", "Hello! Nice to meet you!"],
            "how are you": ["I'm doing great, thank you for asking!", "I'm fine, how about you?"],
            "what is your name": [f"I'm {self.assistant_name}, your personal voice assistant!", f"You can call me {self.assistant_name}.", f"I'm {self.assistant_name}."],
            "goodbye": ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"],
            "thank you": ["You're welcome!", "Happy to help!", "No problem!"],
        }
```


## Assistant Initialization
```python
    def _initialize_assistant(self):
        print("DeepSphere initialized successfully!")
        self.speak(f"Hello! I'm {self.assistant_name}. How can I help you today?")
        self._test_gemini_connection()
```


## Voice Configuration
```python
    def _configure_voice(self):
        voices = self.tts_engine.getProperty('voices')
        print(f"Found {len(voices)} voices")
        priority_voices = ['zira', 'samantha', 'hazel', 'david', 'mark', 'alex', 'victoria']
        for voice in voices:
            name = (voice.name or "").lower()
            if any(priority in name for priority in priority_voices):
                self.tts_engine.setProperty('voice', voice.id)
                print(f"Using: {voice.name}")
                break
        self.tts_engine.setProperty('rate', 200)
        self.tts_engine.setProperty('volume', 1.0)
```


## Gemini API Test
```python
    def _test_gemini_connection(self):
        print("Testing Gemini API connection...")
        if self.ask_gemini("Say hello in one sentence"):
            print("Gemini API connected successfully!")
        else:
            print("Gemini API connection failed - check your API key")
```


## Speak Method
```python
    def speak(self, text):
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
```


## Listen Method
```python
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
```


## Ask Gemini Method
```python
    def ask_gemini(self, prompt, context=""):
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
```


## Handle Math Method
```python
    def handle_math(self, command):
        try:
            expr = command.lower().strip()
            print(f"Processing math command: {expr}")
            # ...math logic...
        except Exception as e:
            print(f"Math calculation error: {e}")
            return f"Sorry, I couldn't calculate that. Error: {str(e)}"
```

## Math Logic: Square Root
```python
if "square root" in expr or "root" in expr:  # Detect square root requests
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers (including decimals)
                if numbers:  # Ensure a number was found
                    number = float(numbers[0])  # Parse the first number
                    result = math.sqrt(number)  # Compute square root
                    return f"The square root of {number} is {result:.4f}"  # Return formatted result
```

## Math Logic: Cube Root
```python
if "cube root" in expr:  # Detect cube root requests
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if numbers:  # Ensure a number was found
                    number = float(numbers[0])  # Parse the first number
                    result = number ** (1/3)  # Compute cube root
                    return f"The cube root of {number} is {result:.4f}"  # Return formatted result
```

## Math Logic: Factorial
```python
if "factorial" in expr:  # Detect factorial requests
                numbers = re.findall(r'\d+', expr)  # Extract integer numbers
                if numbers:  # Ensure a number was found
                    number = int(numbers[0])  # Parse as integer
                    if number < 0:  # Factorial not defined for negatives
                        return "Factorial is not defined for negative numbers"  # Inform user
                    if number > 20:  # Avoid huge computations
                        return f"Factorial of {number} is too large to calculate"  # Limit safeguard
                    result = math.factorial(number)  # Compute factorial
                    return f"The factorial of {number} is {result}"  # Return exact integer result
```

## Math Logic: Power/Exponent
```python
if any(word in expr for word in ["power", "raised to", "to the power"]):  # Detect exponentiation
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need base and exponent
                    base = float(numbers[0])  # Parse base
                    exponent = float(numbers[1])  # Parse exponent
                    result = base ** exponent  # Compute power
                    return f"{base} to the power of {exponent} is {result}"  # Return result
```

## Math Logic: Addition
```python
if any(word in expr for word in ["plus", "add", "addition"]):  # Detect addition
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = float(numbers[0])  # First operand
                    num2 = float(numbers[1])  # Second operand
                    result = num1 + num2  # Compute sum
                    return f"{num1} plus {num2} equals {result}"  # Return result
```

## Math Logic: Subtraction
```python
 if any(word in expr for word in ["minus", "subtract", "subtraction"]):  # Detect subtraction
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = float(numbers[0])  # Minuend
                    num2 = float(numbers[1])  # Subtrahend
                    result = num1 - num2  # Compute difference
                    return f"{num1} minus {num2} equals {result}"  # Return result
```

## Math Logic: Multiplication
```python
if any(word in expr for word in ["times", "multiply", "multiplication"]):  # Detect multiplication
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = float(numbers[0])  # Multiplicand
                    num2 = float(numbers[1])  # Multiplier
                    result = num1 * num2  # Compute product
                    return f"{num1} times {num2} equals {result}"  # Return result
```

## Math Logic: Division
```python
if any(word in expr for word in ["divided by", "divide", "division"]):  # Detect division
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = float(numbers[0])  # Dividend
                    num2 = float(numbers[1])  # Divisor
                    if num2 == 0:  # Guard against division by zero
                        return "Cannot divide by zero"  # Inform user
                    result = num1 / num2  # Compute quotient
                    return f"{num1} divided by {num2} equals {result:.4f}"  # Return result with 4 decimals
```

## Math Logic: Modulo
```python
if any(word in expr for word in ["modulo", "mod", "remainder"]):  # Detect modulus operation
                numbers = re.findall(r'\d+', expr)  # Extract integer numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = int(numbers[0])  # Dividend
                    num2 = int(numbers[1])  # Divisor
                    if num2 == 0:  # Cannot modulo by zero
                        return "Cannot divide by zero"  # Inform user
                    result = num1 % num2  # Compute remainder
                    return f"The remainder when {num1} is divided by {num2} is {result}"  # Return result
```

## Math Logic: Extract Patterns
```python
# Look for patterns like "5 + 3" or "10 * 2"
            if any(op in expr for op in ["+", "-", "*", "/", "**", "%"]):  # Detect presence of operators
                # Clean up the expression
                clean_expr = re.sub(r'[^\d+\-*/.()%]', '', expr)  # Remove non-math characters
                if clean_expr:  # Ensure something to evaluate
                    try:  # Attempt evaluation
                        result = eval(clean_expr)  # Evaluate expression (assumes sanitized input)
                        if isinstance(result, (int, float)):  # Confirm numeric result
                            if result == int(result):  # Convert float integers to int
                                result = int(result)  # Cast to int for cleaner output
                            return f"The answer is {result}"  # Return final result
                    except:  # Any eval error
                        pass  # Fall back to guidance below

            # If no specific operation found, try to extract numbers and suggest operations
            numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract any numbers present
            if numbers:  # If numbers found but no operation
                return f"I found the numbers: {', '.join(numbers)}. Please specify an operation like 'plus', 'minus', 'times', or 'divided by'."  # Ask for operation

            return "I couldn't understand the math operation. Please try phrases like '5 plus 3' or '10 times 2'."  # Generic guidance
```


## Process Command Method
```python
    def process_command(self, command):
        if not command:
            return True
        command = command.lower().strip()
        # ...command routing logic...
```

## Command Routine Logic: Exit Commands
```python
if any(word in command for word in ["quit", "exit", "goodbye", "bye", "stop"]):  # Check for exit intent
    self.speak("Goodbye! Have a great day!")  # Say goodbye
    return False  # Signal to stop main loop
```

## Command Routine Logic: Time and Date
```python
if "time" in command and ("what" in command or "tell" in command):  # Ask current time
    current_time = datetime.datetime.now().strftime("It's %I:%M %p")  # Format time
    self.speak(current_time)  # Speak time
    return True  # Continue loop

if "date" in command or "day" in command:  # Ask current date
    current_date = datetime.datetime.now().strftime("Today is %A, %B %d, %Y")  # Format date
    self.speak(current_date)  # Speak date
    return True  # Continue loop
```

## Command Routine Logic: Math Calculations
```python
math_indicators = ["plus", "minus", "times", "multiply", "divide", "divided by", "add", "subtract", 
                  "addition", "subtraction", "multiplication", "division", "power", "raised to", 
                  "square root", "root", "cube root", "factorial", "modulo", "mod", "remainder", "calculate", 
                  "solve", "compute", "find", "result", "answer", "what is", "how much is", "equals"]  # Keywords for math

# Check for math operations or numbers
if (any(indicator in command for indicator in math_indicators) or  # Keyword trigger
    any(char in command for char in "+-*/%**") or  # Operator characters
    re.search(r'\d+', command)):  # Check if command contains numbers
    
    result = self.handle_math(command)  # Delegate to math handler
    if result:  # If a result was produced
        self.speak(result)  # Speak the result
        return True  # Continue loop
```

## Command Routine Logic: Gemini AI Questions
```python
    if any(word in command for word in ["what", "who", "when", "where", "why", "how", "explain", "define", "tell me", "can you", "could you", "would you", "in detail", "more about", "information", "details", "explanation", "describe", "elaborate", "what is", "how to"]):
        answer = self.ask_gemini(command)  # Query Gemini for an answer
    if answer:  # If model returned an answer
        self.speak(answer)  # Speak the answer
    else:  # If no answer returned
        self.speak("I'm having trouble getting a response right now. Please try again.")  # Inform user
    return True  # Continue loop
```

## Command Routine Logic: Basic Response
```python
        basic_response = self._get_basic_response(command)  # Try canned responses
        if basic_response:  # If a basic response is applicable
            self.speak(basic_response)  # Speak it
            return True  # Continue loop

        # If nothing else matches, ask Gemini AI
        answer = self.ask_gemini(command)  # Fallback to model
        
        if answer:  # If we got an answer
            self.speak(answer)  # Speak it
        else:  # No answer
            self.speak("I couldn't get a response. Could you try rephrasing your question?")  # Ask for rephrase
        
        return True  # Continue loop
```

## Basic Response Method
```python
    def _get_basic_response(self, user_input):
        for key, responses in self.responses.items():
            if key in user_input:
                return random.choice(responses)
        return random.choice([
            "That's interesting! Tell me more.",
            "I'm here to help! What would you like to know?",
            "I'm connected to Gemini AI, so I can help with almost any question!",
            "Could you rephrase that or ask me something else?"
        ])
```


## Run Method
```python
    def run(self):
        print("\n" + "="*60)
        print("DEEPSPHERE VOICE ASSISTANT STARTED")
        print("Connected to Gemini AI")
        print("Say 'quit', 'exit', or 'goodbye' to stop")
        print("Continuous listening mode enabled")
        print("I can do math and answer any questions!")
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
```


## Main Function & Entry Point
```python
def main():
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"Failed to start: {e}")
        print("Check your libraries and API key.")

if __name__ == "__main__":
    main()
```

