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
    dmc.Center(
        dmc.Stack(
            [
                dmc.Group(
                    id="presenter_joker_public_timer_display",
                ),
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
                dmc.Button(
                    "Commencer nouvelle partie",
                    id="presenter_start_button",
                    disabled=True,
                ),
                html.Div(id="presenter_question_container"),
                dmc.Stack(
                    [
                        dmc.Group(
                            [
                                dmc.NumberInput(
                                    id={
                                        "type": "presenter_joker_public_answer",
                                        "index": 0,
                                    },
                                    value=0,
                                ),
                                dmc.NumberInput(
                                    id={
                                        "type": "presenter_joker_public_answer",
                                        "index": 1,
                                    },
                                    value=0,
                                ),
                            ]
                        ),
                        dmc.Group(
                            [
                                dmc.NumberInput(
                                    id={
                                        "type": "presenter_joker_public_answer",
                                        "index": 2,
                                    },
                                    value=0,
                                ),
                                dmc.NumberInput(
                                    id={
                                        "type": "presenter_joker_public_answer",
                                        "index": 3,
                                    },
                                    value=0,
                                ),
                            ]
                        ),
                        dmc.Button(
                            "Valider", id="presenter_joker_public_submit_button"
                        ),
                    ],
                    id="presenter_joker_public_container",
                    display="none",
                ),
                dmc.Stack(
                    [
                        dmc.Button(
                            "Question suivante",
                            leftSection=DashIconify(icon="mdi:navigate-next"),
                            id="presenter_next_question",
                            display="none",
                        ),
                        dmc.Button(
                            "Réponse suivante",
                            leftSection=DashIconify(icon="mdi:navigate-next"),
                            id="presenter_next_option",
                            display="none",
                        ),
                        dmc.Space(h=20),
                        dmc.Button(
                            "Recommencer",
                            leftSection=DashIconify(icon="typcn:arrow-loop"),
                            id="presenter_restart_button",
                        ),
                    ],
                    id="presenter_controls_2",
                    display="none",
                ),
            ]
        )
    ),
    dcc.Interval(id="presenter_check_connected_players", interval=500),
]


def show_question(question: Question, option_nb: int) -> dmc.Stack:
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
                        disabled=option_nb <= 0,
                    ),
                    dmc.Button(
                        question["options"][1],
                        id={"type": "presenter_question", "index": 1},
                        variant="outline",
                        autoContrast=True,
                        color="green"  # pyright: ignore[reportArgumentType]
                        if question["answer"] == question["options"][1]
                        else "white",
                        disabled=option_nb <= 1,
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
                        disabled=option_nb <= 2,
                    ),
                    dmc.Button(
                        question["options"][3],
                        id={"type": "presenter_question", "index": 3},
                        variant="outline",
                        autoContrast=True,
                        color="green"  # pyright: ignore[reportArgumentType]
                        if question["answer"] == question["options"][3]
                        else "white",
                        disabled=option_nb <= 3,
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
    Output("presenter_start_button", "display", allow_duplicate=True),
    Output("presenter_controls", "display", allow_duplicate=True),
    Output("presenter_controls_2", "display", allow_duplicate=True),
    Output("presenter_question_container", "children", allow_duplicate=True),
    Output("presenter_next_option", "display", allow_duplicate=True),
    Input("presenter_start_button", "n_clicks"),
    prevent_initial_call=True,
)
def presenter_start(n: int | None):
    if not n:
        return "block", "none", "none", None, "none"

    game = get_game()
    question = game.start()
    assert question is not None

    return (
        "none",
        "flex",
        "flex",
        show_question(question, game.current_option_nb),
        "block",
    )


@callback(
    Output("presenter_start_button", "display", allow_duplicate=True),
    Output("presenter_controls", "display", allow_duplicate=True),
    Output("presenter_controls_2", "display", allow_duplicate=True),
    Output("presenter_question_container", "children", allow_duplicate=True),
    Output("presenter_next_option", "display", allow_duplicate=True),
    Input("presenter_restart_button", "n_clicks"),
    prevent_initial_call=True,
)
def presenter_restart(n: int | None):
    if not n:
        raise PreventUpdate

    get_game().restart()
    return "block", "none", "none", None, "none"


@callback(
    Output("presenter_question_container", "children", allow_duplicate=True),
    Output("presenter_next_option", "display", allow_duplicate=True),
    Input("presenter_next_option", "n_clicks"),
    prevent_initial_call=True,
)
def presenter_next_option(n: int | None):
    if not n:
        raise PreventUpdate

    game = get_game()
    question = game.get_question()
    option_nb = get_game().next_option()

    return show_question(question, option_nb), no_update if option_nb < 4 else "none"


@callback(
    Output({"type": "presenter_question", "index": ALL}, "variant"),
    Output("presenter_next_question", "display"),
    Input({"type": "presenter_question", "index": ALL}, "n_clicks"),
    Input("presenter_next_question", "n_clicks"),
    State({"type": "presenter_question", "index": ALL}, "variant"),
    prevent_initial_call=True,
)
def presenter_select_answer(n: list[int | None], _, button_variants: list[str]):
    if not any(n):
        raise PreventUpdate

    if not callback_context.triggered_id:
        return [], "none"

    if callback_context.triggered_id == "presenter_next_question":
        return [no_update] * 4, "none"

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
    Output("public_joker_result", "children"),
    Output("presenter_next_option", "display", allow_duplicate=True),
    Input("presenter_next_question", "n_clicks"),
    prevent_initial_call=True,
)
def presenter_next_question(n: int | None):
    if not n:
        raise PreventUpdate

    game = get_game()
    question = game.next_question()

    if question is None:
        # winners, score = game.get_winners()
        # plural = "" if len(winners) == 1 else "s"
        #
        return (
            dmc.Center(
                dmc.Text(
                    # f"Gagnant{plural}: {','.join(winners)} ({score[0]}/{score[1]})",
                    c="white",  # pyright: ignore[reportArgumentType]
                    size="lg",
                ),
                style={"height": "100%"},
            ),
            None,
            "none",
        )

    return show_question(question, game.current_option_nb), None, "block"


@callback(
    Output("presenter_joker_half", "disabled"),
    Output({"type": "presenter_question", "index": ALL}, "disabled"),
    Output("presenter_joker_half", "n_clicks"),
    Input("presenter_joker_half", "n_clicks"),
)
def presenter_use_joker_half(n: int | None):
    if not n:
        raise PreventUpdate

    invalid_options_indices = get_game().use_joker_half()
    return True, [True if i in invalid_options_indices else False for i in range(4)], 0


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
    # Output("joker_public_timer", "disabled"),
    # Output("joker_public_timer", "n_intervals"),
    # Output("joker_public_timer", "max_intervals"),
    Output("presenter_joker_public_container", "display", allow_duplicate=True),
    Input("presenter_joker_public", "n_clicks"),
    prevent_initial_call=True,
)
def presenter_use_joker_public_pre(n: int | None):
    if not n:
        raise PreventUpdate

    # game = get_game()

    return True, "block"
    # game.use_joker_public_set_timer()
    # return True, False, 1, game.config["joker_public_timer"]


@callback(
    Output("public_joker_result", "children", allow_duplicate=True),
    Output("presenter_joker_public_container", "display", allow_duplicate=True),
    # Input("joker_public_timer", "n_intervals"),
    Input("presenter_joker_public_submit_button", "n_clicks"),
    State({"type": "presenter_joker_public_answer", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def presenter_user_joker_public_post(n: int | None, answers: list[int]):
    if not n:
        raise PreventUpdate

    return show_public_stats(get_game().use_joker_public(answers)), "none"

    # game = get_game()
    #
    # if n == game.config["joker_public_timer"]:
    #     answers = game.use_joker_public(answers)
    #
    #     return show_public_stats(answers)


@callback(
    Output("presenter_joker_public_timer_display", "children"),
    Input("joker_public_timer", "n_intervals"),
    prevent_initial_call=True,
)
def presenter_joker_public_timer_display(_):
    game = get_game()

    assert game.jokers.timer is not None
    game.jokers.timer -= 1

    if game.jokers.timer <= 0:
        return None

    return dmc.Center(
        dmc.Text(
            f"Joker(Public) temps restant : {game.jokers.timer}",
            c="white",  # pyright: ignore[reportArgumentType]
            size="xl",
        ),
        style={"width": "100%"},
        className="public-timer",
    )
