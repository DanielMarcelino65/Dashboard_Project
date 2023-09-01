import json
import pandas as pd
import plotly.express as px

def json_loads_single_quotes(text):
    return json.loads(text.replace("'", "\""))

df = pd.read_csv('./assets/steam_app_data.csv')

years = df['release_date'].apply(lambda x: str(x).split(',')[-1].replace("'", "").replace("}", "").strip())
games = df['name']
df_years_games = pd.DataFrame({'Anos': years, 'Jogos': games})
count_by_year = df_years_games['Anos'].value_counts().sort_index()
df['metacritic'] = df['metacritic'].fillna('{"score": 0}')
df['metacritic'] = df['metacritic'].apply(json_loads_single_quotes)
df['score'] = df['metacritic'].apply(lambda x: x['score'])

df_sorted = df.sort_values(by='score', ascending=False)
df_free = df_sorted[df_sorted['is_free'] == True]
df_paid = df_sorted[df_sorted['is_free'] == False]

paid_games_and_score = []
free_games_and_score = []
sorted_games_and_score = []
null_games_and_score = []
counter = 0
        
for index, row in df.iterrows():
    name = row['name']
    score = row['metacritic']['score']
    if score == 0:
        counter = counter + 1
        game_info = f"Jogo: {name}, Nota: {score}"
        null_games_and_score.append(game_info)
        # print(game_info)
        # print(counter)
    

for index, row in df_sorted.iterrows():
    name = row['name']
    score = row['metacritic']['score']
    if score != 0:
        game_info = f"Jogo: {name}, Nota: {score}"
        sorted_games_and_score.append(game_info)
        # print(game_info)

for index, row in df_free.iterrows():
    name = row['name']
    score = row['metacritic']['score']
    if score != 0:
        game_info = f"Jogo: {name}, Nota: {score}"
        free_games_and_score.append(game_info)
        # print(game_info)

for index, row in df_paid.iterrows():
    name = row['name']
    score = row['metacritic']['score']
    if score != 0:
        game_info = f"Jogo: {name}, Nota: {score}"
        paid_games_and_score.append(game_info)
        # print(game_info)


paid_games = []
paid_scores = []
for game_info in paid_games_and_score:
    parts = game_info.split(', ')
    if len(parts) >= 2:
        game_name = parts[0].split(': ')[1]
        game_score_parts = parts[1].split(': ')
        if len(game_score_parts) >= 2:
            game_score = game_score_parts[1]
            paid_games.append(game_name)
            paid_scores.append(game_score)
            # print("Game Name:", game_name)
            # print("Game Score:", game_score)

df_paid_games_score = pd.DataFrame({'Jogos': paid_games, 'Notas': paid_scores})
df_paid_games_score = df_paid_games_score.drop_duplicates(subset=['Jogos'], keep='first')
note_counts = df_paid_games_score['Notas'].value_counts().reset_index()
note_counts.columns = ['Notas', 'Count']
non_zero_note_counts = note_counts[note_counts['Count'] > 0]
non_zero_note_counts = non_zero_note_counts.sort_values(by='Notas', ascending=False)
df_paid_games_score = df_paid_games_score.merge(note_counts, on='Notas', how='right')
df_paid_games_score = df_paid_games_score.sort_values(by='Notas', ascending=False)
