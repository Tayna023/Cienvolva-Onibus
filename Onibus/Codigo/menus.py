from shiny import ui
from Onibus import *

pagina1 = ui.TagList(
                    ui.output_ui("P1T1"),
                    #Caixa de texto p/ horarios
                    ui.input_text_area("text", "", placeholder= "00:00 \n01:00 \n01:15..."),
                    ui.output_ui("P1T2")
                    )

pagina2 = ui.TagList(
                    ui.output_ui("P2T1"),
                    #Slider de foco
                    ui.input_slider("slider", "", min = 0, max = 24, value = 6, step = 1, post = " horas"),
                    ui.output_ui("P2T2"),
                    #Lista p/ duração
                    ui.output_ui("P2T0"),
                    ui.input_radio_buttons("duracao", " ",
                                               {"15": "15 minutos", "30": "30 minutos", "60": "1 hora"}, 
                                                selected = "60"),
                    ui.output_ui("P2T3")
                    )
pagina3 = ui.TagList(
                    ui.output_ui("P3T1"),
                    #Check p/ ajustar proporção
                    ui.input_checkbox("check", "Ajustar a escala", value = False),
                    ui.output_ui("P3T2")
                    )
pagina4 = ui.TagList(
                    ui.output_ui("P4T1")
                    )
    #Sidebar com menu de um gráfico único, criação no gráfico no main tab
onibus = ui.layout_columns(
                ui.navset_card_tab(
                    ui.nav_panel(" ",
                                 {"class":"sidebar"},
                                pagina1,
                                ui.input_action_button("btn", "Próximo"),
                            icon= "🏠︎"
                        ),
                        ui.nav_panel("Playground",
                                    {"class":"sidebar"},
                                    #Caixa de texto p/ horarios
                                    ui.input_text_area("text", "Insira os horários", placeholder= "00:00 \n01:00 \n01:15..."),
                                    #Slider de foco
                                    ui.input_slider("slider", "Selecione o foco", min = 0, max = 24, value = 6, step = 1, post = " horas"),
                                    #Lista p/ duração
                                    ui.input_radio_buttons("duracao", "Selecione o intervalo",
                                                            {"15": "15 minutos", "30": "30 minutos", "60": "1 hora"}, 
                                                            selected = "60"),
                                    #Check p/ ajustar proporção
                                    ui.input_checkbox("check", "Ajustar a escala", value = False)
                    ),
                    ui.nav_panel("Perguntas",
                                 {"class":"sidebar"},
                                 ui.input_action_button("nivel1", "Nivel 1")

                    )
                ),
                ui.card(
                    "Aqui a gente visualiza como os horários desse ônibus estão distribuídos ao longo do dia: ",
                    ui.output_plot("graf_hist_1"),
                    ui.card_footer(
                            ui.markdown("""<br>&emsp;Entre <horário pretendido> e <horário pretendido + intervalo>, saem < contagem no intervalo> ônibus""")
                            )
                ),
                col_widths=(4,8)
            )

comparativo = " "

tempo_de_espera = " "