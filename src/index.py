from app import * 
from data import paid_games_and_score, free_games_and_score, sorted_games_and_score, null_games_and_score
from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import ThemeSwitchAIO

if __name__ == '__main__':
    app.run_server(debug=True, port = 8050)