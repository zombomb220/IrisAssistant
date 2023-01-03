import whisper
import sounddevice as sd
import soundfile as sf
from gtts import gTTS
import os
import Chat
import tempfile

import re
import subprocess
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

def record(audioFileName):
    # Set the recording parameters
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    # Make a recording
    myrecording = sd.rec(int(fs * seconds), samplerate=fs, channels=1)
    print("Recording audio...")
    sd.wait()  # Wait until recording is finished
    print("Audio recording complete.")

    # Save the recording to a file
    sf.write(audioFileName, myrecording, fs)


def gettext(audioFileName):
    model = whisper.load_model("base")
    result = model.transcribe(audioFileName, fp16=False, language='English')
    resultText = result["text"]
    print("Question: " + resultText)
    return resultText



def check_for_code(response, copy_clip) -> bool:
    # Use a regular expression to search for code snippets in the response
    code_snippet = re.search(r'```(.+?)```', response, re.DOTALL)

    if code_snippet:
        # Get the code snippet and strip the leading/trailing white space
        code = code_snippet.group(1).strip()

        if copy_clip:
            # Use the pbcopy command to copy the code to the clipboard
            subprocess.run(['pbcopy'], input=code, encoding='utf-8')
        else:
            # Create a temporary file
            fd, path = tempfile.mkstemp()

            # Write the code to the temporary file
            with open(fd, 'w') as f:
                f.write(code)

            # Open the file in the default text editor
            subprocess.run(['open', path])

    return code_snippet is not None


def trim_response_code(string) -> str:
    # Use a regular expression to search for code snippets in the string
    code_snippets = re.findall(r'```(.+?)```', string, re.DOTALL)

    # Replace the code snippets with an empty string
    for snippet in code_snippets:
        string = string.replace(f"```{snippet}```", "")

    return string


def fuzzy_search(keyword, string):
    return process.extract(string, keyword, score_cutoff=80)


def speakback(textToSpeak):
    # Create a gTTS object
    speech = gTTS(text=textToSpeak, lang='en')

    # Save the speech to a file
    speech.save("outputSpeech.mp3")

    # Play the audio file
    os.system("afplay outputSpeech.mp3")

if __name__ == '__main__':
    inputAudioFileName = "input.mp3"
    responseAudioFileName = "gptResponse.mp3"

    while True:
        command = input("Enter 'r' to record, 's' to speak back last recording or 'q' to quit: ")
        if command == 'r':
            record(inputAudioFileName)
            text = gettext(inputAudioFileName)
            speakback(text)
        if command == 'g':
            record(inputAudioFileName)
            text = gettext(inputAudioFileName)

            response = Chat.chat(text)
            check_for_code(response)
            speakback(response)
        if command == 't':
            question = input("Enter your request: ")

            response = Chat.chat(question)
            copy_to_clipboard = matches = process.extract(question, ['clipboard', 'copy to the clipboard', 'copy code to the clipboard'])[0][1] > 70
            hascode = check_for_code(response, copy_to_clipboard)

            if hascode:
                response = trim_response_code(response)

            if response != '':
                speakback(response)
            else:
                if copy_to_clipboard:
                    speakback("The code you requested has been copied to your clipboard.")
                else:
                    speakback("Here is the code you requested")
        elif command == 'c':
            with open("coderesponse.txt", 'r') as f:
                text = f.read()
                hascode = check_for_code(text)
                print("has code: " + str(hascode))

                if hascode:
                    text = trim_response_code(text)
                    print("Trimmed Code out of string. new string:\n" + text)

                if text != '':
                    speakback(text)
                else:
                    if copy_to_clipboard:
                        speakback("The code you requested has been copied to your clipboard.")
                    else:
                        speakback("Here is the code you requested")

        elif command == 'f':
            question = input("Enter your request: ")
            matches = process.extract(question, ['clipboard', 'copy to the clipboard', 'copy code to the clipboard'])
            print(matches)

        elif command == 'q':
            break
        else:
            print("Invalid command. Enter 'r' to record, 's' to speak back last recording or 'q' to quit.")




