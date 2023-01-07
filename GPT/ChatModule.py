import openai
import os
import configparser
import json
from typing import Dict


class ChatHandler:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        config = configparser.ConfigParser()
        config.read('chat_settings.ini')
        self.engine = config['GPT']['engine']
        self.max_tokens = config.getint('GPT', 'max_tokens')
        self.n = config.getint('GPT', 'n')
        self.stop = config['GPT']['stop']
        self.temperature = config.getfloat('GPT', 'temp')

        pre_prompt_text_path = config['GPT']['pre_prompt_text_path']
        with open(pre_prompt_text_path, 'r') as file:
            self.prePromptText = file.read()

    def chat(self, prompt) -> Dict:
        completions = openai.Completion.create(
            engine=self.engine,
            prompt=self._build_prompt(prompt),
            max_tokens=self.max_tokens,
            n=self.n,
            stop=self.stop,
            temperature=self.temperature
        )

        message = completions.choices[0].text
        print("Response: " + message.strip())
        return json.loads(message.strip(), strict=False)

    def _build_prompt(self, prompt) -> str:
        return self.prePromptText + prompt
