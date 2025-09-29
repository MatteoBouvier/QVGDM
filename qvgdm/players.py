from dataclasses import dataclass


@dataclass
class Player:
    id: str
    score: int


guests: dict[str, Player] = {}
