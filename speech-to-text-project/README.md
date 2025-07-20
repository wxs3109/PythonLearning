# Speech-to-Text Converter

A Python application that converts speech to text using Google's Speech Recognition API. The application can transcribe audio files or record directly from your microphone.

## Features

- **Audio File Transcription**: Convert speech from audio files (WAV, MP3, etc.) to text
- **Microphone Recording**: Record and transcribe speech in real-time
- **Automatic File Saving**: Save transcriptions to text files
- **Error Handling**: Comprehensive error handling for various scenarios
- **Ambient Noise Adjustment**: Automatically adjusts for background noise

## Installation

### Prerequisites

- Python 3.7 or higher
- Microphone (for live recording)
- Internet connection (for Google Speech Recognition API)

### Step 1: Clone or Download the Project

```bash
# If you have this as a git repository
git clone <repository-url>
cd speech-to-text-project

# Or simply navigate to the project directory
cd speech-to-text-project
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

#### Troubleshooting PyAudio Installation

If you encounter issues installing PyAudio, try these solutions:

**On macOS:**
```bash
# Using Homebrew
brew install portaudio
pip install PyAudio

# Or using conda
conda install pyaudio
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
pip install PyAudio
```

**On Windows:**
```bash
# Try installing from wheel
pip install pipwin
pipwin install pyaudio
```

### Step 3: Verify Installation

```bash
python speech_to_text.py --help
```

## Usage

### 1. Transcribe Audio File

```bash
python speech_to_text.py path/to/audio/file.wav
```

**Supported Audio Formats:**
- WAV (recommended)
- MP3
- FLAC
- OGG
- And other formats supported by the `pydub` library

### 2. Record from Microphone

```bash
python speech_to_text.py
```

When using microphone mode:
1. The application will adjust for ambient noise
2. Speak clearly when prompted
3. Pause when you're done speaking
4. The transcription will be displayed and saved

### 3. Output

- Transcriptions are automatically saved to text files
- For audio files: `{filename}_transcription.txt`
- For microphone: `transcription.txt`

## Examples

### Example 1: Transcribe an Audio File

```bash
python speech_to_text.py sample_audio.wav
```

Output:
```
=== Speech-to-Text Converter ===
Loading audio file: sample_audio.wav
Transcribing audio...
File transcription: Hello, this is a test of the speech recognition system.
Transcription saved to: sample_audio_transcription.txt
```

### Example 2: Record from Microphone

```bash
python speech_to_text.py
```

Output:
```
=== Speech-to-Text Converter ===
Adjusting for ambient noise... Please wait.
Please speak (speak clearly and pause when done):
Processing speech...
You said: This is a test of the microphone recording feature.
Transcription saved to: transcription.txt
```
### CELPIP Speaking Practice

Use `celpip_practice.py` to practice the eight CELPIP speaking tasks. Select a task, enter a question, prepare for the allotted time, and the script will record and transcribe your answer. Audio and text files are saved in a directory you choose.

```bash
python celpip_practice.py -o my_recordings
```


## Configuration

### Audio Quality Tips

For best results:
- Use clear, well-recorded audio files
- Minimize background noise
- Speak clearly and at a normal pace
- Use WAV format for audio files when possible

### Microphone Settings

- Ensure your microphone is properly connected and working
- Test your microphone in your system settings
- Speak at a normal volume level
- Wait for the "Please speak" prompt before starting

## Troubleshooting

### Common Issues

1. **"Could not understand audio"**
   - Audio quality is poor or too quiet
   - Background noise is too loud
   - Speech is unclear or mumbled

2. **"API error"**
   - Check your internet connection
   - Google Speech Recognition service might be temporarily unavailable

3. **"No speech detected"**
   - Microphone not working or not connected
   - Speaking too quietly
   - Microphone permissions not granted

4. **PyAudio installation issues**
   - See installation troubleshooting section above

### Error Messages

- `File not found`: Check the audio file path
- `WaitTimeoutError`: No speech detected within timeout period
- `UnknownValueError`: Speech was unclear or not detected
- `RequestError`: API service error

## Dependencies

- **SpeechRecognition**: Main speech recognition library
- **PyAudio**: Audio I/O library for microphone access
- **pydub**: Audio file processing library

## API Usage

This project uses Google's Speech Recognition API, which is free for personal use but has rate limits. For commercial use, consider:

- Google Cloud Speech-to-Text API
- Amazon Transcribe
- Microsoft Azure Speech Services

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Verify your installation
3. Test with a simple audio file first
4. Check your internet connection 