from app import *
from data import df_paid_games_score, non_zero_note_counts, non_zero_free_note_counts, df_free_games_score, media_jogos_gratuitos, media_jogos_pagos
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO
import pandas as pd

# Definição dos temas (URLs) e modelos de tema
url_theme1 = dbc.themes.VAPOR
url_theme2 = dbc.themes.FLATLY
template_theme1 = 'vapor'
template_theme2 = 'flatly'

# Função para truncar texto do eixo X do gráfico de barras
def truncate_text(text, max_length=30):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

# Definição das opções para os dropdowns
game_options = [{'label': x, 'value': x} for x in df_paid_games_score['Jogos'].unique()]
free_game_options = [{'label': x, 'value': x} for x in df_free_games_score['Jogos'].unique()]
note_options = [{'label': x, 'value': x} for x in non_zero_note_counts['Notas'].unique()]
free_note_options = [{'label': x, 'value': x} for x in non_zero_free_note_counts['Notas'].unique()]

# Definição do layout do aplicativo
app.layout = dbc.Container([
    dbc.Row([
        ThemeSwitchAIO(aio_id='theme', themes=[url_theme1, url_theme2]),
    ]),
    dbc.Row([
        html.H1('Steam Games 2023', className='text-center')
    ]),
    dbc.Row([
        # Dropdown e botão para seleção de jogos pagos
        dcc.Dropdown(id='game_picker', options=game_options, multi=True, value=[game['label'] for game in game_options[:10] + game_options[-10:]]),
        dbc.Row([
            html.Button(content, id='show_hide', n_clicks=0, style={'borderRadius': '40px', 'border': '1px solid black', 'width': 'auto', 'margin-left': '10px', 'whiteSpace': 'nowrap', 'padding': '5px', 'background-color': '#ef42f5', 'fontWeight': 'bold'}),
        ], justify='center'),
        dcc.Graph(id='bar_graph'),  # Gráfico de barras para jogos pagos
    ]),
    dbc.Row([
        # Dropdown e botão para seleção de jogos gratuitos
        dcc.Dropdown(id='game_picker2', options=free_game_options, multi=True, value=[game['label'] for game in free_game_options[:10] + free_game_options[-10:]]),
        dbc.Row([
            html.Button(content2, id='show_hide2', n_clicks=0, style={'borderRadius': '40px', 'border': '1px solid black', 'width': 'auto', 'margin-left': '10px', 'whiteSpace': 'nowrap', 'padding': '5px', 'background-color': '#ef42f5', 'fontWeight': 'bold'}),
        ], justify='center'),
        dcc.Graph(id='bar_graph2'),  # Gráfico de barras para jogos gratuitos
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='pie_chart'),  # Gráfico de pizza para notas de jogos pagos
            html.P('Escolha as notas para o gráfico de pizza', className='text-center', style={'position': 'relative', 'bottom': '30px', 'height': '0px'}),
            dcc.Dropdown(id='game_picker_pie', options=note_options, multi=True, value=[note['label'] for note in note_options[:5] + note_options[-5:]]),
        ], width=6),
        dbc.Col([
            dcc.Graph(id='pie_chart2'),  # Gráfico de pizza para notas de jogos gratuitos
            html.P('Escolha as notas para o gráfico de pizza', className='text-center', style={'position': 'relative', 'bottom': '30px', 'height': '0px'}),
            dcc.Dropdown(id='game_picker_pie2', options=free_note_options, multi=True, value=[note['label'] for note in free_note_options[:5] + free_note_options[-5:]]),
        ], width=6),
    ]),
])

# Callbacks e funções para mostrar/ocultar jogos e atualizar gráficos
@app.callback(
    Output('game_picker', 'style'),
    Output('show_hide', 'children'),
    Input('show_hide', 'n_clicks'),
    Input('show_hide', 'children'),
    prevent_initial_call=False,
)
def show_hide(n_clicks, children):
    if n_clicks % 2 == 0:
        content = 'Esconder jogos'
        game_picker_style = {'display': 'block', 'height': 'auto'}
    else:
        content = 'Mostrar jogos'
        game_picker_style = {'display': 'none'}
    
    return game_picker_style, content

@app.callback(
    Output('game_picker2', 'style'),
    Output('show_hide2', 'children'),
    Input('show_hide2', 'n_clicks'),
    Input('show_hide2', 'children'),
    prevent_initial_call=False,
)
def show_hide2(n_clicks, children):
    if n_clicks % 2 == 0:
        content2 = 'Esconder jogos'
        game_picker_style = {'display': 'block', 'height': 'auto'}
    else:
        content2 = 'Mostrar jogos'
        game_picker_style = {'display': 'none'}
    
    return game_picker_style, content2

# Callbacks e funções para atualizar gráficos de barras e gráficos de pizza
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
    filtered_df['Jogos'] = filtered_df['Jogos'].apply(truncate_text)
    filtered_df.loc[:, 'Notas'] = filtered_df['Notas'].astype(float)
    
    fig = px.bar(filtered_df, x='Jogos', y='Notas', title='Metacritic de Jogos Pagos', color='Jogos', template=templates)
    fig.add_trace(go.Scatter(x=filtered_df['Jogos'], y=[media_jogos_pagos] * len(filtered_df['Jogos']), name='Média', hoverinfo='text', hovertext=f'Media: {media_jogos_pagos}', mode='lines', line=dict(color='black', width=2, dash='dash')))
    return fig

@app.callback(
    Output('bar_graph2', 'figure'),
    Input(ThemeSwitchAIO.ids.switch('theme'), 'value'),
    Input('game_picker2', 'value')
)
def update_bar_graph(toggle, games):
    templates = template_theme1 if toggle else template_theme2

    if 'Valor Inicial' not in games:
        games.append('Valor Inicial')

    filtered_df = df_free_games_score[df_free_games_score['Jogos'].isin(games)]
    filtered_df.loc[:, 'Notas'] = filtered_df['Notas'].astype(float)
    
    fig = px.bar(filtered_df, x='Jogos', y='Notas', title='Metacritic de Jogos Gratuitos', color='Jogos', template=templates)
    fig.add_trace(go.Scatter(x=filtered_df['Jogos'], y=[media_jogos_gratuitos] * len(filtered_df['Jogos']), name='Média', hoverinfo='text', hovertext=f'Media: {media_jogos_gratuitos}', mode='lines', line=dict(color='black', width=2, dash='dash')))
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
        fig = px.pie(filtered_df, names='Notas', values='Count', title='Pizza de Notas Jogos Pagos', template=templates)
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

# Executa o servidor Dash
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
