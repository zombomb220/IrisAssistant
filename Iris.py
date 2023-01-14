import json

import Requests
import Utilities
from GPT import ChatModule


class Iris:
    def __init__(self):
        self.chatModule = ChatModule.ChatHandler()
        self.util = Utilities.Utilities()

    def direct_run(self):
        while True:
            command = input("Enter 'r' to record, 's' to speak back last recording or 'q' to quit: ")
            if command == 't':
                txt_query = input("Enter text to send to GPT: ")
                self.process_request(txt_query)

            # if command == 'r':
            #     inputAudioFileName = self.util.record_threshold(.1, 5)
            #     recording_txt = self.util.get_text_from_recording(inputAudioFileName)
            #     self.util.speak_back(recording_txt)
            #
            # if command == 'g':
            #     inputAudioFileName = self.util.record_threshold(.1, 5)
            #     recording_txt = self.util.get_text_from_recording(inputAudioFileName)
            #
            #     try:
            #         response = self.chatModule.chat(recording_txt)
            #     except json.decoder.JSONDecodeError as e:
            #         self.util.speak_back(
            #             "I'm sorry, i did not understand your question as it resulted in a malformed result.  Try again?")
            #         pass
            #     except Exception as e:
            #         self.util.speak_back(
            #             "I'm sorry, i did not understand your question.  Try again? " + e + "  happened")
            #
            #     code = self.get_code(response['request'])
            #     instructions = response.get('instructions')
            #
            #     self.handle_response(code, instructions, code is not None)
            # if command == 'e':
            #     # write a function that loads the text from coderesponse.txt and then runs the function with execute
            #     with open('outputs/coderesponse.txt', 'r') as f:
            #         code_response_text = f.read()
            #         code = self.get_code(code_response_text)
            #         exec(code)
            #
            #
            # elif command == 's':
            #     with open("outputs/coderesponse.txt", 'r') as file:
            #         response = self.get_code(file.read())
            #
            #     instructions = ["copy_to_clipboard", "show_code"]
            #     self.handle_response(response, instructions, response is not None)
            #
            # elif command == 'q':
            #     break
            # else:
            #     print("Invalid command. Enter 'r' to record, 's' to speak back last recording or 'q' to quit.")

    def process_request(self, txt):
        request_handle = Requests.RequestHandler(txt, self.util)

        try:
            response = self.chatModule.chat(txt)

        except json.decoder.JSONDecodeError as e:
            self.util.speak_back(
                "I'm sorry, i did not understand your question as it resulted in a malformed result.  Try again?")
            return

        except Exception as e:
            self.util.speak_back("I'm sorry, i did not understand your question.  Try again?")
            return

        request_handle.handle(response)

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
            self.util.copy_to_clipboard(code)

    def show_code(self):
        print("show code")
        with open('outputs/coderesponse.txt', 'r') as f:
            code = f.read()
            self.util.open_temp_file(code)
