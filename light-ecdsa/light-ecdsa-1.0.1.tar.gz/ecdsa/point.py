INF_POINT = None

class Point:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
