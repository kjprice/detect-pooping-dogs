def ensure_directory_exists(directory):
    try:
        return os.makedirs(directory)
    except:
        return None
