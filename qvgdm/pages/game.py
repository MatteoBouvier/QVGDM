import dash
import dash_mantine_components as dmc
import flask
from dash import Input, Output, callback, dcc, html, no_update
from dash.exceptions import PreventUpdate

from qvgdm.game import get_game
from qvgdm.players import Player
from qvgdm.render import show_question

dash.register_page(__name__)

layout = [
    dmc.Space(h=100),
    html.Div(id="player_question_container", style={"height": "30vh", "width": "80vw"}),
    dcc.Interval(id="player_update", interval=1000),
]


@callback(
    Output("player_question_container", "children", allow_duplicate=True),
    Input("url", "pathname"),
    prevent_initial_call=True,
)
def player_set_connected(url: str):
    if url != "/game":
        raise PreventUpdate

    get_game().login_player(Player(flask.request.origin, 0))
    return (
        dmc.Text(
            "En attente de la première question ...",
            size="xl",
            c="white",  # pyright: ignore[reportArgumentType]
        ),
    )


@callback(
    Output("player_question_container", "children", allow_duplicate=True),
    Input("player_update", "n_intervals"),
    prevent_initial_call=True,
)
def player_update_layout(_):
    game = get_game()
    if game.started:
        return show_question(
            game.get_question(),
            game.current_selected,
            game.get_answer() if game.current_validated else None,
        )

    return no_update
