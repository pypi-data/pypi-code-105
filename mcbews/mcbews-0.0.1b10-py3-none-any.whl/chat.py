from enum import Enum
import re

class Color(Enum):
    BLACK =        "\xA70"
    DARK_BLUE =    "\xA71"
    DARK_GREEN =   "\xA72"
    DARK_AQUA =    "\xA73"
    DARK_RED =     "\xA74"
    DARK_PURPLE =  "\xA75"
    GOLD =         "\xA76"
    GRAY =         "\xA77"
    DARK_GRAY =    "\xA78"
    BLUE =         "\xA79"
    GREEN =        "\xA7a"
    AQUA =         "\xA7b"
    RED =          "\xA7c"
    LIGHT_PURPLE = "\xA7d"
    YELLOW =       "\xA7e"
    WHITE =        "\xA7f"
    DARK_YELLOW =  "\xA7g"

class Style(Enum):
    OBFUSCATED = "\xA7k"
    BOLD =       "\xA7l"
    ITALIC =     "\xA7o"
    RESET =      "\xA7r"

class MinecraftBedrock:
    legal_escape = "%\\$=;"
    def process(obj):
        if isinstance(obj, str):
            string = obj.replace("\n", escape_char + "n")
            obj = Powerstring(f"""
                {string}
            """, syntax = MinecraftBedrock)
        string = obj.text
        
        # style text
        


class Message:
    def __init__(self, text):
        self.text = text
        self.raw = re.sub("\xA7[a-fA-F0-9klor]", "", text)
    
    def __str__(self):
        pass
    


if __name__ == "__main__":
    import powerstring as ps
    text = ps.Powerstring(f"""
        **********************************
        <%GOLD%[Hello World]%>
        Website: <%GREEN%www.example.org%>
    """)