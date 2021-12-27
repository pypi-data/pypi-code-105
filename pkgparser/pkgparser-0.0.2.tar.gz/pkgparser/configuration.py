import os

# FILESYSTEM
DIRECTORY_PATH_OUTPUT = os.environ["DIRECTORY_PATH"] if "DIRECTORY_PATH" in os.environ else os.getcwd()
