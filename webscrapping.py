import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://www.terra.com.br/esportes/futebol/brasileiro-serie-a/tabela/'
url_gazeta = 'https://www.gazetaesportiva.com/campeonatos/brasileiro-serie-a/'

# Requisição da página da Terra.com.br com a tabela do campeonato
pagina = requests.get(url)

# Convertendo em HTML o conteúdo
soup = BeautifulSoup(pagina.content, 'html.parser')

# Pegando todos elementos dentro das tags TR
classificacao = soup.find_all('tr')

# Removendo a primeira linha (cabeçalho da tabela)
classificacao.pop(0)

# Pegando as informações e passando para list

dados_classificacao = list(map(lambda time: {
    'Posição': time.select('.position')[0].text,
    'Time': time.select('.team-name')[0].text,
    'Pontuação': time.select('.points')[0].text,
    'Jogos': time.select('td[title="Jogos"]')[0].text,
    'Vitórias': time.select('td[title="Vitórias"]')[0].text,
    'Empates': time.select('td[title="Empates"]')[0].text,
    'Derrotas': time.select('td[title="Derrotas"]')[0].text,
    'Gols pró': time.select('td[title="Gols Pró"]')[0].text,
    'Gols contra': time.select('td[title="Gols Contra"]')[0].text
}, classificacao))

# Transformando as listas em um dataFrame 
df = pd.DataFrame(dados_classificacao)

# Fazendo as transformações necessárias
df['Time'] = df['Time'].str.replace(' >>\n', '', regex=False)
df['Posição'] = df['Posição'].map(int)
df['Gols pró'] = df['Gols pró'].map(int)
df['Gols contra'] = df['Gols contra'].map(int)
df['Saldo gols'] = df['Gols pró'].map(int) - df['Gols contra'].map(int)
df['Jogos'] = df['Jogos'].map(int)
df['Vitórias'] = df['Vitórias'].map(int)
df['Empates'] = df['Empates'].map(int)
df['Derrotas'] = df['Derrotas'].map(int)
df['Aproveitamento'] = (((df['Vitórias'] * 3) + df['Empates']) / (df['Jogos'] * 3) * 100).round(2)

df = df.sort_values(by='Gols pró', ascending=False).reset_index(drop=True)
df['Ranking ataque'] = df.index + 1

df = df.sort_values(by='Gols contra', ascending=True).reset_index(drop=True)
df['Ranking defesa'] = df.index + 1

df = df.sort_values(by='Posição').reset_index(drop=True)

# Trazendo as informações
def resumo_time(nomeTime):
    time = df[df['Time'].isin([nomeTime])].iloc[0].to_dict()
    return f"""{time['Time']}
{time['Posição']} º - {time['Pontuação']} pontos em {time['Jogos']} jogos ({time['Vitórias']}V/{time['Empates']}E/{time['Derrotas']}D) - {time['Aproveitamento']} % de aproveitamento
Gols pró: {time['Gols pró']} - Gols contra: {time['Gols contra']} - Saldo de gols: {time['Saldo gols']}
Ranking ataque: {time['Ranking ataque']} - Ranking defesa: {time['Ranking defesa']}"""

# Requisição da página da Terra.com.br com a tabela do campeonato
pagina = requests.get(url_gazeta)

# Convertendo em HTML o conteúdo
soup = BeautifulSoup(pagina.content, 'html.parser')

# Extraindo todos os jogos
jogos = soup.find_all('li', class_='table__games__item')

dados_jogos = list(map(lambda jogo: {
    'Mandante': jogo.select('a')[0].text,
    'Placar mandante': jogo.select('span')[5].text,
    'Visitante': jogo.select('a')[4].text,
    'Placar visitante': jogo.select('span')[7].text,
    'Data': jogo.select('span')[0].text
}, jogos))

df = pd.DataFrame(dados_jogos)

print(df)