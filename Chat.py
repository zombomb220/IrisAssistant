import openai


def chat(prompt) -> str:
    openai.api_key = "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"
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


if __name__ == '__main__':
    openai.api_key = "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"
    while True:
        prompt = input("Enter a message: ")
        response = chat(prompt)
        print(response)

