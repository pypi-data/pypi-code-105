import re

def pascalcase_to_snakecase(string: str) -> str:
    """
    Converts PascalCase string into snake_case
    Example: HelloWorld -> hello_world
    """
    # HelloWorld -> helloWorld
    string = re.sub(
        "^[A-Z]",
        lambda m: m.group().lower(),
        string
    )
    
    # helloWorld -> hello_world
    string = re.sub(
        "[A-Z]",
        lambda m: "_" + m.group().lower(),
        string
    )
    
    return string

def uppercase_to_pascalcase(string: str) -> str:
    """
    Converts UPPERCASE string into PascalCase
    Example: HELLO WORLD -> HelloWorld
    """
    # HELLO WORLD -> hello_world
    string = string.lower().replace(" ", "_")
    
    # hello_world -> HelloWorld
    string = snakecase_to_pascalcase(string)
    
    return string

def snakecase_to_pascalcase(string: str) -> str:
    """
    Converts snake_case string into PascalCase
    Example: hello_world -> HelloWorld
    """
    # hello_world -> helloWorld
    string = re.sub(
        "_([a-z])",
        lambda m: m.group(1).upper(),
        string
    )
    
    # helloWorld -> HelloWorld
    string = re.sub(
        "^[a-z]",
        lambda m: m.group().upper(),
        string
    )
    
    return string