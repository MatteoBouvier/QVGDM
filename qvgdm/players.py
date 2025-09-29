from dataclasses import dataclass


@dataclass
class Player:
    id: str
    score: int


players: dict[str, Player] = {}
