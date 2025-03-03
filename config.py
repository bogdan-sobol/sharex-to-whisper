# Entering IP is optional
IP: str = ""
PORT: int = 8000

# Leave empty for auto-detection
# Example values: "en", "de" etc.
LANGUAGE: str = "de"

# Available models and their requirements:
# https://github.com/openai/whisper/blob/main/README.md#available-models-and-languages
# Personal recommendation: "turbo"
MODEL_NAME: str = "turbo"

# If you use backslashes make sure
# to add "r" before the string
# Example: r"D:\sharex_audio"
AUDIO_DIR: str = r"C:\path\to\the\sharex_data\folder"

# Using CUDA will make make transcription significantly faster
# If you have NVIDIA GPU reading the README.md
# CUDA Installation Guide is highly recommended
USE_CUDA = True
