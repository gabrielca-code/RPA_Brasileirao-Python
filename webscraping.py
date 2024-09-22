import requests
import pandas as pd
from bs4 import BeautifulSoup

dfClassificacao = pd.DataFrame()
dfJogos = pd.DataFrame()

class Brasileirao():

    def __init__(self):
        paginaRequisicao = self.requisicaoPagina('https://www.gazetaesportiva.com/campeonatos/brasileiro-serie-a/')
        if paginaRequisicao.status_code == 200:
            conteudoHTMLPagina = self.converterRequisicaoParaHTML(paginaRequisicao)

            htmlJogos = self.extrairJogosHTML(conteudoHTMLPagina)
            dictJogos = self.criarDicionarioJogos(htmlJogos)
            self.dfJogos = self.converterDicionarioEmDataFrame(dictJogos)
            self.dfJogos = self.transformacoesDataFrameJogos(self.dfJogos)

            htmlClassificacao = self.extrairClassificacaoHTML(conteudoHTMLPagina)
            dictClassificacao = self.criarDicionarioClassificacao(htmlClassificacao)
            self.dfClassificacao = self.converterDicionarioEmDataFrame(dictClassificacao)
            self.dfClassificacao = self.transformacoesDataFrameClassificacao(self.dfClassificacao)

            self.dfClassificacao = self.transformacoesInterDataFrames(self.dfClassificacao, self.dfJogos)

            # print(self.resumo_geral(self.procurarTime(self.dfClassificacao, 'Fluminense')))
            # print(self.resumo_geral(self.procurarTime(self.dfClassificacao, 'São Paulo')))
        else:
            print(f"Erro, código {paginaRequisicao.status_code}")    

    def requisicaoPagina(self, url):
        return requests.get(url)
        
    def converterRequisicaoParaHTML(self, pagina) :
        return BeautifulSoup(pagina.content, 'html.parser')

    def extrairJogosHTML(self, html):
        return html.find_all('li', class_='table__games__item')

    def criarDicionarioJogos(self, jogos):
        return list(map(lambda jogo: {
            'Mandante': jogo.select('a')[0]['title'],
            'Placar mandante': jogo.select('span')[5].text,
            'Visitante': jogo.select('a')[3]['title'],
            'Placar visitante': jogo.select('span')[6].text,
            'Data': jogo.select('span')[0].text
        }, jogos))

    def converterDicionarioEmDataFrame(self, dicionario):
        return pd.DataFrame(dicionario)

    def transformacoesDataFrameJogos(self, dfJogos):
        dfJogos['Placar mandante'] = dfJogos['Placar mandante'].apply(lambda cell: int(cell) if pd.notna(cell) and cell.strip() != '' and cell.isdigit() else cell)
        dfJogos['Placar visitante'] = dfJogos['Placar visitante'].apply(lambda cell: int(cell) if pd.notna(cell) and cell.strip() != '' and cell.isdigit() else cell)
        dfJogos['Data'] = dfJogos['Data'].apply(lambda cell: cell.split('\n')[1] if pd.notna(cell) and cell.strip() != '' and len(cell.split('\n')) > 1 else cell)
        dfJogos['Data'] = pd.to_datetime(dfJogos['Data'], format='%d/%m %H:%M', errors='coerce')
        dfJogos['Data'] = dfJogos['Data'].apply(lambda dt: dt.replace(year=2024) if pd.notna(dt) else dt)
        dfJogos['Resultado'] = dfJogos.apply(lambda row: 'Jogo não realizado' if row['Placar mandante'] == '' else 'Visitante' if row['Placar mandante'] < row['Placar visitante'] else 'Mandante' if row['Placar mandante'] > row['Placar visitante'] else 'Empate', axis=1)
        dfJogos = dfJogos.sort_values(by='Data', ascending=False)
        return dfJogos

    def extrairClassificacaoHTML(self, html):
        classificacao = html.find_all('tr')
        classificacao.pop(0)
        return classificacao

    def criarDicionarioClassificacao(self, classificacao):
        return list(map(lambda time: {
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

    def transformacoesDataFrameClassificacao(self, dfClassificacao):
        dfClassificacao['Posição'] = dfClassificacao['Posição'].map(int)
        dfClassificacao['Gols pró'] = dfClassificacao['Gols pró'].map(int)
        dfClassificacao['Gols contra'] = dfClassificacao['Gols contra'].map(int)
        dfClassificacao['Saldo gols'] = dfClassificacao['Gols pró'].map(int) - dfClassificacao['Gols contra'].map(int)
        dfClassificacao['Jogos'] = dfClassificacao['Jogos'].map(int)
        dfClassificacao['Vitórias'] = dfClassificacao['Vitórias'].map(int)
        dfClassificacao['Empates'] = dfClassificacao['Empates'].map(int)
        dfClassificacao['Derrotas'] = dfClassificacao['Derrotas'].map(int)
        dfClassificacao['Aproveitamento'] = (((dfClassificacao['Vitórias'] * 3) + dfClassificacao['Empates']) / (dfClassificacao['Jogos'] * 3) * 100).round(2)
        dfClassificacao = dfClassificacao.sort_values(by='Gols pró', ascending=False).reset_index(drop=True)
        dfClassificacao['Ranking ataque'] = dfClassificacao.index + 1
        dfClassificacao = dfClassificacao.sort_values(by='Gols contra', ascending=True).reset_index(drop=True)
        dfClassificacao['Ranking defesa'] = dfClassificacao.index + 1
        dfClassificacao = dfClassificacao.sort_values(by='Posição').reset_index(drop=True)
        return dfClassificacao

    def ultimos_jogos(self, time):
        ultimos_jogos = self.dfJogos[(self.dfJogos['Resultado'] != 'Jogo não realizado') & ((self.dfJogos['Mandante'] == time) | (self.dfJogos['Visitante'] == time))]
        string_ultimos_jogos = ''
        quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
        i = 5

        for i in range(quantidade_ultimos_jogos, 0, -1):
            resultado = ultimos_jogos.iloc[i-1]['Resultado']
            mandante_visitante = 'Mandante' if ultimos_jogos.iloc[i-1]['Mandante'] == time else 'Visitante'        
            string_ultimos_jogos = string_ultimos_jogos + ('E' if resultado == 'Empate' else 'V' if resultado == mandante_visitante else 'D')

        return string_ultimos_jogos

    def ultimos_jogos_mandante(self, time):
        ultimos_jogos = self.dfJogos[(self.dfJogos['Resultado'] != 'Jogo não realizado') & ((self.dfJogos['Mandante'] == time))]
        string_ultimos_jogos = ''
        quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
        i = 5

        for i in range(quantidade_ultimos_jogos, 0, -1):
            resultado = ultimos_jogos.iloc[i-1]['Resultado']
            string_ultimos_jogos = string_ultimos_jogos + ('E' if resultado == 'Empate' else 'V' if resultado == 'Mandante' else 'D')

        return string_ultimos_jogos

    def ultimos_jogos_visitante(self, time):
        ultimos_jogos = self.dfJogos[(self.dfJogos['Resultado'] != 'Jogo não realizado') & ((self.dfJogos['Visitante'] == time))]
        string_ultimos_jogos = ''
        quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
        i = 5

        for i in range(quantidade_ultimos_jogos, 0, -1):
            resultado = ultimos_jogos.iloc[i-1]['Resultado']
            string_ultimos_jogos = string_ultimos_jogos + ('E' if resultado == 'Empate' else 'V' if resultado == 'Visitante' else 'D')

        return string_ultimos_jogos

    def ultimos_jogos_gols(self, time):
        ultimos_jogos = self.dfJogos[(self.dfJogos['Resultado'] != 'Jogo não realizado') & ((self.dfJogos['Mandante'] == time) | (self.dfJogos['Visitante'] == time))]
        quantidade_gols = 0
        quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
        i = 0

        for i in range(quantidade_ultimos_jogos):
            quantidade_gols = quantidade_gols + (ultimos_jogos.iloc[i]['Placar mandante'] if ultimos_jogos.iloc[i]['Mandante'] == time else ultimos_jogos.iloc[i]['Placar visitante'])

        return quantidade_gols

    def ultimos_jogos_gols_mandante(self, time):
        ultimos_jogos = self.dfJogos[(self.dfJogos['Resultado'] != 'Jogo não realizado') & ((self.dfJogos['Mandante'] == time))]
        quantidade_gols = 0
        quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
        i = 0

        for i in range(quantidade_ultimos_jogos):
            quantidade_gols = quantidade_gols + ultimos_jogos.iloc[i]['Placar mandante']

        return quantidade_gols

    def ultimos_jogos_gols_visitante(self, time):
        ultimos_jogos = self.dfJogos[(self.dfJogos['Resultado'] != 'Jogo não realizado') & ((self.dfJogos['Visitante'] == time))]
        quantidade_gols = 0
        quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
        i = 0

        for i in range(quantidade_ultimos_jogos):
            quantidade_gols = quantidade_gols + ultimos_jogos.iloc[i]['Placar visitante']

        return quantidade_gols

    def ultimos_jogos_golsc(self, time):
        ultimos_jogos = self.dfJogos[(self.dfJogos['Resultado'] != 'Jogo não realizado') & ((self.dfJogos['Mandante'] == time) | (self.dfJogos['Visitante'] == time))]
        quantidade_gols = 0
        quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
        i = 0

        for i in range(quantidade_ultimos_jogos):
            quantidade_gols = quantidade_gols + (ultimos_jogos.iloc[i]['Placar visitante'] if ultimos_jogos.iloc[i]['Mandante'] == time else ultimos_jogos.iloc[i]['Placar mandante'])

        return quantidade_gols

    def ultimos_jogos_golsc_mandante(self, time):
        ultimos_jogos = self.dfJogos[(self.dfJogos['Resultado'] != 'Jogo não realizado') & ((self.dfJogos['Mandante'] == time))]
        quantidade_gols = 0
        quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
        i = 0

        for i in range(quantidade_ultimos_jogos):
            quantidade_gols = quantidade_gols + ultimos_jogos.iloc[i]['Placar visitante']

        return quantidade_gols

    def ultimos_jogos_golsc_visitante(self, time):
        ultimos_jogos = self.dfJogos[(self.dfJogos['Resultado'] != 'Jogo não realizado') & ((self.dfJogos['Visitante'] == time))]
        quantidade_gols = 0
        quantidade_ultimos_jogos = 5 if len(ultimos_jogos) >= 5 else len(ultimos_jogos)
        i = 0

        for i in range(quantidade_ultimos_jogos):
            quantidade_gols = quantidade_gols + ultimos_jogos.iloc[i]['Placar mandante']

        return quantidade_gols

    def transformacoesInterDataFrames(self, dfClassificacao, dfJogos):
        dfClassificacao['Jogos mandante'] = dfClassificacao['Time'].apply(lambda time: len(dfJogos[(dfJogos['Mandante'] == time) & (dfJogos['Resultado'] != 'Jogo não realizado')]))
        dfClassificacao['Vitórias mandante'] = dfClassificacao['Time'].apply(lambda time: len(dfJogos[(dfJogos['Resultado'] == 'Mandante') & (dfJogos['Mandante'] == time)]))
        dfClassificacao['Empates mandante'] = dfClassificacao['Time'].apply(lambda time: len(dfJogos[(dfJogos['Resultado'] == 'Empate') & (dfJogos['Mandante'] == time)]))
        dfClassificacao['Derrotas mandante'] = dfClassificacao['Time'].apply(lambda time: len(dfJogos[(dfJogos['Resultado'] == 'Visitante') & (dfJogos['Mandante'] == time)]))
        dfClassificacao['Aproveitamento mandante'] = ((dfClassificacao['Vitórias mandante'] * 3 + dfClassificacao['Empates mandante']) / (dfClassificacao['Jogos mandante'] * 3) * 100).round(2)

        dfClassificacao['Jogos visitante'] = dfClassificacao['Time'].apply(lambda time: len(dfJogos[(dfJogos['Visitante'] == time) & (dfJogos['Resultado'] != 'Jogo não realizado')]))
        dfClassificacao['Vitórias visitante'] = dfClassificacao['Time'].apply(lambda time: len(dfJogos[(dfJogos['Resultado'] == 'Visitante') & (dfJogos['Visitante'] == time)]))
        dfClassificacao['Empates visitante'] = dfClassificacao['Time'].apply(lambda time: len(dfJogos[(dfJogos['Resultado'] == 'Empate') & (dfJogos['Visitante'] == time)]))
        dfClassificacao['Derrotas visitante'] = dfClassificacao['Time'].apply(lambda time: len(dfJogos[(dfJogos['Resultado'] == 'Mandante') & (dfJogos['Visitante'] == time)]))
        dfClassificacao['Aproveitamento visitante'] = ((dfClassificacao['Vitórias visitante'] * 3 + dfClassificacao['Empates visitante']) / (dfClassificacao['Jogos visitante'] * 3) * 100).round(2)

        dfClassificacao['Ultimos jogos'] = dfClassificacao['Time'].apply(self.ultimos_jogos)
        dfClassificacao['Ultimos jogos - Mandante'] = dfClassificacao['Time'].apply(self.ultimos_jogos_mandante)
        dfClassificacao['Ultimos jogos - Visitante'] = dfClassificacao['Time'].apply(self.ultimos_jogos_visitante)

        dfClassificacao['Gols ultimos jogos'] = dfClassificacao['Time'].apply(self.ultimos_jogos_gols)
        dfClassificacao['Gols ultimos jogos - Mandante'] = dfClassificacao['Time'].apply(self.ultimos_jogos_gols_mandante)
        dfClassificacao['Gols ultimos jogos - Visitante'] = dfClassificacao['Time'].apply(self.ultimos_jogos_gols_visitante)

        dfClassificacao['Gols contra ultimos jogos'] = dfClassificacao['Time'].apply(self.ultimos_jogos_golsc)
        dfClassificacao['Gols contra ultimos jogos - Mandante'] = dfClassificacao['Time'].apply(self.ultimos_jogos_golsc_mandante)
        dfClassificacao['Gols contra ultimos jogos - Visitante'] = dfClassificacao['Time'].apply(self.ultimos_jogos_golsc_visitante)
        return dfClassificacao

    def procurarTime(self, nomeTime):
        return self.dfClassificacao[self.dfClassificacao['Time'] == nomeTime].iloc[0]

    def apresentarRetrospectoGeral(self, time):
        return f"""{time['Time']}
Retrospecto geral:
{time['Posição']} º - {time['Pontuação']} pontos em {time['Jogos']} jogos ({time['Vitórias']}V/{time['Empates']}E/{time['Derrotas']}D)
{time['Aproveitamento']} % de aproveitamento
Gols pró: {time['Gols pró']} - Gols contra: {time['Gols contra']} - Saldo de gols: {time['Saldo gols']}
Ranking ataque: {time['Ranking ataque']} - Ranking defesa: {time['Ranking defesa']}

"""

    def apresentarRetrospectoGeralUltimos5Jogos(self,time):
        return f"""Restrospecto últimos 5 jogos
Últimos jogos: {time['Ultimos jogos']}
Gols pró: {time['Gols ultimos jogos']} - Gols contra: {time['Gols contra ultimos jogos']}

"""

    def apresentarRetrospectoGeralUltimos5JogosMandante(self, time):
        return f"""Retrospecto mandante:
{time['Jogos mandante']} jogos ({time['Vitórias mandante']}V/{time['Empates mandante']}E/{time['Derrotas mandante']}D) - {time['Aproveitamento mandante']}
Últimos jogos: {time['Ultimos jogos - Mandante']}
Gols pró: {time['Gols ultimos jogos - Mandante']} - Gols contra: {time['Gols contra ultimos jogos - Mandante']}

"""

    def apresentarRetrospectoGeralUltimos5JogosVisitante(self, time):
        return f"""Retrospecto visitante:
{time['Jogos visitante']} jogos ({time['Vitórias visitante']}V/{time['Empates visitante']}E/{time['Derrotas visitante']}D) - {time['Aproveitamento visitante']}
Últimos jogos: {time['Ultimos jogos - Visitante']}
Gols pró: {time['Gols ultimos jogos - Visitante']} - Gols contra: {time['Gols contra ultimos jogos - Visitante']}

"""

    def resumo_geral(self, time):
        return self.apresentarRetrospectoGeral(self.procurarTime(time)) + self.apresentarRetrospectoGeralUltimos5Jogos(self.procurarTime(time)) + self.apresentarRetrospectoGeralUltimos5JogosMandante(self.procurarTime(time)) + self.apresentarRetrospectoGeralUltimos5JogosVisitante(self.procurarTime(time))
    
    def nomesTimes(self):
        return self.dfClassificacao['Time'].to_list()
    
#br = Brasileirao()
#print(br.nomesTimes())
#print(br.dfClassificacao['Time'].values)
#print(br.resumo_geral('Bahia'))
#print(br.resumo_geral('Atlético-MG'))