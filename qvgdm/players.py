from dataclasses import dataclass, field


@dataclass
class ScoreItem:
    value: int
    validated: bool | None = None


@dataclass
class Player:
    id: str
    name: str
    score: list[ScoreItem]
    answers: dict[int, int] = field(default_factory=dict)
