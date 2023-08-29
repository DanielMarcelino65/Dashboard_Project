import json
import pandas as pd

def json_loads_single_quotes(text):
    return json.loads(text.replace("'", "\""))

df = pd.read_csv('./assets/steam_app_data.csv')

df['metacritic'] = df['metacritic'].fillna('{"score": 0}')
df['metacritic'] = df['metacritic'].apply(json_loads_single_quotes)
df['score'] = df['metacritic'].apply(lambda x: x['score'])

df_sorted = df.sort_values(by='score', ascending=False)
df_free = df_sorted[df_sorted['is_free'] == True]
df_paid = df_sorted[df_sorted['is_free'] == False]
df_samePublisher = df_sorted[df_sorted['publishers'].apply(lambda x: isinstance(x, list) and 'Valve' in x)]

paid_games_and_score = []
free_games_and_score = []
sorted_games_and_score = []
null_games_and_score = []

        
for index, row in df.iterrows():
    name = row['name']
    score = row['metacritic']['score']
    if score == 0:
        game_info = f"Jogo: {name}, Nota: {score}"
        null_games_and_score.append(game_info)
        # print(game_info)

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
