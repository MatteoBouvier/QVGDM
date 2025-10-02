from typing import Literal

import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import dcc, html

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


def _get_option(
    text: str,
    index: int,
    direction: Literal["left", "right"],
    selected: int | None,
    answer: int | None,
    invalid_options: list[int] | None,
    with_button: bool,
) -> dmc.BackgroundImage | dmc.Button:
    color = _get_color(index, invalid_options)
    txt = dmc.BackgroundImage(
        dmc.Center(
            dmc.Text(text, c=color),  # pyright: ignore[reportArgumentType]
            style={"height": "100%"},
        ),
        src=f"/assets/images/{_get_asset(direction, index, selected, answer, invalid_options)}",
        style={"width": "552px", "height": "64px"},
    )

    if with_button:
        return dmc.Button(
            txt,
            color=color,  # pyright: ignore[reportArgumentType]
            variant="transparent",
            disabled=invalid_options is not None and index in invalid_options,
            id={"type": "guest_option_button", "index": index},
            styles={
                "root": {
                    "padding": "0",
                    "width": "552px",
                    "height": "64px",
                    "background": "transparent",
                }
            },
        )

    return txt


def show_question(
    question: Question,
    selected: int | None = None,
    answer: int | None = None,
    invalid_options: list[int] | None = None,
    with_buttons: bool = False,
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
                            _get_option(
                                question["options"][0],
                                0,
                                "left",
                                selected,
                                answer,
                                invalid_options,
                                with_buttons,
                            ),
                            _get_option(
                                question["options"][1],
                                1,
                                "right",
                                selected,
                                answer,
                                invalid_options,
                                with_buttons,
                            ),
                        ],
                        grow=True,
                        styles={"root": {"width": "100%"}},
                        gap=0,
                    ),
                    dmc.Space(h=5),
                    dmc.Group(
                        [
                            _get_option(
                                question["options"][2],
                                2,
                                "left",
                                selected,
                                answer,
                                invalid_options,
                                with_buttons,
                            ),
                            _get_option(
                                question["options"][3],
                                3,
                                "right",
                                selected,
                                answer,
                                invalid_options,
                                with_buttons,
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


def show_jokers(jokers: Jokers) -> list[html.Img]:
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


def show_public_stats(answers: list[int] | None) -> dcc.Graph | None:
    if answers is None:
        return None

    fig = go.Figure(
        data=[
            go.Bar(
                x=["A", "B", "C", "D"],
                y=answers,
                width=[1, 1, 1, 1],
                marker_color=["blue", "green", "red", "yellow"],
            )
        ]
    )
    fig.update_layout(
        {
            "plot_bgcolor": "black",
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            "xaxis": {"color": "white"},
            "yaxis": {
                "color": "white",
                "tickmode": "array",
                "tickvals": [0, 20, 40, 60, 80, 100],
                "ticktext": ["0%", "20%", "40%", "60%", "80%", "100%"],
            },
            "font": {"size": 30},
        }
    )
    return dcc.Graph(figure=fig)
