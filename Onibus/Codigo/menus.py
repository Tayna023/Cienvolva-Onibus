from shiny import ui
from Onibus import *


    #Sidebar com menu de um gráfico único, criação no gráfico no main tab
onibus = ui.layout_columns(
                ui.navset_card_tab(
                    ui.nav_panel(" ",
                        ui.markdown("""&emsp; Para começar precisamos de horários de ônibus!
                                        <br> &emsp; Você pode conseguir horários reais no [site ônibus de Joinville](https://onibus.info/linhas) basta escolher uma linha qualquer, copiar todos os horários do site e colar na caixa de texto como no exemplo\
                                        <br><br>
                                        <br>**Insira aqui os horários:**"""),
                
                        #Caixa de texto p/ horarios
                        ui.input_text_area("text", "", placeholder= "00:00 \n01:00 \n01:15..."),
                        ui.markdown("""
                                <br> &emsp; Se não conseguir buscar os horários não tem problema, basta inventar alguns seguindo a lógica do exemplo.
                                <br><br>
                                &emsp;Navegue pelos horários mudando a opção de *horário pretendido* à esquerda, e observe os destaques no gráfico :) <br>
                                <br>**Selecione aqui o foco:**"""),
                        #Slider de foco
                        ui.input_slider("slider", "", min = 0, max = 24, value = 6, step = 1, post = " horas"),

                        ui.markdown("""<br>&emsp;Você pode escolher também o *intervalo* de quantos minutos quiser a partir da hora pretendida.<br><br>
                            <br>**Selecione aqui o intervalo:**"""),
                        #Lista p/ duração
                        ui.input_radio_buttons("duracao", " ",
                                                {"15": "15 minutos", "30": "30 minutos", "60": "1 hora"}, 
                                                selected = "60"),
                        ui.markdown("""<br>&emsp;Experimentou diminuir o intervalo?!
                                    <br>&emsp;A altura das barras vai diminuindo: natural, não é?! 
                                    <br>&emsp;Em intervalos menores que 1 hora geralmente vão sair menos ônibus que em 1 hora, e a diminuição de altura das barras expressa isso :)<br>
                                    <br>&emsp;Por outro lado, isso pode dificultar um pouco a leitura, além de ficar bastante espaço vazio no gráfico, concorda?!
                                    <br> &emsp;O que a gente poderia fazer pra melhorar essa visualização com intervalo menor e tirar esse espaço vazio?…<br><br>"""),
                        #Check p/ ajustar proporção
                        ui.input_checkbox("check", "Ajustar a escala", value = False),
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
                                    <ul>"""),
                        icon= "🏠︎"
                    ),
                    ui.nav_panel("Playground",
                                #Caixa de texto p/ horarios
                                ui.input_text_area("text", "Insira os horários", placeholder= "00:00 \n01:00 \n01:15..."),
                                #Slider de foco
                                ui.input_slider("slider", "Selecione o foco", min = 0, max = 24, value = 6, step = 1, post = " horas"),
                                #Lista p/ duração
                                ui.input_radio_buttons("duracao", "Selecione o intervalo",
                                                        {"15": "15 minutos", "30": "30 minutos", "60": "1 hora"}, 
                                                        selected = "60"),
                                #Check p/ ajustar proporção
                                ui.input_checkbox("check", "Ajustar a escala", value = False),
                    ),
                    ui.nav_panel("Perguntas",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sagittis metus sed lacinia aliquet. Praesent vestibulum tortor id libero blandit, in ultrices leo vestibulum. Maecenas lobortis, odio vel eleifend malesuada, elit urna semper dolor, auctor sagittis neque nulla nec nulla. Maecenas bibendum imperdiet justo, in aliquam nisi sodales quis. Quisque aliquam, sem eget elementum accumsan, nisl sem ullamcorper odio, ut consequat odio lectus at purus. Aenean lectus nisi, auctor quis venenatis eu, aliquam commodo velit. Etiam quis ex et magna pellentesque pretium vel non velit. Mauris a lobortis neque. Quisque malesuada justo a faucibus posuere. Curabitur sed vestibulum ipsum, ut consequat nisl. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec eget justo nulla. Vestibulum ut odio feugiat, euismod ligula scelerisque, congue mi. Vivamus cursus augue quis ante vulputate lacinia. Proin non fermentum massa, pharetra ultrices eros."
                    )
                ),
                ui.card(
                    "Aqui a gente visualiza como os horários desse ônibus estão distribuídos ao longo do dia: ",
                    ui.output_plot("graf_hist_1"),
                    ui.card_footer(
                            ui.markdown("""<br>&emsp;Entre <horário pretendido> e <horário pretendido + intervalo>, saem < contagem no intervalo> ônibus""")
                            )
                ),
                icon= "🏠︎",
                col_widths=(4,8)
            )

comparativo = " "

tempo_de_espera = " "

def plot_graf_hist_1():
      if input.text() == "":
          return
      else:
          hist_vertical(valores=tratamento(novo = input.text()), duracao = int(input.duracao()), foco = input.slider(), escalaAutomatica = input.check())
          return hist_vertical.grafico