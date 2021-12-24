import re
import sys


class Constants:
    opener_length: int = len('- [ ] ')
    line_ending: str = '\r\n' if sys.platform == 'win32' else '\n'
    opener_regex = re.compile(r'[-*] \[[x ]] ')
