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
                dmc.Center(
                    dmc.Stack(
                        [
                            dmc.Center(
                                [
                                    html.Div(
                                        id="public_joker_result",
                                        style={"width": "400px"},
                                    ),
                                    html.Img(
                                        src="/assets/logo.png", height=250, width=250
                                    ),
                                    html.Div(
                                        html.Div(
                                            id="score_ladder",
                                            style={
                                                "width": "200px",
                                                "marginLeft": "100px",
                                            },
                                        ),
                                        style={"width": "400px"},
                                    ),
                                ],
                                style={"height": "400px"},
                            ),
                            dash.page_container,
                        ],
                    ),
                    style={"height": "100%", "width": "100%"},
                ),
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
