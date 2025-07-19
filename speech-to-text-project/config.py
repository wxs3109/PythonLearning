"""
Configuration file for Speech-to-Text Converter
Customize these settings according to your needs.
"""

# Audio Recording Settings
AUDIO_SETTINGS = {
    'sample_rate': 16000,        # Audio sample rate (Hz)
    'channels': 1,               # Number of audio channels (1=mono, 2=stereo)
    'chunk_size': 1024,          # Audio chunk size for processing
    'format': 'pyaudio.paInt16', # Audio format
}

# Speech Recognition Settings
RECOGNITION_SETTINGS = {
    'language': 'en-US',         # Default language for recognition
    'timeout': 10,               # Timeout for listening (seconds)
    'phrase_time_limit': 30,     # Maximum phrase length (seconds)
    'ambient_duration': 1,       # Duration for ambient noise adjustment (seconds)
}

# Microphone Settings
MICROPHONE_SETTINGS = {
    'device_index': None,        # Specific microphone device index (None = default)
    'energy_threshold': 4000,    # Energy threshold for speech detection
    'dynamic_energy_threshold': True,  # Automatically adjust energy threshold
    'pause_threshold': 0.8,      # Pause threshold (seconds)
}

# File Settings
FILE_SETTINGS = {
    'output_directory': 'transcriptions',  # Directory for output files
    'default_filename': 'transcription.txt',  # Default output filename
    'supported_formats': ['.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac'],
}

# API Settings
API_SETTINGS = {
    'google_api_key': None,      # Google Cloud Speech API key (optional)
    'show_all': False,           # Show all possible transcriptions
    'with_confidence': False,    # Include confidence scores
}

# Logging Settings
LOGGING_SETTINGS = {
    'level': 'INFO',             # Logging level (DEBUG, INFO, WARNING, ERROR)
    'log_file': 'speech_to_text.log',  # Log file name
    'console_output': True,      # Show logs in console
}

# Supported Languages
SUPPORTED_LANGUAGES = {
    'English (US)': 'en-US',
    'English (UK)': 'en-GB',
    'Spanish': 'es-ES',
    'French': 'fr-FR',
    'German': 'de-DE',
    'Italian': 'it-IT',
    'Portuguese': 'pt-PT',
    'Russian': 'ru-RU',
    'Japanese': 'ja-JP',
    'Korean': 'ko-KR',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Arabic': 'ar-SA',
    'Hindi': 'hi-IN',
    'Dutch': 'nl-NL',
    'Swedish': 'sv-SE',
    'Norwegian': 'no-NO',
    'Danish': 'da-DK',
    'Finnish': 'fi-FI',
    'Polish': 'pl-PL',
    'Turkish': 'tr-TR',
    'Greek': 'el-GR',
    'Hebrew': 'he-IL',
    'Thai': 'th-TH',
    'Vietnamese': 'vi-VN',
    'Indonesian': 'id-ID',
    'Malay': 'ms-MY',
    'Filipino': 'fil-PH',
    'Czech': 'cs-CZ',
    'Hungarian': 'hu-HU',
    'Romanian': 'ro-RO',
    'Bulgarian': 'bg-BG',
    'Croatian': 'hr-HR',
    'Slovak': 'sk-SK',
    'Slovenian': 'sl-SI',
    'Estonian': 'et-EE',
    'Latvian': 'lv-LV',
    'Lithuanian': 'lt-LT',
    'Ukrainian': 'uk-UA',
    'Belarusian': 'be-BY',
    'Kazakh': 'kk-KZ',
    'Uzbek': 'uz-UZ',
    'Kyrgyz': 'ky-KG',
    'Tajik': 'tg-TJ',
    'Turkmen': 'tk-TM',
    'Mongolian': 'mn-MN',
    'Georgian': 'ka-GE',
    'Armenian': 'hy-AM',
    'Azerbaijani': 'az-AZ',
    'Persian': 'fa-IR',
    'Urdu': 'ur-PK',
    'Bengali': 'bn-BD',
    'Tamil': 'ta-IN',
    'Telugu': 'te-IN',
    'Kannada': 'kn-IN',
    'Malayalam': 'ml-IN',
    'Gujarati': 'gu-IN',
    'Marathi': 'mr-IN',
    'Punjabi': 'pa-IN',
    'Nepali': 'ne-NP',
    'Sinhala': 'si-LK',
    'Khmer': 'km-KH',
    'Lao': 'lo-LA',
    'Burmese': 'my-MM',
    'Amharic': 'am-ET',
    'Swahili': 'sw-KE',
    'Yoruba': 'yo-NG',
    'Igbo': 'ig-NG',
    'Hausa': 'ha-NG',
    'Zulu': 'zu-ZA',
    'Xhosa': 'xh-ZA',
    'Afrikaans': 'af-ZA',
    'Albanian': 'sq-AL',
    'Macedonian': 'mk-MK',
    'Serbian': 'sr-RS',
    'Bosnian': 'bs-BA',
    'Montenegrin': 'cnr-ME',
    'Icelandic': 'is-IS',
    'Faroese': 'fo-FO',
    'Greenlandic': 'kl-GL',
    'Sami': 'se-NO',
    'Basque': 'eu-ES',
    'Catalan': 'ca-ES',
    'Galician': 'gl-ES',
    'Welsh': 'cy-GB',
    'Irish': 'ga-IE',
    'Scottish Gaelic': 'gd-GB',
    'Manx': 'gv-IM',
    'Cornish': 'kw-GB',
    'Breton': 'br-FR',
    'Luxembourgish': 'lb-LU',
    'Maltese': 'mt-MT',
    'Kurdish': 'ku-TR',
    'Pashto': 'ps-AF',
    'Dari': 'prs-AF',
    'Uyghur': 'ug-CN',
    'Tibetan': 'bo-CN',
    'Nepali': 'ne-NP',
    'Sindhi': 'sd-PK',
    'Kashmiri': 'ks-IN',
    'Dogri': 'doi-IN',
    'Konkani': 'kok-IN',
    'Manipuri': 'mni-IN',
    'Bodo': 'brx-IN',
    'Santali': 'sat-IN',
    'Maithili': 'mai-IN',
    'Sanskrit': 'sa-IN',
    'Kashmiri': 'ks-IN',
    'Nepali': 'ne-NP',
    'Sindhi': 'sd-PK',
    'Dari': 'prs-AF',
    'Pashto': 'ps-AF',
    'Kurdish': 'ku-TR',
    'Maltese': 'mt-MT',
    'Luxembourgish': 'lb-LU',
    'Breton': 'br-FR',
    'Cornish': 'kw-GB',
    'Manx': 'gv-IM',
    'Scottish Gaelic': 'gd-GB',
    'Irish': 'ga-IE',
    'Welsh': 'cy-GB',
    'Galician': 'gl-ES',
    'Catalan': 'ca-ES',
    'Basque': 'eu-ES',
    'Sami': 'se-NO',
    'Greenlandic': 'kl-GL',
    'Faroese': 'fo-FO',
    'Icelandic': 'is-IS',
    'Montenegrin': 'cnr-ME',
    'Bosnian': 'bs-BA',
    'Serbian': 'sr-RS',
    'Macedonian': 'mk-MK',
    'Albanian': 'sq-AL',
    'Afrikaans': 'af-ZA',
    'Xhosa': 'xh-ZA',
    'Zulu': 'zu-ZA',
    'Hausa': 'ha-NG',
    'Igbo': 'ig-NG',
    'Yoruba': 'yo-NG',
    'Swahili': 'sw-KE',
    'Amharic': 'am-ET',
    'Burmese': 'my-MM',
    'Lao': 'lo-LA',
    'Khmer': 'km-KH',
    'Sinhala': 'si-LK',
    'Nepali': 'ne-NP',
    'Punjabi': 'pa-IN',
    'Marathi': 'mr-IN',
    'Gujarati': 'gu-IN',
    'Malayalam': 'ml-IN',
    'Kannada': 'kn-IN',
    'Telugu': 'te-IN',
    'Tamil': 'ta-IN',
    'Bengali': 'bn-BD',
    'Urdu': 'ur-PK',
    'Persian': 'fa-IR',
    'Azerbaijani': 'az-AZ',
    'Armenian': 'hy-AM',
    'Georgian': 'ka-GE',
    'Mongolian': 'mn-MN',
    'Turkmen': 'tk-TM',
    'Tajik': 'tg-TJ',
    'Kyrgyz': 'ky-KG',
    'Uzbek': 'uz-UZ',
    'Kazakh': 'kk-KZ',
    'Belarusian': 'be-BY',
    'Ukrainian': 'uk-UA',
    'Lithuanian': 'lt-LT',
    'Latvian': 'lv-LV',
    'Estonian': 'et-EE',
    'Slovenian': 'sl-SI',
    'Slovak': 'sk-SK',
    'Croatian': 'hr-HR',
    'Bulgarian': 'bg-BG',
    'Romanian': 'ro-RO',
    'Hungarian': 'hu-HU',
    'Czech': 'cs-CZ',
    'Filipino': 'fil-PH',
    'Malay': 'ms-MY',
    'Indonesian': 'id-ID',
    'Vietnamese': 'vi-VN',
    'Thai': 'th-TH',
    'Hebrew': 'he-IL',
    'Greek': 'el-GR',
    'Turkish': 'tr-TR',
    'Polish': 'pl-PL',
    'Finnish': 'fi-FI',
    'Danish': 'da-DK',
    'Norwegian': 'no-NO',
    'Swedish': 'sv-SE',
    'Dutch': 'nl-NL',
    'Hindi': 'hi-IN',
    'Arabic': 'ar-SA',
    'Chinese (Traditional)': 'zh-TW',
    'Chinese (Simplified)': 'zh-CN',
    'Korean': 'ko-KR',
    'Japanese': 'ja-JP',
    'Russian': 'ru-RU',
    'Portuguese': 'pt-PT',
    'Italian': 'it-IT',
    'German': 'de-DE',
    'French': 'fr-FR',
    'Spanish': 'es-ES',
    'English (UK)': 'en-GB',
    'English (US)': 'en-US',
} 