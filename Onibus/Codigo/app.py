#Código base para o shinylive, aqui é implementada a interface do usuário

from shiny import App, ui, render, Inputs, Outputs, Session, reactive
import numpy as np

from Onibus import *
import menus
import quiz

rng = np.random.default_rng()

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style("""
            .sidebar {
                height: 75vh; /* Set height to 90% of the viewport height */
                overflow-y: auto; /* Add vertical scrollbar if content exceeds height */
            }
            """)
    ),
    ui.navset_bar(
       ui.nav_panel("Horários de Ônibus", menus.onibus),
       ui.nav_panel("Comparativo", "menu.comparativo"),
       ui.nav_panel("Tempo de espera", "menu.tempo_de_espera"),
    title = "Cienvolva"
    ),
    fillable=True
    )

def server(input, output, session):
  @render.ui
  def P1T1():
      return ui.markdown("""&emsp; Para começar precisamos de horários de ônibus!
               <br> &emsp; Você pode conseguir horários reais no [site ônibus de Joinville](https://onibus.info/linhas) basta escolher uma linha qualquer, copiar todos os horários do site e colar na caixa de texto como no exemplo
                <br><br>
                <br>**Insira aqui os horários:**""")
    
  @render.ui
  def P1T2():
      return ui.markdown("<br> &emsp; Se não conseguir buscar os horários não tem problema, basta inventar alguns seguindo a lógica do exemplo.")
    
  @render.ui
  def P2T1():
      return ui.markdown("""&emsp;Navegue pelos horários mudando a opção de *horário pretendido* à esquerda, e observe os destaques no gráfico :) <br>
                                    <br>**Selecione aqui o foco:**""")
    
  @render.ui
  def P2T2():
      return ui.markdown("""<br>&emsp;Você pode escolher também o *intervalo* de quantos minutos quiser a partir da hora pretendida.<br><br>
                        """)
    
  @render.ui
  def P2T0():
      return ui.markdown("""<br>**Selecione aqui o intervalo:**""")
  @render.ui
  def P2T3():
      return ui.markdown("""
                         <br>&emsp;Experimentou diminuir o intervalo?!
                                    <br>&emsp;A altura das barras vai diminuindo: natural, não é?! 
                                    <br>&emsp;Em intervalos menores que 1 hora geralmente vão sair menos ônibus que em 1 hora, e a diminuição de altura das barras expressa isso :)<br>""")

  @render.ui
  def P3T1():
      return ui.markdown("""&emsp;<br>&emsp;Por outro lado, isso pode dificultar um pouco a leitura, além de ficar bastante espaço vazio no gráfico, concorda?!
                                        <br> &emsp;O que a gente poderia fazer pra melhorar essa visualização com intervalo menor e tirar esse espaço vazio?…<br><br>
                         <br>Experimente *ajustar a escala* e observe o que acontece…""")
    
  @render.ui
  def P3T2():
      return ui.markdown("""
                        <br><br>Pronto! :D
                        <br>Agora você conhece todas as funcionalidades dessa aba, pode interpretar o gráfico para ter as informações que quiser — pelo menos de quantos ônibus saem numa certa faixa de horário…
                        """)
  
  @render.ui
  def P4T1():
      return ui.markdown("""<br>Se quiser continuar explorando nossas interatividades experimente a aba *Playground* onde você pode vizualizar melhor as funções
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

  @reactive.effect
  @reactive.event(input.btn)
  def _():
      i = input.btn()
      if i == 1:
          ui.insert_ui(
              menus.pagina2,
              selector="#btn",
              where="beforeBegin"  
          )
          ui.remove_ui(selector="div:has(> #text)")
          ui.remove_ui(selector="#P1T1")
          ui.remove_ui(selector="#P1T2")

      if input.btn() == 2:
          ui.insert_ui(
              menus.pagina3,
              selector = "#btn",
              where="beforeBegin"
          )
          
          ui.remove_ui(selector="div:has(> #slider)")
          #ui.remove_ui(selector="div:has(> #duracao)")
          ui.remove_ui(selector="#P2T1")
          ui.remove_ui(selector="#P2T2")
          ui.remove_ui(selector="#P2T3")
          #ui.remove_ui(selector="#btn")

      if input.btn() == 3:
          ui.insert_ui(
              menus.pagina4,
              selector = "#btn",
              where="beforeBegin"
          )
          ui.remove_ui(selector = "#P2T0")
          ui.remove_ui(selector="#P3T1")
          ui.remove_ui(selector="#P3T2")
          ui.remove_ui(selector="#duracao")
          ui.remove_ui(selector="#check") #Não apaga o texto, só o próprio check
         
  @reactive.effect
  @reactive.event(input.nivel1)
  def _():
        if input.nivel1() == 1:
            horario = rng.choice(23)
            certa = quiz.resposta(horario,horario,4, tratamento(novo = input.text()))
            escolhas = quiz.posicao(certa)
            ui.insert_ui(ui.input_radio_buttons("resposta", f"Quantos ônibus saem as {horario} horas? ", escolhas),
                        selector="#nivel1",
                        where="beforeBegin")
            ui.update_action_button("nivel1", label = "Próximo")
        else:
              if True:#int(input.resposta()) == int(certa):
                  ui.insert_ui(ui.markdown("Resposta Certa!!!! Parabéns :D"),
                               selector="#nivel1",
                              where="beforeBegin")
              else:
                  ui.insert_ui(ui.markdown("Foi por pouco, mas sua resposta está errada :("),
                               selector="#nivel1",
                              where="beforeBegin")
                  ui.insert_ui(ui.markdown("A resposta certa era AAAAAAAAA, tente novamente"),
                               selector="#nivel1",
                              where="beforeBegin")
              horario = rng.choice(23)
              certa = quiz.resposta(horario,horario,4, tratamento(novo = input.text()))
              escolhas = quiz.posicao(certa)
              ui.insert_ui(ui.input_radio_buttons("resposta", f"Quantos ônibus saem as {horario} horas? ", escolhas),
                          selector="#nivel1",
                          where="beforeBegin")
  
  @render.plot()
  def graf_hist_1():
    if input.text() == "":
          return
    else:
        aux = hist_vertical(valores=tratamento(novo = input.text()), duracao = int(input.duracao()), foco = input.slider(), escalaAutomatica = input.check())
        return aux.grafico()
              
              
  @render.plot()
  def graf_hist_2():
        pass
     
     
  @render.plot()
  def cordeiro_rosa_plot():
       pass
  

  #@reactive.effect
  #@reactive.event(menus.input.teste, ignore_none= True)
  #def _():
    #ui.remove_ui(selector="div:has(> #teste)")
  

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
