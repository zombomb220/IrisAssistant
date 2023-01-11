import json
import re

import Utilities
from GPT import ChatModule


class main:
    def get_code(self, txt) -> str:
        # Use a regular expression to search for code snippets in the response
        code_snippet = re.search(r'\u003ccode\u003e(.+?)\u003c/code\u003e', txt, re.DOTALL)

        if code_snippet:
            # Get the code snippet and strip the leading/trailing white space
            code = code_snippet.group(1).strip()
            return code

        return ""

    def handle_response(self, response_txt, instr, has_code):
        if has_code and instr is not None:
            # if 'copy_to_clipboard' in instr:
            #     util.copy_to_clipboard(response_txt)
            # if 'show_code' in instr:
            #     util.open_temp_file(response_txt)
            for i in instr:
                exec("self." + i)
            util.speak_back('Here is the code you requested!')

        util.speak_back(response_txt)

    def check_dict_key(self, dictionary, key):
        if key in dictionary:
            return dictionary[key]
        else:
            return None

    def direct_run(self):
        while True:
            command = input("Enter 'r' to record, 's' to speak back last recording or 'q' to quit: ")
            if command == 'r':
                inputAudioFileName = util.record_threshold(.1, 5)
                recording_txt = util.get_text_from_recording(inputAudioFileName)
                util.speak_back(recording_txt)

            if command == 'g':
                inputAudioFileName = util.record_threshold(.1, 5)
                recording_txt = util.get_text_from_recording(inputAudioFileName)

                try:
                    response = chatModule.chat(recording_txt)
                except json.decoder.JSONDecodeError as e:
                    util.speak_back(
                        "I'm sorry, i did not understand your question as it resulted in a malformed result.  Try again?")
                    pass
                except Exception as e:
                    util.speak_back("I'm sorry, i did not understand your question.  Try again? " + e + "  happened")

                code = self.get_code(response['request'])
                instructions = response.get('instructions')

                self.handle_response(code, instructions, code is not None)
            if command == 't':
                txtQuery = input("Enter text to send to GPT: ")
                self.text(txtQuery)

            if command == 'e':
                # write a function that loads the text from coderesponse.txt and then runs the function with execute
                with open('outputs/coderesponse.txt', 'r') as f:
                    code_response_text = f.read()
                    code = self.get_code(code_response_text)
                    exec(code)


            elif command == 's':
                with open("outputs/coderesponse.txt", 'r') as file:
                    response = self.get_code(file.read())

                instructions = ["copy_to_clipboard", "show_code"]
                self.handle_response(response, instructions, response is not None)

            elif command == 'q':
                break
            else:
                print("Invalid command. Enter 'r' to record, 's' to speak back last recording or 'q' to quit.")

    def text(self, txt):
        try:
            response = chatModule.chat(txt)

        except json.decoder.JSONDecodeError as e:
            util.speak_back(
                "I'm sorry, i did not understand your question as it resulted in a malformed result.  Try again?")
            return

        except Exception as e:
            util.speak_back("I'm sorry, i did not understand your question.  Try again?")
            return

        code = self.get_code(response['request'])

        # save code to outputs/coderesponse.txt
        with open('outputs/coderesponse.txt', 'w') as f:
            f.write(code)

        self.handle_response(code, self.check_dict_key(response, 'instructions'), code is not None)

    # def cli_run():
    #     global text, chatModule, util
    #
    #     chatModule = ChatModule.ChatHandler()
    #     util = Utilities.Utilities()
    #     # Get the first command-line argument (the function name)
    #     function_name = sys.argv[1]
    #     # Get the second command-line argument (the string argument)
    #     argument = sys.argv[2]
    #     # Call the function with the string argument
    #     globals()[function_name](argument)

    def copy_to_clipboard(self):
        print("copy to clipboard")
        # read text from outputs/coderesponse.txt and copy it to the clipboard
        with open('outputs/coderesponse.txt', 'r') as f:
            code = f.read()
            util.copy_to_clipboard(code)

    def show_code(self):
        print("show code")
        with open('outputs/coderesponse.txt', 'r') as f:
            code = f.read()
            util.open_temp_file(code)

    def __init__(self):
        global chatModule, util

        chatModule = ChatModule.ChatHandler()
        util = Utilities.Utilities()


if __name__ == '__main__':
    # if len(sys.argv) > 0:
    #     if sys.argv[0].endswith('.bat'):
    #         cli_run()
    #     else:

    m = main()
    m.direct_run()
