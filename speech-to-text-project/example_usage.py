#!/usr/bin/env python3
"""
Example usage script for the speech-to-text converter.
This script demonstrates various features and usage patterns.
"""

import speech_recognition as sr
import os
from speech_to_text import transcribe_file, transcribe_mic, save_transcription


def example_microphone_transcription():
    """Example: Record and transcribe from microphone."""
    print("\n=== Example 1: Microphone Transcription ===")
    print("This will record your voice and convert it to text.")
    
    text = transcribe_mic()
    if text:
        save_transcription(text, "microphone_example.txt")
        print(f"Transcription: '{text}'")
    else:
        print("Transcription failed.")


def example_continuous_recording():
    """Example: Continuous recording with multiple phrases."""
    print("\n=== Example 2: Continuous Recording ===")
    print("This will record multiple phrases until you say 'stop'.")
    
    r = sr.Recognizer()
    all_text = []
    
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            
            while True:
                print("\nSpeak now (say 'stop' to end):")
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    text = r.recognize_google(audio)
                    print(f"You said: {text}")
                    
                    if text.lower().strip() == 'stop':
                        break
                    
                    all_text.append(text)
                    
                except sr.WaitTimeoutError:
                    print("No speech detected. Continuing...")
                except sr.UnknownValueError:
                    print("Could not understand audio. Please try again.")
                except sr.RequestError as e:
                    print(f"API error: {e}")
                    break
                    
    except KeyboardInterrupt:
        print("\nRecording stopped by user.")
    
    if all_text:
        full_text = " ".join(all_text)
        save_transcription(full_text, "continuous_recording.txt")
        print(f"\nFull transcription: '{full_text}'")
    else:
        print("No text was transcribed.")


def example_audio_file_processing():
    """Example: Process multiple audio files."""
    print("\n=== Example 3: Audio File Processing ===")
    print("This example shows how to process multiple audio files.")
    
    # Example audio files (you would replace these with actual files)
    audio_files = [
        "sample1.wav",
        "sample2.mp3", 
        "sample3.flac"
    ]
    
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            print(f"\nProcessing: {audio_file}")
            text = transcribe_file(audio_file)
            if text:
                output_file = f"{os.path.splitext(audio_file)[0]}_transcription.txt"
                save_transcription(text, output_file)
        else:
            print(f"File not found: {audio_file}")


def example_with_different_languages():
    """Example: Speech recognition with different languages."""
    print("\n=== Example 4: Multi-language Support ===")
    print("This example shows how to use different languages.")
    
    r = sr.Recognizer()
    
    # Language codes for Google Speech Recognition
    languages = {
        'English': 'en-US',
        'Spanish': 'es-ES', 
        'French': 'fr-FR',
        'German': 'de-DE',
        'Japanese': 'ja-JP'
    }
    
    print("Available languages:")
    for name, code in languages.items():
        print(f"  {name}: {code}")
    
    try:
        with sr.Microphone() as source:
            print("\nAdjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            
            print("Please speak in your chosen language:")
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
            
            # Try recognition with different languages
            for lang_name, lang_code in languages.items():
                try:
                    text = r.recognize_google(audio, language=lang_code)
                    print(f"Detected ({lang_name}): {text}")
                    save_transcription(text, f"{lang_name.lower()}_transcription.txt")
                    break
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    print(f"API error with {lang_name}: {e}")
                    break
            else:
                print("Could not recognize speech in any of the supported languages.")
                
    except Exception as e:
        print(f"Error: {e}")


def example_batch_processing():
    """Example: Batch processing of audio files in a directory."""
    print("\n=== Example 5: Batch Processing ===")
    print("This example processes all audio files in a directory.")
    
    audio_dir = "audio_files"  # Directory containing audio files
    output_dir = "transcriptions"  # Directory for output files
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(audio_dir):
        print(f"Directory '{audio_dir}' not found. Creating example structure...")
        os.makedirs(audio_dir, exist_ok=True)
        print(f"Please place your audio files in the '{audio_dir}' directory.")
        return
    
    # Supported audio extensions
    audio_extensions = {'.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac'}
    
    processed_count = 0
    failed_count = 0
    
    for filename in os.listdir(audio_dir):
        file_path = os.path.join(audio_dir, filename)
        
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in audio_extensions):
            print(f"\nProcessing: {filename}")
            
            try:
                text = transcribe_file(file_path)
                if text:
                    output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
                    save_transcription(text, output_file)
                    processed_count += 1
                else:
                    failed_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                failed_count += 1
    
    print(f"\nBatch processing complete!")
    print(f"Successfully processed: {processed_count} files")
    print(f"Failed: {failed_count} files")
    print(f"Output saved to: {output_dir}/")


def main():
    """Run all examples."""
    print("Speech-to-Text Examples")
    print("=" * 50)
    
    while True:
        print("\nChoose an example to run:")
        print("1. Microphone Transcription")
        print("2. Continuous Recording")
        print("3. Audio File Processing")
        print("4. Multi-language Support")
        print("5. Batch Processing")
        print("6. Run all examples")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            example_microphone_transcription()
        elif choice == '2':
            example_continuous_recording()
        elif choice == '3':
            example_audio_file_processing()
        elif choice == '4':
            example_with_different_languages()
        elif choice == '5':
            example_batch_processing()
        elif choice == '6':
            example_microphone_transcription()
            example_continuous_recording()
            example_audio_file_processing()
            example_with_different_languages()
            example_batch_processing()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main() 