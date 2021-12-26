from .anonfields import AnonFields

class RocketUser:
    def __init__(self, 
                id: str, 
                username: str, 
                name: str,
                anonFields: AnonFields) -> None:
        self.id: str = id
        self.username: str = username
        self.name: str = name
        self.anonFields: AnonFields = anonFields