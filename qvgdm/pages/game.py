import dash
import dash_mantine_components as dmc
import flask
from dash import Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate

from qvgdm.game import get_game
from qvgdm.players import Player
from qvgdm.render import show_jokers, show_question

dash.register_page(__name__)

layout = [
    dmc.Space(h=50),
    html.Div(id="player_question_container", style={"height": "30vh", "width": "80vw"}),
    dmc.Center(
        dmc.Group(
            id="player_joker_container",
        ),
        style={"width": "80vw"},
    ),
    dcc.Interval(id="player_update", interval=1000),
]


@callback(
    Input("url", "pathname"),
    prevent_initial_call=True,
)
def player_set_connected(url: str):
    if url != "/game":
        raise PreventUpdate

    get_game().login_player(Player(flask.request.origin, "__RESERVED:PLAYER__"))


@callback(
    Output("player_question_container", "children"),
    Output("player_joker_container", "children"),
    Input("player_update", "n_intervals"),
    prevent_initial_call=True,
)
def player_update_layout(_):
    game = get_game()
    if game.started:
        return show_question(
            game.get_question(),
            game.current_selected,
            game.get_answer_index() if game.current_validated else None,
            game.jokers.invalid_options,
        ), show_jokers(game.jokers)

    else:
        return dmc.Center(
            dmc.Loader(
                size="xl",
                type="oval",
                color="white",  # pyright: ignore[reportArgumentType]
            ),
        ), None
