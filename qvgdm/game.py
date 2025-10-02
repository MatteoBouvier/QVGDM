import itertools as it
from dataclasses import dataclass
import random
import tomllib
from typing import Any, Literal

from dash import get_app

from qvgdm.players import Player, ScoreItem
from qvgdm.questions import Question, load_questions


@dataclass
class Jokers:
    half: bool = True
    invalid_options: list[int] | None = None

    public: bool = True
    timer: int | None = None
    answers: list[int] | None = None

    call: bool = True


class Game:
    def __init__(self) -> None:
        with open("config.toml", "rb") as conf:
            self.config: dict[str, Any] = tomllib.load(conf)["qvgdm"]

        self.status: Literal["waiting", "started", "ended"] = "waiting"

        self.player: Player | None = None
        self.guests: dict[str, Player] = {}

        self.questions: list[Question] = load_questions()
        self.current_index: int = -1
        self.current_selected: int | None = None
        self.current_validated: bool = False
        self.current_option_nb: int = 0

        self.jokers: Jokers = Jokers()

    def start(self) -> Question | None:
        self.status = "started"

        return self.next_question()

    def restart(self) -> None:
        self.status = "waiting"

        self.player = None
        self.guests = {}

        self.current_index = -1
        self.current_selected = None
        self.current_validated = False
        self.current_option_nb = 0

        self.jokers = Jokers()

    def login_player(self, player_id: str) -> None:
        if self.player is None:
            self.player = Player(
                player_id,
                "__RESERVED:PLAYER__",
                [ScoreItem(question["value"]) for question in self.questions],
            )

    def login_guest(self, player_id: str, name: str) -> bool:
        if player_id in self.guests:
            return False

        self.guests[player_id] = Player(
            player_id,
            name,
            [ScoreItem(question["value"]) for question in self.questions],
        )
        return True

    def get_question(self) -> Question:
        return self.questions[self.current_index]

    def get_answer_index(self) -> int:
        question = self.get_question()
        return question["options"].index(question["answer"])

    def get_current_guest_selected(self, player_id: str) -> int | None:
        return self.guests[player_id].answers.get(self.current_index)

    def select_answer(self, index: int) -> None:
        assert 4 > index >= 0, index
        self.current_selected = index

    def select_guest_answer(self, player_id: str, index: int) -> None:
        assert 4 > index >= 0, index

        if not self.current_validated:
            guest = self.guests[player_id]
            guest.answers[self.current_index] = index

            if self.get_answer_index() == index:
                guest.score[self.current_index].validated = True

            else:
                guest.score[self.current_index].validated = False

    def validate_answer(self) -> None:
        assert self.current_selected is not None
        assert self.player is not None

        self.current_validated = True

        question = self.get_question()
        if question["options"][self.current_selected] == question["answer"]:
            self.player.score[self.current_index].validated = True

        else:
            self.player.score[self.current_index].validated = False

    def next_question(self) -> Question | None:
        self.current_index += 1
        self.current_selected = None
        self.current_validated = False
        self.current_option_nb = 0

        self.jokers.invalid_options = None
        self.jokers.answers = None

        if self.current_index >= len(self.questions):
            self.status = "ended"
            return None

        return self.questions[self.current_index]

    def next_option(self) -> int:
        self.current_option_nb += 1
        assert self.current_option_nb <= 4

        return self.current_option_nb

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

    def use_joker_public_set_timer(self) -> None:
        assert self.jokers.public
        self.jokers.timer = self.config["joker_public_timer"]

    def use_joker_public(self) -> list[int]:
        assert self.jokers.public
        self.jokers.public = False
        self.jokers.timer = None

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

    def get_player_score(self) -> int:
        assert self.player is not None
        return sum(bool(s.validated) * s.value for s in self.player.score)

    def get_guest_score(self, player_id: str) -> int:
        guest = self.guests[player_id]
        return sum(bool(s.validated) * s.value for s in guest.score)

    def get_total_score(self) -> int:
        return sum(q["value"] for q in self.questions)

    def get_winners(self) -> tuple[list[str], tuple[int, int]]:
        scores = [
            (guest.name, self.get_guest_score(guest.id))
            for guest in self.guests.values()
        ]
        best_score, best_names = next(
            it.groupby(sorted(scores, key=lambda s: s[1], reverse=True), lambda e: e[1])
        )
        total_score = self.get_total_score()

        return [b[0] for b in best_names], (best_score, total_score)


def get_game() -> Game:
    return get_app().game
