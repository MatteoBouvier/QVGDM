import dash
import dash_mantine_components as dmc
import flask
from dash import Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate

from qvgdm.game import get_game
from qvgdm.render import show_jokers, show_public_stats, show_question, show_score

dash.register_page(__name__)

layout = [
    dmc.Space(h=50),
    dmc.Center(
        dmc.Text("", c="white", size="50px", id="player_joker_public_timer_display")  # pyright: ignore[reportArgumentType]
    ),
    dmc.Space(h=20),
    html.Div(id="player_question_container", style={"height": "30vh"}),
    dmc.Center(
        dmc.Group(
            id="player_joker_container",
        ),
    ),
    dcc.Interval(id="player_update", interval=500),
]


@callback(
    Input("url", "pathname"),
    prevent_initial_call=True,
)
def player_set_connected(url: str):
    if url != "/game":
        raise PreventUpdate

    get_game().login_player(flask.request.origin)


@callback(
    Output("player_question_container", "children"),
    Output("player_joker_container", "children"),
    Output("score_ladder", "children", allow_duplicate=True),
    Output("public_joker_result", "children", allow_duplicate=True),
    Output("player_joker_public_timer_display", "children"),
    Input("player_update", "n_intervals"),
    prevent_initial_call=True,
)
def player_update_layout(_):
    game = get_game()

    match game.status:
        case "waiting":
            return (
                dmc.Center(
                    html.Img(src="/assets/QRCode.png"),
                    style={"height": "100%"},
                ),
                None,
                None,
                None,
                None,
            )

        case "started":
            assert game.player is not None

            return (
                show_question(
                    game.get_question(),
                    game.current_option_nb,
                    game.current_selected,
                    game.get_answer_index() if game.current_validated else None,
                    game.jokers.invalid_options,
                ),
                show_jokers(game.jokers),
                show_score(
                    game.player.score,
                    game.current_index,
                ),
                show_public_stats(game.jokers.answers),
                game.jokers.timer,
            )

        case "ended":
            score = game.get_player_score()
            winners, _ = game.get_winners()

            return (
                dmc.Center(
                    dmc.Stack(
                        [
                            dmc.Text(
                                f"Félicitations, vous avez gagné {score} mozzas",
                                c="white",  # pyright: ignore[reportArgumentType]
                                size=50,  # pyright: ignore[reportArgumentType]
                            ),
                            dmc.Text(
                                f"Dans le public, {' & '.join(winners)} {'a' if len(winners) == 1 else 'ont'} le mieux répondu"
                            ),
                        ]
                    ),
                    style={"height": "100%"},
                ),
                None,
                show_score(
                    None if game.player is None else game.player.score,
                    game.current_index,
                ),
                None,
                None,
            )
