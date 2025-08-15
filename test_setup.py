#!/usr/bin/env python3
"""
Test script to verify all dependencies are installed correctly
Run this before starting the workshop to ensure everything works
"""

def test_imports():
    """Test if all required libraries can be imported"""
    print("Testing library imports...")
    
    try:
        import speech_recognition as sr
        print("✓ speech_recognition imported successfully")
    except ImportError as e:
        print(f"✗ speech_recognition failed: {e}")
        return False
    
    try:
        import pyttsx3
        print("✓ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"✗ pyttsx3 failed: {e}")
        return False
    
    try:
        import pygame
        print("✓ pygame imported successfully")
    except ImportError as e:
        print(f"✗ pygame failed: {e}")
        return False
    
    try:
        import requests
        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ requests failed: {e}")
        return False
    
    return True

def test_microphone():
    """Test if microphone is accessible"""
    print("\nTesting microphone access...")
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        mic = sr.Microphone()
        print("✓ Microphone accessible")
        return True
    except Exception as e:
        print(f"✗ Microphone test failed: {e}")
        return False

def test_text_to_speech():
    """Test if text-to-speech works"""
    print("\nTesting text-to-speech...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("✓ Text-to-speech engine initialized")
        
        # Test speaking (comment out if you don't want audio during test)
        # engine.say("Testing text to speech")
        # engine.runAndWait()
        # print("✓ Text-to-speech audio test completed")
        
        return True
    except Exception as e:
        print(f"✗ Text-to-speech test failed: {e}")
        return False

def test_audio_playback():
    """Test if pygame audio works"""
    print("\nTesting audio playback capability...")
    try:
        import pygame
        pygame.mixer.init()
        print("✓ Pygame audio mixer initialized")
        return True
    except Exception as e:
        print(f"✗ Audio playback test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("VOICE ASSISTANT SETUP TEST")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test microphone
    if not test_microphone():
        all_passed = False
    
    # Test TTS
    if not test_text_to_speech():
        all_passed = False
    
    # Test audio
    if not test_audio_playback():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Ready for the workshop!")
        print("You can now run: python voice_assistant.py")
    else:
        print("❌ Some tests failed. Please check the installation instructions.")
        print("Run: pip install -r requirements.txt")
    print("=" * 50)

if __name__ == "__main__":
    main()