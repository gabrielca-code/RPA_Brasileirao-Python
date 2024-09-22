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

br = Brasileirao()
opcoes_times = sorted(br.nomesTimes())

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
        self.combobox_time1.place(x = 25, y = 80, width = 300, height = 30)

        self.combobox_time2 = ttk.Combobox(self.tela, values=opcoes_times)
        self.combobox_time2.place(x = 370, y = 80, width = 300, height = 30)

        self.label_time1 = tk.Label(self.tela, text='Time 1', anchor = "w")
        self.label_time1.place(x = 25, y = 120, width = 300, height = 320)

        self.label_time2 = tk.Label(self.tela, text='Time 2', anchor = "w")
        self.label_time2.place(x = 370, y = 120, width = 300, height = 320)

    def centralizar(self, pai, filho):
        return int(pai / 2 - filho / 2)
    
    def estatisticasTimes(self):
        self.label_time1.config(text = br.resumo_geral(self.combobox_time1.get()), anchor = "w", width = 300, justify = 'left')
        self.label_time2.config(text = br.resumo_geral(self.combobox_time2.get()), anchor = "w", width = 300, justify = 'left')

Application()
#brasileirao = Brasileirao()
#brasileirao.resumo_geral('Internacional')
#brasileirao.resumo_geral('Fortaleza')