# @title Código
# @markdown Pressione o botão ´Play´ ao lado para executar o aplicativo
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


#Variaveis de design
pontos = '#0023FF'
palavras = '#FFC400'
media_cor = '#FFC400'
grafico1 = '#0023FF'
grafico2 = '#FFC400'

#Tratamento do input de horarios
## -- Recebe e formata os valores -- recebe horarios e retorna os valores em decimais
#Salva input de horarios em uma lista
def tratamento (novo):
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
#Histograma vertical
#Aqui contém todo processamento necessário para criar e formatar um histograma único

def hist_vertical(valores, duracao, escalaAutomatica):
  #Seleciona o tamanho de intevalos como um int
  duracao = duracao.split()
  duracao = int(duracao[0])
  if duracao == 1:
    duracao = 60

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

  #Cria e formata o menu de um gráfico único
def graficoUnico ():
    #Menu com:
    #Check p/ ajustar proporção
    #Slider p/ duração
    #Caixa de texto p/ horarios
    #Botao de atualizar
    #Botao de voltar

    #Check de ajustar proporção
    check = widgets.Checkbox(value=False,
                          description='Ajustar Proporção',
                          disabled=False,
                          indent=False
                          )
    #caixa de texto para horários
    text = widgets.Text(
                        value='',
                        placeholder='00:00 01:00 ...',
                        description='',
                        disabled=False
                        )

    #Duracao - slider para selecionar o intervalo
    slider = widgets.SelectionSlider(options=['15 minutos','20 minutos', '30 minutos', '1 hora'],
                                     value= '1 hora',
                                     description='',
                                     disabled=False,
                                     continuous_update=False,
                                     orientation='horizontal',
                                     readout=True
                                     )
    #Botao de atualizar
    button = widgets.Button(description="Enviar horários")
    #botao de voltar
    voltar = widgets.Button(description="Voltar")
    #Caixa para permitir a organização
    caixa1 = widgets.Box(
        [
            widgets.Label(value='Insira os horarios de ônibus:'),
            text,
            button
        ]
    )
    #caixa para permitir a organização
    caixa2 = widgets.Box(
        [
            widgets.Label(value='Selecione o intervalo:'),
            slider,
        ]
    )
    out = widgets.Output(wait = True) #Cria um ambiente de exposição
    display (out)
    with out:
      display(caixa1, caixa2, check, voltar)

    outGraf = widgets.Output()
    display(outGraf)

    def on_button_clicked(button): #Quando o botão de enviar for apertado, limpa a área do gráfico e chama um novo grafico com os valores mais atualizados
      outGraf.clear_output(wait = True)
      with outGraf:
        hist_vertical(valores=tratamento(novo = text.value), duracao = slider.value, escalaAutomatica = check.value)

    def on_voltar_clicked(voltar): #Quando o botão de voltar for apertado, limpa toda a área e volta ao menu principal
      out.clear_output()
      outGraf.clear_output()
      principal()

    def valueChange(change): #Quando qualquer valor for alterado, limpa a area do gráfico e cria um novo gráfico com os valores atualizados
      outGraf.clear_output(wait = True)
      with outGraf:
        hist_vertical(valores=tratamento(novo = text.value), duracao = slider.value, escalaAutomatica = check.value)

    check.observe(valueChange, names= "value")
    slider.observe(valueChange, names= "value")
    voltar.on_click(on_voltar_clicked)
    button.on_click(on_button_clicked)

#Define e formata as opções de um gráfico comparativo -- dois histogramas
def graficoComp ():
    #Menu com:
    #Escala fixa ou automática
    #2 Slider p/ duração
    #Caixa de texto p/ horarios
    #Botao de atualizar
    #Botao de voltar?

    #escala
    check = widgets.Checkbox(value=False,
                          description='Mesma Proporção',
                          disabled=False,
                          indent=False
                          )
    #caixa de texto
    text = widgets.Text(value='',
                        placeholder='00:00 01:00 ...',
                        description='',
                        disabled=False
                        )
    #Duração 1
    slider1 = widgets.SelectionSlider(options=['15 minutos','20 minutos', '30 minutos', '1 hora'],
                                     value= '1 hora',
                                     description='',
                                     disabled=False,
                                     continuous_update=False,
                                     orientation='horizontal',
                                     readout=True
                                     )
    #Duração 2
    slider2 = widgets.SelectionSlider(options=['15 minutos','20 minutos', '30 minutos', '1 hora'],
                                     value= '1 hora',
                                     description='',
                                     disabled=False,
                                     continuous_update=False,
                                     orientation='horizontal',
                                     readout=True)
    #Botao de atualizar
    button = widgets.Button(description="Enviar horários")
    #botao de voltar
    voltar = widgets.Button(description="Voltar")
    caixa1 = widgets.Box(
        [
            widgets.Label(value='Insira os horarios de ônibus:'),
            text,
            button
        ]
    )
    caixa2 = widgets.Box(
        [
            widgets.Label(value='Intervalo do gráfico da esquerda:'),
            slider1,
            widgets.Label(value='   Intervalo do gráfico da direita:'),
            slider2,
        ]
    )
    out = widgets.Output()
    display (out)
    with out:
      display(caixa1, caixa2, check, voltar)

    outGraf = widgets.Output()
    display(outGraf)
    def on_button_clicked(button):#Quando o botão de enviar for apertado, limpa a área do gráfico e chama um novo grafico com os valores mais atualizados
      outGraf.clear_output(wait = True)
      with outGraf:
        hist_horizontal_comparativo(valores = tratamento(novo = text.value), duracao1 = slider1.value, duracao2 = slider2.value, mesmaEscala=check.value)

    def on_voltar_clicked(voltar): #Quando o botão de voltar for apertado, limpa toda a área e volta ao menu principal
      out.clear_output()
      outGraf.clear_output()
      principal()

    def valueChange(change): #Quando qualquer valor for alterado, limpa a area do gráfico e cria um novo gráfico com os valores atualizados
      outGraf.clear_output(wait = True)
      with outGraf:
        hist_horizontal_comparativo(valores = tratamento(novo = text.value), duracao1 = slider1.value, duracao2 = slider2.value, mesmaEscala=check.value)

    check.observe(valueChange, names= "value")
    slider1.observe(valueChange, names= "value")
    slider2.observe(valueChange, names= "value")
    voltar.on_click(on_voltar_clicked)
    button.on_click(on_button_clicked)


def delta_tempo(valores, intervalo):

  #organização dos horários por ordem crescente
  valores.sort()
  if len(valores) == 0:
    valores = [0]
  valores = [0]+valores+[24+valores[0]]#Adiciona 0 e 24 mais primeiro valor, pra funcinar nas bordas
  #Criação do gráfico e do seu tamanho
  fig, ax = plt.subplots(figsize=(18, 5))

  axes1 = fig.add_subplot(111)
  for i in range(0,len(valores)-1):
    #Plot de cada subconjunto do gráfico com o horario e o horario seguinte sendo o eixo x e o eixo y sendo o valor da diferença até 0
    axes1.plot ([valores[i], valores[i+1]],[(valores[i+1]-valores[i]), 0], color = grafico1)

  duracao = 1
  escala = 1
  axes2 = plt.axes([.475, .45, .4, .4])

  #axes1 é o gráfico maior
  #axes2 é o gráfico menor

  plt.setp(ax, xticks=[], yticks=[])
  valores_intervalo = [intervalo[0]] #Lista com todos os valores de dentro do intervalo
  for valor in valores:
    if valor > intervalo[0] and valor < intervalo[1]:
      valores_intervalo.append(valor)
    elif valor >= intervalo[1]:
      valores_intervalo.append(valor)
      break

  for i in range(0,len(valores)-1):
    #Plot de cada subconjunto do gráfico com o horario e o horario seguinte sendo o eixo x e o eixo y sendo o valor da diferença até 0
    axes2.plot ([valores[i], valores[i+1]],[(valores[i+1]-valores[i]), 0], color = grafico1)
    #Plot de pontos na absissa de cada horario em que sai um onibus
    axes2.plot (valores[i],0, marker = 'o', color = pontos)

  media = sum([(valores_intervalo[i+1]-valores_intervalo[i])**2/2 for i in range(len(valores_intervalo)-1)]) #soma dos valores de dentro do intervalo
  media -= (valores_intervalo[-1] - intervalo[1])**2/2 #Tirar o triangulo do final
  media /= (intervalo[1]-intervalo[0]) #Dividido pela área


  #Plot da linha de média
  axes2.plot((intervalo[0], intervalo[-1]), [media]*2, color = media_cor)

  #Formata os ticks que aparecem na tela como horas
  #Posição das horas
  major_positions=list(range(0,25))
  cont =1
  major_positions2 = list(range(0,25))
  minor_positions2 = []
  #Major_positions são as horas, passa por todas as horas e adiciona em minor_positions todas as divisões necessárias
  for major_position in major_positions2:
      while cont < 1:
        minor_positions2.append(major_position+cont*0.5)
        cont+=1
      cont=1

  #Valores que aparecem na tela
  major_hora = []
  minor_hora = []
  i=0

  while len(major_hora)<25:
    major_hora.append(str(i)+':'+"00")
    i+=1

  #seta os ticks do gráfico maior no formato
  axes1.tick_params(which='major', labelsize= 10, width=1.0, length=9)
  axes1.tick_params(which='minor', labelsize = 8,  width=0.75, length=2.5)

  #Fixa a posição dos ticks nos eixos do gráfico maior
  axes1.xaxis.set_major_locator(ticker.FixedLocator(major_positions))
  axes1.xaxis.set_major_formatter(ticker.FixedFormatter(major_hora))

  #formata os ticks do gráfico menor
  axes2.tick_params(which='major', labelsize= 10, width=1.0, length=9)
  axes2.tick_params(which='minor', labelsize = 8,  width=0.75, length=2.5)

  max_y = []
  for i  in range(len(valores)-1):
    if valores[i] >= intervalo[0] and valores[i] <= intervalo[-1]:
      if len(max_y) == 0:
        max_y.append(valores[i] - intervalo[0])
      else:
        max_y.append(valores[i+1]-valores[i])

  i=0
  while valores[i]<intervalo[-1]:
    i += 1

  if max_y == []:
    max_y = [0,max(valores[i]-intervalo[0],media)]
  axes2.set_ylim(0, max(max_y)+max(max_y)/10)
  axes2.set_xlim(intervalo[0], intervalo[-1])

  axes2.text((intervalo[-1] - ((intervalo[-1]-intervalo[0])/2)),(media + (max(max_y)/40)), "Tempo médio de espera no intervalo selecionado", color = palavras)

  def float_para_hora(y, pos):
    return f'{int(y):02d}:{int((y-int(y))*60):02d}'

  axes2.yaxis.set_major_formatter(float_para_hora)
  axes1.yaxis.set_major_formatter(float_para_hora)

  axes2.xaxis.set_major_formatter(float_para_hora)

  max_y = []
  for i in range(0,len(valores)-1):
    max_y.append(valores[i+1]-valores[i])
  if max_y == []:
    max_y = [0,24]
  axes1.set_ylim(0,max(max_y)+max(max_y)/10)
  axes1.set_xlim(0, 24.5)

  #Indicadores são as linhas que ligam o gráfico menor e a maior
  indicadores =  axes1.indicate_inset_zoom(inset_ax = axes2, edgecolor='black')

  indicadores.connectors[0].set_visible(True)
  indicadores.connectors[1].set_visible(False)
  indicadores.connectors[2].set_visible(True)
  indicadores.connectors[3].set_visible(False)

  plt.show()

#Cria e formata o menu de um gráfico único
def graficoDelta ():
    #Menu com:
    #Slider p/ duração
    #Caixa de texto p/ horarios
    #Botao de atualizar
    #Botao de voltar

    #caixa de texto
    text = widgets.Text(
                        value='',
                        placeholder='00:00 01:00 ...',
                        description='',
                        disabled=False
                        )

    #Duracao
    slider = widgets.FloatRangeSlider(
                                      value=[0,24],
                                      min=0,
                                      max=24.0,
                                      step=0.25,
                                      description='',
                                      disabled=False,
                                      continuous_update=False,
                                      orientation='horizontal',
                                      readout=False,
                                     )

    #Botao de atualizar
    button = widgets.Button(description="Enviar horários")
    #botao de voltar
    voltar = widgets.Button(description="Voltar")
    def float_para_hora(y):
      return f'{int(y):02d}:{int((y-int(y))*60):02d}'
    def caixa2():
      hora_inicio = widgets.Label(value= float_para_hora(slider.value[0]))
      hora_fim = widgets.Label(value= float_para_hora(slider.value[1]))
      caixa2 = widgets.Box(  #Caixa 2 com o slider
        [
            widgets.Label(value='Selecione o intervalo:'),
            slider,
            hora_inicio,
            hora_fim
        ]
      )
      return caixa2
    #Caixas organizam os widgets na tela
    caixa1 = widgets.Box( #Caixa 1 com a caixa de texto e o botao
        [
            widgets.Label(value='Insira os horarios de ônibus:'),
            text,
            button
        ]
    )
    caixa3 = widgets.Box(  #Caixa 3 com o botao de voltar
        [
            voltar
        ]
    )
    out = widgets.Output(wait = True)
    display (out)
    with out:
      display(caixa1)

    outGraf = widgets.Output()
    display(outGraf)
    with outGraf:
      display(caixa2(),caixa3)

    def on_button_clicked(button): #Quando o botão de enviar for apertado, limpa a área do gráfico e chama um novo grafico com os valores mais atualizados
      outGraf.clear_output(wait = True)
      if text.value == '':
        outGraf.clear_output(wait = True)
        with outGraf:
          display(caixa2(),caixa3)
          display('Este é o gráfico de espera sem nenhum horário de ônibus')
      else:
        outGraf.clear_output(wait = True)
        with outGraf:
          display(caixa2(),caixa3)
      with outGraf:
        delta_tempo(valores=tratamento(novo = text.value), intervalo = slider.value)

    def on_voltar_clicked(voltar): #Quando o botão de voltar for apertado, limpa toda a área e volta ao menu principal
      out.clear_output()
      outGraf.clear_output()
      principal()

    def valueChange(change): #Quando qualquer valor for alterado, limpa a area do gráfico e cria um novo gráfico com os valores atualizados
      outGraf.clear_output(wait = True)

      validador = True
      if slider.value[0] == slider.value[1]:
        validador = False
        slider.value = [0,24]
        outGraf.clear_output(wait = True)
        with outGraf:
          display(caixa2(),caixa3)
          display('Os valores de máximo e de mínimo não podem ser iguais')

      if text.value == '':
        outGraf.clear_output(wait = True)
        with outGraf:
          display(caixa2(),caixa3)
          display('Este é o gráfico de espera sem nenhum horário de ônibus')
      else:
        if validador:
          outGraf.clear_output(wait = True)
          with outGraf:
            display(caixa2(),caixa3)

      with outGraf:
        delta_tempo(valores=tratamento(novo = text.value), intervalo = slider.value)

    slider.observe(valueChange, names= "value")
    voltar.on_click(on_voltar_clicked)
    button.on_click(on_button_clicked)

#Cria e formata o menu principal
choice = widgets.Dropdown(options=[('Selecione...', 1), ('Gráfico único', 2), ('Gráfico Comparativo', 3), ('Gráfico de Tempo de Espera', 4) ],
                        value= 1,
                        description='',
                        )
out = widgets.Output()
display(out)
caixa = widgets.Box(
    [
        widgets.Label(value='Selecione o tipo de gráfico:'),
        choice
    ]
)
with out:
display(caixa)

def valueChangeChoice(change): #Quando o valor do menu mudar chama a função
with out:
    if change['new'] == 2: #Se for gráfico único, chama o menu de gráfico único
    out.clear_output(wait = True)
    graficoUnico()
    elif change['new'] == 3: #Se for gráfico comparativo, chama o menu de gráfico comparativo
    out.clear_output(wait = True)
    graficoComp()
    elif change['new'] == 4: #Se for gráfico de tempo de espera, chama o menu de tempo de espera
    out.clear_output(wait = True)
    graficoDelta()

choice.observe(valueChangeChoice, names='value')