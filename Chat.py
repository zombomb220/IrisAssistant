import openai
import os


def chat(prompt) -> str:
    openai.api_key = os.environ['OPENAI_API_KEY']
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    print("Response: " + message)
    return message.strip()

