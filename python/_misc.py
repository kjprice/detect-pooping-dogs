import os, glob

def ensure_directory_exists(directory):
    try:
        os.makedirs(directory)
        print(directory)
    except Exception as e:
        return None

def go_to_script_directory():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

def get_file_by_date(directory_filepath, desc=True):
    try:
        glob_filepath = os.path.join(directory_filepath, '*')
        list_of_files = glob.glob(glob_filepath)
    except Exception as e:
        print(e)
        return None
    
    if len(list_of_files) == 0:
        return None
    
    if desc:
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    
    oldest_file = min(list_of_files, key=os.path.getctime)
    return oldest_file


def get_most_recent_file(directory_filepath):
    return get_file_by_date(directory_filepath, True)

def get_oldest_file(directory_filepath):
    return get_file_by_date(directory_filepath, False)

def get_file_count(directory_filepath):
    possible_files = os.listdir(directory_filepath)
    files_count = 0

    for filename in possible_files:
        filepath = os.path.join(directory_filepath, filename)
        if os.path.isfile(filepath):
            files_count += 1
    
    return files_count
