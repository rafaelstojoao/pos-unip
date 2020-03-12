import copy
estadoinicial = [[1,2,3],
                 [0,4,6],
                 [7,5,8]]

estadoatual = copy.deepcopy(estadoinicial)
objetivo = [[1,2,3],
            [4,5,6],
            [7,8,0]]

estadospassados = []
estadospassados.append(estadoinicial)

def somadiferencas(simulado):
    # print("calculando a diferenca para: ")
    # print(simulado)
    dif = 0
    for i in range(3):
        for j in range(3):
            dif += abs(objetivo[i][j] - simulado[i][j])
    return dif



def troca(tabuleiro,i,j,novoi,novoj):
    if novoj >= 0 and novoi >= 0 and novoj <3 and novoi < 3:
        aux = tabuleiro[i][j]
        tabuleiro[i][j] = tabuleiro[novoi][novoj]
        tabuleiro[novoi][novoj] = aux

    return tabuleiro


def simulaMovimento(distanciaAtual):
    movimentou = False
    menorValor = 999
    estadoatual = []
    for i in range(3):
        for j in range(3):
            if estadoinicial[i][j] == 0: #zero encontrado

                tabuleirocopia = copy.deepcopy(estadoinicial)
                simulado = troca(tabuleirocopia,i,j,i-1,j)
                val1 = somadiferencas(simulado)

                if val1 <= menorValor and simulado not in estadospassados:
                    menorValor = val1
                    estadoatual = copy.deepcopy(simulado)
                    estadospassados.append(estadoatual)
                    movimentou = True
                    # print("\menor valor encontrado: "+str(val1)+" era: "+str(menorValor))




                tabuleirocopia = copy.deepcopy(estadoinicial)
                simulado = troca(tabuleirocopia,i,j,i,j-1)
                val1 = somadiferencas(simulado)
                if val1 <= menorValor and simulado not in estadospassados:
                    menorValor = val1
                    estadoatual = copy.deepcopy(simulado)
                    movimentou = True
                    # print("\menor valor encontrado: "+str(val1)+" era: "+str(menorValor))
                    estadospassados.append(estadoatual)


                tabuleirocopia = copy.deepcopy(estadoinicial)
                simulado = troca(tabuleirocopia,i,j,i,j+1)
                val1 = somadiferencas(simulado)
                if val1 <= menorValor and simulado not in estadospassados:
                    menorValor = val1
                    estadoatual = copy.deepcopy(simulado)
                    movimentou = True
                    # print("\menor valor encontrado: "+str(val1)+" era: "+str(menorValor))
                    estadospassados.append(estadoatual)


                tabuleirocopia = copy.deepcopy(estadoinicial)
                simulado = troca(tabuleirocopia,i,j,i+1,j)
                # print(simulado)
                val1 = somadiferencas(simulado)


                if (val1 <= menorValor and simulado not in estadospassados) or movimentou == False:
                    menorValor = val1
                    estadoatual = copy.deepcopy(simulado)
                    movimentou = True
                    # print("\menor valor encontrado: " + str(val1) + " era: " + str(menorValor))
                    estadospassados.append(estadoatual)

    return estadoatual, menorValor



diferenca = 999
contadorDeJogadas = 1

while diferenca  > 0 and contadorDeJogadas<=10:
    print("\n Movimento: "+str(contadorDeJogadas))
    contadorDeJogadas+=1

    print("\n Estado atual:")
    print(estadoatual)

    estadoatual, diferenca = simulaMovimento(diferenca)
    print("\n Novo estado")
    print(estadoatual)

    print("\nDiferença para estado ótimo")
    print(diferenca)
