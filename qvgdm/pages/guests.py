import dash
import dash_mantine_components as dmc
import flask
from dash import ALL, Input, Output, State, callback, callback_context, dcc, html
from dash.exceptions import PreventUpdate

from qvgdm.game import get_game
from qvgdm.render import show_public_stats, show_question, show_score

dash.register_page(__name__, path="/")


layout = [
    dmc.Space(h=50),
    dmc.Center(
        [
            dmc.Stack(
                [
                    dmc.TextInput(placeholder="votre nom ...", id="guest_name"),
                    dmc.Space(h=10),
                    dmc.Button(
                        "Rejoindre la partie",
                        id="guest_join_button",
                        size="xl",
                        variant="filled",
                        color="#ff931e",  # pyright: ignore[reportArgumentType]
                        style={"float": "right"},
                        disabled=True,
                    ),
                ],
                style={"width": "50%"},
                id="guest_layout_logged_out",
            ),
        ],
        id="guest_layout",
    ),
    html.Div(id="guest_question_container", style={"height": "30vh"}),
    dcc.Interval(id="guest_update", interval=1000),
]


@callback(Output("guest_join_button", "disabled"), Input("guest_name", "value"))
def guest_handle_join_button(name: str | None):
    return not name


@callback(
    Output("guest_layout_logged_out", "display"),
    Input("guest_join_button", "n_clicks"),
    State("guest_name", "value"),
)
def guest_join(n: int | None, name: str):
    player_id = flask.request.origin

    game = get_game()

    if not n:
        if player_id in game.guests:
            # guest player already connected
            return "none"

        else:
            # new connection, main page
            return "block"

    # new connection success
    assert name, name
    game.login_guest(player_id, name)
    return "none"


@callback(
    Output("guest_question_container", "children"),
    Output("score_ladder", "children", allow_duplicate=True),
    Output("public_joker_result", "children", allow_duplicate=True),
    Input("guest_update", "n_intervals"),
    prevent_initial_call=True,
)
def guest_update_layout(_):
    game = get_game()
    player_id = flask.request.origin

    if player_id in game.guests:
        if game.started:
            return (
                show_question(
                    game.get_question(),
                    game.get_current_guest_selected(player_id),
                    game.get_answer_index() if game.current_validated else None,
                    game.jokers.invalid_options,
                    with_buttons=True,
                ),
                show_score(
                    game.guests[player_id].score,
                    game.current_index,
                ),
                show_public_stats(game.jokers.answers),
            )

        return (
            dmc.Center(
                dmc.Loader(
                    size="xl",
                    type="oval",
                    color="white",  # pyright: ignore[reportArgumentType]
                ),
                style={"height": "100%"},
            ),
            None,
            None,
        )

    return None, None, None


@callback(Input({"type": "guest_option_button", "index": ALL}, "n_clicks"))
def guest_register_answer(_):
    trigger = callback_context.triggered_id

    if trigger is None:
        raise PreventUpdate

    player_id = flask.request.origin
    get_game().select_guest_answer(player_id, trigger["index"])
