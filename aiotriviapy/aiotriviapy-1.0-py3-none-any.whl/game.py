from random import shuffle
from html import unescape

from triviapy import errors, urls
from triviapy.utils import request_json
from triviapy.question import Question


class Game(object):
    def __init__(self):
        self.token = ""

    def _format_url(self, amount: int, category: int) -> str:
        url = urls.QUESTION_URL.format(amount=amount, category=category)
        if self.token:
            url += f"&token={self.token}"
        return url

    async def categories(self):
        """
        Returns an array of tuples with the category and their id's used to request them.
        """
        data = await request_json(urls.CATEGORY_URL)
        categories = []

        for category in data["trivia_categories"]:
            categories.append((category["name"], category["id"]))
        return categories

    async def gen_token(self):
        """
        Use this to generate a token, this is an optional step but will keep questions from repeating.
        """
        data = await request_json(urls.TOKEN_URL)

        if data["response_code"] == 0:
            self.token = data["token"]
        else:
            raise errors.TokenError

    async def round(self, quantity: int = 1, category: int = 0):
        """
        Use this to get questions, takes in a category
        """
        url = self._format_url(quantity, category)

        data = await request_json(url)

        if data["response_code"] == 1:
            raise errors.QuestionError
        elif data["response_code"] == 2:
            raise errors.CategoryError(category)
        elif data["response_code"] == 3:
            raise errors.InvalidTokenError
        elif data["response_code"] == 4:
            raise errors.QuestionError

        questions = []
        for question in data["results"]:
            answers = question["incorrect_answers"]
            answers.append(question["correct_answer"])
            shuffle(answers)
            questions.append(
                Question(
                    question=unescape(question["question"]),
                    answer=unescape(question["correct_answer"]),
                    answers=unescape(answers),
                    category=unescape(question["category"]),
                    difficulty=unescape(question["difficulty"]),
                )
            )

        if len(questions) > 1:
            return questions
        else:
            return questions[0]

    async def reset(self):
        """
        Use this to reset a token and allow old questions to be seen again.
        """
        if not self.token:
            return

        url = urls.RESET_URL.format(self.token)
        print(url)
        data = await request_json(urls.RESET_URL.format(self.token))

        if data["response_code"] == 0:
            self.token = data["token"]
        else:
            raise errors.TokenError
