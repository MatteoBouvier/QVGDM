from dataclasses import dataclass, field


@dataclass
class Player:
    id: str
    name: str
    answers: dict[int, int] = field(default_factory=dict)
