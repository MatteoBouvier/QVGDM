from dataclasses import dataclass
import random

from dash import get_app

from qvgdm.players import Player
from qvgdm.questions import Question, load_questions


@dataclass
class ScoreItem:
    value: int
    validated: bool


@dataclass
class Jokers:
    half: bool = True
    invalid_options: list[int] | None = None

    public: bool = True
    answers: list[int] | None = None

    call: bool = True


class Game:
    def __init__(self) -> None:
        self.started: bool = False

        self.player: Player | None = None
        self.guests: dict[str, Player] = {}

        self.questions: list[Question] = load_questions()
        self.current_index: int = 0
        self.current_selected: int | None = None
        self.current_validated: bool = False

        self.score: dict[int, ScoreItem] = {
            idx: ScoreItem(question["value"], False)
            for idx, question in enumerate(self.questions)
        }

        self.jokers: Jokers = Jokers()

    def start(self) -> Question | None:
        self.started = True
        self.current_index = -1

        return self.next_question()

    def login_player(self, player: Player) -> None:
        if self.player is None:
            self.player = player

    def login_guest(self, player: Player) -> bool:
        if player.id in self.guests:
            return False

        self.guests[player.id] = player
        return True

    def get_question(self) -> Question:
        return self.questions[self.current_index]

    def get_answer_index(self) -> int:
        question = self.get_question()
        return question["options"].index(question["answer"])

    def get_current_guest_selected(self, player_id) -> int | None:
        return self.guests[player_id].answers.get(self.current_index)

    def select_answer(self, index: int) -> None:
        assert 4 > index >= 0, index
        self.current_selected = index

    def select_guest_answer(self, player_id: str, index: int) -> None:
        assert 4 > index >= 0, index

        if not self.current_validated:
            self.guests[player_id].answers[self.current_index] = index

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

        self.jokers.invalid_options = None

        if self.current_index >= len(self.questions):
            return None

        return self.questions[self.current_index]

    def use_joker_half(self) -> list[int]:
        assert self.jokers.half
        self.jokers.half = False

        answer_index = self.get_answer_index()
        invalid_options = random.sample([i for i in range(4) if i != answer_index], 2)

        self.jokers.invalid_options = invalid_options

        return invalid_options

    def use_joker_call(self) -> None:
        assert self.jokers.call
        self.jokers.call = False

    def use_joker_public(self) -> list[int]:
        assert self.jokers.public
        self.jokers.public = False

        # TODO: add timer

        answers = [0, 0, 0, 0]

        for guest in self.guests.values():
            guest_ans = guest.answers.get(self.current_index)
            if guest_ans is not None:
                answers[guest_ans] += 1

        total_answers = sum(answers)

        if total_answers > 0:
            answers = [int(nb / total_answers * 100) for nb in answers]

        self.jokers.answers = answers
        return answers


def get_game() -> Game:
    return get_app().game
