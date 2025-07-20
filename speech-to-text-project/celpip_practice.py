#!/usr/bin/env python3
"""CELPIP Speaking Practice Tool

This script allows you to practice the eight CELPIP speaking tasks.
You select a task and provide a question. The script gives you the
specified preparation time, records your answer for the required
speaking time, transcribes the response, and saves both the audio and
text to a directory of your choice.
"""

import argparse
import os
import time
from datetime import datetime
from typing import Dict, List

import speech_recognition as sr


TASKS: Dict[int, Dict[str, object]] = {
    1: {
        "name": "Giving Advice",
        "description": "Give advice in response to a friend's or colleague's request",
        "prep": 30,
        "speak": 90,
        "samples": [
            "Your friend wants to eat healthier—what do you recommend?",
            "A colleague is stressed about a presentation—how can they prepare?",
        ],
    },
    2: {
        "name": "Talking About a Personal Experience",
        "description": "Describe a memorable past event",
        "prep": 30,
        "speak": 60,
        "samples": [
            "Describe a time when you learned something important.",
            "Talk about a time you met someone special.",
        ],
    },
    3: {
        "name": "Describing a Scene",
        "description": "Describe clearly what is happening in a provided picture",
        "prep": 30,
        "speak": 60,
        "samples": [
            "Describe what you see happening at a community festival.",
            "Describe the scene at a busy café.",
        ],
    },
    4: {
        "name": "Making Predictions",
        "description": "Predict likely future events based on a picture",
        "prep": 30,
        "speak": 60,
        "samples": [
            "Someone has just missed their bus—what might they do next?",
            "Children are playing soccer—what will happen in the next hour?",
        ],
    },
    5: {
        "name": "Comparing and Persuading",
        "description": "Compare two provided options and persuade a listener",
        "prep": 30,
        "speak": 60,
        "samples": [
            "Persuade your friend to choose between two different vacation destinations.",
            "Recommend either a bicycle or scooter to commute to work.",
        ],
    },
    6: {
        "name": "Dealing with a Difficult Situation",
        "description": "Explain a problem and request assistance",
        "prep": 30,
        "speak": 60,
        "samples": [
            "Your internet service stopped working—call customer support for help.",
            "You received incorrect food at a restaurant—politely ask for the correct order.",
        ],
    },
    7: {
        "name": "Expressing Opinions",
        "description": "Give your view on an issue, providing support",
        "prep": 30,
        "speak": 90,
        "samples": [
            "Should schools have a mandatory sports program? Why or why not?",
            "Should smoking be banned in all public areas?",
        ],
    },
    8: {
        "name": "Describing an Unusual Situation",
        "description": "Describe an unusual object or scenario clearly over the phone",
        "prep": 30,
        "speak": 60,
        "samples": [
            "Explain to your friend what a strange art installation looks like.",
            "Describe an unusual vehicle parked outside your home.",
        ],
    },
}


def countdown(seconds: int, message: str) -> None:
    """Display a simple countdown timer."""
    for remaining in range(seconds, 0, -1):
        print(f"{message}: {remaining:02d}s remaining", end="\r", flush=True)
        time.sleep(1)
    print("\n")


def record_response(duration: int) -> sr.AudioData:
    """Record audio from the microphone for a fixed duration."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Start speaking now!")
        audio = recognizer.record(source, duration=duration)
    return audio, recognizer


def transcribe_audio(recognizer: sr.Recognizer, audio: sr.AudioData) -> str:
    """Transcribe the provided audio using Google's API."""
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "[Unrecognized speech]"
    except sr.RequestError as e:
        return f"[API error: {e}]"


def save_audio(audio: sr.AudioData, path: str) -> None:
    """Save AudioData to a WAV file."""
    with open(path, "wb") as f:
        f.write(audio.get_wav_data())


def save_text(text: str, path: str, question: str) -> None:
    """Save transcribed text to a file with the question prepended."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Question: {question}\n\n{text}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="CELPIP speaking practice")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="celpip_recordings",
        help="Directory to save audio and transcripts",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("CELPIP Speaking Practice\n")
    for tid, info in TASKS.items():
        name = info["name"]
        prep = info["prep"]
        speak = info["speak"]
        print(f"{tid}. {name} (prep {prep}s, speak {speak}s)")

    while True:
        try:
            task_id = int(input("\nSelect a task ID (1-8): ").strip())
            if task_id in TASKS:
                break
            print("Invalid task. Please enter a number from 1 to 8.")
        except ValueError:
            print("Please enter a valid number.")

    task = TASKS[task_id]
    print(f"\nYou selected: {task['name']}")
    print("Sample questions:")
    for q in task["samples"]:
        print(f" - {q}")

    question = input("\nEnter your question (or press Enter to use the first sample): ").strip()
    if not question:
        question = task["samples"][0]

    prep_time = int(task["prep"])
    speak_time = int(task["speak"])

    print(f"\nQuestion:\n{question}\n")
    print(f"You have {prep_time} seconds to prepare...")
    countdown(prep_time, "Preparation")

    audio, recognizer = record_response(speak_time)

    print("Transcribing...")
    text = transcribe_audio(recognizer, audio)
    print("\nYour response:\n" + text)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.join(args.output_dir, f"task{task_id}_{timestamp}")
    audio_path = base + ".wav"
    text_path = base + ".txt"

    save_audio(audio, audio_path)
    save_text(text, text_path, question)

    print(f"\nSaved audio to {audio_path}")
    print(f"Saved transcript to {text_path}")


if __name__ == "__main__":
    main()
