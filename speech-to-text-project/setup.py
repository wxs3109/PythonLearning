#!/usr/bin/env python3
"""
Setup script for Speech-to-Text Converter
Automates the installation process and handles common issues.
"""

import os
import sys
import subprocess
import platform


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - Failed: {e}")
        if e.stdout:
            print(f"  Output: {e.stdout}")
        if e.stderr:
            print(f"  Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"✗ Python version {version.major}.{version.minor} is not supported.")
        print("  Please use Python 3.7 or higher.")
        return False
    else:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True


def install_system_dependencies():
    """Install system-level dependencies based on the operating system."""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        print("\n=== Installing macOS Dependencies ===")
        return install_macos_dependencies()
    elif system == "linux":
        print("\n=== Installing Linux Dependencies ===")
        return install_linux_dependencies()
    elif system == "windows":
        print("\n=== Installing Windows Dependencies ===")
        return install_windows_dependencies()
    else:
        print(f"Unsupported operating system: {system}")
        return False


def install_macos_dependencies():
    """Install dependencies on macOS."""
    # Check if Homebrew is installed
    if not run_command("which brew", "Checking Homebrew installation"):
        print("Homebrew not found. Installing Homebrew...")
        install_brew_cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        if not run_command(install_brew_cmd, "Installing Homebrew"):
            return False
    
    # Install portaudio
    if not run_command("brew install portaudio", "Installing portaudio"):
        return False
    
    return True


def install_linux_dependencies():
    """Install dependencies on Linux."""
    # Detect package manager
    if os.path.exists("/etc/debian_version"):
        # Debian/Ubuntu
        commands = [
            ("sudo apt-get update", "Updating package list"),
            ("sudo apt-get install -y python3-pyaudio portaudio19-dev python3-pip", "Installing audio dependencies"),
            ("sudo apt-get install -y ffmpeg", "Installing ffmpeg")
        ]
    elif os.path.exists("/etc/redhat-release"):
        # Red Hat/CentOS/Fedora
        commands = [
            ("sudo yum update -y", "Updating package list"),
            ("sudo yum install -y portaudio-devel python3-pip", "Installing audio dependencies"),
            ("sudo yum install -y ffmpeg", "Installing ffmpeg")
        ]
    else:
        print("Unsupported Linux distribution. Please install manually:")
        print("  - portaudio19-dev")
        print("  - python3-pyaudio")
        print("  - ffmpeg")
        return False
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True


def install_windows_dependencies():
    """Install dependencies on Windows."""
    print("For Windows, please install dependencies manually:")
    print("1. Install Visual C++ Build Tools")
    print("2. Install pipwin: pip install pipwin")
    print("3. Install PyAudio: pipwin install pyaudio")
    print("4. Install ffmpeg from https://ffmpeg.org/download.html")
    return True


def install_python_packages():
    """Install Python packages."""
    print("\n=== Installing Python Packages ===")
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install packages from requirements.txt
    if os.path.exists("requirements.txt"):
        if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing Python packages"):
            return False
    else:
        # Install packages individually if requirements.txt doesn't exist
        packages = [
            "SpeechRecognition==3.10.0",
            "PyAudio==0.2.11", 
            "pydub==0.25.1"
        ]
        
        for package in packages:
            if not run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}"):
                return False
    
    return True


def test_installation():
    """Test if the installation was successful."""
    print("\n=== Testing Installation ===")
    
    # Run the test script
    if os.path.exists("test_installation.py"):
        return run_command(f"{sys.executable} test_installation.py", "Running installation tests")
    else:
        print("Test script not found. Please run test_installation.py manually.")
        return True


def create_sample_audio():
    """Create a sample audio file for testing."""
    print("\n=== Creating Sample Audio File ===")
    
    try:
        import speech_recognition as sr
        import wave
        import numpy as np
        
        # Create a simple sine wave as a test audio file
        sample_rate = 16000
        duration = 3  # seconds
        frequency = 440  # Hz (A note)
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        # Convert to 16-bit PCM
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # Save as WAV file
        with wave.open("sample_audio.wav", 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        print("✓ Created sample_audio.wav for testing")
        return True
        
    except ImportError:
        print("✗ Could not create sample audio (numpy not available)")
        return False
    except Exception as e:
        print(f"✗ Error creating sample audio: {e}")
        return False


def main():
    """Main setup function."""
    print("=== Speech-to-Text Converter Setup ===")
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version}")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install system dependencies
    if not install_system_dependencies():
        print("\nSystem dependency installation failed.")
        print("Please install manually and run setup again.")
        sys.exit(1)
    
    # Install Python packages
    if not install_python_packages():
        print("\nPython package installation failed.")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\nInstallation test failed.")
        sys.exit(1)
    
    # Create sample audio file
    create_sample_audio()
    
    print("\n" + "="*50)
    print("🎉 Setup completed successfully!")
    print("\nYou can now use the speech-to-text converter:")
    print("  python speech_to_text.py                    # Record from microphone")
    print("  python speech_to_text.py sample_audio.wav   # Transcribe audio file")
    print("  python example_usage.py                     # Run examples")
    print("\nFor help, see README.md")


if __name__ == "__main__":
    main() 