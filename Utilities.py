import os
import platform
import subprocess
import tempfile
from gtts import gTTS
from playsound import playsound
import pyperclip3
import sounddevice as sd
import soundfile as sf
import whisper
from pydub import AudioSegment
import time

class Utilities:
    def __init__(self):
        self.platform = platform.system()

    def open_file(self, path):
        if self.platform == 'Windows':
            subprocess.Popen(['C:\\Windows\\system32\\notepad.exe', path])
        elif self.platform == 'Darwin':  # macOS
            subprocess.run(['open', path])
        else:
            print('Unsupported platform')

    def create_temp_file(self, contents):
        _, path = tempfile.mkstemp()
        with open(path, 'w') as f:
            f.write(contents)
        return path

    def open_temp_file(self, contents):
        path = self.create_temp_file(contents)
        self.open_file(path)

    @staticmethod
    def speak_back(txt):
        # Create a gTTS object
        speech = gTTS(text=txt, lang='en')

        path = 'temp_responseSpeech.mp3'
        # Save the speech to a file
        speech.save(path)

        playsound(path)
        os.remove(path)

    @staticmethod
    def copy_to_clipboard(code):
        pyperclip3.copy(code)

    def get_clipboard(self):
        if self.platform == 'Windows':
            # Windows requires the pyperclip module
            return pyperclip3.paste()
        elif self.platform == 'Darwin':  # macOS
            return subprocess.run(['pbpaste'], capture_output=True).stdout.decode()
        else:
            print('Unsupported platform')
            return ''

    def set_clipboard(self, contents):
        if self.platform == 'Windows':
            # Windows requires the pyperclip module
            pyperclip3.copy(contents)
        elif self.platform == 'Darwin':  # macOS
            subprocess.run(['pbcopy'], input=contents.encode())
        else:
            print('Unsupported platform')

    def open_folder(self, path):
        if self.platform == 'Windows':
            subprocess.run(['explorer', path])
        elif self.platform == 'Darwin':  # macOS
            subprocess.run(['open', path])
        else:
            print('Unsupported platform')

    @staticmethod
    def get_environment_variable(name):
        return os.environ.get(name)

    @staticmethod
    def set_environment_variable(name, value):
        os.environ[name] = value

    @staticmethod
    def record_mac(seconds) -> str:
        audio_path = 'outputs/tmp_audioRecording.mp3'
        # Set the recording parameters
        fs = 44100  # Sample rate

        # Make a recording
        my_recording = sd.rec(int(fs * seconds), samplerate=fs, channels=1)
        print("Recording audio...")
        sd.wait()  # Wait until recording is finished
        print("Audio recording complete.")

        # Save the recording to a file
        sf.write(audio_path, my_recording, fs)
        return audio_path

    @staticmethod
    def record(duration):
        samplerate = 44100  # 44.1 kHz
        print("Recording audio...")
        # Start recording
        recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2)
        sd.wait()  # Wait until recording is finished
        print("Audio recording complete.")

        # Convert the recording to an MP3 file
        filename = "recording.mp3"
        sound = AudioSegment(
            recording.tobytes(),
            frame_rate=samplerate,
            sample_width=2,
            channels=2
        )
        sound.export(filename, format="mp3")

        return filename

    @staticmethod
    def get_text_from_recording(audio_file_path):
        # Wait until the file is created, with a timeout of 10 seconds
        timeout = 100  # seconds
        counter = 0
        while not os.path.exists(audio_file_path):
            time.sleep(0.1)
            counter += 1
            if counter > timeout * 10:
                # File was not created within the timeout
                break

        print("Path " + audio_file_path + " exists: " + str(os.path.exists(audio_file_path)))

        if os.path.exists(audio_file_path):
            model = whisper.load_model("base")
            result = model.transcribe(audio_file_path, fp16=False, language='English')
            result_text = result["text"]
            print("Question: " + result_text)
            os.remove(audio_file_path)
            return result_text
