def boolean(arg: str) -> bool:
    """
    Turns a boolean value into a python
    boolean.
    """
    if arg in ("0", "false"):
        return False
    if arg in ("1", "true"):
        return True

def color(arg: str) -> int:
    """
    Minecraft has color values from white to
    black (0-15). This converter turn the
    color name into the matchung data value.
    """
    if arg in ("0", "white"):
        return 0
    if arg in ("1", "orange"):
        return 1
    if arg in ("2", "magenta"):
        return 2
    if arg in ("3", "lightblue"):
        return 3
    if arg in ("4", "yellow"):
        return 4
    if arg in ("5", "lime"):
        return 5
    if arg in ("6", "pink"):
        return 6
    if arg in ("7", "gray"):
        return 7
    if arg in ("8", "lightgray"):
        return 8
    if arg in ("9", "cyan"):
        return 9
    if arg in ("10", "purple"):
        return 10
    if arg in ("11", "blue"):
        return 11
    if arg in ("12", "brown"):
        return 12
    if arg in ("13", "green"):
        return 13
    if arg in ("14", "red"):
        return 14
    if arg in ("15", "black"):
        return 15