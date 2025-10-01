from typing import Literal

import dash_mantine_components as dmc
from dash import html

from qvgdm.game import Jokers
from qvgdm.questions import Question


def _get_asset(
    direction: Literal["left", "right"],
    index: int,
    selected: int | None,
    answer: int | None,
    invalid_options: list[int] | None,
) -> str:
    is_invalid = invalid_options is not None and index in invalid_options
    is_answer = index == answer
    is_selected = index == selected

    return f"question_{direction}{'_grey' if is_invalid else '_green' if is_answer else '_orange' if is_selected else ''}.svg"


def _get_color(index: int, invalid_options: list[int] | None) -> str:
    if invalid_options is None:
        return "white"

    return "darkgrey" if index in invalid_options else "white"


def show_question(
    question: Question,
    selected: int | None = None,
    answer: int | None = None,
    invalid_options: list[int] | None = None,
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
                                        c=_get_color(0, invalid_options),  # pyright: ignore[reportArgumentType]
                                    ),
                                    style={"height": "100%"},
                                ),
                                src=f"/assets/images/{_get_asset('left', 0, selected, answer, invalid_options)}",
                                style={"width": "552px", "height": "64px"},
                            ),
                            dmc.BackgroundImage(
                                dmc.Center(
                                    dmc.Text(
                                        question["options"][1],
                                        c=_get_color(1, invalid_options),  # pyright: ignore[reportArgumentType]
                                    ),
                                    style={"height": "100%"},
                                ),
                                src=f"/assets/images/{_get_asset('right', 1, selected, answer, invalid_options)}",
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
                                        c=_get_color(2, invalid_options),  # pyright: ignore[reportArgumentType]
                                    ),
                                    style={"height": "100%"},
                                ),
                                src=f"/assets/images/{_get_asset('left', 2, selected, answer, invalid_options)}",
                                style={"width": "552px", "height": "64px"},
                            ),
                            dmc.BackgroundImage(
                                dmc.Center(
                                    dmc.Text(
                                        question["options"][3],
                                        c=_get_color(3, invalid_options),  # pyright: ignore[reportArgumentType]
                                    ),
                                    style={"height": "100%"},
                                ),
                                src=f"/assets/images/{_get_asset('right', 3, selected, answer, invalid_options)}",
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


def show_jokers(jokers: Jokers):
    return [
        html.Img(
            src=f"/assets/images/joker/{'' if jokers.half else 'no_'}50_50.svg",
            style={"height": "320px", "width": "196px"},
        ),
        html.Img(
            src=f"/assets/images/joker/{'' if jokers.call else 'no_'}phone.svg",
            style={"height": "320px", "width": "196px"},
        ),
        html.Img(
            src=f"/assets/images/joker/{'' if jokers.public else 'no_'}public.svg",
            style={"height": "320px", "width": "196px"},
        ),
    ]
