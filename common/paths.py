import os
from shutil import rmtree
from common.logger import Logger

class Paths:
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    DATA_DIR = os.path.join(PROJECT_DIR, "data")
    ALL_HTML = os.path.join(DATA_DIR, "all.html")
    QUERY_EMBEDDINGS = os.path.join(DATA_DIR, 'query.embeddings.json')
    PREVIOUS_EVENTS = os.path.join(PROJECT_DIR, 'previous_events')

def remove_dir(dir):
    if os.path.exists(dir):
        rmtree(dir)
    else:
        Logger.log(f"{dir} not found, nothing to delete")

def clear_directory(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        Logger.log(f"Directory {directory_path} does not exist.")
        return

    # Iterate through all items in the directory
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        try:
            # If it's a file, remove it
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            # If it's a directory, remove it and its contents
            elif os.path.isdir(item_path):
                rmtree(item_path)
        except Exception as e:
            Logger.error(f"Failed to delete {item_path}: {e}")
            return False
    return True