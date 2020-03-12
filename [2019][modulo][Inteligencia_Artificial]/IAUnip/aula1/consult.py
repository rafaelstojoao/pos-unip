from pyswip import Prolog

p = Prolog()

p.consult("ds/minhaBD.pl")

q =          list(p.query('filho(X,nao)')           )

print(len(q))



