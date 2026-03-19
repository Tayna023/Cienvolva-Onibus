import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

import cores
import quiz
#Código dos onibus, gera os gráficos e trata os dados

def tratamento (novo): #Tratamento dos dados de horarios
  
    #Novo é uma str, vem diretamente da entrada de dados, tratada para uma lista (horarios)
    if novo[1] == ":": #Para o caso de o primeiro horario ser no formato 2:10
        novo = "0" + novo

    horarios = []
    for i in range(0, len(novo)): #Para qualquer separador, usa apenas os : para se basear
        if novo[i] == ':':
            horarios.append(novo[i-2:i+3])

    for i in range(0,len(horarios)): #Para corrigir horarios como 4:15 para 04:15
        if horarios[i][0] == ' ':
            horarios[i] = '0'+horarios[i].strip()

    #Transforma os horarios no formato de decimais
    valores  = []

    for horario in horarios:
        hora, min = horario.split(":")
        min = int(min)/60
        valores.append (int(hora) + min)

    for valor in valores: #Elimina valores como 24:15
        valor %= 24

    if valores == []:
        valores = [0]
    return valores

class hist_vertical:
  #Seleciona o tamanho de intevalos como um int
  def __init__ (self, valores, duracao, foco, escalaAutomatica):
    self.valores = valores
    self.duracao = duracao
    self.foco = foco
    self.escalaAutomatica = escalaAutomatica
    self.escala = int(60/duracao)
    self.passo = 1/self.escala
    self.eixo_y = 0

  def get_escala(self):
     return self.escala
  
  def distribuicao(self):
    if self.escalaAutomatica:
      distribuicao = [0]*24*self.escala #Numero de bins caso a escala seja automatica
      for valor in self.valores:
        valor %= 24
        distribuicao[int(valor*self.escala)] += 1 #Seleciona o bin especifico onde cabe aquele valor e adiciona +1
    else:
      distribuicao = [0]*24 #Se não seria o mesmo que escala = 1
      for valor in self.valores:
        valor %= 24
        distribuicao[int(valor)] += 1
    self.eixo_y = max(distribuicao) + 1 #Distribuição faz o trabalho manual do histograma para descobrir o valor máximo em y
    return distribuicao
  
  def grafico(self):
    #Formata os major positions - inteiros e de 0 a 23 e os minor positions -- dependem da escala (0,5 0,25 ou 0,75)
    #Essas serão as posições que os horarios entarão na tela
    major_positions=list(range(0,24))
    minor_positions=[]
    cont =1
    #Major_positions são as horas, passa por todas as horas e adiciona em minor_positions todas as divisões necessárias
    for major_position in major_positions:
        while cont < self.escala:
          minor_positions.append(major_position+cont*self.passo)
          cont+=1
        cont=1

    #Formata os ticks que aparecem na tela como horas
    major_hora = []
    minor_hora = []
    cont = 1
    i=0
    while len(major_hora)<24:
      major_hora.append(str(i)+':'+"00")
      while cont<self.escala:
        if cont*self.duracao == 30:
          minor_hora.append(str(i)+":30")
        else:
          minor_hora.append('')
        cont+=1
      cont=1
      i+=1

    ##A partir daqui: Criação e formatação do gráfico
    # plot:
    fig, ax = plt.subplots(figsize=(14,5))

    bins = []
    cont = 0
    #Cria as bins como uma lista com todas as divisões
    for i in range(0,25):
      bins.append(i)
      while cont < self.escala:
          bins.append(bins[len(bins)-1]+(self.passo))
          cont+=1
      cont=1

    ax.hist(self.valores, bins,width=self.passo, linewidth=0.5, edgecolor="white", color = cores.grafico_cor1)#valores = valores a serem sorteados, bins = quais as divisões

    #formata os ticks
    ax.tick_params(which='major', labelsize= 8, width=1.0, length=9)
    ax.tick_params(which='minor', labelsize = 5,  width=0.75, length=2.5)

    #Fixa a posição dos ticks nos eixos
    ax.xaxis.set_major_locator(ticker.FixedLocator(major_positions))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(major_hora))

    #Fixa o valor dos ticks no eixo
    ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_positions))
    ax.xaxis.set_minor_formatter(ticker.FixedFormatter(minor_hora))

    self.distribuicao()
    ax.set(xlim=(-0.5, 24.5*self.passo), xticks=np.arange(0, 24.5),
          ylim=(0, self.eixo_y), yticks=np.arange(0, self.eixo_y))
    
    self.altura = 0
    for valor in self.valores:
      if valor >= self.foco and valor < self.foco+self.duracao/60:
        self.altura += 1
    
    plt.plot([-0.5,self.foco], [self.altura]*2, color = "orange", linestyle = ":")
    ax.bar(self.foco, self.altura, color = "orange", align = "edge", width = self.duracao/60)

    return fig

  def get_altura(self):
    return self.altura