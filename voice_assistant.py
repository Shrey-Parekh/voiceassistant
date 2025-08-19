"""
DeepSphere Voice Assistant
-------------------------

What it does:
- Listens to your voice through the microphone and turns speech into text
- Answers general questions by calling the Gemini AI HTTP API
- Speaks answers out loud using the computer's text-to-speech voice
- Handles simple math (e.g., "5 plus 7", "square root of 9")

How it works (high level):
1) `listen()` records audio and uses Google Speech Recognition to get text
2) `process_command()` decides what to do (time, date, math, or ask Gemini)
3) `ask_gemini()` sends the text to the Gemini API and returns the answer
4) `speak()` uses `pyttsx3` to read the answer aloud

Requirements:
- A working microphone
- Internet access for the Gemini API
- Python packages: pyttsx3, speech_recognition, requests

Setup tip:
- For security, store your Gemini API key in an environment variable and load it instead of hardcoding it.
"""
import datetime  # Provides date and time utilities
import math  # Provides mathematical functions and constants
import random  # Used to randomly choose from response lists
import re  # Regular expression operations for parsing text
import pyttsx3  # Text-to-speech engine for local voice output
import requests  # HTTP client for calling the Gemini API
import speech_recognition as sr  # Speech recognition for listening and transcription


class VoiceAssistant:  # Encapsulates all voice assistant behavior
    """A simple voice assistant that listens, understands, and speaks back.

    Responsibilities:
    - Convert microphone speech to text
    - Handle quick commands (time, date, math)
    - Ask Gemini AI for answers to general questions
    - Speak responses aloud via text-to-speech
    """

    def __init__(self):  # Constructor initializes subsystems
        """Create and initialize the assistant.

        Steps:
        1) Prepare core I/O components (microphone, recognizer, TTS)
        2) Configure API credentials/endpoints
        3) Load basic canned responses
        4) Greet the user and test connectivity to Gemini
        """
        self._setup_core_components()  # Initialize recognizer, mic, TTS, and voice
        self._setup_apis()  # Configure API keys and endpoints
        self._setup_responses()  # Prepare basic canned responses
        self._initialize_assistant()  # Greet user and test external services

    def _setup_core_components(self):  # Prepare core I/O and state
        """Initialize microphone, recognizer, TTS, name, and voice.

        No arguments. Sets attributes on `self` used by other methods.
        """
        self.recognizer = sr.Recognizer()  # Create a speech recognizer instance
        self.microphone = sr.Microphone()  # Select default system microphone
        self.tts_engine = pyttsx3.init()  # Initialize text-to-speech engine
        self.assistant_name = "DeepSphere"  # Set assistant's display name
        self._configure_voice()  # Configure TTS voice, rate, and volume

    def _setup_apis(self):  # Configure external API credentials
        """Configure API key and endpoint for Gemini.

        Tip: Prefer loading `self.gemini_api_key` from an environment variable.
        """
        self.gemini_api_key = "AIzaSyBVbzio3hQ6-Vr69n1wO_KmKAavAyB7X1M"  # Google Gemini API key (should be secured)
        self.gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"  # Gemini model endpoint

    def _setup_responses(self):  # Define simple, hardcoded responses
        """Build a dictionary of simple triggers to friendly responses."""
        self.responses = {  # Mapping of trigger phrases to response options
            "hello": ["Hello! How can I help you today?", "Hi there!", "Hello! Nice to meet you!"],  # Greetings
            "how are you": ["I'm doing great, thank you for asking!", "I'm fine, how about you?"],  # Status replies
            "what is your name": [f"I'm {self.assistant_name}, your personal voice assistant!", f"You can call me {self.assistant_name}.", f"I'm {self.assistant_name}."],  # Name introduction
            "goodbye": ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"],  # Farewells
            "thank you": ["You're welcome!", "Happy to help!", "No problem!"],  # Polite acknowledgements
        }

    def _initialize_assistant(self):  # Announce readiness and verify API connectivity
        """Greet the user and run a quick Gemini connectivity test."""
        print("DeepSphere initialized successfully!")  # Log initialization success
        self.speak(f"Hello! I'm {self.assistant_name}. How can I help you today?")  # Speak greeting
        self._test_gemini_connection()  # Quick API connectivity check

    def _configure_voice(self):  # Pick a pleasant voice and tune speaking parameters
        """Choose a preferred TTS voice and tune rate/volume.

        The code tries to find a familiar voice by name, then sets speed and volume.
        """
        voices = self.tts_engine.getProperty('voices')  # Retrieve available TTS voices
        print(f"Found {len(voices)} voices")  # Log how many voices are available
        priority_voices = ['zira', 'samantha', 'hazel', 'david', 'mark', 'alex', 'victoria']  # Preferred voice names
        for voice in voices:  # Iterate over available voices
            name = (voice.name or "").lower()  # Normalize voice name to lowercase
            if any(priority in name for priority in priority_voices):  # Select first preferred voice
                self.tts_engine.setProperty('voice', voice.id)  # Set TTS to chosen voice
                print(f"Using: {voice.name}")  # Log chosen voice
                break  # Stop searching after finding a match
        self.tts_engine.setProperty('rate', 200)  # Set speech rate (words per minute)
        self.tts_engine.setProperty('volume', 1.0)  # Set maximum volume

    def _test_gemini_connection(self):  # Sanity-check the Gemini API
        """Send a tiny test prompt to verify the API is reachable and responding."""
        print("Testing Gemini API connection...")  # Indicate test start
        if self.ask_gemini("Say hello in one sentence"):  # Make a simple test request
            print("Gemini API connected successfully!")  # Success message
        else:  # If no response
            print("Gemini API connection failed - check your API key")  # Failure message

    def speak(self, text):  # Convert text to audio and print to console
        """Speak text out loud and also print it to the console.

        Args:
            text: The message to speak.
        """
        print(f"Assistant: {text}")  # Console log of the spoken text
        self.tts_engine.say(text)  # Queue text for speech
        self.tts_engine.runAndWait()  # Block until speech finishes

    def listen(self):  # Capture audio from microphone and transcribe to text
        """Listen from the microphone and return recognized lowercase text.

        Returns:
            Recognized text as a string, or None if nothing was recognized.

        Notes:
            - `timeout` is how long we wait for speech to start
            - `phrase_limit` caps how long we record once speech begins
            - `pause_threshold` controls how much silence ends the phrase
        """
        timeout = 30  # Max seconds to wait for speech to start
        phrase_limit = 60  # Max duration of a phrase in seconds
        threshold = 200  # Initial energy threshold for detecting speech
        pause_threshold = 1.5  # Seconds of silence that end a phrase
        try:  # Protect the listening block from runtime errors
            with self.microphone as source:  # Open microphone stream
                print("Listening for input...")  # Prompt user to speak
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)  # Calibrate to ambient noise
                
                self.recognizer.energy_threshold = threshold  # Set custom energy threshold
                self.recognizer.dynamic_energy_threshold = True  # Enable adaptive thresholding
                self.recognizer.pause_threshold = pause_threshold  # Configure pause duration

                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)  # Record audio

            print("Processing speech...")  # Indicate transcription begins
            text = self.recognizer.recognize_google(audio).lower()  # Use Google Speech API to recognize speech
            print(f"You said: {text}")  # Echo recognized text
            return text  # Return the recognized text

        except sr.WaitTimeoutError:  # No speech detected before timeout
            print("No speech detected within timeout period")  # Inform about timeout
            return None  # Return no result
        except sr.UnknownValueError:  # Speech could not be understood
            error_msg = "I couldn't understand that clearly. Please try again with clearer speech."  # Feedback message
            print("Speech was unclear - please try again")  # Log the issue
            self.speak(error_msg)  # Speak feedback
            return None  # Return no result
        except sr.RequestError as e:  # Recognition service error
            print(f"Speech recognition service error: {e}")  # Log service error details
            self.speak("Sorry, I'm having trouble with the speech recognition service.")  # Inform user
            return None  # Return no result
        except Exception as e:  # Any other unexpected error
            print(f"Error during listening: {e}")  # Log error
            self.speak("Sorry, something went wrong while listening. Please try again.")  # Inform user
            return None  # Return no result

    def ask_gemini(self, prompt, context=""):  # Send a prompt to Gemini and return the text answer
        """Call the Gemini API with a question and return the answer text.

        Args:
            prompt: The user's question or instruction.
            context: Optional extra instructions or background to prepend.

        Returns:
            A string answer from Gemini, or None if the call fails or has no text.
        """
        try:  # Wrap network call with error handling
            full_prompt = f"You are a helpful AI assistant. {context}\nQuestion: {prompt}\nPlease provide a clear, helpful, and natural response:"  # Construct instruction-rich prompt
            payload = {  # Request payload per Gemini API spec
                "contents": [{"parts": [{"text": full_prompt}]}],  # Provide text content
                "generationConfig": {  # Control generation behavior
                    "temperature": 0.7,  # Creativity level
                    "maxOutputTokens": 500,  # Max response length
                    "topP": 0.8,  # Nucleus sampling parameter
                    "topK": 40  # Top-K sampling parameter
                }
            }
            headers = {"Content-Type": "application/json"}  # JSON request header
            response = requests.post(  # Perform HTTP POST to Gemini API
                f"{self.gemini_api_url}?key={self.gemini_api_key}",  # Endpoint with API key in query
                json=payload,  # Send JSON body
                headers=headers,  # Set headers
                timeout=30  # Timeout in seconds
            )
            if response.ok:  # HTTP status indicates success
                data = response.json()  # Parse JSON response
                if "candidates" in data and data["candidates"]:  # Check for candidates array
                    candidate = data["candidates"][0]  # Take the first candidate
                    if "content" in candidate and "parts" in candidate["content"]:  # Ensure structure exists
                        answer = candidate["content"]["parts"][0]["text"].strip()  # Extract text answer
                        print(f"Gemini Response: {answer[:100]}...")  # Log preview of the answer
                        return answer  # Return full answer text
                else:  # Unexpected structure or empty candidates
                    print(f"Gemini API error: {data}")  # Log API error payload
            else:  # Non-2xx HTTP status
                print(f"Gemini API request failed: {response.status_code} - {response.text}")  # Log failure details
            
            return None  # No valid answer

        except Exception as e:  # Network or parsing error
            print(f"Gemini API request failed: {e}")  # Log exception
            return None  # Return no answer

    def handle_math(self, command):  # Parse and compute math-related requests
        """Parse simple math in natural language or symbols and compute a result.

        Supports:
        - Square root, cube root, factorial, exponentiation
        - Addition, subtraction, multiplication, division, modulo
        - Direct expressions like "5 + 3 * 2" (basic sanitization applied)

        Args:
            command: The raw text of the user's math request.

        Returns:
            A friendly result string, or guidance if the intent is unclear.
        """
        try:  # Guard against parsing or math errors
            expr = command.lower().strip()  # Normalize input text
            print(f"Processing math command: {expr}")  # Log the expression being handled

            # Handle special functions first
            # Square root
            if "square root" in expr or "root" in expr:  # Detect square root requests
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers (including decimals)
                if numbers:  # Ensure a number was found
                    number = float(numbers[0])  # Parse the first number
                    result = math.sqrt(number)  # Compute square root
                    return f"The square root of {number} is {result:.4f}"  # Return formatted result

            # Cube root
            if "cube root" in expr:  # Detect cube root requests
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if numbers:  # Ensure a number was found
                    number = float(numbers[0])  # Parse the first number
                    result = number ** (1/3)  # Compute cube root
                    return f"The cube root of {number} is {result:.4f}"  # Return formatted result

            # Factorial
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

            # Power/Exponent
            if any(word in expr for word in ["power", "raised to", "to the power"]):  # Detect exponentiation
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need base and exponent
                    base = float(numbers[0])  # Parse base
                    exponent = float(numbers[1])  # Parse exponent
                    result = base ** exponent  # Compute power
                    return f"{base} to the power of {exponent} is {result}"  # Return result

            # Basic arithmetic operations
            # Addition
            if any(word in expr for word in ["plus", "add", "addition"]):  # Detect addition
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = float(numbers[0])  # First operand
                    num2 = float(numbers[1])  # Second operand
                    result = num1 + num2  # Compute sum
                    return f"{num1} plus {num2} equals {result}"  # Return result

            # Subtraction
            if any(word in expr for word in ["minus", "subtract", "subtraction"]):  # Detect subtraction
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = float(numbers[0])  # Minuend
                    num2 = float(numbers[1])  # Subtrahend
                    result = num1 - num2  # Compute difference
                    return f"{num1} minus {num2} equals {result}"  # Return result

            # Multiplication
            if any(word in expr for word in ["times", "multiply", "multiplication"]):  # Detect multiplication
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = float(numbers[0])  # Multiplicand
                    num2 = float(numbers[1])  # Multiplier
                    result = num1 * num2  # Compute product
                    return f"{num1} times {num2} equals {result}"  # Return result

            # Division
            if any(word in expr for word in ["divided by", "divide", "division"]):  # Detect division
                numbers = re.findall(r'\d+(?:\.\d+)?', expr)  # Extract numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = float(numbers[0])  # Dividend
                    num2 = float(numbers[1])  # Divisor
                    if num2 == 0:  # Guard against division by zero
                        return "Cannot divide by zero"  # Inform user
                    result = num1 / num2  # Compute quotient
                    return f"{num1} divided by {num2} equals {result:.4f}"  # Return result with 4 decimals

            # Modulo
            if any(word in expr for word in ["modulo", "mod", "remainder"]):  # Detect modulus operation
                numbers = re.findall(r'\d+', expr)  # Extract integer numbers
                if len(numbers) >= 2:  # Need two operands
                    num1 = int(numbers[0])  # Dividend
                    num2 = int(numbers[1])  # Divisor
                    if num2 == 0:  # Cannot modulo by zero
                        return "Cannot divide by zero"  # Inform user
                    result = num1 % num2  # Compute remainder
                    return f"The remainder when {num1} is divided by {num2} is {result}"  # Return result

            # Try to extract simple expressions with operators
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

        except Exception as e:  # Catch unexpected errors
            print(f"Math calculation error: {e}")  # Log error
            return f"Sorry, I couldn't calculate that. Error: {str(e)}"  # Inform user

    def process_command(self, command):  # Route a user's command to the right handler
        """Decide what to do with recognized text and act on it.

        Flow:
        1) Exit if the user said a stop word
        2) Tell time/date if asked
        3) Detect and solve math
        4) For general questions, ask Gemini; otherwise try a basic friendly reply

        Returns:
            False only when the user asks to quit; True otherwise.
        """
        if not command:  # Ignore empty inputs
            return True  # Continue loop

        command = command.lower().strip()  # Normalize input for matching

        # Exit commands
        if any(word in command for word in ["quit", "exit", "goodbye", "bye", "stop"]):  # Check for exit intent
            self.speak("Goodbye! Have a great day!")  # Say goodbye
            return False  # Signal to stop main loop

        # Time and date
        if "time" in command and ("what" in command or "tell" in command):  # Ask current time
            current_time = datetime.datetime.now().strftime("It's %I:%M %p")  # Format time
            self.speak(current_time)  # Speak time
            return True  # Continue loop

        if "date" in command or "day" in command:  # Ask current date
            current_date = datetime.datetime.now().strftime("Today is %A, %B %d, %Y")  # Format date
            self.speak(current_date)  # Speak date
            return True  # Continue loop

        # Math calculations
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

        # All other questions go to Gemini AI
        if any(word in command for word in ["what", "who", "when", "where", "why", "how", "explain",  # Broad Q/A triggers
                                          "define", "tell me", "can you", "could you", "would you", 
                                          "in detail", "more about", "information", "details", 
                                          "explanation", "describe", "elaborate", "what is", "how to"]):
            
            answer = self.ask_gemini(command)  # Query Gemini for an answer
            
            if answer:  # If model returned an answer
                self.speak(answer)  # Speak the answer
            else:  # If no answer returned
                self.speak("I'm having trouble getting a response right now. Please try again.")  # Inform user
            return True  # Continue loop

        # Basic responses for greetings and simple commands
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

    def _get_basic_response(self, user_input):  # Try to match simple, friendly replies
        """Return a friendly canned response when the input matches a simple trigger."""
        for key, responses in self.responses.items():  # Iterate trigger-response pairs
            if key in user_input:  # If the trigger appears in input
                return random.choice(responses)  # Return a random canned response

        return random.choice([  # Fallback generic responses
            "That's interesting! Tell me more.",
            "I'm here to help! What would you like to know?",
            "I'm connected to Gemini AI, so I can help with almost any question!",
            "Could you rephrase that or ask me something else?"
        ])

    def run(self):  # Continuous loop to listen and respond
        """Main loop: listen, process, and speak until the user exits.

        Press Ctrl+C in the terminal to interrupt and exit.
        """
        print("\n" + "="*60)  # Visual separator
        print("DEEPSPHERE VOICE ASSISTANT STARTED")  # Startup banner
        print("Connected to Gemini AI")  # Indicate API connectivity
        print("Say 'quit', 'exit', or 'goodbye' to stop")  # Show exit instructions
        print("Continuous listening mode enabled")  # Inform about mode
        print("I can do math and answer any questions!")  # Features summary
        print("="*60 + "\n")  # Closing separator

        while True:  # Main loop
            try:  # Protect loop from runtime exceptions
                user_input = self.listen()  # Capture user speech

                if user_input:  # If we recognized some text
                    result = self.process_command(user_input)  # Handle the command

                    if result == False:  # If told to exit
                        break  # Break out of loop

            except KeyboardInterrupt:  # User pressed Ctrl+C
                print("\nShutting down...")  # Log shutdown
                self.speak("Goodbye!")  # Say goodbye
                break  # Exit loop
            except Exception as e:  # Any unexpected error
                print(f"Error: {e}")  # Log error details
                self.speak("Sorry, something went wrong. Let's try again.")  # Inform user
def main():  # Entry point to start the voice assistant
    """Create the assistant and start the interactive session."""
    try:  # Guard assistant startup
        assistant = VoiceAssistant()  # Instantiate the assistant
        assistant.run()  # Begin the main interaction loop
    except Exception as e:  # On startup failure
        print(f"Failed to start: {e}")  # Log the error
        print("Check your libraries and API key.")  # Suggest remediation


if __name__ == "__main__":  # Run only when executed as a script
    main()  # Call the entry point