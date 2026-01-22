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
                
#Histograma comparativo
#Aqui está todo o processamento para formatar e criar um gráfico com dois histogramas lado a lado
def hist_horizontal_comparativo(valores, duracao1, duracao2, mesmaEscala):

  #Definições histograma esquerda

  duracao1 = duracao1.split()
  duracao1 = int(duracao1[0])
  if duracao1 == 1:
    duracao1 = 60

  escala1 = 60/duracao1
  passo = 1/escala1

  #Cria as bins como uma lista com todas as divisões
  bins =[]
  cont = 1
  for i in range(0,25):
    bins.append(i)
    while cont < escala1:
        bins.append(bins[len(bins)-1]+(passo))
        cont+=1
    cont=1

  #Fim definições histograma esquerda

  #Definições histograma direita
  duracao2 = duracao2.split()
  duracao2 = int(duracao2[0])
  if duracao2 == 1:
    duracao2 = 60

  escala2 = 60/duracao2
  passo = 1/escala2

  bins2 =[]
  cont = 1
  for i in range(0,25):
    bins2.append(i)
    while cont < escala2:
        bins2.append(bins2[len(bins2)-1]+(passo))
        cont+=1
    cont=1

  #fim definições histograma direita

  escala = min(escala1,escala2)

  #Escala automática
  if mesmaEscala:
    #encaixa os valores de horarios em suas posições dependendo do proprio horario
    distribuicao = [0]*24*int(escala)

    for valor in valores:
      valor %= 24
      valor *= escala
      distribuicao[int((valor//1))] += 1
      valor /= escala
    distribuicao2 = distribuicao.copy()
    distribuicao1 = distribuicao.copy()
  else:
    distribuicao1 = [0]*24*int(escala1)
    distribuicao2 = [0]*24*int(escala2)
    for valor in valores:
      valor %= 24
      valor *= escala1
      distribuicao1[int((valor//1))] += 1
      valor /= escala1
      valor *= escala2
      distribuicao2[int((valor//1))] += 1
      valor /= escala2

  eixo_x1 = max(distribuicao1) + 1
  eixo_x2 = max(distribuicao2) + 1


  #Igual para ambos
  escala = max(escala1,escala2)
  duracao = 60/escala
  passo = 1/escala
  #Formata os major positions - inteiros e de 0 a 23 e os minor positions -- dependem da escala (0,5 0,25 ou 0,75)
  major_positions=list(range(0,25))
  minor_positions=[]
  cont = 1
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
  while len(major_hora)<=24:
    major_hora.append(str(i)+':'+"00")

    if len(major_hora)<=24:
      while cont<escala:
        if cont*duracao == 30:
          minor_hora.append(str(i)+":30")
        else:
          minor_hora.append('')
        cont+=1
    cont=1
    i+=1
  # plot:
  #fig = plt.figure(figsize=(8,10), facecolor='lightblue')
  #ax[0] = fig.add_axes([2,4,2,8])
  #ax[1] = fig.add_axes([4,6,2,8])
  fig, ax = plt.subplots(1,2,figsize=(8,10), sharey=True)

  #Histograma esquerdo
  #Cria o histograma na horizontal esquerdo
  ax[0].hist(valores, bins, height=1/escala1,weights=-np.ones_like(valores), linewidth=0.5, edgecolor="white", orientation = "horizontal", color = grafico2)#valores = valores a serem sorteados, bins = quais as divisões
  #Habilita o grid
  ax[0].grid(visible = True, which = 'major', axis = 'y')

  #formata os ticks
  ax[0].tick_params(which='major', labelsize= 10, width=1.0, length=7)
  ax[0].tick_params(which='minor', labelsize = 8,  width=0.75, length=2.5)

  #Fixa a posição dos ticks
  ax[0].yaxis.set_major_locator(ticker.FixedLocator(major_positions))
  ax[0].yaxis.set_major_formatter(ticker.FixedFormatter(major_hora))

  #Define o texto dos ticks
  ax[0].yaxis.set_minor_locator(ticker.FixedLocator(minor_positions))
  ax[0].yaxis.set_minor_formatter(ticker.FixedFormatter(minor_hora))

  #Arruma o eixo x - pois está negativo
  ax[0].xaxis.set_major_locator(ticker.FixedLocator(range(-eixo_x1, 0)))

  #Arruma para que todo eixo seja positivo
  valor  = []
  for i in range(-eixo_x1, 0):
    valor.append(abs(i))

  ax[0].xaxis.set_major_formatter(ticker.FixedFormatter(valor))

  ax[0].set_xlim(-eixo_x1, 0)
  ax[0].set_ylim(-0.5, 24.5)

  #Cria o histograma na horizontal direito
  ax[1].hist(valores, bins2, height=1/escala2, linewidth=0.5, edgecolor="white", orientation = "horizontal", color = grafico1)
  #Habilita o grid
  ax[1].grid(visible = True, which = 'major', axis = 'y')

  #formata os ticks
  ax[1].tick_params(which='major', labelsize= 10, width=1.0, length=7)
  ax[1].tick_params(which='minor', labelsize = 8,  width=0.75, length=2.5)

  #Fixa a posição dos ticks
  ax[1].yaxis.set_major_locator(ticker.FixedLocator(major_positions))
  ax[1].yaxis.set_major_formatter(ticker.FixedFormatter(major_hora))

  #Define o texto dos ticks
  ax[1].yaxis.set_minor_locator(ticker.FixedLocator(minor_positions))
  ax[1].yaxis.set_minor_formatter(ticker.FixedFormatter(minor_hora))

  #Define a posição e valor do eixo x
  ax[1].xaxis.set_major_locator(ticker.FixedLocator(range(0, eixo_x2+1)))
  ax[1].xaxis.set_major_formatter(ticker.FixedFormatter(range(0, eixo_x2+1)))

  ax[1].set_xlim(0,eixo_x2)
  ax[1].set_ylim(-0.5, 24.5)

  # Adjust spacing
  plt.subplots_adjust(left=0.1, right=0.9,
                      top=0.9, bottom=0.1,
                      wspace=0.0) #A distância pra ficar só ticks entre eles é 0.035

  plt.show()                

with ui.nav_panel("Gráfico Comparativo"):  
    #Sidebar com menu de um gráfico comparativo, criação no gráfico no main tab
    with ui.layout_columns(col_widths=(3,9)):
        with ui.card():  
            #"Aqui ficará o menu do gráfico comparativo" 
            #Caixa de texto p/ horarios
            ui.input_text_area("text", "Insira os horários", placeholder= "00:00 01:00 01:15...") 
            #Slider p/ duração
            ui.input_slider("slider1", "Intervalo do gráfico da direita: ", min = 15, max = 60, value = 60, step = 15, post = " minutos")
            #Slider p/duração 2
            ui.input_slider("slider2", "Intervalo do gráfico da esquerda: ", min = 15, max = 60, value = 60, step = 15, post = " minutos")
            #Check p/ ajustar proporção
            ui.input_checkbox("check", "Ajustar proporção", value = False)
        with ui.card():
            #"Aqui ficará o gráfico comparativo"
            @render.plot()
            #@reactive.event(input.button)
            def graf():
                if input.text() == "":
                   return
                else:
                    return hist_horizontal_comparativo(valores=tratamento(novo = input.text()), duracao1 = input.slider1(), duracao2 = input.slider2(), mesmaEscala = input.check())



with ui.nav_panel("Gráfico de tempo de espera"):  
    #Sidebar com menu de um gráfico de tempo de espera, criação no gráfico no main tab
    with ui.layout_columns(col_widths=(3,9)):
        with ui.card(): 
            "Aqui ficará o menu do gráfico de tempo de espera"  
        with ui.card():
            "Aqui ficará o gráfico de tempo de espera"