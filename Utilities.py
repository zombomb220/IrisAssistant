import os
import platform
import subprocess
import tempfile
import time

import numpy as np
import pyperclip3
import scipy.io.wavfile as wf
import sounddevice as sd
import soundfile as sf
import whisper
from gtts import gTTS
from playsound import playsound
from pydub import AudioSegment


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

        playsound(path, 0)
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
        # Start recording
        recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2)
        sd.wait()  # Wait until recording is finished

        # Convert the recording to an MP3 file
        filename = "recording.mp3"
        # sound = AudioSegment(
        #     recording.tobytes(),
        #     frame_rate=samplerate,
        #     sample_width=2,
        #     channels=2
        # )
        # sound.export(filename, format="mp3")
        wf.write("recording.wav", samplerate, recording)
        sound = AudioSegment.from_file("recording.wav", format="wav")

        # Save the audio as an MP3 file
        sound.export(filename, format="mp3")

        return filename

    @staticmethod
    def record_threshold(threshold, min_duration):
        samplerate = 44100  # 44.1 kHz
        recording = []  # Initialize an empty list to store the recording

        start_time = time.time()  # Get the current time
        while True:
            # Start recording for 0.1 seconds
            data = sd.rec(int(samplerate * 0.1), samplerate=samplerate, channels=2)
            recording.append(data)  # Append the recorded data to the list
            sd.wait()  # Wait until recording is finished

            # Calculate the volume of the input audio
            volume = np.max(np.abs(data))

            # If the volume is above the threshold, continue recording
            if volume > threshold:
                continue
            # If the volume is below the threshold, stop recording and exit the loop
            else:
                # Calculate the elapsed time
                elapsed_time = time.time() - start_time
                # If the elapsed time is less than the minimum duration, keep recording
                if elapsed_time < min_duration:
                    continue
                # If the elapsed time is greater than or equal to the minimum duration, start recording for an additional second
                else:
                    # Start recording for an additional second
                    data = sd.rec(int(samplerate * 1), samplerate=samplerate, channels=2)
                    recording.append(data)  # Append the recorded data to the list
                    sd.wait()  # Wait until recording is finished

                    # Calculate the volume of the input audio
                    volume = np.max(np.abs(data))
                    # If the volume is above the threshold, continue recording
                    if volume > threshold:
                        continue
                    # If the volume is below the threshold, stop recording
                    else:
                        break

        # Concatenate all the recorded data into a single numpy array
        recording = np.concatenate(recording)

        # Convert the recording to an MP3 file
        filename = "recording.mp3"
        wf.write("recording.wav", samplerate, recording)
        sound = AudioSegment.from_file("recording.wav", format="wav")
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
            result = model.transcribe(audio_file_path, fp16=False, language='English', verbose=1)
            result_text = result["text"]
            os.remove(audio_file_path)
            return result_text
