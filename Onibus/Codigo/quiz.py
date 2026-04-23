#Dividir em niveis de dificuldade
#Nivel um - Ler um único valor do histograma
#Nível dois - Ler somas de valores para horarios extendidos
#Nível três - Ler valores em um intervalo aleatório no histograma -- orientar a mudar o intervalo para visualizar?
#Nível quatro - Ler somas de valores para horários extendidos em intervalos aleatórios

#Como coordenar os níveis? Uma questão de cada, ou várias até acertar aí passa de nível
# 3 nivel 1, 2 nivel 2, 3 nivel 3, 2 nivel 4
#Botão de encerramento para ver o número de acertos?
'''
import Onibus
import random
from shiny import ui

def resposta(a, b):
  escala = Onibus.hist_vertical.get_escala(Onibus.hist_vertical)
  distribuicao = Onibus.hist_vertical.distribuicao #Numero de bins caso a escala seja automatica
  
  soma = 0
  for i in range(int(a*escala),int(b*escala)):
    soma+=distribuicao[i] 
  
  return soma

def random_alt(resposta):
  alt = random.randint(resposta-5, resposta+7)
  if alt == resposta:
    random_alt(resposta)
  else:
    return alt
def posicao(resposta):
  certa = random.randint(1,4)
  alternativas = {f"{random_alt(resposta)}: {random_alt(resposta)}"}*4
  alternativas[certa] = f"{resposta}: {resposta}"

Onibus.hist_vertical
horario = random.randint(0,23)
certa = resposta(horario,horario)
tag = ui.markdown(f"Quantos ônibus saem as {horario} horas? "),
ui.input_radio_buttons('alternativas', " ", posicao(certa))
if input.alternativas() == certa:
  feedback = ui.markdown("Resposta Certa")
else:
  feedback = ui.markdown("Resposta Errada")

  '''

#Dividir em niveis de dificuldade
#Nivel um - Ler um único valor do histograma
#Nível dois - Ler somas de valores para horarios extendidos
#Nível três - Ler valores em um intervalo aleatório no histograma -- orientar a mudar o intervalo para visualizar?
#Nível quatro - Ler somas de valores para horários extendidos em intervalos aleatórios

#Implementar aleatório do Numpy
#Estruturar dinâmica de tentativa
#Adicionar estrelas para pontuação
#Adicionar cookies na página para salvar dados
#Como coordenar os níveis? Uma questão de cada, ou várias até acertar aí passa de nível
# 3 nivel 1, 2 nivel 2, 3 nivel 3, 2 nivel 4
#Botão de encerramento para ver o número de acertos?
import numpy as np
from shiny import ui, App, Inputs
import Onibus

rng = np.random.default_rng()


def resposta(a, b, intervalo, valores):
    escala = int(4/intervalo)
    distribuicao = [0]*24*escala #Numero de bins caso a escala seja automatica
    for valor in valores:
        valor %= 24
        distribuicao[int(valor*escala)] += 1
    soma = 0
    for i in range(int(a*escala),int(b*escala)):
        soma+=distribuicao[i] 
    print(distribuicao)
    print (a,b, escala)
  
    return soma

  
def posicao(resposta): #randomiza uma lista com as respostas e a resposta certa entre elas
    certa = rng.choice(a=4)
    if resposta >= 5:
      minimo = 5
    else:
      minimo = resposta
    alternativas = rng.choice(a=range(resposta-minimo, resposta+7), size = 5, replace= False)
    alternativas[certa] = resposta
    alternativa_dict = dict()
    for alternativa in alternativas:
        alternativa_dict[str(alternativa)] = str(alternativa)
    return alternativa_dict

class nivel1:
    def __init__(self):
        self.horario = rng.choice(23)
        self.certa = resposta(self.horario,self.horario,4)
        self.escolhas = posicao(self.certa)
    
    def atualizar(self):
        self.horario = rng.choice(23)
        self.certa = resposta(self.horario,self.horario,4)
        self.escolhas = posicao(self.certa)
        return [self.horario, self.escolhas]

    def get_questao(self):
        return ui.input_radio_buttons("alternativas", f"Quantos ônibus saem as {self.horario} horas? ", self.escolhas)
'''a = nivel1.atualizar
horario = a[0]
escolhas = a[1]'''
'''horario = rng.choice(23)
certa = resposta(horario,horario,4)
escolhas = posicao(certa)
Nivel1 = ui.input_radio_buttons("alternativas", f"Quantos ônibus saem as {horario} horas? ", escolhas)'''
"""if input.alternativas() == str(certa):
    resposta_certa = True
else:
    resposta_certa = False
"""
'''def Nivel1():
    horario = rng.choice(23)
    certa = resposta(horario,horario,4)
    #print(f"Quantos ônibus saem as {horario} horas? ")
    #print(f"{posicao(certa)}")
    #entrada = int(input("A alternativa certa é:"))
    #if entrada == certa:
    #    feedback = "Resposta Certa"
    #else:
    #    feedback = "Resposta Errada"

    #print(feedback)
    #print(f"A resposta certa é {certa}")
    return posicao(certa)'''


def Nivel2():
    inicio = rng.choice(23)
    fim = rng.choice(range(inicio,23))
    certa = resposta(inicio,fim,4)
    print(f"Quantos ônibus saem depois das {inicio} e antes das {fim} horas?")
    print(f"{posicao(certa)}")
    entrada = int(input("A alternativa certa é:"))
    if entrada == certa:
        feedback = "Resposta Certa"
    else:
        feedback = "Resposta Errada"

    print(feedback)
    print(f"A resposta certa é {certa}")

def Nivel3():
    horas = rng.choice(23)
    minutos = rng.choice((1,2))
    intervalo = minutos
    if minutos == 0:
        intervalo = 4
    horario = horas+(minutos/4)
    certa = resposta(horario, horario+(intervalo/4), intervalo)
    print(f"Quantos onibus saem as até {intervalo*15} minutos depois das {horas}:{minutos*15}?")
    print(f"{posicao(certa)}")
    entrada = int(input("A alternativa certa é:"))
    if entrada == certa:
        feedback = "Resposta Certa"
    else:
        feedback = "Resposta Errada"

    print(feedback)
    print(f"A resposta certa é {certa}")

def Nivel4():
    horas = rng.choice(23)
    minutos = rng.choice((1,2))
    intervalo = rng.choice(range(0,minutos))
    if intervalo == 0:
        intervalo = 4
    horario = horas+(minutos/4)

    certa = resposta(horario, horario+(intervalo/4), intervalo)
    print(f"Quantos onibus saem as até {intervalo*15} minutos depois das {horas}:{minutos*15}?")
    print(f"{posicao(certa)}")
    entrada = int(input("A alternativa certa é:"))
    if entrada == certa:
        feedback = "Resposta Certa"
    else:
        feedback = "Resposta Errada"

    print(feedback)
    print(f"A resposta certa é {certa}")




"""APP teste para perguntas

from shiny import ui, App, render, reactive
from . import quiz_teste

app_ui = ui.page_fluid(
    ui.tags.head(
    ),
    ui.navset_bar(
       ui.nav_panel("Teste perguntas",
                    ui.input_action_button("nivel1", "Nivel 1"),
                    ui.panel_conditional(
                        "input.nivel1",
                        quiz_teste.Nivel1
                    ),
                    ui.panel_conditional(
                        "quiz_teste.resposta_certa",
                        ui.markdown("Resposta Certa!!!")
                    )
                    ),
        title = "Teste"
    )
  )
def server(input, output, session): 


    @reactive.effect
    @reactive.event(input.nivel1)
    def _():
        pass#ui.remove_ui(selector="div:has(> #nivel1)")

  
app = App(app_ui, server)"""