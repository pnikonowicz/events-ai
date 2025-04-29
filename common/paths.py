import os
from shutil import rmtree
from common.logger import Logger

class Paths:
    PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    DATA_DIR = os.path.join(PROJECT_DIR, "data")
    ALL_HTML = os.path.join(DATA_DIR, "all.html")def remove_dir(dir):
def remove_dir(dir):
    if os.path.exists(dir):
        rmtree(dir)
    else:
        Logger.log(f"{dir} not found, nothing to delete")