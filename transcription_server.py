import os
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

import torch
import pyperclip

from config import IP, PORT, LANGUAGE, MODEL_NAME, AUDIO_DIR, USE_CUDA


WHISPER_MODEL = None


def load_whisper_model():
    """Loads the whisper model once and keeps it in memory"""
    global WHISPER_MODEL

    if WHISPER_MODEL is None:
        print("Loading whisper library...")
        import whisper

        # Check if CUDA (GPU) is available
        device = select_device()
        print(f"Using device: {device}")

        # Load the Whisper model
        print(f"Loading {MODEL_NAME} model...")
        WHISPER_MODEL = whisper.load_model(MODEL_NAME, device=device)
        print("Model loaded and ready!")

    return WHISPER_MODEL


def select_device() -> str:
    """
    Checks if corrent device supports CUDA
    Returns either "cpu" or "cuda"
    """
    if USE_CUDA:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = "cpu"

    return device


def validate_audio_directory() -> bool:
    if not AUDIO_DIR:
        print("\nERROR:")
        print("Please enter the directory with ShareX audio files")
        print("For that you need to change the variable 'AUDIO_DIR'")
        print("inside of 'config.py'\n")
        return False

    directory = Path(AUDIO_DIR)

    # Check if the directory exists
    if not directory.exists():
        print("\nERROR:")
        print(f"The directory '{AUDIO_DIR}' doesn't exist")
        print("Please make sure you entered it properly\n")
        return False

    return True


def get_most_recent_audio_file() -> str:
    """
    Gets a path to the most recently added audio file
    Returns None if there are no such file in directory
    Returns full path as a string
    """
    audio_extensions = [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"]

    audio_files = []

    # Take only files and only with the audio extension
    for file in Path(AUDIO_DIR).iterdir():
        if file.is_file():
            file_extension = os.path.splitext(file)[1].lower()

            if file_extension in audio_extensions:
                audio_files.append(file)

    if len(audio_files) > 0:
        # Find the most recently added audio file
        most_recent_file = max(audio_files, key=lambda f: os.path.getctime(f))
        # Convert the Path object to string and return
        return str(most_recent_file)

    return None


def check_gpu():
    """
    Check if GPU is properly detected and print relevant information
    """
    print("\nGPU Information:")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Device name: {torch.cuda.get_device_name()}\n")
    else:
        print("No GPU detected! Please check if CUDA is properly installed.")
        print("You can follow the guide in the README.md\n")


def transcribe_audio(audio_path):
    """
    Transcribes audio file using Whisper and returns it
    """
    model = load_whisper_model()

    # Prepare transcription options
    transcribe_options = {}
    if LANGUAGE:
        transcribe_options["language"] = LANGUAGE

    # Transcribe the audio
    print("Transcribing audio...")
    result = model.transcribe(audio_path, **transcribe_options)

    # Copy the transcription to clipboard
    transcription = result["text"]

    return transcription


def display_json_error(self, response_code: int, error_message: dict) -> None:
    self.send_response(response_code)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(error_message).encode("utf-8"))


class TranscriptionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/transcribe":
            try:
                if not validate_audio_directory():
                    error_message = {
                        "error": "Entered wrong directory to ShareX files",
                        "hint": "Read the terminal for details",
                    }
                    display_json_error(self, 404, error_message)
                    return

                # Get the most recent audio file
                audio_file_path = get_most_recent_audio_file()

                if not audio_file_path:
                    error_message = {"error": "No audio files found"}
                    display_json_error(self, 404, error_message)
                    return

                # Transcribe audio
                transcription = transcribe_audio(audio_file_path)

                # Copy result to the clipboard
                pyperclip.copy(transcription)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                response = {
                    "transcription": transcription,
                    "file": os.path.basename(audio_file_path),
                }

                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )
            except Exception as e:
                error_message = {"error": str(e)}
                display_json_error(self, 500, error_message)
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(
                """
            <html>
            <body>
                <h1>Transcription Service</h1>
                <p>Service is running! To transcribe, visit <a href="/transcribe">/transcribe</a></p>
            </body>
            </html>
            """.encode()
            )


def run_server():
    global IP

    server_address = (IP, PORT)
    httpd = HTTPServer(server_address, TranscriptionHandler)

    if not IP:
        print(f"Server started on http://localhost:{PORT}/")
    else:
        print(f"Server started on http://{IP}:{PORT}/")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()


def main():
    if USE_CUDA:
        check_gpu()

    run_server()


if __name__ == "__main__":
    main()
