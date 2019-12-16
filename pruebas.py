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

## test función representación
val = 0.05
result = {}
rep = []
for i in dt_train[categoricas]:
    result.update({i: dt_train[i].value_counts()/len(dt_train)})

for key in result:
    for cc, i in enumerate(result[key]):
        if i<=val:
            rep.append([key, result[key].keys()[cc], result[key][cc]])
            
rep = pd.DataFrame(rep)
rep.columns = ['var', 'value', '%']
resumen = rep[['var', '%']].groupby('var').count()
rep['count'] = rep['var'].apply(lambda x: resumen.loc[x, '%'])
rep[rep['count']!=1]
rep[rep['count']==1]



for i in range(0, len(categoricas) - 2, 6):
    g1 = alt.Chart(dt_train).mark_bar().encode(alt.X(categoricas[i], type='nominal'),
                                   alt.Y(categoricas[i], type='nominal', aggregate='count'), color=color_).properties(width=180)
    g2 = alt.Chart(dt_train).mark_bar().encode(alt.X(categoricas[i + 1], type='nominal'),
                                   alt.Y(categoricas[i + 1], type='nominal', aggregate='count'), color=color_).properties(width=180)
    g3 = alt.Chart(dt_train).mark_bar().encode(alt.X(categoricas[i + 2], type='nominal'),
                                   alt.Y(categoricas[i + 2], type='nominal', aggregate='count'), color=color_).properties(width=180)  
    g4 = alt.Chart(dt_train).mark_bar().encode(alt.X(categoricas[i + 3], type='nominal'),
                                   alt.Y(categoricas[i + 3], type='nominal', aggregate='count'), color=color_).properties(width=180)
    g5 = alt.Chart(dt_train).mark_bar().encode(alt.X(categoricas[i + 4], type='nominal'),
                                   alt.Y(categoricas[i + 4], type='nominal', aggregate='count'), color=color_).properties(width=180)
    g6 = alt.Chart(dt_train).mark_bar().encode(alt.X(categoricas[i + 5], type='nominal'),
                                   alt.Y(categoricas[i + 5], type='nominal', aggregate='count'), color=color_).properties(width=180)

    alt.hconcat(g1, g2, g3, g4, g5, g6).display()

g7 = alt.Chart(dt_train).mark_bar().encode(alt.X(categoricas[-2], type='nominal'),
                                   alt.Y(categoricas[-2], type='nominal', aggregate='count'), color=color_).properties(width=180)
g8 = alt.Chart(dt_train).mark_bar().encode(alt.X(categoricas[-1], type='nominal'),
                                   alt.Y(categoricas[-1], type='nominal', aggregate='count'), color=color_).properties(width=180)