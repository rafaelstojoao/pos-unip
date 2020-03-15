
##Algoritmo de regressão
##Duas entradas em X independentes para gerar um valor em Y
from sklearn import tree
X = [[0, 0], [1, 1], [1,2], [2,3], [4,9]]
Y = [0,1,1,2,2.4]
clf = tree.DecisionTreeRegressor()
clf = clf.fit(X, Y)
res = clf.predict([[2., 8.]])
print(res)


import matplotlib.pyplot as plt

plt.plot(X, label="Entrada")
plt.plot(Y, label="Regressão")
plt.legend()
plt.show()