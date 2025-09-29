import time
import dash
import dash_mantine_components as dmc
import flask
from dash import Input, Output, callback, no_update

from qvgdm.players import Player, players

dash.register_page(__name__, path="/")


layout = [
    dmc.Space(h=100),
    dmc.Center(
        [
            dmc.Stack(
                dmc.Button(
                    "Rejoindre la partie",
                    id="guest_join_button",
                    size="xl",
                    variant="filled",
                    color="#ff931e",  # pyright: ignore[reportArgumentType]
                ),
                id="guest_layout_logged_out",
            ),
            dmc.Stack(
                dmc.Text(
                    "En attente de la première question ...",
                    size="xl",
                    c="white",  # pyright: ignore[reportArgumentType]
                ),
                id="guest_layout_logged_in",
                display="none",
            ),
        ],
        id="guest_layout",
    ),
]


@callback(
    Output("guest_layout_logged_out", "display"),
    Output("guest_layout_logged_in", "display"),
    Output("guest_connection_trigger", "data"),
    Input("guest_join_button", "n_clicks"),
)
def guest_join(n: int | None):
    player_id = flask.request.origin

    if not n:
        if player_id in players:
            # guest player already connected
            return "none", "block", no_update

        # new connection, main page
        return "block", "none", no_update

    # new connection success
    players[player_id] = Player(player_id, 0)
    return "none", "block", time.time()
