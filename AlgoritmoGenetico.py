import copy
import math
import random
import numpy

def printaMatriz(matriz):
    for i in range(0, len(matriz)):
        print(matriz[i])





def calcula_distancias_cidades():
    global distancia_cidades
    for i in range(0, 20):
        vet_temp = []
        for j in range(0, 20):
            vet_temp.append(calcula_distancia_euclidiana(i, j))
        distanciaCidades.append(vet_temp)


def ordenaTudo():
    global matrix_cromossomos
    global vet_aptidao


def geraPrimeiraGeracao():
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
        # verifica se esse pai escolhido n esta na primeira lista
        #garantindo que as lista n possuam pais iguais
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
        while (len(filho1) != len(set(filho1))):
            indice = verifica_repitido(filho1,indice)
            valorTroca = filho1[indice]
            filho1[indice] = filho2[indice]
            filho2[indice] = valorTroca
        listaNovosFilhos.append(filho1)
        listaNovosFilhos.append(filho2)
    # substitui os 10 piores da matriz pelos 10 novos filhos
    for i in range(10, 20):
        matrix_cromossomos[i] = listaNovosFilhos[i-10]
    print('Matriz com novos filhos')
    printaMatriz(matrix_cromossomos)


def verifica_repitido(filho1,indice):
    #função usada para pegar o indice do proximo cromossomo a ser trocado
    #pega o ultimo cromossomo que foi trocado
    valor = filho1[indice]
    #vare a lista de cromossomos
    for i in range(0,20):
        # caso o filho1 possua o ultimo valor trocado e esse n esteja na mesma posição do indice recebido
        # é nessa posição em que tera que ser feita a procima troca de cromossomo
        if filho1[i] == valor and i != indice:
            return i
    # caso n possua nenhum cromossomo a ser trocado retorna -1
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
    vet_roleta = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,5,5,5,5,5,6,6,6,6,7,7,7,8,8,9] #55 numeros
    matrix_cromossomos = []
    vet_aptidao = []
    listaPai1 = []
    listaPai2 = []


    calcula_distancias_cidades()
    geraPrimeiraGeracao()
    print('----------primeira matriz gerada------------')
    printaMatriz(matrix_cromossomos)
    print('**********')
    interacoes = 0
    while interacoes < 1000:
        calcula_aptidao(matrix_cromossomos)
        ordena_matrixcromo_vetapt_dist()
        escolhe_pais()
        gera_filhos()
        mutacao()
        interacoes += 1

    ordena_matrixcromo_vetapt_dist()