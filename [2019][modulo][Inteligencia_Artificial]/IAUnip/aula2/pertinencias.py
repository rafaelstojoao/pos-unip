#regras
classes = {'jovem':'acessivel','adulto':'caro','idoso':'muitocaro'}
valores = {'acessivel':180,'caro':500,'muitocaro':1200}



jovem = [0,15,20,25]


def pertinenciaTriangular(x,a,b,c):
    resultado = max( min((x-a)/(b-a),(c-x)/(c-b)),0 )
    return resultado

def pertinenciaTrapezoidal(x,a,b,c,d):
    resultado = max(min((x-a)/(b-a),1,(d-x)/(d-c)),0)
    return resultado

idade = int(input())
valorTotal = 0.0

print("Para jovem o valor de entrada tem pertinencia igual a:")
pertJovem =  pertinenciaTrapezoidal(idade,jovem[0],jovem[1],jovem[2],jovem[3])
print(pertJovem)
valorTotal += pertJovem*valores[classes['jovem']]



print("Para adulto o valor de entrada tem pertinencia igual a:")
pertAdulto = pertinenciaTrapezoidal(idade, 20, 25, 50,60)
print(pertAdulto)
valorTotal += pertAdulto*valores[classes['adulto']]


print("Para idosos o valor de entrada tem pertinencia igual a:")
pertIdoso =  pertinenciaTrapezoidal(idade, 55, 60, 200, 250)
print(pertIdoso)
valorTotal += pertIdoso*valores[classes['idoso']]

print("O valor total do seguro para essa idade é de:")
print(valorTotal)