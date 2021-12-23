class File:
    @classmethod
    def read(path:str) -> str:
        with open(path, "r") as file:
            return file.read()

    @classmethod
    def write(path:str, message:str) -> None:
        with open(path, "w") as file:
            file.write(message)

    @classmethod
    def append(path:str, message:str) -> None:
        with open(path, "a") as file:
            file.write(message)

    @classmethod
    def get_size(path:str) -> int:
        pass
