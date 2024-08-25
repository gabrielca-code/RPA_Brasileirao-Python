import requests
import pandas as pd
from bs4 import BeautifulSoup

url_gazeta = 'https://www.gazetaesportiva.com/campeonatos/brasileiro-serie-a/'

# Requisição da página da Terra.com.br com a tabela do campeonato
pagina = requests.get(url_gazeta)

# Convertendo em HTML o conteúdo
soup = BeautifulSoup(pagina.content, 'html.parser')

# Extração e transformação dos dados da classificação
# Extraindo todos os jogos
jogos = soup.find_all('li', class_='table__games__item')

dados_jogos = list(map(lambda jogo: {
    'Mandante': jogo.select('a')[0]['title'],
    'Placar mandante': jogo.select('span')[5].text,
    'Visitante': jogo.select('a')[3]['title'],
    'Placar visitante': jogo.select('span')[6].text,
    'Data': jogo.select('span')[0].text
}, jogos))

df2 = pd.DataFrame(dados_jogos)
df2['Placar mandante'] = df2['Placar mandante'].apply(lambda cell: int(cell) if pd.notna(cell) and cell.strip() != '' and cell.isdigit() else cell)
df2['Placar visitante'] = df2['Placar visitante'].apply(lambda cell: int(cell) if pd.notna(cell) and cell.strip() != '' and cell.isdigit() else cell)
df2['Data'] = df2['Data'].apply(lambda cell: cell.split('\n')[1] if pd.notna(cell) and cell.strip() != '' and len(cell.split('\n')) > 1 else cell)
df2['Data'] = pd.to_datetime(df2['Data'], format='%d/%m %H:%M', errors='coerce')
df2['Data'] = df2['Data'].apply(lambda dt: dt.replace(year=2024) if pd.notna(dt) else dt)
df2['Resultado'] = df2.apply(
    lambda row: 'Jogo não realizado' if row['Placar mandante'] == ''
                else 'Visitante' if row['Placar mandante'] < row['Placar visitante']  
                else 'Mandante' if row['Placar mandante'] > row['Placar visitante']
                else 'Empate',
    axis=1
)

# Extração e transformação dos dados da classificação
# Pegando todos elementos dentro das tags TR
classificacao = soup.find_all('tr')

# Removendo a primeira linha (cabeçalho da tabela)
classificacao.pop(0)

# Pegando as informações e passando para list
dados_classificacao = list(map(lambda time: {
    'Posição': time.select('.table__position')[0].text,
    'Time': time.select('.team-link')[0]['title'],
    'Pontuação': time.select('.table__stats')[0].text,
    'Jogos': time.select('.table__stats')[1].text,
    'Vitórias': time.select('.table__stats')[2].text,
    'Empates': time.select('.table__stats')[3].text,
    'Derrotas': time.select('.table__stats')[4].text,
    'Gols pró': time.select('.table__stats')[5].text,
    'Gols contra': time.select('.table__stats')[6].text,
}, classificacao))

# Transformando as listas em um dataFrame 
df = pd.DataFrame(dados_classificacao)

# Fazendo as transformações necessárias
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

df['Jogos mandante'] = df['Time'].apply(lambda time: len(df2[(df2['Mandante'] == time) & (df2['Resultado'] != 'Jogo não realizado')]))
df['Vitórias mandante'] = df['Time'].apply(lambda time: len(df2[(df2['Resultado'] == 'Mandante') & (df2['Mandante'] == time)]))
df['Empates mandante'] = df['Time'].apply(lambda time: len(df2[(df2['Resultado'] == 'Empate') & (df2['Mandante'] == time)]))
df['Aproveitamento mandante'] = ((df['Vitórias mandante'] * 3 + df['Empates mandante']) / (df['Jogos mandante'] * 3) * 100).round(2)

df['Jogos visitante'] = df['Time'].apply(lambda time: len(df2[(df2['Visitante'] == time) & (df2['Resultado'] != 'Jogo não realizado')]))
df['Vitórias visitante'] = df['Time'].apply(lambda time: len(df2[(df2['Resultado'] == 'Visitante') & (df2['Visitante'] == time)]))
df['Empates visitante'] = df['Time'].apply(lambda time: len(df2[(df2['Resultado'] == 'Empate') & (df2['Visitante'] == time)]))
df['Aproveitamento visitante'] = ((df['Vitórias visitante'] * 3 + df['Empates visitante']) / (df['Jogos visitante'] * 3) * 100).round(2)

df2 = df2.sort_values(by='Data', ascending=False)

def ultimos_jogos(time):
    ultimos_jogos = df2[(df2['Resultado'] != 'Jogo não realizado') & ((df2['Mandante'] == time) | (df2['Visitante'] == time))]
    string_ultimos_jogos = ''
    quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
    i = 5

    for i in range(quantidade_ultimos_jogos, 0, -1):
        print(i)
        resultado = ultimos_jogos.iloc[i-1]['Resultado']
        mandante_visitante = 'Mandante' if ultimos_jogos.iloc[i-1]['Mandante'] == time else 'Visitante'        
        string_ultimos_jogos = string_ultimos_jogos + ('E' if resultado == 'Empate' else 'V' if resultado == mandante_visitante else 'D')

    return string_ultimos_jogos

df['Ultimos jogos'] = df['Time'].apply(ultimos_jogos)

# Trazendo as informações
def resumo_time(nomeTime):
    time = df[df['Time'].isin([nomeTime])].iloc[0].to_dict()
    return f"""{time['Time']}
{time['Posição']} º - {time['Pontuação']} pontos em {time['Jogos']} jogos ({time['Vitórias']}V/{time['Empates']}E/{time['Derrotas']}D) - {time['Aproveitamento']} % de aproveitamento
Gols pró: {time['Gols pró']} - Gols contra: {time['Gols contra']} - Saldo de gols: {time['Saldo gols']}
Ranking ataque: {time['Ranking ataque']} - Ranking defesa: {time['Ranking defesa']}"""

print(df)