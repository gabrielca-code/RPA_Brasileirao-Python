# Projeto Brasileirão

Este projeto tem como objetivo principal reforçar conhecimentos de programação na linguagem Python e em algumas de suas bibliotecas mais comumente usadas. Essas bibliotecas serão utilizadas para agilizar os processos de extração, transformação e apresentação dos dados.
Com isso, surgiu a ideia de realizar uma automação para análise de dados da atual temporada do campeonato brasileiro de futebol série A, aonde conseguiria de maneira "simples" exercitar a base dos conceitos de scraping, tratamento e transformações de dados e interface interativa com o usuário.

## Coleta de Dados

Os dados serão coletados via web scraping, utilizando o site da Gazeta Esportiva como fonte. Por meio da biblioteca `Requests`, o conteúdo da página que contém a tabela de classificação e jogos do Brasileirão será capturado. Em seguida, a biblioteca `BeautifulSoup` será utilizada para obter conteúdos específicos do HTML da requisição, possibilitando a extração dos dados da classificação dos times e de todos os jogos do campeonato.

## Processamento de Dados

Após a coleta, a biblioteca `Pandas` será usada para converter os dados em um DataFrame e, posteriormente, extrair mais informações disponíveis no site sobre cada time. Exemplos de informações adicionais incluem:

- Desempenho do time em casa e fora de casa
- Desempenho nos últimos 5 jogos
- Melhores ataques e defesas
- E outras estatísticas relevantes

## Interação com o Usuário

A interação com o usuário e a apresentação das informações serão realizadas com a biblioteca `Tkinter`.

## Objetivos do Projeto

- Reforçar conhecimentos de programação em Python
- Aprimorar habilidades em web scraping com `Requests` e `BeautifulSoup`
- Praticar manipulação e análise de dados com `Pandas`
- Desenvolver uma interface gráfica simples usando `Tkinter`
