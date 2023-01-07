import Utilities
from GPT import ChatModule

import re




def get_code(text) -> str:
    # Use a regular expression to search for code snippets in the response
    code_snippet = re.search(r'\u003ccode\u003e(.+?)\u003c/code\u003e', text, re.DOTALL)

    if code_snippet:
        # Get the code snippet and strip the leading/trailing white space
        code = code_snippet.group(1).strip()
        return code

    return ""


def handle_response(response_txt, instructions, has_code):
    if has_code:
        if 'copy_to_clipboard' in instructions:
            util.copy_to_clipboard(code)
        if 'show_code' in instructions:
            util.open_temp_file(code)
        util.speak_back('Here is the code you requested!')

    util.speak_back(response_txt)


if __name__ == '__main__':
    chatModule = ChatModule.ChatHandler()
    util = Utilities.Utilities()

    while True:
        command = input("Enter 'r' to record, 's' to speak back last recording or 'q' to quit: ")
        if command == 'r':
            inputAudioFileName = util.record(5)
            text = util.get_text_from_recording(inputAudioFileName)
            util.speak_back(text)

        if command == 'g':
            inputAudioFileName = util.record(5)
            text = util.get_text_from_recording(inputAudioFileName)

            response = chatModule.chat(text)

            code = get_code(response['request'])
            handle_response(code, response['instructions'], code is not None)
        if command == 't':
            question = input("Enter your request: ")

            response = chatModule.chat(question)

            code = get_code(response['request'])
            handle_response(code, response['instructions'], code is not None)

        elif command == 's':
            with open("outputs/coderesponse.txt", 'r') as file:
                response = get_code(file.read())

            instructions = ["copy_to_clipboard", "show_code"]
            handle_response(response, instructions, response is not None)

        elif command == 'q':
            break
        else:
            print("Invalid command. Enter 'r' to record, 's' to speak back last recording or 'q' to quit.")




