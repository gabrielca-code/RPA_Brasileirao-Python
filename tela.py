import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from webscraping import Brasileirao
import pyautogui

tela = tk.Tk()

largura_tkinter = 700
altura_tkinter = 500
largura_monitor, altura_monitor = pyautogui.size()
cor_fundo_branco = "#DFDFDF"
cor_letra_preta = "#101010"

opcoes_times = ["Cruzeiro", "Flamengo"]

class Application():
    def __init__(self):
        self.tela = tela
        self.configuracoesTela()
        self.criarWidgets()
        tela.mainloop()
    
    def configuracoesTela(self):
        self.tela.title("Brasileirão Betano") 
        self.tela.configure(background = cor_fundo_branco)
        #self.tela.iconphoto(False, PhotoImage(file='C:/Users/gabri/Desktop/Developer/Python/Scrapping/Brasileirao/betanologo.png')) #mal otimizado
        self.tela.geometry(f"{largura_tkinter}x{altura_tkinter}+{self.centralizar(largura_monitor, largura_tkinter)}+{self.centralizar(altura_monitor, altura_tkinter)}")
        self.tela.resizable(False, False) 

    def criarWidgets(self):
        self.botao_pesquisar = tk.Button(self.tela, text="Pesquisar", command = self.estatisticasTimes)
        self.botao_pesquisar.place(x = self.centralizar(largura_tkinter, 100), y = altura_tkinter - 50, width = 100, height = 40)
        
        self.label_titulo = tk.Label(self.tela, text="Estatísticas brasileirão", bg = cor_fundo_branco, fg = cor_letra_preta, font=("Arial", 24))
        self.label_titulo.place(x = self.centralizar(largura_tkinter, largura_tkinter), y = 10, width = largura_tkinter, height = 50)

        self.combobox_time1 = ttk.Combobox(self.tela, values=opcoes_times)
        self.combobox_time1.place(x = 25, y = 100, width = 300, height = 30)

        self.combobox_time2 = ttk.Combobox(self.tela, values=opcoes_times)
        self.combobox_time2.place(x = 370, y = 100, width = 300, height = 30)

        self.label_time1 = tk.Label(self.tela, text='Time 1')
        self.label_time1.place(x = 25, y = 140, width = 300, height = 300)

        self.label_time2 = tk.Label(self.tela, text='Time 2')
        self.label_time2.place(x = 370, y = 140, width = 300, height = 300)

    def centralizar(self, pai, filho):
        return int(pai / 2 - filho / 2)
    
    def estatisticasTimes(self):
        self.label_time1.config(text = self.combobox_time1.get())
        self.label_time2.config(text = self.combobox_time2.get())

Application()
#brasileirao = Brasileirao()
#brasileirao.resumo_geral('Internacional')
#brasileirao.resumo_geral('Fortaleza')