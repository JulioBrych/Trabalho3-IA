import copy
import math
import random
import numpy
import matplotlib
from matplotlib import pyplot as plt

def printa_matriz(matriz):
    for i in range(0, len(matriz)):
        print(matriz[i])

def calcula_distancias_cidades():
    global distancia_cidades
    for i in range(0, 20):
        vet_temp = []
        for j in range(0, 20):
            vet_temp.append(calcula_distancia_euclidiana(i, j))
        distanciaCidades.append(vet_temp)

def gera_primeira_geracao():
    global matrix_cromossomos
    for i in range(0, 20):
        #preenche a matriz de cromossomos com valores de 0 a 20 sem repeticoes
        matrix_cromossomos.append(random.sample(range(20), 20))


def calcula_distancia_euclidiana(ini, des):
    global mapa
    return math.sqrt(((mapa[des][0]-mapa[ini][0])**2)+((mapa[des][1]-mapa[ini][1])**2))

def calcula_aptidao(matriz):
    global vet_aptidao
    global distanciaCidades

    matrixTemp = copy.deepcopy(matriz)
    for i in range(0, 20):
        aux = matrixTemp[i][0]
        matrixTemp[i].append(aux)
    vet_aptidao.clear()
    for i in range(0, 20):
        aux = 0
        for j in range(0, 20):
            aux += distanciaCidades[matrixTemp[i][j]][matrixTemp[i][j+1]]
        vet_aptidao.append(aux)
    print('------vetor de aptidão--------')
    print(vet_aptidao)
    print('******************')


def ordena_matrixcromo_vetapt_dist():
    global matrix_cromossomos
    global vet_aptidao
    # pega os valores da matriz de cromossomos e do vetor de aptidão
    matriz = numpy.array(matrix_cromossomos)
    aptidoes = numpy.array(vet_aptidao)
    #cria uma lista com os indices do vetor de aptidão ordenados do menor para o maior
    inds = aptidoes.argsort()
    #usando os indices ordenados, criamos uma matriz e um vetor ordenados
    matrizOrdenada = matriz[inds]

    aptidoesOrdenadas = aptidoes[inds]
    #substituimos a matriz
    matrix_cromossomos = matrizOrdenada.tolist()
    vet_aptidao = aptidoesOrdenadas.tolist()


def escolhe_pais():
    global vet_roleta
    global listaPai1
    global listaPai2
    # criamos uma lista vazia(listaPai1) que sera preenchida com 5 valores aletorio removidos da lista2
    listaPai1 = []
    listaPai2 = [0,1,2,3,4,5,6,7,8,9]
    while (len(listaPai1) < 5):
        # gera um valor aleatorio, para pegar um pai da roleta
        aux = random.randint(0,54)
        # verifica se esse pai escolhido nao esta na primeira lista
        #garantindo que as lista nao possuam pais iguais
        if not vet_roleta[aux] in listaPai1:
            listaPai1.append(vet_roleta[aux])
            listaPai2.remove(vet_roleta[aux])
    print('pais 1')
    print(listaPai1)
    print('pais 2')
    print(listaPai2)
    print('---------------')


def gera_filhos():
    global matrix_cromossomos
    global listaPai1
    global listaPai2
    listaNovosFilhos = []
    for i in range(0,5):
        #gera indice aleatorio para troca de cromossomos
        indice = random.randint(0,19)
        #copia os cromossomos dos dois pais
        filho1 = copy.deepcopy(matrix_cromossomos[listaPai1[i]])
        filho2 = copy.deepcopy(matrix_cromossomos[listaPai2[i]])
        # faz a troca dos valores dos comossomos
        valorTroca = filho1[indice]
        filho1[indice] = filho2[indice]
        filho2[indice] = valorTroca
        while (len(filho1) != len(set(filho1))): # repete ate nao haver mais numeros duplicados
            indice = verifica_repetido(filho1,indice)
            valorTroca = filho1[indice]
            filho1[indice] = filho2[indice]
            filho2[indice] = valorTroca
        listaNovosFilhos.append(filho1)
        listaNovosFilhos.append(filho2)
    # substitui os 10 piores da matriz pelos 10 novos filhos
    for i in range(10, 20):
        matrix_cromossomos[i] = listaNovosFilhos[i-10]
    print('Matriz com novos filhos')
    printa_matriz(matrix_cromossomos)


def verifica_repetido(filho1,indice):
    #função usada para pegar o indice do proximo cromossomo a ser trocado
    #pega o ultimo cromossomo que foi trocado
    valor = filho1[indice]
    #varre a lista de cromossomos
    for i in range(0,20):
        # caso o filho1 possua o ultimo valor trocado e esse nao esteja na mesma posição do indice recebido
        # é nessa posição em que tera que ser feita a proxima troca de cromossomo
        if filho1[i] == valor and i != indice:
            return i
    # caso nao possua nenhum cromossomo a ser trocado retorna -1
    return -1


def mutacao():
    global matrix_cromossomos
    for i in range(10,20):
        # gera um numero com ponto flutuante entre 0 e 1, caso esse valor seja menor que a chance de mutação ele faz a mutação
        if random.random() < 0.05:
            #gera dois indices para fazer a troca de cromossomos
            indice1 = random.randint(0,19)
            indice2 = random.randint(0, 19)
            #fica gerando um novo indice ate os dois serem diferentes
            while indice2 == indice1:
                indice2 = random.randint(0, 19)
            #faz a troca dos cromossomos
            valor = matrix_cromossomos[i][indice1]
            matrix_cromossomos[i][indice1] = matrix_cromossomos[i][indice2]
            matrix_cromossomos[i][indice2] = valor

def imprime_solucao():
    global matrix_cromossomos
    global vet_aptidao

    x = len(matrix_cromossomos)
    taxaMutacao = 0.05;
    numCidades = 20;
    melhorCusto = vet_aptidao[0]
    melhorSolucao = matrix_cromossomos[0]
    print("Tamanho da populacao: ", x)
    print("Taxa de mutacao: ", taxaMutacao)
    print("Numero de cidades: ", numCidades)
    print("Melhor custo: ", melhorCusto)
    print("Melhor solucao: ", melhorSolucao)


def funcao_plot(caminhos, pontos):

    x = []
    y = []
    for i in caminhos[0]:
        x.append(pontos[i][0])
        y.append(pontos[i][1])

    for i in range(0, 20):
        plt.plot(x[i], y[i], 'co', marker="${}$".format(caminhos[0][i]), markersize=17)

    # Tamanho da seta
    tam_seta = float(max(x)) / float(100)

    # Desenho dos caminhos
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=tam_seta,
              color='g', length_includes_head=True)
    for i in range(0, len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=tam_seta,
        color='g', length_includes_head=True)

    # alterando limites das coordenadas
    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.show()

if __name__  == '__main__':
    mapa = [[0.77687122244663642, 0.27943919986108079], [0.5572653296455039, 0.11661366329340583],
            [0.65639441309858648, 0.39053913424199571],
            [0.60439895238077324, 0.66616903964750607], [0.10984792404443977, 0.6985758378186272],
            [0.30681838758814639, 0.20730006383213373],
            [0.036420458719028548, 0.5024721283845478], [0.50750194272285054, 0.073938685056537334],
            [0.79819787712259027, 0.67991802460956252],
            [0.79896874846157562, 0.39749277989717913], [0.14326939769923641, 0.14151256215331487],
            [0.071101926660729675, 0.12773617026441342],
            [0.72613149506352259, 0.37197289724774407], [0.22624105387667293, 0.69033435138929333],
            [0.6248041238023041, 0.9189034809361033],
            [0.5483227916626594, 0.52333815217506263], [0.39699387912590556, 0.42525694545543524],
            [0.075454958741316913, 0.37166915101708831],
            [0.67595096782693853, 0.99033329254439939], [0.074297051769727118, 0.15694231625653665]]

    distanciaCidades = []
    vet_roleta = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,6,6,6,6,7,7,7,8,8,9] #55 numeros, distribuidos para as chances da roleta
    matrix_cromossomos = []
    vet_aptidao = []
    listaPai1 = []
    listaPai2 = []

    calcula_distancias_cidades()
    gera_primeira_geracao()
    print('----------primeira matriz gerada------------')
    printa_matriz(matrix_cromossomos)
    print('**********')
    interacoes = 0
    while interacoes < 1000:
        calcula_aptidao(matrix_cromossomos)
        ordena_matrixcromo_vetapt_dist()
        escolhe_pais()
        gera_filhos()
        mutacao()
        interacoes += 1

    #ordena os cromossomos e aptidoes e imprime a solucao
    ordena_matrixcromo_vetapt_dist()
    imprime_solucao()

   # coordenadas para os pontos x e y da função plot
    coord_x = [1, 8, 4, 9, 1, 1, 8, 2, 16, 8, 18, 13, 2, 3, 13, 15, 14, 3, 16, 10]
    coord_y = [1, 2, 3, 4, 9, 5, 7, 9, 8, 6, 10, 9, 11, 2, 1, 13, 7, 10, 3, 18]
    pontos = []
    for i in range(0, len(coord_x)):
        pontos.append((coord_x[i], coord_y[i]))

    #caminhos abaixo somente para testes, caminho principal vem da matrix_cromossomos

    caminho1 = [14, 18, 8, 9, 0, 12, 2, 15, 13, 4, 6, 17, 5, 7, 1, 10, 11, 19, 16, 3]

    caminho2 = [16, 6, 17, 10, 5, 0, 12, 9, 8, 18, 14, 3, 1, 7, 11, 19, 4, 13, 15, 2]

    caminhos = [matrix_cromossomos[0],caminho2]


    # solucao graficamente
    funcao_plot(caminhos, pontos)
