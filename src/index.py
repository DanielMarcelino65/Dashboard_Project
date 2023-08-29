from app import * 
from data import paid_games_and_score, free_games_and_score, sorted_games_and_score, null_games_and_score

if __name__ == '__main__':
    app.run_server(debug=True, port = 8050)