import Utilities
from GPT import ChatModule


def query_gpt(prompt):
    print("Querying GPT...")
    print(prompt)
    return ChatModule.ChatHandler().chat_raw(prompt)


def get_string_from_clipboard():
    """
    Get the string from the user's clipboard.
    Ensure that the function works on both Mac and PC.
    """
    try:
        # For Mac
        from AppKit import NSPasteboard
        pasteboard = NSPasteboard.generalPasteboard()
        return pasteboard.stringForType_(NSPasteboard.PasteboardType_String)
    except ImportError:
        # For PC
        import win32clipboard
        win32clipboard.OpenClipboard()
        return win32clipboard.GetClipboardData()
    finally:
        # Cleanup
        win32clipboard.CloseClipboard()


def execute_code(code):
    try:
        print("Trying to execute code..." + code)
        exec(code)
        print("Successfully executed code.")
    except Exception as e:
        return Exception("Error executing code: " + str(e))


def run_or_fix_code(code):
    try:
        result = execute_code(code)
    except Exception as e:
        result = fix_code(code, e)
    return result


def fix_code(code, e):
    prompt = f"Given the code {code} and the exception {e}, can you try to fix the code?"
    return query_gpt(prompt)


def generate_and_validate(prompt):
    code = query_gpt(prompt)
    try:
        print("Trying to execute code..." + code)
        execute_code(code)
        return code
    except Exception as e:
        attempts = 0
        while attempts < 5:
            code = fix_code(code, e)
            print("Attempt [" + str(attempts) + "] - Trying to execute code..." + code)
            try:
                execute_code(code)
                return code
            except Exception as e2:
                attempts += 1
        if attempts == 5:
            raise Exception('Failed to fix code after 5 attempts')


def clipboard_fix():
    code = get_string_from_clipboard()
    return generate_and_validate("There are issues in the following python code. Fix the code: \n" + code)


c = clipboard_fix()
Utilities.Utilities.copy_to_clipboard(c)
