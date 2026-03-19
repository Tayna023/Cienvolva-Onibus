#Dividir em niveis de dificuldade
#Nivel um - Ler um único valor do histograma
#Nível dois - Ler somas de valores para horarios extendidos
#Nível três - Ler valores em um intervalo aleatório no histograma -- orientar a mudar o intervalo para visualizar?
#Nível quatro - Ler somas de valores para horários extendidos em intervalos aleatórios

#Como coordenar os níveis? Uma questão de cada, ou várias até acertar aí passa de nível
#Botão de encerramento para ver o número de acertos?
import Onibus

def quiz_hist_vert():
  escala = Onibus.hist_vertical.get_escala
  distribuicao = Onibus.hist_vertical.distribuicao #Numero de bins caso a escala seja automatica
      
  a = float(input("inicio: "))
  b = float(input ("fim: "))
  soma = 0
  for i in range(int(a*escala),int(b*escala)):
    soma+=distribuicao[i] 
  print(soma)
  print(distribuicao)