import dash
import dash_mantine_components as dmc
from dash import dcc, html

from qvgdm.game import Game

app = dash.Dash(
    "qvgdm",
    title="Qui veut gagner des mozzas ?",
    update_title="",
    use_pages=True,
)

app.game = Game()  # pyright: ignore[reportAttributeAccessIssue]

app.layout = dmc.MantineProvider(
    html.Div(
        [
            dmc.BackgroundImage(
                [
                    dmc.Center(
                        [
                            html.Div(
                                id="public_joker_result",
                                style={"width": "33%"},
                            ),
                            html.Img(
                                src="/assets/logo.png",
                                width="33%",
                                id="logo",
                            ),
                            html.Div(
                                html.Div(
                                    id="score_ladder",
                                    style={
                                        "width": "80%",
                                        "marginLeft": "10%",
                                    },
                                ),
                                style={"width": "33%"},
                            ),
                        ],
                        style={"height": "25%", "width": "100%"},
                    ),
                    dmc.Space(h=20),
                    html.Div(
                        dash.page_container,
                        style={"height": "75%", "width": "100%"},
                        id="page_container_wrapper",
                    ),
                ],
                src="/assets/background.jpg",
                styles={"root": {"height": "100%"}},
            ),
            dcc.Location(id="url"),
            dcc.Interval(
                id="joker_public_timer",
                interval=1000,
                n_intervals=0,
                max_intervals=60,
                disabled=True,
            ),
        ],
        style={"height": "100vh", "width": "100vw"},
    )
)
