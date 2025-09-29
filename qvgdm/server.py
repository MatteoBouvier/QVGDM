import dash
import dash_mantine_components as dmc
from dash import html, dcc

app = dash.Dash(
    "qvgdm",
    title="Qui veut gagner des mozzas ?",
    use_pages=True,
)

app.layout = dmc.MantineProvider(
    html.Div(
        [
            dmc.BackgroundImage(
                dmc.Center(
                    dmc.Stack(
                        [
                            dmc.Center(
                                html.Img(src="/assets/logo.png", height=250, width=250)
                            ),
                            dmc.Text(
                                "Qui veut gagner des mozzas",
                                size="40px",  # pyright: ignore[reportArgumentType]
                                c="white",  # pyright: ignore[reportArgumentType]
                            ),
                            dash.page_container,
                        ],
                    ),
                    style={"height": "100%", "width": "100%"},
                ),
                src="/assets/background.jpg",
                styles={"root": {"height": "100%"}},
            ),
            dcc.Store(id="player_connection_trigger", data=0),
        ],
        style={"height": "100vh", "width": "100vw"},
    )
)
