import pyaudio
import wave
from pynput import keyboard
import whisper


class VoiceRecorder:
    def __init__(self, output_file="output.wav"):
        self.output_file = output_file
        self.is_recording = False
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.frames = []
        self.audio = pyaudio.PyAudio()

    def start_recording(self):
        """Start recording audio and stop when Spacebar is pressed."""
        print("Recording started. Press 'Spacebar' to stop recording.")
        self.is_recording = True
        self.frames = []
        stream = self.audio.open(format=self.format,
                                 channels=self.channels,
                                 rate=self.rate,
                                 input=True,
                                 frames_per_buffer=self.chunk)

        def on_press(key):
            if key == keyboard.Key.space:
                print("\nSpacebar pressed. Stopping the recording...")
                self.is_recording = False
                return False  # Stops the listener

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while self.is_recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()

        with wave.open(self.output_file, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(self.frames))
        print(f"Recording saved as {self.output_file}")


def transcribe_with_whisper(file_path):
    """Transcribe audio using OpenAI Whisper in English."""
    print("Transcribing audio...")
    model = whisper.load_model("base")  # Load Whisper model
    # Specify English transcription
    result = model.transcribe(file_path, language="english")
    print("\nTranscription:")
    print(result["text"])


if __name__ == "__main__":
    recorder = VoiceRecorder()

    while True:
        print("\nOptions:")
        print("1. Start Recording")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            recorder.start_recording()
            transcribe_with_whisper(recorder.output_file)
        elif choice == "2":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
