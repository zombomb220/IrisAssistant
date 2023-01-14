import re


class RequestHandler:
    def __init__(self, request, util):
        self.request = request
        self.util = util
        self.response = None
        self.instructions = None
        self.code = None
        self.context = None

    def handle(self, response_dict):
        self.response = response_dict

        self.code = self.get_code(self.request['request'])

        # save code to outputs/coderesponse.txt
        with open('outputs/coderesponse.txt', 'w') as f:
            f.write(self.code)

        # self.handle_response(self.code, instr, code is not None)
        instr = self.check_dict_key(self.response, 'instructions')

        if instr is not None:
            for i in instr:
                exec("self." + i)

            if self.code is not None:
                self.util.speak_back('Here is the code you requested!')

        self.util.speak_back(self.response)

    @staticmethod
    def get_code(txt) -> str:
        # Use a regular expression to search for code snippets in the response
        code_snippet = re.search(r'\u003ccode\u003e(.+?)\u003c/code\u003e', txt, re.DOTALL)

        if code_snippet:
            # Get the code snippet and strip the leading/trailing white space
            code = code_snippet.group(1).strip()
            return code

        return ""

    @staticmethod
    def check_dict_key(dictionary, key):
        if key in dictionary:
            return dictionary[key]
        else:
            return None
