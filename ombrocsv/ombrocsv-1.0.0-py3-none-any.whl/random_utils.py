import random
import string
from datetime import datetime, timedelta


class RandomBase:

    HEADER_BASE: str = None

    def __init__(self, custom_header: str = None):
        self._counter: int = 0
        self._custom_header = custom_header

    def generate(self) -> str:
        pass

    def header(self):
        if not self.HEADER_BASE:
            self.HEADER_BASE = type(self).__name__[1:]
        self._counter += 1
        return f"{self.HEADER_BASE}{self._counter}"

    def __str__(self):
        return self.generate()


# implementations


class RBit(RandomBase):

    def generate(self) -> str:
        return str(random.randint(0, 1))


class RPhonePrefix(RandomBase):

    def generate(self) -> str:
        return ''.join(str(random.randint(0, 9)) for _ in range(4))


class RPhoneNumber(RandomBase):

    def generate(self) -> str:
        return ''.join(str(random.randint(0, 9)) for _ in range(10))


class RPhoneNumberComplete(RandomBase):

    def generate(self) -> str:
        return ''.join(str(random.randint(0, 9)) for _ in range(14))


class RString(RandomBase):

    def generate(self, length: int = 20) -> str:
        return ''.join(random.SystemRandom()
                       .choice(string.ascii_uppercase + string.digits) for _ in range(length))


class REmpty(RandomBase):

    def generate(self) -> str:
        return ""


class RName(RandomBase):

    def generate(self) -> str:
        length = random.randint(5, 20)
        offset = random.randint(0, 1)
        name = ""
        for i in range(length):
            if (i + offset) % 2 == 0:
                name += random.choice("aeiouy")
            else:
                letter = random.choice("qwrtpsdfghjklzxcvbnm")
                if random.randint(0, 5) == 3:
                    name += letter
                    i += 1
                name += letter
        return name


class REmail(RandomBase):

    _PROVIDERS = ("gmail.com", "hotmail.it", "mailup.com", "yahoo.com")

    def __init__(self, namegen: RName):
        super().__init__()
        self.namegen = namegen

    def generate(self, length: int = 20) -> str:
        return f"{self.namegen.generate()}{random.randint(0, 5000)}@{random.choice(self._PROVIDERS)}"


class RNumber(RandomBase):

    def generate(self, max_value: int = 1000000) -> str:
        return str(random.randint(0, max_value))


class RID(RandomBase):

    def __init__(self):
        super().__init__()
        self.last_id = 0

    def generate(self) -> str:
        self.last_id += 1
        return str(self.last_id)


class RDate(RandomBase):

    def generate(self, max_delta: int = 1000000) -> str:
        return str(datetime.now() + timedelta(seconds=random.randint(0, max_delta)))


# register and expose random utils

class RandUtils:

    def __init__(self):
        self.bit = RBit()
        self.phone_prefix = RPhonePrefix()
        self.phone_number = RPhoneNumber()
        self.phone_complete = RPhoneNumberComplete()
        self.string = RString()
        self.name = RName()
        self.email = REmail(self.name)
        self.number = RNumber()
        self.id = RID()
        self.date = RDate()
