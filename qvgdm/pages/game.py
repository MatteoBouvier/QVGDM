import dash
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash import callback, Input, get_app
import flask

from qvgdm.players import Player

dash.register_page(__name__)

layout = [dmc.Space(h=100), dmc.Center()]


@callback(Input("url", "pathname"))
def player_set_connected(url: str):
    app = get_app()

    if url != "/game" or app.player:
        raise PreventUpdate

    app.player = Player(flask.request.origin, 0)
