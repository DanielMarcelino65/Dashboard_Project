from app import * 
from data import df_paid_games_score, non_zero_note_counts, non_zero_free_note_counts
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
free_note_options =[{ 'label': x, 'value': x} for x in non_zero_free_note_counts['Notas'].unique()]

app.layout = dbc.Container([
    dbc.Row([
            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
    ]),
    dbc.Row([
        html.H1('Steam Games 2023', className='text-center')
    ]),
    dbc.Row([
        dcc.Graph(id='bar_graph'),
        dbc.Row([
            html.Button('Show/hide games', id='show_hide', n_clicks=0, style={'borderRadius': '40px', 'border': '1px solid black', 'width': 'auto', 'margin-left': '10px', 'whiteSpace': 'nowrap', 'padding': '5px', 'background-color': '#ef42f5'}),
        ], justify='center'),  
        dcc.Dropdown(id='game_picker', options=game_options, multi=True, value=[game['label'] for game in game_options[:10] + game_options[-10:]])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='pie_chart'),
            dcc.Dropdown(id='game_picker_pie', options=note_options, multi=True, value=[note['label'] for note in note_options[:5] + note_options[-5:]]),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='pie_chart2'),
            html.P('Escolha as notas para o gráfico de pizza', className='text-center', style={'position': 'relative', 'bottom': '30px', 'height': '0px'}),
            dcc.Dropdown(id='game_picker_pie2', options=free_note_options, multi=True, value=[note['label'] for note in free_note_options[:5] + free_note_options[-5:]]),
        ], width=6),
    ]),
])

@app.callback(
    Output('game_picker', 'style'),
    Input('show_hide', 'n_clicks'),
    prevent_initial_call=True,
)

def show_hide(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'block', 'height': 'auto'}
    else:
        return {'display': 'none'}

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
    
    fig = px.bar(filtered_df, x='Jogos', y='Notas', title='Metacritic de Jogos Pagos', color='Jogos', template=templates)
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
        fig = px.pie(filtered_df, names='Notas', values='Count', title='Pizza de Jogos Pagos',template=templates)


        return fig
    
@app.callback(
    Output('pie_chart2', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('game_picker_pie2', 'value')
)

def update_pie_chart2(toggle, games):
    templates = template_theme1 if toggle else template_theme2
    
    if 'Valor Inicial' not in games:
        games.append('Valor Inicial')

    filtered_df = non_zero_free_note_counts[non_zero_free_note_counts['Notas'].isin(games)]
    
    fig = px.pie(filtered_df, names='Notas', values='Count', title='Pizza de Notas de Jogos Gratuitos', color='Notas', template=templates)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)
