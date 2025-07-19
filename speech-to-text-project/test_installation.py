#!/usr/bin/env python3
"""
Test script to verify speech-to-text installation and dependencies.
Run this script to check if everything is set up correctly.
"""

import sys
import importlib


def test_import(module_name: str, package_name: str = None) -> bool:
    """
    Test if a module can be imported successfully.
    
    Args:
        module_name (str): Name of the module to import
        package_name (str): Display name for the package (if different)
        
    Returns:
        bool: True if import successful, False otherwise
    """
    try:
        importlib.import_module(module_name)
        display_name = package_name or module_name
        print(f"✓ {display_name} - OK")
        return True
    except ImportError as e:
        display_name = package_name or module_name
        print(f"✗ {display_name} - FAILED: {e}")
        return False


def test_microphone_access():
    """Test if microphone access is working."""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        
        # Try to access microphone
        with sr.Microphone() as source:
            print("✓ Microphone access - OK")
            return True
    except Exception as e:
        print(f"✗ Microphone access - FAILED: {e}")
        return False


def test_audio_file_support():
    """Test if audio file processing is working."""
    try:
        from pydub import AudioSegment
        print("✓ Audio file processing - OK")
        return True
    except Exception as e:
        print(f"✗ Audio file processing - FAILED: {e}")
        return False


def main():
    """Run all installation tests."""
    print("=== Speech-to-Text Installation Test ===\n")
    
    # Test core dependencies
    print("Testing core dependencies:")
    core_deps = [
        ("speech_recognition", "SpeechRecognition"),
        ("pyaudio", "PyAudio"),
        ("pydub", "pydub"),
    ]
    
    core_success = all(test_import(module, package) for module, package in core_deps)
    
    print("\nTesting hardware access:")
    mic_success = test_microphone_access()
    
    print("\nTesting audio processing:")
    audio_success = test_audio_file_support()
    
    # Summary
    print("\n" + "="*40)
    print("SUMMARY:")
    
    if core_success and mic_success and audio_success:
        print("🎉 All tests passed! Your installation is ready.")
        print("\nYou can now run:")
        print("  python speech_to_text.py                    # Record from microphone")
        print("  python speech_to_text.py audio_file.wav     # Transcribe audio file")
    else:
        print("❌ Some tests failed. Please check the installation.")
        
        if not core_success:
            print("\nTo fix dependency issues:")
            print("  pip install -r requirements.txt")
            
        if not mic_success:
            print("\nTo fix microphone issues:")
            print("  - Check microphone permissions")
            print("  - Ensure microphone is connected and working")
            print("  - On macOS: brew install portaudio")
            print("  - On Ubuntu: sudo apt-get install portaudio19-dev")
            
        if not audio_success:
            print("\nTo fix audio processing issues:")
            print("  pip install pydub")
            print("  - On Ubuntu: sudo apt-get install ffmpeg")


if __name__ == "__main__":
    main() 