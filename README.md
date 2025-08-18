# AI Voice Assistant with Gemini AI Integration

A powerful voice assistant that connects to Google's Gemini AI to answer any questions, perform calculations, and provide various utilities through natural voice commands.

## 🌟 Features

### 🤖 AI Integration
- **Gemini AI Powered**: All questions are automatically sent to Gemini AI for intelligent responses
- **Natural Language Processing**: Understands complex questions and provides detailed answers
- **Context Awareness**: Remembers previous conversations for better context

### 🎤 Voice Processing
- **High-Quality Speech Recognition**: Handles long speech prompts (up to 2-3 minutes)
- **Natural Text-to-Speech**: Uses high-quality TTS for human-like responses
- **Noise Filtering**: Real-time microphone capture with ambient noise adjustment
- **Continuous Listening Mode**: Switch between normal and extended listening modes

### 🧮 Mathematical Capabilities
- **Basic Operations**: Addition, subtraction, multiplication, division
- **Advanced Math**: Power (x^y), square root, cube root, nth root
- **Scientific Functions**: Trigonometry (sine, cosine, tangent), logarithms
- **Natural Language Math**: "What's 5 plus 3" or "calculate the square root of 16"

### ⏰ Utility Functions
- **Timer/Stopwatch**: Set timers with voice commands ("Set timer for 10 minutes")
- **Weather Information**: Current weather and forecasts for any city
- **Time/Date**: Current time, date, and timezone information
- **System Commands**: Volume control, system information, open browser
- **News Headlines**: Get current news and headlines

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Microphone access
- Internet connection for Gemini AI and weather services

### Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys** (optional for enhanced features):
   ```bash
   # For weather information
   set OPENWEATHER_API_KEY=your_openweather_api_key
   
   # For news headlines
   set NEWS_API_KEY=your_news_api_key
   ```

4. **Run the assistant**:
   ```bash
   python voice_assistant.py
   ```

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

### Weather Information
- "What's the weather in London?"
- "Temperature in New York"
- "Weather forecast for Tokyo"

### Timer and Stopwatch
- "Set timer for 5 minutes"
- "Start stopwatch"
- "Stop stopwatch"

### System Commands
- "What's the system information?"
- "Open web browser"
- "What time is it?"
- "What day is today?"

### Voice Commands
- "Continuous listening" - Switch to extended listening mode
- "Normal listening" - Switch to standard listening mode
- "Quit" or "Goodbye" - Exit the assistant
- "Clear memory" - Clear conversation history

## 🔧 Configuration

### Voice Settings
The assistant automatically detects and configures the best available voice on your system. You can modify voice settings in the `_configure_voice()` method.

### API Configuration
- **Gemini AI**: Already configured with the provided API key
- **Weather API**: Set `OPENWEATHER_API_KEY` environment variable
- **News API**: Set `NEWS_API_KEY` environment variable

### Listening Modes
- **Normal Mode**: 15-second timeout, 30-second phrase limit
- **Continuous Mode**: 30-second timeout, 60-second phrase limit

## 🛠️ Technical Details

### Core Technologies
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: pyttsx3 (cross-platform TTS)
- **AI Integration**: Google Gemini 2.0 Flash API
- **Audio Processing**: PyAudio for microphone input

### Architecture
- **Modular Design**: Separate handlers for different command types
- **Error Handling**: Comprehensive error handling for all operations
- **Memory Management**: Intelligent conversation memory with topic categorization
- **Background Processing**: Timers and long-running tasks run in background threads

### Performance Features
- **Dynamic Energy Threshold**: Automatically adjusts to ambient noise
- **Timeout Management**: Configurable listening timeouts
- **Memory Optimization**: Limited conversation memory to prevent memory bloat

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
- Use continuous listening mode for longer questions
- Speak clearly and at a consistent pace
- Keep the microphone at a consistent distance
- Minimize background noise

## 🔒 Privacy and Security

- **Local Processing**: Speech recognition and TTS run locally
- **API Communication**: Only sends text queries to Gemini AI
- **No Recording**: No audio is stored or transmitted
- **Memory**: Conversation history is stored locally and can be cleared

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the assistant!

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review the error messages in the console
3. Ensure all dependencies are properly installed
4. Verify your API keys and internet connection

---

**Enjoy your AI-powered voice assistant! 🎉**