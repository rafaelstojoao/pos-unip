
classes = [[0,15,20,25], #jovem
           [20,25,50,60], #adulto
           [55,60,200,250]] #idoso


def pertinenciaTriangular(x,a,b,c):
    resultado = max( min((x-a)/(b-a),(c-x)/(c-b)),0 )
    return resultado

def pertinenciaTrapezoidal(x,a,b,c,d):
    resultado = max(min((x-a)/(b-a),1,(d-x)/(d-c)),0)
    return resultado



idade = int(input())


print("Para jovem o valor de entrada tem pertinencia igual a:")
print(pertinenciaTrapezoidal(idade,classes[0][0],classes[0][1],classes[0][2],classes[0][3]))

print("Para adulto o valor de entrada tem pertinencia igual a:")
print(pertinenciaTrapezoidal(idade,classes[1][0],classes[1][1],classes[1][2],classes[1][3]))

print("Para idosos o valor de entrada tem pertinencia igual a:")
print(pertinenciaTrapezoidal(idade,classes[2][0],classes[2][1],classes[2][2],classes[2][3]))
