import dash
import dash_mantine_components as dmc
from dash import (
    ALL,
    Input,
    Output,
    State,
    callback,
    callback_context,
    dcc,
    html,
    no_update,
)
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

from qvgdm.game import get_game
from qvgdm.questions import Question
from qvgdm.render import show_public_stats

dash.register_page(__name__)

layout = [
    dmc.Space(h=50),
    dmc.Center(
        dmc.Stack(
            [
                dmc.Group(
                    [
                        dmc.Text("Joueur connecté: ", size="xl", c="white"),  # pyright: ignore[reportArgumentType]
                        dmc.Text(
                            "Non",
                            id="presenter_player_status",
                            size="xl",
                            c="white",  # pyright: ignore[reportArgumentType]
                        ),
                    ]
                ),
                dmc.Group(
                    [
                        dmc.Text("Public connecté: ", size="xl", c="white"),  # pyright: ignore[reportArgumentType]
                        dmc.Text(
                            "0",
                            id="presenter_guest_counter",
                            size="xl",
                            c="white",  # pyright: ignore[reportArgumentType]
                        ),
                    ]
                ),
                dmc.Space(h=20),
                dmc.Stack(
                    [
                        dmc.Button(
                            "50/50",
                            leftSection=DashIconify(icon="mdi:fraction-one-half"),
                            id="presenter_joker_half",
                        ),
                        dmc.Button(
                            "Phone",
                            leftSection=DashIconify(icon="mdi:phone"),
                            id="presenter_joker_call",
                        ),
                        dmc.Button(
                            "Public",
                            leftSection=DashIconify(icon="mdi:people"),
                            id="presenter_joker_public",
                        ),
                    ],
                    id="presenter_controls",
                    display="none",
                ),
                dmc.Stack(
                    dmc.Button(
                        "Commencer nouvelle partie",
                        id="presenter_start_button",
                        disabled=True,
                    ),
                    id="presenter_start_button_stack",
                ),
                html.Div(id="presenter_question_container"),
                dmc.Button(
                    "Question suivante",
                    leftSection=DashIconify(icon="mdi:navigate-next"),
                    id="presenter_next_question",
                    display="none",
                ),
                dmc.Space(h=20),
            ]
        )
    ),
    dcc.Interval(id="presenter_check_connected_players", interval=1000),
]


def show_question(question: Question) -> dmc.Stack:
    return dmc.Stack(
        [
            dmc.Text(question["question"], size="xl", c="white"),  # pyright: ignore[reportArgumentType]
            dmc.Group(
                [
                    dmc.Button(
                        question["options"][0],
                        id={"type": "presenter_question", "index": 0},
                        variant="outline",
                        autoContrast=True,
                        color="green"  # pyright: ignore[reportArgumentType]
                        if question["answer"] == question["options"][0]
                        else "white",
                    ),
                    dmc.Button(
                        question["options"][1],
                        id={"type": "presenter_question", "index": 1},
                        variant="outline",
                        autoContrast=True,
                        color="green"  # pyright: ignore[reportArgumentType]
                        if question["answer"] == question["options"][1]
                        else "white",
                    ),
                ]
            ),
            dmc.Group(
                [
                    dmc.Button(
                        question["options"][2],
                        id={"type": "presenter_question", "index": 2},
                        variant="outline",
                        autoContrast=True,
                        color="green"  # pyright: ignore[reportArgumentType]
                        if question["answer"] == question["options"][2]
                        else "white",
                    ),
                    dmc.Button(
                        question["options"][3],
                        id={"type": "presenter_question", "index": 3},
                        variant="outline",
                        autoContrast=True,
                        color="green"  # pyright: ignore[reportArgumentType]
                        if question["answer"] == question["options"][3]
                        else "white",
                    ),
                ]
            ),
        ]
    )


@callback(
    Output("presenter_player_status", "children"),
    Output("presenter_guest_counter", "children"),
    Output("presenter_start_button", "disabled"),
    Input("presenter_check_connected_players", "n_intervals"),
)
def presenter_update_guest_counter(_):
    game = get_game()
    status, disabled = ("Non", True) if game.player is None else ("Oui", False)
    return status, len(game.guests), disabled


@callback(
    Output("presenter_start_button_stack", "display"),
    Output("presenter_controls", "display"),
    Output("presenter_question_container", "children", allow_duplicate=True),
    Input("presenter_start_button", "n_clicks"),
    prevent_initial_call=True,
)
def presenter_start(n: int | None):
    if not n:
        return "block", "none", None

    question = get_game().start()
    assert question is not None

    return "none", "flex", show_question(question)


@callback(
    Output({"type": "presenter_question", "index": ALL}, "variant"),
    Output("presenter_next_question", "display"),
    Input({"type": "presenter_question", "index": ALL}, "n_clicks"),
    State({"type": "presenter_question", "index": ALL}, "variant"),
)
def presenter_select_answer(n: list[int | None], button_variants: list[str]):
    if not any(n):
        raise PreventUpdate

    if not callback_context.triggered_id:
        return [], "none"

    index = callback_context.triggered_id["index"]
    game = get_game()

    if button_variants[index] == "filled":
        game.validate_answer()
        return [no_update] * 4, "flex"

    else:
        game.select_answer(index)

        variants = ["outline"] * 4
        variants[index] = "filled"

        return variants, "none"


@callback(
    Output("presenter_question_container", "children", allow_duplicate=True),
    Input("presenter_next_question", "n_clicks"),
    prevent_initial_call=True,
)
def presenter_next_question(n: int | None):
    if not n:
        raise PreventUpdate

    game = get_game()
    question = game.next_question()

    # TODO: question apparition "animation"
    # TODO: reduire interval

    if question is None:
        winners, score = game.get_winners()
        plural = "" if len(winners) == 1 else "s"

        return dmc.Center(
            dmc.Text(
                f"Gagnant{plural}: {','.join(winners)} ({score[0]}/{score[1]})",
                c="white",  # pyright: ignore[reportArgumentType]
                size="lg",
            ),
            style={"height": "100%"},
        )

    return show_question(question)


@callback(
    Output("presenter_joker_half", "disabled"),
    Output({"type": "presenter_question", "index": ALL}, "disabled"),
    Input("presenter_joker_half", "n_clicks"),
)
def presenter_use_joker_half(n: int | None):
    if not n:
        raise PreventUpdate

    invalid_options_indices = get_game().use_joker_half()
    return True, [True if i in invalid_options_indices else False for i in range(4)]


@callback(
    Output("presenter_joker_call", "disabled"),
    Input("presenter_joker_call", "n_clicks"),
)
def presenter_use_joker_call(n: int | None):
    if not n:
        raise PreventUpdate

    get_game().use_joker_call()
    return True


@callback(
    Output("presenter_joker_public", "disabled"),
    Output("public_joker_result", "children", allow_duplicate=True),
    Input("presenter_joker_public", "n_clicks"),
    prevent_initial_call=True,
)
def presenter_use_joker_public(n: int | None):
    if not n:
        raise PreventUpdate

    answers = get_game().use_joker_public()

    return True, show_public_stats(answers)
