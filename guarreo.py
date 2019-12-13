import pandas as pd
elem = zip(*[('a', 1), ('b', 2), ('c', 3), ('d', 4)])

objeto = [((1, 2), (3, 4)),
          ((4, 5), (6, 7)),
          ((7, 8), (9, 10)),
          ((10, 11), (12, 13)),
          ((13, 14), (15, 16)),
          ((16, 17), (18, 19))]

resultado = []
for tupla in objeto:
    for elem in tupla:
        resultado.append(elem[0])

resultado


diccionario = {}
for i in range(len(objeto)):
    datos = {}
    for tupla in objeto[i]:
        datos.update({
            tupla[0]: tupla[1]
        })
    diccionario.update({i: datos})


dataframe = pd.DataFrame(diccionario).T

