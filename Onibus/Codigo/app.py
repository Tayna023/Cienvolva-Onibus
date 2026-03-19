#Código base para o shinylive, aqui é implementada a interface do usuário

from shiny import App, ui, render, Inputs, Outputs, Session

from Onibus import *
import menus

app_ui = ui.page_fluid(
    ui.navset_bar(
       ui.nav_panel("Horários de Ônibus", menus.onibus),
       ui.nav_panel("Comparativo", "menu.comparativo"),
       ui.nav_panel("Tempo de espera", "menu.tempo_de_espera"),
    title = "Cienvolva"
    ),
    fillable=True
    )

def server(input, output, session):  
  @render.plot()
  def graf_hist_1():
    if input.text() == "":
          return
    else:
        teste = hist_vertical(valores=tratamento(novo = input.text()), duracao = int(input.duracao()), foco = input.slider(), escalaAutomatica = input.check())
        return teste.grafico()
    #menus.plot_graf_hist_1()
              
  @render.plot()
  def graf_hist_2():
        pass
     
  @render.plot()
  def cordeiro_rosa_plot():
       pass
app = App(app_ui, server)

#with ui.nav_panel("Comparativo"):  
'''Sidebar com menu de um gráfico comparativo, criação no gráfico no main tab"
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
'''
#with ui.nav_panel("Tempo de espera"):  
'''#Sidebar com menu de um gráfico de tempo de espera, criação no gráfico no main tab
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
'''
