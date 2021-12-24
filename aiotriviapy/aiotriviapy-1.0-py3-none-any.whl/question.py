import typing as _t


class Question(object):
    def __init__(
        self, question: str, answer: str, answers: _t.List[str], category: str, difficulty: str
    ):
        self.question = question
        self.answer = answer
        self.answers = answers
        self.category = category
        self.difficulty = difficulty
