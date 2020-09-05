import sys
import re

regex = r"[-'a-zA-ZÀ-ÖØ-öø-ÿ0-9]+"   # raw string

if __name__ == '__main__':
    fileName = sys.argv[1]

    # leitura do documento
    document = open(fileName,'r')
    content  = document.read()

    # identificacao de palavras
    words       = re.findall(regex, content)
    frequencies = dict([])

    # quantidade de vezes no documento
    for w in words:
        w = w.lower()
        if w not in frequencies:
            frequencies[w] = 0
        frequencies[w] += 1
    print (f"Tokens: {len(words)}, Vocabulario: {len(frequencies)}")

    # imprimir as 20 palavras mais frequentes
    fs = sorted(frequencies, key=frequencies.get, reverse=True)
    for i in range(0,20):
        print (f"--> {frequencies[fs[i]]} {fs[i]}")








