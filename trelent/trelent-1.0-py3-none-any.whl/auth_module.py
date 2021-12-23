# Copyright (c) 2021 Trelent Inc.

# External modules
import configparser
import os
from pathlib import Path
import requests

# Setup our config file paths
home_path = str(Path.home())
config_dir = home_path + '/.trelent'
config_path = config_dir + '/config.ini'

# Create a default config file if one doesn't exist already
if not os.path.isfile(config_path):
    os.makedirs(config_dir, exist_ok=True)
    f = open(config_path, "w")
    f.write("[CREDENTIALS]\nTrelentAPIKey = none")
    f.close()

# Initialize our ConfigParser
config = configparser.ConfigParser()
config.read(config_path)

def get_api_key():
    """
    Returns the API key for Trelent.

    :returns: The API key for Trelent. If no API key is found, returns None.
    """

    api_key = config["CREDENTIALS"]["TrelentAPIKey"]
    if(api_key == "none"):
        return None
    
    return api_key


def set_api_key(api_key):
    """
    Set the Trelent API key.

    :param api_key: The API key to set. Must be a string starting with "sk_trlnt_".
    :returns bool: True if the operation was successful, False otherwise.
    """
    if(api_key[:9] != "sk_trlnt_"):
        return False
    else:
        config["CREDENTIALS"]["TrelentAPIKey"] = api_key
        with open(config_path, 'w+') as configfile:
            config.write(configfile)
        return True

def is_valid_api_key(api_key):
    result = requests.post("https://trelent.npkn.net/check-api-key/", headers={
        "X-Trelent-Api-Key": api_key
    })

    return result.status_code == 200