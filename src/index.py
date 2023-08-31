from app import * 
from data import df_paid_games_score, non_zero_note_counts
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
note_options =[{ 'label': x, 'value': x} for x in non_zero_note_counts['Notas'].unique()]

app.layout = dbc.Container([
    dbc.Row([
        ThemeSwitchAIO(aio_id = 'theme', themes = [url_theme1, url_theme2])
    ]),
    dbc.Row([
        html.H1('Steam Games 2023', className = 'text-center')
    ]),
    dbc.Row([
        dcc.Graph(id = 'bar_graph'),
        dcc.Dropdown(id = 'game_picker', options = game_options, multi = True, value = [game['label'] for game in game_options[:10] + game_options[-10:]])
    ]),
    dbc.Row([
        dcc.Graph(id = 'pie_chart'),
        dcc.Dropdown(id = 'game_picker_pie', options = note_options, multi = True, value = [game['label'] for game in note_options[:5] + note_options[-5:]])
    ])
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
    filtered_df.loc[:, 'Notas'] = filtered_df['Notas'].astype(float)
    
    fig = px.bar(filtered_df, x = 'Jogos', y = 'Notas', title = 'Jogos Grátis & Pagos + Notas', color = 'Jogos', template = templates)

    return fig

@app.callback(
    Output('pie_chart', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('game_picker_pie', 'value')
)
def update_pie_chart(toggle, selected_games):
    templates = template_theme1 if toggle else template_theme2

    if selected_games:
        filtered_df = non_zero_note_counts[non_zero_note_counts['Notas'].isin(selected_games)]
        
        fig = px.pie(filtered_df, names = 'Notas', values = 'Count', title = 'Games Pagos', template = templates)

        fig.update_traces(textinfo='label+percent', hoverinfo='label+percent')

        return fig

if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)
