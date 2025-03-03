# ShareX-to-Whisper

## Description

This application generates subtitles for audio files and copies them to your clipboard. It's intended to be used with ShareX for sentence mining workflow. It will take the most recent audio file from your ShareX data folder, generate accurate subtitles for it, and copy the result to your clipboard in seconds (depending on your system and the length of the audio file).

**This program is developed for Windows and works on Windows only!**

### Do I need it?

If you're familiar with [Language Immersion](https://refold.la/roadmap/stage-2/a/active-immersion) and create Anki cards for new words you encounter in media, and you understand the struggle of finding perfect media for sentence mining that doesn't have accurate subtitles, then the answer is likely YES!

Not every language has accurate subtitles, especially for dubbed content. As a German learner myself, I can relate to this issue, which is why I created this program. You can use it either for creating Anki cards or just checking what's being said in audio content that you can't understand without subtitles.

Whisper is so accurate that I no longer rely solely on media with existing subtitles. This is especially true if you have a decent GPU with [CUDA](https://developer.nvidia.com/cuda-toolkit) support.

### How does it work?

1. The program finds the most recent audio file in your ShareX folder (which you need to specify manually). Other subdirectories or files with non-audio extensions (like screenshots) will be ignored.
2. When you visit http://localhost:8000/transcribe, subtitles are generated and automatically copied to your clipboard.

You can specify which [Whisper model](https://github.com/openai/whisper#available-models-and-languages) you'd like to use, choose any other port, or specify if you want to use [CUDA](#cuda-installation-guide).

For less technical users, you can use the recommended settings, though I must admit that the program in its current state is not the most user-friendly.

## Setup

### Prerequisites

- Python 3.12
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bogdan-sobol/sharex-to-whisper.git
   cd sharex-to-whisper
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Open `config.py` and make the following changes:

   - `AUDIO_DIR: str = r"C:\path\to\the\sharex_data\folder"`:
     Change this to the actual path where you save your ShareX audio files.

   - If you want to change the model, please refer to the [Whisper repository](https://github.com/openai/whisper). My personal recommendation is `MODEL_NAME: str = "turbo"`, which **requires at least 6 GB of VRAM**.

   - If you want to set up CUDA from the start, you can jump to the [CUDA Installation Guide section](#cuda-installation-guide) and continue after completing it.

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   This might take a while depending on your internet connection.
   
   **NOTE:** At this point, you will download about 2-3 GB of data. The Whisper model of your choice will be downloaded the first time you run the program.

5. Run the application:
   ```bash
   python transcription_server.py
   ```

   After you see `Server started on http://localhost:8000/`, visit that URL or go directly to http://localhost:8000/transcribe. This will trigger Whisper to download your chosen model (if not already downloaded) and can take some time on the first run.

   You can visit the transcribe URL each time you want to transcribe an audio file or set up automation for it.

### CUDA Installation Guide

This guide will help you set up CUDA to use your NVIDIA GPU. Using your GPU will make transcription significantly faster than using just your CPU.

You can skip this section if you're uncomfortable with these steps. However, if you have a decent NVIDIA GPU and aren't satisfied with the transcription speed using your CPU, the following might help:

#### Requirements
- An NVIDIA graphics card (GTX 750 or newer recommended)
- Windows 10 or 11 (64-bit)
- At least 4GB of free disk space

#### Step-by-Step Installation Guide

1. Check If You Have an NVIDIA GPU
   1. Press Win + X → Select "Device Manager"
   2. Expand "Display adapters"
   3. Check if you see an NVIDIA GPU listed

2. Install the Latest NVIDIA Drivers
   1. Visit [NVIDIA Driver Downloads](https://www.nvidia.com/en-us/drivers/)
   2. Select your GPU model and operating system
   3. Download and run the installer
   4. Restart your computer after installation

   If you're not a fan of NVIDIA's bloatware, I recommend watching [this video guide](https://youtu.be/LR1XkjtylCM?si=SkO5erC5GTRLWQmM).

3. Install PyTorch with CUDA Support
   1. In the program folder, activate the virtual environment if you created one:
      ```bash
      .\venv\Scripts\activate
      ```
   2. Uninstall the PyTorch version you installed with the dependencies:
      ```bash
      pip uninstall torch torchvision torchaudio
      ```
   3. Copy and paste the following command to install PyTorch with CUDA support:
      ```bash
      pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
      ```
      **NOTE:** The "cu121" refers to CUDA version 12.1. This version works with most modern NVIDIA GPUs and recent drivers.
   4. Go to `config.py` and change `USE_CUDA` to `True`
   5. Run the server and check if your GPU is detected and CUDA is True (this information will be printed to the terminal when you run the server)
   6. If it's not working, check the [Troubleshooting section](#troubleshooting) for help.

### Troubleshooting

#### "CUDA available: False" error

If your GPU isn't being detected:

1. **Outdated Drivers**: Try updating to the newest NVIDIA drivers
2. **Incompatible CUDA**: Try a different PyTorch CUDA version by changing the `cu121` part in the installation command to `cu118` or `cu117`

If you have an older NVIDIA GPU, you may need an older CUDA version. Try:
```bash
pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu116
```