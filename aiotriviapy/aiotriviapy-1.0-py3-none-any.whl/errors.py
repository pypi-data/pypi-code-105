class TokenError(Exception):
    def __repr__(self) -> str:
        return "A token could not be generated."


class QuestionError(Exception):
    def __repr__(self) -> str:
        return "Not enough questions available."


class InvalidTokenError(Exception):
    def __repr__(self) -> str:
        return "Token is invalid or has expired."


class CategoryError(Exception):
    def __init__(self, category: int):
        self.category = category

    def __repr__(self) -> str:
        return f"Category {self.category} is invalid."
