from typing import Literal
import dash_mantine_components as dmc

from qvgdm.questions import Question


def _get_asset(
    direction: Literal["left", "right"], is_selected: bool, is_answer: bool
) -> str:
    return f"question_{direction}{'_green' if is_answer else '_orange' if is_selected else ''}.svg"


def show_question(
    question: Question, selected: int | None = None, answer: int | None = None
):
    return (
        dmc.Center(
            dmc.Stack(
                [
                    dmc.Center(
                        dmc.BackgroundImage(
                            dmc.Center(
                                dmc.Text(
                                    question["question"],
                                    c="white",  # pyright: ignore[reportArgumentType]
                                    size="30px",  # pyright: ignore[reportArgumentType]
                                ),
                                style={"height": "100%"},
                            ),
                            src="/assets/images/question_main.svg",
                            style={"width": "1083px", "height": "118px"},
                        )
                    ),
                    dmc.Space(h=10),
                    dmc.Group(
                        [
                            dmc.BackgroundImage(
                                dmc.Center(
                                    dmc.Text(
                                        question["options"][0],
                                        c="white",  # pyright: ignore[reportArgumentType]
                                    ),
                                    style={"height": "100%"},
                                ),
                                src=f"/assets/images/{_get_asset('left', selected == 0, answer == 0)}",
                                style={"width": "552px", "height": "64px"},
                            ),
                            dmc.BackgroundImage(
                                dmc.Center(
                                    dmc.Text(
                                        question["options"][1],
                                        c="white",  # pyright: ignore[reportArgumentType]
                                    ),
                                    style={"height": "100%"},
                                ),
                                src=f"/assets/images/{_get_asset('right', selected == 1, answer == 1)}",
                                style={"width": "552px", "height": "64px"},
                            ),
                        ],
                        grow=True,
                        styles={"root": {"width": "100%"}},
                        gap=0,
                    ),
                    dmc.Space(h=5),
                    dmc.Group(
                        [
                            dmc.BackgroundImage(
                                dmc.Center(
                                    dmc.Text(
                                        question["options"][2],
                                        c="white",  # pyright: ignore[reportArgumentType]
                                    ),
                                    style={"height": "100%"},
                                ),
                                src=f"/assets/images/{_get_asset('left', selected == 2, answer == 2)}",
                                style={"width": "552px", "height": "64px"},
                            ),
                            dmc.BackgroundImage(
                                dmc.Center(
                                    dmc.Text(
                                        question["options"][3],
                                        c="white",  # pyright: ignore[reportArgumentType]
                                    ),
                                    style={"height": "100%"},
                                ),
                                src=f"/assets/images/{_get_asset('right', selected == 3, answer == 3)}",
                                style={"width": "552px", "height": "64px"},
                            ),
                        ],
                        grow=True,
                        styles={"root": {"width": "100%"}},
                        gap=0,
                    ),
                ],
                styles={"root": {"width": "100%"}},
            )
        ),
    )
