import json
from typing import TypedDict, cast


class Question(TypedDict):
    question: str
    options: list[str]
    answer: str
    value: int


def load_questions() -> list[Question]:
    with open("questions.json") as q:
        data = json.load(q)

    questions = cast(list[Question], data["questions"])

    for question in questions:
        assert question["answer"] in question["options"]
        assert isinstance(question["value"], int)

    return questions
