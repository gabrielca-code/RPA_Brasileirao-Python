import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from webscraping import Brasileirao
import pyautogui

tela = tk.Tk()

# Definindo tamanho da janela do tkinter
largura_tkinter = 700
altura_tkinter = 500

# Pegando tamanho de altura e largura do monitor com pyautogui
largura_monitor, altura_monitor = pyautogui.size()

# Cores padrão
cor_fundo_branco = "#DFDFDF"
cor_letra_preta = "#101010"

# Instanciando classe do webscrapping
br = Brasileirao()

# Ordenando nome dos times e salvando em uma lista de opções
opcoes_times = sorted(br.nomesTimes())

# Classe principal para gerar a aplicação
class Application():

    # Construtor da classe
    def __init__(self):
        self.tela = tela
        self.configuracoesTela()
        self.criarWidgets()
        tela.mainloop()
    
    # Setando as configurações gerais da janela do tkinter
    def configuracoesTela(self):
        # Título
        self.tela.title("Brasileirão Betano") 
        # Alterando cor de fundo
        self.tela.configure(background = cor_fundo_branco)
        # Alterando tamanho da janela e aonde ela se dispõe inicialmente
        self.tela.geometry(f"{largura_tkinter}x{altura_tkinter}+{self.centralizar(largura_monitor, largura_tkinter)}+{self.centralizar(altura_monitor, altura_tkinter)}")
        # Definindo que a janela não pode ser redimensionada nem verticalmente nem horizontalmente
        self.tela.resizable(False, False) 

    # Criando elementos da tela
    def criarWidgets(self):
        # Botão de pesquisar que trás aciona a função estatisticasTimes
        self.botao_pesquisar = tk.Button(self.tela, text="Pesquisar", command = self.estatisticasTimes)
        self.botao_pesquisar.place(x = self.centralizar(largura_tkinter, 100), y = altura_tkinter - 50, width = 100, height = 40)
        
        # Label título
        self.label_titulo = tk.Label(self.tela, text="Estatísticas brasileirão", bg = cor_fundo_branco, fg = cor_letra_preta, font=("Arial", 24))
        self.label_titulo.place(x = self.centralizar(largura_tkinter, largura_tkinter), y = 10, width = largura_tkinter, height = 50)

        # Combobox para selecionar o time 1
        self.combobox_time1 = ttk.Combobox(self.tela, values=opcoes_times)
        self.combobox_time1.place(x = 25, y = 80, width = 300, height = 30)

        # Combobox para selecionar o time 2
        self.combobox_time2 = ttk.Combobox(self.tela, values=opcoes_times)
        self.combobox_time2.place(x = 370, y = 80, width = 300, height = 30)

        # Label estatisticas time 1
        self.label_time1 = tk.Label(self.tela, text='Time 1', anchor = "w")
        self.label_time1.place(x = 25, y = 120, width = 300, height = 320)

        # Label estatisticas time 2
        self.label_time2 = tk.Label(self.tela, text='Time 2', anchor = "w")
        self.label_time2.place(x = 370, y = 120, width = 300, height = 320)

    # Método padrão para centralizar elementos
    def centralizar(self, pai, filho):
        return int(pai / 2 - filho / 2)
    
    # Método para setar as labels de estatísticas com as estatísticas dos times escolhidos
    def estatisticasTimes(self):
        self.label_time1.config(text = br.resumo_geral(self.combobox_time1.get()), anchor = "w", width = 300, justify = 'left')
        self.label_time2.config(text = br.resumo_geral(self.combobox_time2.get()), anchor = "w", width = 300, justify = 'left')

Application()
#brasileirao = Brasileirao()
#brasileirao.resumo_geral('Internacional')
#brasileirao.resumo_geral('Fortaleza')