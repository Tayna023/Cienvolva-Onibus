import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

from functools import partial
from shiny.ui import page_navbar
from shiny.express import render, ui, input
from shiny import reactive

#Variaveis de design
pontos = '#0023FF'
palavras = '#FFC400'
media_cor = '#FFC400'
grafico1 = '#0023FF'
grafico2 = '#FFC400'

ui.page_opts(
    title= "Cienvolva",  
    page_fn=partial(page_navbar, id="page"),  
    fillable=True
)

def tratamento (novo): #Tratamento dos dados de horarios
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

  for i in range(len(valores)): #Elimina valores como 24:15
      valores[i] %= 24

  if valores == []:
    valores = [0]
  return valores

def hist_vertical(valores, duracao, escalaAutomatica):
  #Seleciona o tamanho de intevalos como um int
  '''duracao = duracao.split()
  duracao = int(duracao[0])
  if duracao == 1:
    duracao = 60'''

  escala = 60/duracao
  passo = 1/escala

  if escalaAutomatica:
    distribuicao = [0]*24*int(escala) #Numero de bins caso a escala seja automatica

    for valor in valores:
      valor %= 24
      valor *= escala
      distribuicao[int((valor//1))] += 1 #Seleciona o bin especifico onde cabe aquele valor e adiciona +1
      valor /= escala


  else:
    distribuicao = [0]*24 #Se não seria o mesmo que escala = 1

    for valor in valores:
      valor %= 24
      distribuicao[int((valor//1))] += 1

  eixo_y = max(distribuicao) + 1 #Distribuição faz o trabalho manual do histograma para descobrir o valor máximo em y

  #Formata os major positions - inteiros e de 0 a 23 e os minor positions -- dependem da escala (0,5 0,25 ou 0,75)
  #Essas serão as posições que os horarios entarão na tela
  major_positions=list(range(0,24))
  minor_positions=[]
  cont =1
  #Major_positions são as horas, passa por todas as horas e adiciona em minor_positions todas as divisões necessárias
  for major_position in major_positions:
      while cont < escala:
        minor_positions.append(major_position+cont*passo)
        cont+=1
      cont=1

  #Formata os ticks que aparecem na tela como horas
  major_hora = []
  minor_hora = []
  cont = 1
  i=0
  while len(major_hora)<24:
    major_hora.append(str(i)+':'+"00")
    while cont<escala:
      if cont*duracao == 30:
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
  for i in range(0,24):
    bins.append(i)
    while cont < escala:
        bins.append(bins[len(bins)-1]+(passo))
        cont+=1
    cont=1

  ax.hist(valores, bins,width=passo, linewidth=0.5, edgecolor="white", color = grafico1)#valores = valores a serem sorteados, bins = quais as divisões

  #formata os ticks
  ax.tick_params(which='major', labelsize= 10, width=1.0, length=9)
  ax.tick_params(which='minor', labelsize = 8,  width=0.75, length=2.5)

  #Fixa a posição dos ticks nos eixos
  ax.xaxis.set_major_locator(ticker.FixedLocator(major_positions))
  ax.xaxis.set_major_formatter(ticker.FixedFormatter(major_hora))

  #Fixa o valor dos ticks no eixo
  ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_positions))
  ax.xaxis.set_minor_formatter(ticker.FixedFormatter(minor_hora))

  ax.set(xlim=(-0.5, 24.5*passo), xticks=np.arange(0, 24.5),
        ylim=(0, eixo_y), yticks=np.arange(0, eixo_y))

  plt.show()

with ui.nav_panel("Gráfico Único"):  
    #Sidebar com menu de um gráfico único, criação no gráfico no main tab
    with ui.layout_columns(col_widths=(3,9)):
        with ui.card():  
            #"Aqui ficará o menu do gráfico Único"
            #Caixa de texto p/ horarios
            ui.input_text_area("text", "Insira os horários", placeholder= "00:00 01:00 01:15...") 
            #Slider p/ duração
            ui.input_slider("slider", "Selecione o Intervalo", min = 15, max = 60, value = 60, step = 15, post = " minutos")
            #Check p/ ajustar proporção
            ui.input_checkbox("check", "Ajustar proporção", value = False)
            #Botão de atualizar gráfico
            #ui.input_action_button("button", "Enviar Horários")
        with ui.card():
            #"Aqui ficará o gráfico Único"
            @render.plot()
            #@reactive.event(input.button)
            def graf():
                if input.text() == "":
                   return
                else:
                    return hist_vertical(valores=tratamento(novo = input.text()), duracao = input.slider(), escalaAutomatica = input.check())
with ui.nav_panel("Gráfico Comparativo"):  
    #Sidebar com menu de um gráfico comparativo, criação no gráfico no main tab
    with ui.layout_columns(col_widths=(3,9)):
        with ui.card():  
            "Aqui ficará o menu do gráfico comparativo"  
        with ui.card():
            "Aqui ficará o gráfico comparativo"

with ui.nav_panel("Gráfico de tempo de espera"):  
    #Sidebar com menu de um gráfico de tempo de espera, criação no gráfico no main tab
    with ui.layout_columns(col_widths=(3,9)):
        with ui.card(): 
            "Aqui ficará o menu do gráfico de tempo de espera"  
        with ui.card():
            "Aqui ficará o gráfico de tempo de espera"