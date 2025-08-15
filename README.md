# Personal Voice Assistant Workshop

A beginner-friendly Python voice assistant that can answer questions, play music, tell time, and respond to voice commands.

## Features

- 🎤 **Voice Recognition**: Converts speech to text
- 🔊 **Text-to-Speech**: Responds with natural voice
- 🎵 **Music Player**: Plays local music files
- ⏰ **Time & Date**: Tells current time and date
- 💬 **Simple Chatbot**: Answers basic questions
- 🌤️ **Weather Info**: Demo weather feature (extensible)
- 🧠 **LLM Answers**: Route open-ended questions to Gemini 2.0 Flash API
- 🧮 **Math Calculator**: Handles basic arithmetic operations
- 😄 **Jokes & Fun Facts**: Entertainment features
- 🎲 **Games**: Coin flip and dice roll
- ⏱️ **Timer**: Set countdown timers

## Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Music (Optional)

Create a `music` folder and add some MP3 or WAV files:

```
project/
├── voice_assistant.py
├── music/
│   ├── song1.mp3
│   ├── song2.mp3
│   └── song3.wav
```

### 3. Run the Assistant

```bash
python voice_assistant.py
```

### 4. (Optional) Enable Open‑Ended Answers with Gemma 3N API

The assistant now uses Google's Gemma 3N API by default for answering open-ended questions. The API key is already configured, but you can customize it if needed.

1) **Default Setup**: The assistant is ready to use with Gemma 3N API out of the box.

2) **Customize API Key** (optional): If you want to use your own API key:
```powershell
# PowerShell (Windows)
$env:GEMMA_API_KEY = "your_api_key_here"
```
```bash
# Bash (macOS/Linux)
export GEMMA_API_KEY="your_api_key_here"
```

Now, when you ask open-ended questions (e.g., "What is photosynthesis?"), the assistant will use Gemma 3N API to provide intelligent, contextual answers.

## How to Use

Once running, you can say:

- **"What time is it?"** - Get current time
- **"What's the date?"** - Get current date  
- **"Play music"** - Play a random song from music folder
- **"Stop music"** - Stop currently playing music
- **"Hello"** - Basic conversation
- **"How are you?"** - Chatbot response
- **"Tell me a joke"** - Get a random joke
- **"Fun fact"** - Learn something interesting
- **"Flip coin"** - Virtual coin flip
- **"Roll dice"** - Roll a virtual dice
- **"Set timer for 30 seconds"** - Set a countdown timer
- **"What is 15 plus 27?"** - Math calculations
- **"Calculate 8 times 6"** - More math operations
- **"What is machine learning?"** - AI-powered answers
- **"Goodbye"** - Exit the program

## Installation Troubleshooting

### Windows Users

If you get PyAudio installation errors:

```bash
pip install pipwin
pipwin install pyaudio
```

Or download PyAudio wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### macOS Users

```bash
brew install portaudio
pip install pyaudio
```

### Linux Users

```bash
sudo apt-get install python3-pyaudio
# or
sudo apt-get install portaudio19-dev python3-pyaudio
```

## Code Structure Explanation

### Main Components

1. **VoiceAssistant Class**: Core functionality
2. **Speech Recognition**: Converts voice to text using Google's API
3. **Text-to-Speech**: Uses pyttsx3 for offline voice synthesis
4. **Music Player**: Uses pygame for audio playback
5. **Chatbot Logic**: Simple pattern matching for responses

### Key Methods

- `listen()`: Captures and processes voice input
- `speak()`: Converts text to speech output
- `process_command()`: Determines what action to take
- `simple_chatbot()`: Handles conversational responses

## Workshop Teaching Points

### Beginner Concepts Covered

1. **Object-Oriented Programming**: Class structure and methods
2. **Exception Handling**: Try/catch blocks for error management
3. **File Operations**: Working with files and directories
4. **API Integration**: Using external libraries
5. **Control Flow**: Loops, conditionals, and program flow

### Code Walkthrough (30 minutes)

1. **Imports and Setup** (5 min)
   - Explain each library's purpose
   - Show how imports work

2. **Class Initialization** (10 min)
   - Constructor method `__init__`
   - Setting up speech recognition and TTS
   - Creating the music folder

3. **Core Methods** (10 min)
   - `listen()` method breakdown
   - `speak()` method explanation
   - Error handling examples

4. **Command Processing** (5 min)
   - How commands are parsed
   - Pattern matching logic

### Hands-On Activities (90 minutes)

1. **Basic Setup** (20 min)
   - Install dependencies
   - Run the basic version
   - Test voice recognition

2. **Customization** (30 min)
   - Add new responses to chatbot
   - Modify voice settings
   - Add music files

3. **Feature Extensions** (40 min)
   - Add new voice commands
   - Implement simple calculations
   - Create custom responses

## Extension Ideas

### Easy Extensions (15-30 minutes each)

1. **Calculator Feature**
```python
def calculate(self, expression):
    try:
        # Simple math evaluation
        result = eval(expression.replace("plus", "+").replace("minus", "-"))
        return f"The answer is {result}"
    except:
        return "Sorry, I couldn't calculate that"
```

2. **Joke Teller**
```python
def tell_joke(self):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
    ]
    return random.choice(jokes)
```

3. **Timer Feature**
```python
def set_timer(self, seconds):
    import time
    self.speak(f"Timer set for {seconds} seconds")
    time.sleep(seconds)
    self.speak("Time's up!")
```

### Advanced Extensions (45+ minutes)

1. **Web Search Integration**
2. **Email Sending Capability**  
3. **Smart Home Control (with APIs)**
4. **Language Translation**
5. **News Headlines Fetcher**

## Common Issues & Solutions

### "Module not found" errors
- Make sure all packages are installed: `pip install -r requirements.txt`

### Microphone not working
- Check system microphone permissions
- Test with: `python -m speech_recognition`

### No audio output
- Check system volume and audio drivers
- Test TTS separately: `import pyttsx3; engine = pyttsx3.init(); engine.say("test"); engine.runAndWait()`

### Music not playing
- Ensure music files are in the `music/` folder
- Check file formats (MP3, WAV supported)
- Verify pygame installation

## Learning Resources

- [Python Speech Recognition Documentation](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3 Text-to-Speech Guide](https://pypi.org/project/pyttsx3/)
- [Pygame Audio Tutorial](https://www.pygame.org/docs/ref/mixer.html)

## Workshop Timeline (3 hours)

- **Hour 1**: Setup, installation, and basic code walkthrough
- **Hour 2**: Hands-on coding and customization
- **Hour 3**: Extensions and troubleshooting

Perfect for beginners who want to build something cool and functional!