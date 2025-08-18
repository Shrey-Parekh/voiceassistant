#!/usr/bin/env python3
"""
Test Setup Script for AI Voice Assistant
This script helps verify that all components are working correctly.
"""

import sys
import os
import time

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition imported successfully")
    except ImportError as e:
        print(f"❌ SpeechRecognition import failed: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"❌ pyttsx3 import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        import psutil
        print("✅ psutil imported successfully")
    except ImportError as e:
        print(f"❌ psutil import failed: {e}")
        return False
    
    return True

def test_microphone():
    """Test microphone access"""
    print("\n🎤 Testing microphone access...")
    
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        with microphone as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone access successful")
            return True
    except Exception as e:
        print(f"❌ Microphone test failed: {e}")
        print("💡 Make sure your microphone is connected and permissions are granted")
        return False

def test_tts():
    """Test text-to-speech"""
    print("\n🔊 Testing text-to-speech...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        print(f"Found {len(voices)} voice(s)")
        
        # Test speaking
        engine.say("Text to speech is working")
        engine.runAndWait()
        print("✅ Text-to-speech working")
        return True
    except Exception as e:
        print(f"❌ Text-to-speech test failed: {e}")
        return False

def test_gemini_api():
    """Test Gemini API connection"""
    print("\n🤖 Testing Gemini API connection...")
    
    try:
        import requests
        
        # Use the API key from the voice assistant
        api_key = "AIzaSyBVbzio3hQ6-Vr69n1wO_KmKAavAyB7X1M"
        api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        payload = {
            "contents": [{"parts": [{"text": "Say hello in one sentence"}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 50}
        }
        
        response = requests.post(f"{api_url}?key={api_key}", json=payload, timeout=10)
        
        if response.ok:
            data = response.json()
            if "candidates" in data and data["candidates"]:
                print("✅ Gemini API connection successful")
                return True
            else:
                print("❌ Gemini API response format error")
                return False
        else:
            print(f"❌ Gemini API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def test_weather_api():
    """Test weather API (if key is set)"""
    print("\n🌤️ Testing weather API...")
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("⚠️  No OpenWeather API key found (set OPENWEATHER_API_KEY environment variable)")
        print("   Weather features will not work without this key")
        return True  # Not a failure, just a warning
    
    try:
        import requests
        
        # Test with a simple city
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": "London", "appid": api_key, "units": "metric"}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.ok:
            print("✅ Weather API connection successful")
            return True
        else:
            print(f"❌ Weather API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Weather API test failed: {e}")
        return False

def test_news_api():
    """Test news API (if key is set)"""
    print("\n📰 Testing news API...")
    
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        print("⚠️  No News API key found (set NEWS_API_KEY environment variable)")
        print("   News features will not work without this key")
        return True  # Not a failure, just a warning
    
    try:
        import requests
        
        url = "https://newsapi.org/v2/top-headlines"
        params = {"apiKey": api_key, "country": "us", "pageSize": 1}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.ok:
            print("✅ News API connection successful")
            return True
        else:
            print(f"❌ News API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ News API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Voice Assistant Setup Test")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Microphone Access", test_microphone),
        ("Text-to-Speech", test_tts),
        ("Gemini API", test_gemini_api),
        ("Weather API", test_weather_api),
        ("News API", test_news_api)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("   You can now run: python voice_assistant.py")
    elif passed >= total - 2:  # Allow 2 optional tests to fail
        print("✅ Core functionality is working!")
        print("   Some optional features may not work, but the main assistant should run.")
        print("   You can now run: python voice_assistant.py")
    else:
        print("❌ Several tests failed. Please fix the issues before running the assistant.")
        print("   Check the error messages above for guidance.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
