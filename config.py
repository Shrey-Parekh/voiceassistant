# Configuration file for AI Voice Assistant
# Copy this file to config_local.py and modify the values

# Gemini AI Configuration (Already configured)
GEMINI_API_KEY = "AIzaSyBVbzio3hQ6-Vr69n1wO_KmKAavAyB7X1M"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Weather API Configuration (Optional - for weather features)
# Get your free API key from: https://home.openweathermap.org/api_keys
OPENWEATHER_API_KEY = "your_openweather_api_key_here"

# News API Configuration (Optional - for news features)
# Get your free API key from: https://newsapi.org/
NEWS_API_KEY = "your_news_api_key_here"

# Voice Assistant Settings
ASSISTANT_NAME = "AI Voice Assistant"
DEFAULT_VOICE_RATE = 150  # Words per minute
DEFAULT_VOICE_VOLUME = 1.0  # 0.0 to 1.0

# Listening Settings
NORMAL_TIMEOUT = 15  # seconds
CONTINUOUS_TIMEOUT = 30  # seconds
NORMAL_PHRASE_LIMIT = 30  # seconds
CONTINUOUS_PHRASE_LIMIT = 60  # seconds

# Memory Settings
MAX_MEMORY_ITEMS = 50  # Maximum conversations to remember

# Timer Settings
MAX_TIMER_DURATION = 3600  # Maximum timer duration in seconds (1 hour)

# Weather Settings
DEFAULT_CITY = "London"  # Default city for weather queries
WEATHER_UNITS = "metric"  # metric or imperial

# News Settings
DEFAULT_NEWS_COUNTRY = "us"  # Default country for news
MAX_NEWS_ARTICLES = 5  # Maximum news articles to fetch

# System Settings
ENABLE_SYSTEM_COMMANDS = True  # Enable system information and browser control
ENABLE_VOLUME_CONTROL = False  # Enable volume control (requires additional setup)

# Debug Settings
DEBUG_MODE = False  # Enable debug logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Example usage:
# 1. Copy this file to config_local.py
# 2. Modify the values you want to change
# 3. In voice_assistant.py, import from config_local instead of hardcoded values
