import dash
import dash_mantine_components as dmc

dash.register_page(__name__, path="/")

layout = [
    dmc.Space(h=100),
    dmc.Center(
        dmc.Button("Rejoindre la partie", size="xl", variant="filled", color="#ff931e")
    ),
]
