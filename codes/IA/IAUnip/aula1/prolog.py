from pyswip import Prolog
prolog = Prolog()
prolog.assertz("human(john)")
prolog.assertz("human(ana)")
prolog.assertz("human(cleber)")
prolog.assertz("human(joaquim)")
prolog.assertz("mulher(joana)")
prolog.assertz("mulher(ana)")
prolog.assertz("homem(john)")
prolog.assertz("homem(cleber)")
prolog.assertz("pai(john,ana)")
prolog.assertz("avo(X,Z) :- homem(X), pai(X,K),pai(K,Z)")


for resultado in prolog.query('avo(X,Y)'):
    print(resultado['X'])