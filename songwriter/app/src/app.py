import os
import pickle

import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from autoencoder.trained_model import TrainedAutoEncoder
from song_interpolation import interpolate_songs

##########
## Config
##########

songs_df = pd.read_csv("../data/songs_with_coordinates.csv", sep=";")

all_artists = songs_df["artista"].unique().tolist()
song_list = list(zip(
    songs_df.apply(lambda x: f"{x['musica']} - ({x['artista']})", axis=1).values,
    songs_df["song_idx"].values
))

auto_encoder = TrainedAutoEncoder("../data/")

########
# APP
########

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Song Vector Space"),
                        html.Small(html.A("Developed by Tiago Alves", href="https://tiagohca.com/")),
                        html.P(),
                        html.P("A deep learning model read the lyrics of all the songs in this space and mapped them in the figure below"),
                    ]
                )
            )
        ),
        dbc.Row(
            [
                dbc.Col([
                    html.Br(),
                    html.Div(
                        [
                            html.P(["Select the artists:", dcc.Dropdown(
                                id="selected_artists",
                                options=[dict(label=art, value=art) for art in all_artists],
                                multi=True,
                                # value=all_artists,
                                placeholder="Artist"
                            )])
                        ]
                    )
                ], width=2),
                dbc.Col([
                    html.Div(
                        dcc.Graph(id="graph", config={
                            'displayModeBar': False
                        })
                    )],
                    width=10
                )
            ]
        ),
        dbc.Row([
           html.H2("Lyrics Generator")
        ]),
        dbc.Row([
            dbc.Col([
                html.P("Select the weight of each song on the new one:"),
                dcc.Slider(
                    id='song_weight',
                    min=0,
                    max=1,
                    step=0.05,
                    value=0.5,
                ),
            ], width=8),
            dbc.Col([
                daq.BooleanSwitch(
                    id="shuffle_song",
                    on=True,
                    label="Shuffle",
                    labelPosition="top"
                )
            ])
        ]),
        dbc.Row(
            [
                dbc.Col([
                    html.Div(
                        [
                            html.P(["Select a song:", dcc.Dropdown(
                                id="song1",
                                options=[dict(label=song_name, value=song_idx) for song_name, song_idx in
                                         song_list],
                                multi=False,
                            )])
                        ]
                    ),
                    html.Div(id="song1_lyrics", style={'whiteSpace': 'pre-wrap'}),
                ], width=4),
                dbc.Col([
                    html.Div(
                        [
                            html.P(["Select a song:", dcc.Dropdown(
                                id="song2",
                                options=[dict(label=song_name, value=song_idx) for song_name, song_idx in
                                         song_list],
                                multi=False,
                            )])
                        ]
                    ),
                    html.Div(id="song2_lyrics", style={'whiteSpace': 'pre-wrap'}),
                ], width=4),
                dbc.Col([
                    html.P("New song:"),
                    html.Div(id="generated_lyrics", style={'whiteSpace': 'pre-wrap'}),
                ], width=4),
            ]
        )
    ],
    fluid=True
)


#######
# Figure
#######

@app.callback(
    Output("graph", "figure"),
    [Input("selected_artists", "value")]
)
def make_figure(selected_artists):
    display_df = songs_df
    if selected_artists:
        display_df = songs_df[songs_df["artista"].isin(selected_artists)] if len(selected_artists) > 0 else songs_df

    fig = px.scatter(
        display_df,
        x="x", y="y",
        color="artista",
        hover_data=["musica"],
        height=600,
        opacity=0.8,
        template="plotly_white"
    )

    # # Configure plot
    fig.update_traces(marker_size=10)
    # fig.update_layout(showlegend=False, autosize=True)

    return fig

@app.callback(
    Output("song1_lyrics", "children"),
    [Input("song1", "value")]
)
def display_song1(song1):
    if song1:
        return songs_df[songs_df["song_idx"] == song1]["letra"].values[0]
    return ""


@app.callback(
    Output("song2_lyrics", "children"),
    [Input("song2", "value")]
)
def display_song2(song2):
    if song2:
        return songs_df[songs_df["song_idx"] == song2]["letra"].values[0]
    return ""


@app.callback(
    Output("generated_lyrics", "children"),
    [Input("song1", "value")] +
    [Input("song2", "value")] +
    [Input("song_weight", "value")] +
    [Input("shuffle_song", "on")]
)
def display_song2(song1, song2, song_weight, shuffle_song):
    if song1 and song2:
        return interpolate_songs(
            auto_encoder,
            song1, song2,
            1-song_weight, song_weight, shuffle_song
        )
    return ""


port = os.environ.get('PORT', 5000)
app.run_server(host="0.0.0.0", debug=True, port=port)
