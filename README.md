# DeepSphere Voice Assistant

A Python-based voice assistant that uses Google's Gemini AI to answer questions, perform mathematical calculations, and provide basic utility functions through natural voice commands.

## 🌟 Features

### 🤖 AI Integration
- **Gemini AI Powered**: All questions are automatically sent to Gemini AI for intelligent responses
- **Natural Language Processing**: Understands complex questions and provides detailed answers
- **Pre-configured API**: Already set up with a working Gemini API key

### 🎤 Voice Processing
- **High-Quality Speech Recognition**: Uses Google Speech Recognition API for accurate transcription
- **Natural Text-to-Speech**: Uses pyttsx3 for local text-to-speech with automatic voice selection
- **Noise Filtering**: Real-time microphone capture with ambient noise adjustment
- **Continuous Listening**: 30-second timeout with 60-second phrase limit for longer questions

### 🧮 Mathematical Capabilities
- **Basic Operations**: Addition, subtraction, multiplication, division, modulo
- **Advanced Math**: Power (x^y), square root, cube root, factorial
- **Natural Language Math**: "What's 5 plus 3" or "calculate the square root of 16"
- **Direct Expressions**: Handles simple expressions like "5 + 3 * 2"

### ⏰ Utility Functions
- **Time/Date**: Current time and date information
- **Basic Responses**: Greetings, farewells, and simple interactions
- **System Integration**: Works with any microphone and speaker setup

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Microphone access
- Internet connection for Gemini AI and speech recognition

### Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test your setup** (recommended):
   ```bash
   python test_setup.py
   ```

4. **Run the assistant**:
   ```bash
   python voice_assistant.py
   ```

### Alternative Launch Methods

**Windows**: Double-click `run_assistant.bat`
**Mac/Linux**: Run `./run_assistant.sh` in terminal

## 🎯 Usage Examples

### Basic Questions (Automatically sent to Gemini AI)
- "What is the capital of France?"
- "How does photosynthesis work?"
- "Explain quantum computing"
- "What are the benefits of exercise?"
- "Tell me about artificial intelligence"

### Mathematical Calculations
- "What's 15 plus 27?"
- "Calculate 8 times 9"
- "What is the square root of 144?"
- "What's 5 to the power of 3?"
- "Calculate the factorial of 6"
- "What's 10 divided by 3?"
- "What's the remainder when 17 is divided by 5?"

### Utility Commands
- "What time is it?"
- "What day is today?"
- "Hello" or "Hi"
- "What is your name?"
- "How are you?"

### Voice Commands
- "Quit", "Exit", "Goodbye", or "Bye" - Exit the assistant

## 🔧 Configuration

### Voice Settings
The assistant automatically detects and configures the best available voice on your system. It prioritizes voices like Zira, Samantha, Hazel, David, Mark, Alex, and Victoria.

### API Configuration
- **Gemini AI**: Already configured with the provided API key
- **Speech Recognition**: Uses Google Speech Recognition API (requires internet)

### Listening Settings
- **Timeout**: 30 seconds to wait for speech to start
- **Phrase Limit**: 60 seconds maximum recording duration
- **Pause Threshold**: 1.5 seconds of silence ends recording

## 🛠️ Technical Details

### Core Technologies
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: pyttsx3 (cross-platform TTS)
- **AI Integration**: Google Gemini 2.0 Flash API
- **Audio Processing**: PyAudio for microphone input

### Architecture
- **Modular Design**: Separate methods for different command types
- **Error Handling**: Comprehensive error handling for all operations
- **Voice Configuration**: Automatic voice selection and configuration
- **Math Processing**: Natural language math parsing and evaluation

### Performance Features
- **Dynamic Energy Threshold**: Automatically adjusts to ambient noise
- **Timeout Management**: Configurable listening timeouts
- **Voice Optimization**: Automatic voice selection and rate/volume tuning

## 🐛 Troubleshooting

### Common Issues

1. **Microphone not working**:
   - Check microphone permissions
   - Ensure PyAudio is properly installed
   - Try different microphone input devices

2. **Speech recognition issues**:
   - Speak clearly and at normal volume
   - Reduce background noise
   - Check internet connection (required for Google Speech Recognition)

3. **Gemini AI not responding**:
   - Verify internet connection
   - Check if the API key is valid
   - Ensure the API endpoint is accessible

4. **Installation problems**:
   - Use Python 3.7+ 
   - Install Visual C++ build tools on Windows (for PyAudio)
   - Try `pip install --upgrade pip` before installing requirements

### Performance Tips
- Speak clearly and at a consistent pace
- Keep the microphone at a consistent distance
- Minimize background noise
- The assistant handles longer questions automatically

## 🔒 Privacy and Security

- **Local Processing**: Text-to-speech runs locally
- **API Communication**: Only sends text queries to Gemini AI and Google Speech Recognition
- **No Recording**: No audio is stored or transmitted
- **No Memory**: Conversations are not stored between sessions

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the assistant!

## 📞 Support

If you encounter any issues or have questions:
1. Run `python test_setup.py` to diagnose problems
2. Check the troubleshooting section
3. Review the error messages in the console
4. Ensure all dependencies are properly installed
5. Verify your internet connection

---

**Enjoy your AI-powered voice assistant! 🎉**