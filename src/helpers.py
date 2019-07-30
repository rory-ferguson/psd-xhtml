import os

def psd_name(path: str, message: str):
    user_input = input(f"{message}\n")
    if user_input:
        if directory_exists(path):
            for file in os.listdir(path):
                if user_input in file:
                    return file

    if not user_input:
        if directory_exists(path):
            for file in os.listdir(path):
                if ".psb" in file or ".psd" in file:
                    return file

def directory_exists(path: str) -> bool:
    if os.path.exists(os.path.dirname(path)):
        return True
    return False