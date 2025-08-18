# 🚀 AI Voice Assistant - Complete Setup Guide

This guide will walk you through setting up your AI Voice Assistant step by step.

## 📋 What You'll Get

Your voice assistant will have these capabilities:
- **🤖 Gemini AI Integration**: Ask any question and get intelligent answers
- **🎤 Voice Commands**: Natural speech recognition and text-to-speech
- **🧮 Math Calculator**: Handle complex mathematical expressions
- **⏰ Timer & Stopwatch**: Set timers and track time
- **🌤️ Weather Information**: Get current weather for any city
- **📰 News Headlines**: Stay updated with current events
- **💻 System Commands**: Get system information and control

## 🛠️ Installation Steps

### Step 1: Install Python
1. Download Python 3.7+ from [python.org](https://python.org)
2. During installation, **check "Add Python to PATH"**
3. Verify installation: Open terminal/command prompt and type `python --version`

### Step 2: Download the Project
1. Download all files to a folder on your computer
2. Open terminal/command prompt in that folder

### Step 3: Install Dependencies
```bash
# Windows
pip install -r requirements.txt

# Mac/Linux
pip3 install -r requirements.txt
```

### Step 4: Test Your Setup
```bash
# Windows
python test_setup.py

# Mac/Linux
python3 test_setup.py
```

This will test all components and tell you if anything needs fixing.

## 🎯 Quick Start

### Option 1: Use the Launcher (Recommended)
- **Windows**: Double-click `run_assistant.bat`
- **Mac/Linux**: Double-click `run_assistant.sh` (or run `./run_assistant.sh` in terminal)

### Option 2: Manual Start
```bash
# Windows
python voice_assistant.py

# Mac/Linux
python3 voice_assistant.py
```

## 🔑 API Keys (Optional)

### Weather API (OpenWeatherMap)
1. Go to [OpenWeatherMap](https://home.openweathermap.org/api_keys)
2. Sign up for free account
3. Get your API key
4. Set environment variable: `OPENWEATHER_API_KEY=your_key_here`

### News API
1. Go to [NewsAPI](https://newsapi.org/)
2. Sign up for free account
3. Get your API key
4. Set environment variable: `NEWS_API_KEY=your_key_here`

**Note**: The Gemini AI key is already configured in the code!

## 🎤 First Use

1. **Start the assistant** using one of the methods above
2. **Allow microphone access** when prompted
3. **Speak clearly** - try saying "Hello"
4. **Ask questions** like "What's the weather in London?"
5. **Use commands** like "Set timer for 5 minutes"

## 🗣️ Voice Commands

### Basic Commands
- "Hello" → Greeting
- "What time is it?" → Current time
- "What day is today?" → Current date
- "Quit" or "Goodbye" → Exit

### Math Operations
- "What's 15 plus 27?" → "The answer is 42"
- "Calculate the square root of 144" → "The answer is 12.0"
- "What's 5 to the power of 3?" → "The answer is 125"

### AI Questions (Go to Gemini)
- "What is the capital of France?"
- "How does photosynthesis work?"
- "Explain quantum computing"
- "What are the benefits of exercise?"

### Utility Commands
- "Set timer for 10 minutes"
- "What's the weather in New York?"
- "Tell me the news"
- "System information"

### Listening Mode
- **Continuous listening mode** - Handles longer speech inputs automatically

## 🐛 Troubleshooting

### Common Issues

#### 1. "No module named 'pyaudio'"
**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Mac:**
```bash
brew install portaudio
pip3 install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-pyaudio
```

#### 2. Microphone not working
- Check microphone permissions in system settings
- Ensure microphone is set as default input device
- Try different microphone input devices

#### 3. Speech recognition issues
- Speak clearly and at normal volume
- Reduce background noise
- Check internet connection (required for Google Speech Recognition)

#### 4. Gemini AI not responding
- Verify internet connection
- Check if the API key is valid
- Ensure the API endpoint is accessible

### Performance Tips
- Use in quiet environments
- Speak clearly and at consistent pace
- The assistant automatically handles longer questions
- Keep microphone at consistent distance

## 🔧 Customization

### Voice Settings
Edit `voice_assistant.py` and modify the `_configure_voice()` method:
```python
self.tts_engine.setProperty('rate', 150)      # Speed (words per minute)
self.tts_engine.setProperty('volume', 1.0)    # Volume (0.0 to 1.0)
```

### Configuration File
1. Copy `config.py` to `config_local.py`
2. Modify values in `config_local.py`
3. Update `voice_assistant.py` to import from `config_local`

## 📱 Advanced Features

### Memory Management
- The assistant remembers your conversations
- Say "memory" to see conversation history
- Say "clear memory" to forget everything

### Background Timers
- Set multiple timers simultaneously
- Timers run in background while you chat
- Get voice notifications when timers finish

### Topic Classification
- Conversations are automatically categorized
- AI responses use context from previous chats
- Better, more relevant answers over time

## 🎓 Learning Resources

### For Beginners
- Start with simple questions
- Practice with basic commands
- Use the test script to understand what works

### For Developers
- Code is well-commented and modular
- Easy to add new features
- Clean API integration patterns

## 🆘 Getting Help

1. **Check the test script**: `python test_setup.py`
2. **Review error messages**: Look at console output
3. **Check dependencies**: Ensure all packages are installed
4. **Verify API keys**: Check environment variables
5. **Test microphone**: Use system sound settings

## 🎉 Success!

Once everything is working, you'll have:
- A powerful AI voice assistant
- Natural conversation capabilities
- Mathematical and utility functions
- Professional-grade voice processing

**Enjoy your AI-powered voice assistant! 🚀**

---

**Need more help?** Check the main README.md file for detailed documentation.
