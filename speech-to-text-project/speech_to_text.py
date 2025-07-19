#!/usr/bin/env python3
"""
Speech-to-Text Converter

This script provides functionality to convert speech to text using Google's Speech Recognition API.
It can transcribe audio files or record from microphone input.

Usage:
    python speech_to_text.py [audio_file_path]  # Transcribe audio file
    python speech_to_text.py                    # Record from microphone
"""

import sys
import speech_recognition as sr
import os
from typing import Optional


def transcribe_file(path: str) -> Optional[str]:
    """
    Transcribe an audio file to text.
    
    Args:
        path (str): Path to the audio file
        
    Returns:
        Optional[str]: Transcribed text or None if failed
    """
    if not os.path.exists(path):
        print(f"Error: File '{path}' not found")
        return None
        
    r = sr.Recognizer()
    
    try:
        with sr.AudioFile(path) as src:
            print(f"Loading audio file: {path}")
            audio = r.record(src)
            
        print("Transcribing audio...")
        text = r.recognize_google(audio)
        print("File transcription:", text)
        return text
        
    except sr.UnknownValueError:
        print("Could not understand audio - speech was unclear or not detected")
        return None
    except sr.RequestError as e:
        print(f"API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def transcribe_mic() -> Optional[str]:
    """
    Record audio from microphone and transcribe to text.
    
    Returns:
        Optional[str]: Transcribed text or None if failed
    """
    r = sr.Recognizer()
    
    try:
        with sr.Microphone() as src:
            print("Adjusting for ambient noise... Please wait.")
            r.adjust_for_ambient_noise(src, duration=1)
            
            print("Please speak (speak clearly and pause when done):")
            audio = r.listen(src, timeout=10, phrase_time_limit=30)
            
        print("Processing speech...")
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
        
    except sr.WaitTimeoutError:
        print("No speech detected within timeout period")
        return None
    except sr.UnknownValueError:
        print("Could not understand audio - speech was unclear or not detected")
        return None
    except sr.RequestError as e:
        print(f"API error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def save_transcription(text: str, filename: str = "transcription.txt") -> None:
    """
    Save transcribed text to a file.
    
    Args:
        text (str): Transcribed text to save
        filename (str): Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Transcription saved to: {filename}")
    except Exception as e:
        print(f"Error saving transcription: {e}")


def main():
    """Main function to handle command line arguments and execute transcription."""
    print("=== Speech-to-Text Converter ===")
    
    if len(sys.argv) == 2:
        # Transcribe audio file
        audio_file = sys.argv[1]
        text = transcribe_file(audio_file)
        if text:
            save_transcription(text, f"{os.path.splitext(audio_file)[0]}_transcription.txt")
    else:
        # Record from microphone
        text = transcribe_mic()
        if text:
            save_transcription(text)


if __name__ == "__main__":
    main() 