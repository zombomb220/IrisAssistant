import os

from code_gen import gpt_gen


def generate_code(prompt):
    return gpt_gen.generate_and_validate(prompt)
    # return ChatModule.ChatHandler().chat_raw(prompt)


def write_function_to_file(function_name, function_body):
    if not os.path.exists("code_gen"):
        os.makedirs("code_gen")
    with open(f"code_gen/gpt_gen.py", "a") as f:
        f.write("\n" + function_body + "\n")


def add_function(function_name, prompt):
    function_body = generate_code(prompt)
    write_function_to_file(function_name, function_body)
    print(f"Successfully added function {function_name} to file code_gen/gpt_gen.py")


def get_existing_functions():
    if os.path.isfile("code_gen/gpt_gen.py"):
        with open("code_gen/gpt_gen.py", "r") as f:
            lines = f.readlines()
            functions = []
            for line in lines:
                if "def " in line:
                    functions.append(line.strip().split(" ")[1].split("(")[0])
            return functions
    else:
        os.makedirs("code_gen", exist_ok=True)
        open("code_gen/gpt_gen.py", "w").close()
        return []


def run_gpt_function_generator():
    existing_functions = get_existing_functions()

    function_name = input("Enter a name for the new function: ")
    prompt = f"Write a Python function named '{function_name}' that "
    prompt += input("Enter a description of the desired function: ")

    if existing_functions:
        prompt += "\n\nExisting functions: " + ", ".join(existing_functions)
    add_function(function_name, prompt)


while True:
    run_gpt_function_generator()
