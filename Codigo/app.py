import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

from functools import partial
from shiny.ui import page_navbar
from shiny.express import render, ui, input
from shiny import reactive

from matplotlib import cbook
#Variaveis de design
pontos = '#0023FF'
palavras = '#FFC400'
media_cor = '#FFC400'
grafico1 = '#0023FF'
grafico2 = '#FFC400'

ui.page_opts(
    title= "Cienvolva",  
    #page_fn=partial(page_navbar, id="page"),  
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

def hist_vertical(valores, duracao, foco, escalaAutomatica):
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
  for i in range(0,25):
    bins.append(i)
    while cont < escala:
        bins.append(bins[len(bins)-1]+(passo))
        cont+=1
    cont=1

  ax.hist(valores, bins,width=passo, linewidth=0.5, edgecolor="white", color = grafico1)#valores = valores a serem sorteados, bins = quais as divisões

  #formata os ticks
  ax.tick_params(which='major', labelsize= 8, width=1.0, length=9)
  ax.tick_params(which='minor', labelsize = 5,  width=0.75, length=2.5)

  #Fixa a posição dos ticks nos eixos
  ax.xaxis.set_major_locator(ticker.FixedLocator(major_positions))
  ax.xaxis.set_major_formatter(ticker.FixedFormatter(major_hora))

  #Fixa o valor dos ticks no eixo
  ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_positions))
  ax.xaxis.set_minor_formatter(ticker.FixedFormatter(minor_hora))

  ax.set(xlim=(-0.5, 24.5*passo), xticks=np.arange(0, 24.5),
        ylim=(0, eixo_y), yticks=np.arange(0, eixo_y))
  
  altura = 0
  for valor in valores:
    if valor >= foco and valor < foco+duracao/60:
      altura += 1
  
  plt.plot([-0.5,foco], [altura]*2, color = "orange", linestyle = ":")
  ax.bar(foco, altura, color = "orange", align = "edge", width = duracao/60)

  plt.show()

with ui.nav_panel("Horários de Ônibus"):  
    #Sidebar com menu de um gráfico único, criação no gráfico no main tab
    with ui.layout_columns(col_widths=(4,8)):
      with ui.navset_card_tab():
        with ui.nav_panel(" ", icon= "🏠︎"):  
          ui.markdown("""&emsp; Para começar precisamos de horários de ônibus!
                      <br> &emsp; Você pode conseguir horários reais no [site ônibus de Joinville](https://onibus.info/linhas) basta escolher uma linha qualquer, copiar todos os horários do site e colar na caixa de texto como no exemplo\
                      <br><br>""")
          
          #Caixa de texto p/ horarios
          ui.input_text_area("text", "Insira os horários", placeholder= "00:00 \n01:00 \n01:15...") 
          def min_horas(min):
            horas = min/60
            return horas
          ui.markdown("""
                      <br> &emsp; Se não conseguir buscar os horários não tem problema, basta inventar alguns seguindo a lógica do exemplo.
                      <br><br>
                      &emsp;Navegue pelos horários mudando a opção de *horário pretendido* à esquerda, e observe os destaques no gráfico :) <br>""")
          #Slider de foco
          ui.input_slider("slider", "Selecione o foco", min = 0, max = 24, value = 6, step = 1, post = " horas")
          
          ui.markdown("""<br>&emsp;Você pode escolher também o *intervalo* de quantos minutos quiser a partir da hora pretendida.<br><br>""")
          #Lista p/ duração
          ui.input_radio_buttons("duracao", "Selecione o intervalo",
                                 {"15": "15 minutos", "30": "30 minutos", "60": "1 hora"}, 
                                 selected = "60")
          ui.markdown("""<br>&emsp;Experimentou diminuir o intervalo?!
                        <br>&emsp;A altura das barras vai diminuindo: natural, não é?! 
                        <br>&emsp;Em intervalos menores que 1 hora geralmente vão sair menos ônibus que em 1 hora, e a diminuição de altura das barras expressa isso :)<br>
                        <br>&emsp;Por outro lado, isso pode dificultar um pouco a leitura, além de ficar bastante espaço vazio no gráfico, concorda?!
                        <br> &emsp;O que a gente poderia fazer pra melhorar essa visualização com intervalo menor e tirar esse espaço vazio?…<br><br>""")
          #Check p/ ajustar proporção
          ui.input_checkbox("check", "Ajustar a escala", value = False)
          ui.markdown("""<br>Experimente *ajustar a escala* e observe o que acontece…
                      <br><br>Pronto! :D
                      <br>Agora você conhece todas as funcionalidades dessa aba, pode interpretar o gráfico para ter as informações que quiser — pelo menos de quantos ônibus saem numa certa faixa de horário…
                      <br>Se quiser continuar explorando nossas interatividades experimente a aba *Playground* onde você pode vizualizar melhor as funções
                      <ul>
                      <br><br><li> Quer testar seu conhecimento?! 
                          <br>&emsp;--> explore nosso painel de perguntas!
                      <br> <li> Quer explorar mais as diferenças de intervalos?!
                      <br>&emsp;--> selecione *Comparativo* no topo da página!
                      <br><li> Quer ter uma ideia do tempo de espera pra uma faixa de horário?! 
                      <br>&emsp;--> selecione *Tempo de espera* no topo da página!
                      <br><li> Quer contar pra gente como foi pra você passear por aqui?! 
                      <br>&emsp;--> [clique aqui](link do formulário de satisfação)!
                      <ul>""")

        with ui.nav_panel("Playground"):
          #Caixa de texto p/ horarios
          ui.input_text_area("text", "Insira os horários", placeholder= "00:00 \n01:00 \n01:15...")
          #Slider de foco
          ui.input_slider("slider", "Selecione o foco", min = 0, max = 24, value = 6, step = 1, post = " horas")
          #Lista p/ duração
          ui.input_radio_buttons("duracao", "Selecione o intervalo",
                                 {"15": "15 minutos", "30": "30 minutos", "60": "1 hora"}, 
                                 selected = "60")
          #Check p/ ajustar proporção
          ui.input_checkbox("check", "Ajustar a escala", value = False)
        with ui.nav_panel("Perguntas"):
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sagittis metus sed lacinia aliquet. Praesent vestibulum tortor id libero blandit, in ultrices leo vestibulum. Maecenas lobortis, odio vel eleifend malesuada, elit urna semper dolor, auctor sagittis neque nulla nec nulla. Maecenas bibendum imperdiet justo, in aliquam nisi sodales quis. Quisque aliquam, sem eget elementum accumsan, nisl sem ullamcorper odio, ut consequat odio lectus at purus. Aenean lectus nisi, auctor quis venenatis eu, aliquam commodo velit. Etiam quis ex et magna pellentesque pretium vel non velit. Mauris a lobortis neque. Quisque malesuada justo a faucibus posuere. Curabitur sed vestibulum ipsum, ut consequat nisl. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec eget justo nulla. Vestibulum ut odio feugiat, euismod ligula scelerisque, congue mi. Vivamus cursus augue quis ante vulputate lacinia. Proin non fermentum massa, pharetra ultrices eros."
      with ui.card():
        "Aqui a gente visualiza como os horários desse ônibus estão distribuídos ao longo do dia: "
        @render.plot()
        #@reactive.event(input.button)
        def graf():
          if input.text() == "":
            return
          else:
            return hist_vertical(valores=tratamento(novo = input.text()), duracao = int(input.duracao()), foco = input.slider(), escalaAutomatica = input.check())

        ui.markdown("""<br>&emsp;Entre <horário pretendido> e <horário pretendido + intervalo>, saem < contagem no intervalo> ônibus""")        
#Histograma comparativo
#Aqui está todo o processamento para formatar e criar um gráfico com dois histogramas lado a lado
def hist_horizontal_comparativo(valores, duracao1, duracao2, mesmaEscala):

  #Definições histograma esquerda

  #duracao1 = duracao1.split()
  #duracao1 = int(duracao1[0])
  #if duracao1 == 1:
  # duracao1 = 60

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
  #duracao2 = duracao2.split()
  #duracao2 = int(duracao2[0])
  #if duracao2 == 1:
  #  duracao2 = 60

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

with ui.nav_panel("Comparativo"):  
  #Sidebar com menu de um gráfico comparativo, criação no gráfico no main tab
  with ui.layout_columns(col_widths=(3,9), row_heights= (12), fill = True):
    with ui.navset_card_tab():
      with ui.nav_panel("Interativo"):  
        #"Aqui ficará o menu do gráfico comparativo" 
        #Caixa de texto p/ horarios
        ui.input_text_area("text1", "Insira os horários", placeholder= "00:00 \n01:00 \n01:15...") 
        #Slider p/ duração
        ui.input_slider("slider1", "Intervalo do gráfico da direita: ", min = 15, max = 60, value = 60, step = 15, post = " minutos")
        #Slider p/duração 2
        ui.input_slider("slider2", "Intervalo do gráfico da esquerda: ", min = 15, max = 60, value = 60, step = 15, post = " minutos")
        #Check p/ ajustar proporção
        ui.input_checkbox("check1", "Ajustar proporção", value = False)
      with ui.nav_panel("Explicação"):
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sagittis metus sed lacinia aliquet. Praesent vestibulum tortor id libero blandit, in ultrices leo vestibulum. Maecenas lobortis, odio vel eleifend malesuada, elit urna semper dolor, auctor sagittis neque nulla nec nulla. Maecenas bibendum imperdiet justo, in aliquam nisi sodales quis. Quisque aliquam, sem eget elementum accumsan, nisl sem ullamcorper odio, ut consequat odio lectus at purus. Aenean lectus nisi, auctor quis venenatis eu, aliquam commodo velit. Etiam quis ex et magna pellentesque pretium vel non velit. Mauris a lobortis neque. Quisque malesuada justo a faucibus posuere. Curabitur sed vestibulum ipsum, ut consequat nisl. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec eget justo nulla. Vestibulum ut odio feugiat, euismod ligula scelerisque, congue mi. Vivamus cursus augue quis ante vulputate lacinia. Proin non fermentum massa, pharetra ultrices eros."
      with ui.nav_panel("Perguntas"):
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sagittis metus sed lacinia aliquet. Praesent vestibulum tortor id libero blandit, in ultrices leo vestibulum. Maecenas lobortis, odio vel eleifend malesuada, elit urna semper dolor, auctor sagittis neque nulla nec nulla. Maecenas bibendum imperdiet justo, in aliquam nisi sodales quis. Quisque aliquam, sem eget elementum accumsan, nisl sem ullamcorper odio, ut consequat odio lectus at purus. Aenean lectus nisi, auctor quis venenatis eu, aliquam commodo velit. Etiam quis ex et magna pellentesque pretium vel non velit. Mauris a lobortis neque. Quisque malesuada justo a faucibus posuere. Curabitur sed vestibulum ipsum, ut consequat nisl. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec eget justo nulla. Vestibulum ut odio feugiat, euismod ligula scelerisque, congue mi. Vivamus cursus augue quis ante vulputate lacinia. Proin non fermentum massa, pharetra ultrices eros."
    with ui.card():
      #"Aqui ficará o gráfico comparativo"
      @render.plot()
      #@reactive.event(input.button)
      def graf1():
        if input.text1() == "":
          return
        else:
          return hist_horizontal_comparativo(valores=tratamento(novo = input.text1()), duracao1 = input.slider1(), duracao2 = input.slider2(), mesmaEscala = input.check1())

def delta_tempo(valores, intervalo):

  #organização dos horários por ordem crescente
  valores.sort()
  if len(valores) == 0:
    valores = [0]
  valores = [0]+valores+[24+valores[0]]#Adiciona 0 e 24 mais primeiro valor, pra funcinar nas bordas
  #Criação do gráfico e do seu tamanho
  fig, axes1 = plt.subplots(figsize=(30, 7))

  for i in range(0,len(valores)-1):
    #Plot de cada subconjunto do gráfico com o horario e o horario seguinte sendo o eixo x e o eixo y sendo o valor da diferença até 0
    axes1.plot ([valores[i], valores[i+1]],[(valores[i+1]-valores[i]), 0], color = grafico1)

  duracao = 1
  escala = 1

  axes2 = axes1.inset_axes(bounds = [.575, .55, .4, .4],zorder=6)
  #axes1 é o gráfico maior
  #axes2 é o gráfico menor

  #plt.setp(ax, xticks=[], yticks=[])
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

  axes2.text(intervalo[0],(media + (max(max_y)/40)), " Tempo médio de espera no intervalo selecionado", color = palavras)

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

  plt.show()


with ui.nav_panel("Tempo de espera"):  
  #Sidebar com menu de um gráfico de tempo de espera, criação no gráfico no main tab
  with ui.layout_columns(col_widths=(3,9)):
    with ui.navset_card_tab(): 
      with ui.nav_panel("Interativo"):
        #"Aqui ficará o menu do gráfico de tempo de espera"  
        ui.input_text_area("text2", "Insira os horários: ", placeholder = "00:00 \n01:00 \n02:00 ...")
        ui.input_slider("range", "Intervalo", min=0, max= 24, value = [00, 24], step = 0.5)
      with ui.nav_panel("Explicação"):
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sagittis metus sed lacinia aliquet. Praesent vestibulum tortor id libero blandit, in ultrices leo vestibulum. Maecenas lobortis, odio vel eleifend malesuada, elit urna semper dolor, auctor sagittis neque nulla nec nulla. Maecenas bibendum imperdiet justo, in aliquam nisi sodales quis. Quisque aliquam, sem eget elementum accumsan, nisl sem ullamcorper odio, ut consequat odio lectus at purus. Aenean lectus nisi, auctor quis venenatis eu, aliquam commodo velit. Etiam quis ex et magna pellentesque pretium vel non velit. Mauris a lobortis neque. Quisque malesuada justo a faucibus posuere. Curabitur sed vestibulum ipsum, ut consequat nisl. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec eget justo nulla. Vestibulum ut odio feugiat, euismod ligula scelerisque, congue mi. Vivamus cursus augue quis ante vulputate lacinia. Proin non fermentum massa, pharetra ultrices eros."
      with ui.nav_panel("Fixação"):
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sagittis metus sed lacinia aliquet. Praesent vestibulum tortor id libero blandit, in ultrices leo vestibulum. Maecenas lobortis, odio vel eleifend malesuada, elit urna semper dolor, auctor sagittis neque nulla nec nulla. Maecenas bibendum imperdiet justo, in aliquam nisi sodales quis. Quisque aliquam, sem eget elementum accumsan, nisl sem ullamcorper odio, ut consequat odio lectus at purus. Aenean lectus nisi, auctor quis venenatis eu, aliquam commodo velit. Etiam quis ex et magna pellentesque pretium vel non velit. Mauris a lobortis neque. Quisque malesuada justo a faucibus posuere. Curabitur sed vestibulum ipsum, ut consequat nisl. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec eget justo nulla. Vestibulum ut odio feugiat, euismod ligula scelerisque, congue mi. Vivamus cursus augue quis ante vulputate lacinia. Proin non fermentum massa, pharetra ultrices eros."          
    with ui.card():
      #"Aqui ficará o gráfico de tempo de espera"
      @render.plot()
      #@reactive.event(input.button)
      def graf2():
        if input.text2() == "":
          return
        else:
          return delta_tempo(valores = tratamento(input.text2()), intervalo = input.range())