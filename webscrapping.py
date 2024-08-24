import requests
import pandas as pd
from bs4 import BeautifulSoup

# Requisição da página da Terra.com.br com a tabela do campeonato
pagina = requests.get('https://www.terra.com.br/esportes/futebol/brasileiro-serie-a/tabela/')

# Convertendo em HTML o conteúdo
soup = BeautifulSoup(pagina.content, 'html.parser')

# Pegando todos elementos dentro das tags TR
linhas = soup.find_all('tr')

# Removendo a primeira linha (cabeçalho da tabela)
linhas.pop(0)

# Pegando as informações e passando para list
posicoes = list(map(lambda time: time.select('.position')[0].text, linhas))
times = list(map(lambda time: time.select('.team-name')[0].text, linhas))
pontuacao = list(map(lambda time: time.select('.points')[0].text, linhas))
qntd_jogos = list(map(lambda time: time.select('td[title="Jogos"]')[0].text, linhas))
qtd_vitorias = list(map(lambda time: time.select('td[title="Vitórias"]')[0].text, linhas))
qtd_empates = list(map(lambda time: time.select('td[title="Empates"]')[0].text, linhas))
qtd_derrotas = list(map(lambda time: time.select('td[title="Derrotas"]')[0].text, linhas))
gols = list(map(lambda time: time.select('td[title="Gols Pró"]')[0].text, linhas))
gols_contra = list(map(lambda time: time.select('td[title="Gols Contra"]')[0].text, linhas))

# Transformando as listas em um dataFrame 
df = pd.DataFrame({
    'Posição': posicoes,
    'Time': times,
    'Pontuação': pontuacao,
    'Jogos': qntd_jogos,
    'Vitórias': qtd_vitorias,
    'Empates': qtd_empates,
    'Derrotas': qtd_derrotas,
    'Gols Pró': gols,
    'Gols Contra': gols_contra
})

# Fazendo as transformações
df['Time'] = df['Time'].str.replace(' >>\n', '', regex=False)
df['Posição'] = df['Posição'].map(int)
df['Gols Pró'] = df['Gols Pró'].map(int)
df['Gols Contra'] = df['Gols Contra'].map(int)
df['Saldo Gols'] = df['Gols Pró'].map(int) - df['Gols Contra'].map(int)
df['Jogos'] = df['Jogos'].map(int)
df['Vitórias'] = df['Vitórias'].map(int)
df['Empates'] = df['Empates'].map(int)
df['Derrotas'] = df['Derrotas'].map(int)
df['Aproveitamento'] = (((df['Vitórias'] * 3) + df['Empates']) / (df['Jogos'] * 3) * 100).round(2)

df = df.sort_values(by='Gols Pró', ascending=False).reset_index(drop=True)
df['Ranking ataque'] = df.index + 1

df = df.sort_values(by='Gols Contra', ascending=True).reset_index(drop=True)
df['Ranking defesa'] = df.index + 1

df = df.sort_values(by='Posição').reset_index(drop=True)

# Trazendo as informações
def resumo_time(nomeTime):
    time = df[df['Time'].isin([nomeTime])].iloc[0].to_dict()
    return f"""{time['Time']}
{time['Posição']} º - {time['Pontuação']} pontos em {time['Jogos']} jogos ({time['Vitórias']}V/{time['Empates']}E/{time['Derrotas']}D) - {time['Aproveitamento']} % de aproveitamento
Gols pró: {time['Gols Pró']} - Gols contra: {time['Gols Contra']} - Saldo de gols: {time['Saldo Gols']}
Ranking ataque: {time['Ranking ataque']} - Ranking defesa: {time['Ranking defesa']}"""

resumo_time('Cruzeiro')

teste