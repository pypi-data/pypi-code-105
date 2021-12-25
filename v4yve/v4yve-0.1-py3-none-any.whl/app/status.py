###########################
####    v4yve corp.    ####
####  bomber by v4yve  ####
####  status.py - файл ####
###########################

from asyncio import Task
from typing import Dict, Union, Optional

status: Dict[str, Dict[str, Optional[Union[str, int]]]] = {}

attack_tasks: Dict[str, Task] = {}
