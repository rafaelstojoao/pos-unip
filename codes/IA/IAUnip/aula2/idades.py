


idade = int(input())
if idade >= 1 and idade <25:
    if(idade >20):
        print("Essa pessoa é considerada JOVEM E ADULTA")
        classificacao = "jovem-adulta"
    else:
        print("Essa idade é considerada apenas JOVEM")
        classificacao = "jovem"
elif idade > 20 and idade < 60:
    if idade > 55:
        print("Essa pessoa já é considerada pré idosa")
        classificacao = "pre-idoso"
    else:
        print("Essa idade é considerada  apenas Adulta")
        classificacao = "adulta"
elif idade > 55:
    print("Essa pessoa é considerada IDOSA")
    classificacao = "idosa"


if classificacao == 'idosa':
    print("O SEGURO É CARO")