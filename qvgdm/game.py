from dataclasses import dataclass
from dash import get_app

from qvgdm.players import Player
from qvgdm.questions import Question, load_questions


@dataclass
class ScoreItem:
    value: int
    validated: bool


class Game:
    def __init__(self) -> None:
        self.started: bool = False
        self.player: Player | None = None
        self.questions: list[Question] = load_questions()
        self.current_index: int = 0
        self.current_selected: int | None = None
        self.current_validated: bool = False

        self.score: dict[int, ScoreItem] = {
            idx: ScoreItem(question["value"], False)
            for idx, question in enumerate(self.questions)
        }

    def start(self) -> Question | None:
        self.started = True
        self.current_index = -1

        return self.next_question()

    def login_player(self, player: Player) -> None:
        if self.player is None:
            self.player = player

    def get_question(self) -> Question:
        return self.questions[self.current_index]

    def get_answer(self) -> int:
        question = self.get_question()
        return question["options"].index(question["answer"])

    def select_answer(self, index: int) -> None:
        assert 4 > index >= 0, index
        self.current_selected = index

    def validate_answer(self) -> None:
        assert self.current_selected is not None
        self.current_validated = True

        question = self.get_question()
        if question["options"][self.current_selected] == question["answer"]:
            self.score[self.current_index].validated = True

    def next_question(self) -> Question | None:
        self.current_index += 1
        self.current_selected = None
        self.current_validated = False

        if self.current_index >= len(self.questions):
            return None

        return self.questions[self.current_index]


def get_game() -> Game:
    return get_app().game
