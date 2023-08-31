from app import * 
from data import df_paid_games_score, note_counts
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO
import pandas as pd

url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.FLATLY

template_theme1 = 'vapor'
template_theme2 = 'flatly'

game_options = [{'label': x, 'value': x} for x in df_paid_games_score['Jogos'].unique()]

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
        ]),
        dbc.Col([
            html.H1('Steam Games 2023'),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar_graph')
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='game_picker', options=game_options, multi=True, value=[game['label'] for game in game_options[:10] + game_options[-10:]]),
        ])
    ]),
    dbc.Row([
        dcc.Graph(id='scatter_graph'),
    ]),
    dbc.Row([
        dcc.Graph(id='line_graph'),  # Novo componente para o gráfico de linhas
    ]),
    dbc.Row([
        dcc.Dropdown(id='game_picker_pie', options=game_options, multi=True, value=[game['label'] for game in game_options[:4] + game_options[-4:]]),
        dcc.Graph(id='pie_chart')
    ]),
])

@app.callback(
    Output('bar_graph', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('game_picker', 'value')
)
def update_bar_graph(toggle, games):
    templates = template_theme1 if toggle else template_theme2
    
    if 'Valor Inicial' not in games:
        games.append('Valor Inicial')

    filtered_df = df_paid_games_score[df_paid_games_score['Jogos'].isin(games)]
    
    fig = px.bar(filtered_df, x='Jogos', y='Notas', title='Notas dos Jogos', color='Notas')
    return fig

@app.callback(
    Output('scatter_graph', 'figure'),  # Update the correct graph id here
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_scatter_graph(toggle):
    templates = template_theme1 if toggle else template_theme2;
    fig = px.scatter(df_paid_games_score, x='Notas', y='Jogos', color='Notas', title='Outro Título')
    fig.update_layout(xaxis_title='Jogos', yaxis_title='Notas', xaxis_tickangle=-45)

    return fig

@app.callback(
    Output('line_graph', 'figure'),  # Update the correct graph id here
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
)
def update_line_graph(toggle):
    templates = template_theme1 if toggle else template_theme2

    fig = px.line(df_paid_games_score, x='Notas', y='Jogos', color='Notas', title='Outro Título')
    fig.update_layout(xaxis_title='Jogos', yaxis_title='Notas', xaxis_tickangle=-45)

    return fig

@app.callback(
    Output('pie_chart', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('game_picker_pie', 'value')
)
def update_pie_chart(toggle, selected_games):
    templates = template_theme1 if toggle else template_theme2

    if selected_games:
        filtered_df = df_paid_games_score[df_paid_games_score['Jogos'].isin(selected_games)]
        note_counts_games = filtered_df['Notas'].value_counts().reset_index()
        note_counts_games.columns = ['Notas', 'Count']
    
        non_zero_note_counts = note_counts_games[note_counts_games['Count'] > 0]
        fig = px.pie(non_zero_note_counts, names='Notas', values='Count', title='Pizza minha e pizza nossa paizão')

        game_names = filtered_df['Jogos']
        fig.update_traces(textinfo='label+percent+text', hoverinfo='label+percent+text', text=game_names)

        return fig

if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)