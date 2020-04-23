from pprint import pprint
from pyswip import Prolog


motor  = Prolog()
motor.consult("ds/minhaBD.pl")

novasInfos = ""
perguntas = ['sexo','idade','peso','cor','filho','brasil','esporte','cabelo','musica','casado','irmaos','altura','careca']


res = list(motor.query('sexo(X,_)'))
possibilidades = list([chave['X'] for chave in res])
novasPossibilidades = []

op = input("\n consultar; ou  \n jogar ?")

if(op == 'jogar'):
    print("\n O indivíduo que está pensando:")
    resposta = ""
    achei = False

    for fato in perguntas:
        if(fato == 'sexo'):
            print('\n é homem ou \n mulher?')

        elif (fato == 'idade'):
            print('\n é jovem, adulto ou idoso?')
        elif (fato == 'peso'):
            print("\n É magro, gordo ou normal?")
        elif(fato =='cor'):
            print("\n é branca, preta ou amarela?")
        elif (fato == 'filhos'):
            print('\n Tem filhos, sim ou nao?')
        elif (fato == 'brasil'):
            print('\n é brasileiro(a)?')
        elif (fato == 'esporte'):
            print('\n é relacionado(a) a algum esporte?')
        elif (fato == 'cabelo'):
            print('\n o cabelo é loiro, escuro, branco, vermelho ou outro?')
        elif (fato == 'careca'):
            print('\n é careca?')
        elif (fato == 'casado'):
            print('\n é casado(a), sim ou nao?')
        elif (fato == 'irmaos'):
            print('\n tem irmaos, sim ou nao?')
        elif (fato == 'altura'):
            print('\n é baixa, media ou alta?')

        print(fato)
        resposta = input()




        q = list(motor.query(fato+'(X,'+resposta+')'))
        novasPossibilidades = list([d['X'] for d in q])
        possibilidades = list(set(novasPossibilidades) & set(possibilidades))

        if(len(possibilidades) > 1):
                print("\n Estou em dúvida entre "+str(len(possibilidades))+" pessoas")
        elif (len(possibilidades) == 1):
                print("vou chutar.......\n "
                  "hmmmmmmmmm\n "
                  "hmmmmmmm.....\n "
                  "já sei"
                  "\n eu acho que a pessoa que você está pensando é: ")
                print(possibilidades)
                resp = input("\n E aí, acertei??? \n sim ou \n não")
                if(resp =='sim'):
                    achei = True
                    print("Fim...")
                    break
                else:
                    print("\n Ok, todo mundo erra. preciso conhecer essa pessoa!\n Vamos continuar!")

        else:
            print("\n Preciso de mais informações.... não imagino quem possa ser")
        novasInfos += fato+"(XX,"+str(resposta)+").\n"

    if(achei == False):
        print("\n Infelizmente ainda não conheci essa pessoa. Por favor, me diga o nome para eu aprender")
        nome = input()
        novasInfos =  novasInfos.replace('XX',nome)

        print("\nGravar novas informações na base de dados. \n Obrigado por me ensinar"+novasInfos)
        with open("../ds/minhaBD.pl", "a") as fp:
            fp.seek(0,0)
            fp.write(novasInfos)



elif(op=='consultar'):
    listaResultado = []
    print("\n Digite sua query de busca")
    pergunta = input()

    q = list(motor.query(pergunta))
    print(len(q))
    pprint(q)
    print(q[0]['X'])
    listaResultado = list([d['X'] for d in q])

    print(listaResultado)