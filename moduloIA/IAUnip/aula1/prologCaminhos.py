from pyswip import Prolog
prolog = Prolog()




prolog.assertz("gosta(maria,flores)")
prolog.assertz("gosta(maria,pedro)")
prolog.assertz("gosta(pedro,flores)")

res = list(prolog.query("gosta(maria,X)"))
print(res)
prolog.assertz("ligacao(birigui,aracatuba)")
prolog.assertz("ligacao(birigui,bilac)")
prolog.assertz("ligacao(bilac,ocz)")
prolog.assertz("caminho(X,Z) :- ligacao(X,Y),caminho(Y,Z)")


res2 = list(prolog.query("caminho(birigui,X)"))
print(res2)



res3 =  list(prolog.query("caminho(birigui,joaopessoa)"))
print(res3)

#
#
# #
# for resultado in prolog.query('ligacao(aracatuba, lins)'):
#     print(resultado[''])
#     # print(resultado)