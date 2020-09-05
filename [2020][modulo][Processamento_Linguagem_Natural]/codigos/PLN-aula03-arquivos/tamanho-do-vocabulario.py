# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"[-'a-zA-ZÀ-ÖØ-öø-ÿ]+"

test_str = ("A capivara (nome científico: Hydrochoerus hydrochaeris) é uma espécie de mamífero roedor da família Caviidae e subfamília Hydrochoerinae. Alguns autores consideram que deva ser classificada em uma família própria. Está incluída no mesmo grupo de roedores ao qual se classificam as pacas, cutias, os preás e o porquinho-da-índia. Ocorre por toda a América do Sul ao leste dos Andes em habitats associados a rios, lagos e pântanos, do nível do mar até 1 300 m de altitude. Extremamente adaptável, pode ocorrer em ambientes altamente alterados pelo ser humano. (d'água)\n"
	"É o maior roedor do mundo, pesando até 91 kg e medindo até 1,2 m de comprimento e 60 cm de altura. A pelagem é densa, de cor avermelhada a marrom escuro. É possível distinguir os machos por conta da presença de uma glândula proeminente no focinho apesar do dimorfismo sexual não ser aparente. Existe uma série de adaptações no sistema digestório à herbivoria, principalmente no ceco. Alcança a maturidade sexual com cerca de 1,5 ano de idade, e as fêmeas dão à luz geralmente a quatro filhotes por vez, pesando até 1,5 kg e já nascem com pelos e dentição permanente. Em cativeiro, pode viver até 12 anos de idade.")

matches = re.finditer(regex, test_str)

V = set([])

for (i, match) in enumerate(matches):
    print (f"Palavra {i} foi identificada nas posições {match.start()}-{match.end()}: {match.group()}")
    V.add(match.group())
    

print (f"V={len(V)}, N={i+1}")
