class PostList(list):
    def __init__(self, cursor: str) -> None:
        super().__init__()
        self.cursor: str = cursor