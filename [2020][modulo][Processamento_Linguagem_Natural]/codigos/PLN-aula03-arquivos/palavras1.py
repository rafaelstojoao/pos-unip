import sys
import re

#regex = r"[-'a-zA-ZÀ-ÖØ-öø-ÿ]+"   # raw string
regex = r"[-'a-zA-ZÀ-ÖØ-öø-ÿ0-9]+"   # raw string


if __name__ == '__main__':
    fileName = sys.argv[1]

    document = open(fileName,'r')

    content  = document.read()
    # document.read()       # devolve o conteudo do arquivo 'fileName'
    # document.readline()   # devolve a seguinte linha do arquivo 'fileName'
    # document.readlines()  # devolve uma lista de linhas do arquivo 'fileName'


    words = re.findall(regex, content)
    for w in words:
        print (w)
    print (f"Quantidade de palavras: {len(words)}")   



