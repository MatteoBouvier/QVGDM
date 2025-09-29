import dash
import dash_mantine_components as dmc
from dash import (
    ALL,
    Input,
    Output,
    State,
    callback,
    callback_context,
    html,
    no_update,
    dcc,
)
from dash.exceptions import PreventUpdate

from qvgdm.players import players
from qvgdm.questions import load_questions

dash.register_page(__name__)

questions = load_questions()
current_question = 0

layout = [
    dmc.Space(h=100),
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
                    dmc.Button(
                        "Commencer nouvelle partie", id="presenter_start_button"
                    ),
                    id="presenter_start_button_stack",
                ),
                html.Div(id="presenter_question_container"),
                dmc.Button(
                    "Question suivante", id="presenter_next_question", display="none"
                ),
            ]
        )
    ),
    dcc.Interval(id="presenter_check_connected_guests", interval=1000),
]


def show_question(index: int) -> dmc.Stack:
    question = questions[index]

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
    Output("presenter_player_status", "chilren"),
    Input("player_connection_trigger", "data"),
)
def presenter_update_guest_counter(_):
    return "Non"  # TODO:


@callback(
    Output("presenter_guest_counter", "children"),
    Input("presenter_check_connected_guests", "n_intervals"),
)
def presenter_update_guest_counter(_):
    return len(players)


@callback(
    Output("presenter_start_button_stack", "display"),
    Output("presenter_question_container", "children", allow_duplicate=True),
    Input("presenter_start_button", "n_clicks"),
    prevent_initial_call=True,
)
def presenter_start(n: int | None):
    if not n:
        return "block", None

    global current_question

    current_question = 0

    return "none", show_question(current_question)


@callback(
    Output({"type": "presenter_question", "index": ALL}, "variant"),
    Output("presenter_next_question", "display"),
    Input({"type": "presenter_question", "index": ALL}, "n_clicks"),
    State({"type": "presenter_question", "index": ALL}, "variant"),
)
def presenter_select_answer(n: list[int | None], button_variants: list[str]):
    if not callback_context.triggered_id:
        return [], "none"

    index = callback_context.triggered_id["index"]

    if button_variants[index] == "filled":
        return [no_update] * 4, "block"

    else:
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

    global current_question
    current_question += 1

    if current_question == len(questions):
        # TODO:
        print("fin")

    else:
        return show_question(current_question)
