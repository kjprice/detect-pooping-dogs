import os

def ensure_directory_exists(directory):
    try:
        os.makedirs(directory)
        print(directory)
    except Exception as e:
        return None

def go_to_script_directory():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)
