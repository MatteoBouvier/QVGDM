import dash
import dash_mantine_components as dmc
import flask
from dash import Input, Output, callback

from qvgdm.players import Player, guests

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
    Input("guest_join_button", "n_clicks"),
)
def guest_join(n: int | None):
    player_id = flask.request.origin

    if not n:
        if player_id in guests:
            # guest player already connected
            return "none", "block"

        # new connection, main page
        return "block", "none"

    # new connection success
    guests[player_id] = Player(player_id, 0)
    return "none", "block"
