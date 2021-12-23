import json
import os
from pathlib import Path

def load_user_credentials():
    root_path = os.path.join(Path.home(), '.entropy')
    with open(f"{root_path}/user.conf", "r") as f:
        user_info = json.load(f)
    print(user_info)
    return user_info
