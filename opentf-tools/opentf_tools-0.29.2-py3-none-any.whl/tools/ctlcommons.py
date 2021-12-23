# Copyright 2021 Henix, henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""opentf-ctl commons"""

import sys

########################################################################


def _is_command(command, args):
    """Check if args matches command.

    `_` are placeholders.

    # Examples

    ```text
    _is_command('get job _', ['', 'get', 'job', 'foo'])  -> True
    _is_command('get   job  _', ['', 'get', 'job', 'foo'])  -> True
    _is_command('GET JOB _', ['', 'get', 'job', 'foo'])  -> False
    ```

    # Required parameters

    - command: a string
    - args: a list of strings

    # Returned value

    A boolean.
    """
    if len(args) <= len(command.split()):
        return False
    for pos, item in enumerate(command.split(), start=1):
        if item not in ('_', args[pos]):
            return False
    return True


def _get_value(prefix):
    for item in sys.argv[1:]:
        if item.startswith('--') and item.replace('_', '-').startswith(prefix):
            return item[len(prefix) :]
    return None
