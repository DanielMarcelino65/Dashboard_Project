import json
import pandas as pd
import plotly.express as px

# Função para carregar JSON com aspas simples
def json_loads_single_quotes(text):
    return json.loads(text.replace("'", "\""))

# Carregamento do dataset e preparação dos dados
df = pd.read_csv('./assets/steam_app_data.csv')  # Carrega o conjunto de dados a partir de um arquivo CSV
games = df['name']  # Extrai a coluna 'name' para a lista de jogos
df['metacritic'] = df['metacritic'].fillna('{"score": 0}')  # Preenche valores ausentes em 'metacritic' com JSON padrão
df['metacritic'] = df['metacritic'].apply(json_loads_single_quotes)  # Converte JSON com aspas simples para JSON válido
df['score'] = df['metacritic'].apply(lambda x: x['score'])  # Extrai a pontuação de 'metacritic' para a coluna 'score'

# Separação de jogos pagos e gratuitos
df_sorted = df.sort_values(by='score', ascending=False)  # Classifica o DataFrame pelo score em ordem decrescente
df_free = df_sorted[df_sorted['is_free'] == True]  # Filtra jogos gratuitos
df_paid = df_sorted[df_sorted['is_free'] == False]  # Filtra jogos pagos

# Inicialização de listas para armazenar informações de jogos
paid_games_and_score = []
free_games_and_score = []
sorted_games_and_score = []
null_games_and_score = []
counter = 0

# Laços de repetição para salvar informações de jogos
for index, row in df.iterrows():
    name = row['name']
    score = row['metacritic']['score']
    if score == 0:
        counter = counter + 1
        game_info = f"Jogo: {name}, Nota: {score}"
        null_games_and_score.append(game_info)

for index, row in df_sorted.iterrows():
    name = row['name']
    score = row['metacritic']['score']
    if score != 0:
        game_info = f"Jogo: {name}, Nota: {score}"
        sorted_games_and_score.append(game_info)

for index, row in df_free.iterrows():
    name = row['name']
    score = row['metacritic']['score']
    if score != 0:
        game_info = f"Jogo: {name}, Nota: {score}"
        free_games_and_score.append(game_info)

for index, row in df_paid.iterrows():
    name = row['name']
    score = row['metacritic']['score']
    if score != 0:
        game_info = f"Jogo: {name}, Nota: {score}"
        paid_games_and_score.append(game_info)

# Separação de jogos pagos e suas notas
paid_games = []
paid_scores = []
for game_info in paid_games_and_score:
    game_name_start = game_info.find('Jogo: ')
    game_name_end = game_info.find(', Nota:')
    
    if game_name_start != -1 and game_name_end != -1:
        game_name = game_info[game_name_start + len('Jogo: '):game_name_end].strip()
        game_score_start = game_info.find('Nota: ')
        if game_score_start != -1:
            game_score = game_info[game_score_start + len('Nota: '):].strip()
            paid_games.append(game_name)
            paid_scores.append(game_score)

# Separação de jogos gratuitos e suas notas
free_games = []
free_scores = []
for game_info in free_games_and_score:
    game_name_start = game_info.find('Jogo: ')
    game_name_end = game_info.find(', Nota:')
    
    if game_name_start != -1 and game_name_end != -1:
        game_name = game_info[game_name_start + len('Jogo: '):game_name_end].strip()
        game_score_start = game_info.find('Nota: ')
        if game_score_start != -1:
            game_score = game_info[game_score_start + len('Nota: '):].strip()
            free_games.append(game_name)
            free_scores.append(game_score)

# Criação de um DataFrame com dados dos jogos gratuitos e suas notas
df_free_games_score = pd.DataFrame({'Jogos': free_games, 'Notas': free_scores})

# Contagem das notas dos jogos gratuitos
free_note_counts = df_free_games_score['Notas'].value_counts().reset_index()
free_note_counts.columns = ['Notas', 'Count']
non_zero_free_note_counts = free_note_counts[free_note_counts['Count'] > 0]
non_zero_free_note_counts = non_zero_free_note_counts.sort_values(by='Notas', ascending=False)

# Criação de um DataFrame com dados dos jogos pagos e suas notas
df_paid_games_score = pd.DataFrame({'Jogos': paid_games, 'Notas': paid_scores})
df_paid_games_score = df_paid_games_score.drop_duplicates(subset=['Jogos'], keep='first')

# Contagem das notas dos jogos pagos
note_counts = df_paid_games_score['Notas'].value_counts().reset_index()
note_counts.columns = ['Notas', 'Count']

# Cálculo da média das notas dos jogos pagos e gratuitos (acima de 0)
non_zero_note_counts = note_counts[note_counts['Count'] > 0]
non_zero_note_counts = non_zero_note_counts.sort_values(by='Notas', ascending=False)
df_paid_games_score = df_paid_games_score.merge(note_counts, on='Notas', how='right')
df_paid_games_score = df_paid_games_score.sort_values(by='Notas', ascending=False)

# Cálculo da média das notas dos jogos pagos e gratuitos
media_jogos_pagos_noround = df_paid_games_score['Notas'].astype(float).mean()
media_jogos_gratuitos_noround = df_free_games_score['Notas'].astype(float).mean()
media_jogos_pagos = round(media_jogos_pagos_noround, 2)
media_jogos_gratuitos = round(media_jogos_gratuitos_noround, 2)
