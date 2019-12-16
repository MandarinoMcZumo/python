import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import seaborn as sns
import altair as alt
from functions import nans, drop_nans, nans_row_index, nans_per_row, representative

sns.set(style='darkgrid')

dt_train = pd.read_csv('train.csv')
dt_test = pd.read_csv('test.csv')

# Hay 81 columnas en el dataset, vamos a evaluar tanto % de nans, outliers, correlaciones...
# dt_train.dtypes

# NaNs
# plt.figure(figsize=(15, 8))
# sns.barplot(nans(dt_train)['index'], nans(dt_train)['%_nans'])
# plt.xticks(rotation=45)
# plt.title('Nans train')
# plt.show()

# plt.figure(figsize=(15, 8))
# sns.barplot(nans(dt_test)['index'], nans(dt_test)['%_nans'])
# plt.xticks(rotation=45)
# plt.title('Nans test')
# plt.show()

# Variables como 'Alley', 'PoolQC', 'Fence' o 'MiscFeature' tienen un % de nans muy alto
# Llenamos los NaN's de la variable Alley, Fence y Misc con una nueva categoría ('NO')

no = ['Alley', 'Fence', 'MiscFeature']
for i in no:
    dt_train[i].fillna('NO', inplace=True)
    dt_test[i].fillna('NO', inplace=True)

dt_train = drop_nans(dt_train, 0.5)
# plt.figure(figsize=(15, 8))
# sns.barplot(nans(dt_train)['index'], nans(dt_train)['%_nans'])
# plt.xticks(rotation=45)
# plt.title('Nans')
# plt.show()

dt_test = drop_nans(dt_test, 0.51)
# plt.figure(figsize=(15, 8))
# sns.barplot(nans(dt_test)['index'], nans(dt_test)['%_nans'])
# plt.xticks(rotation=45)
# plt.title('Nans')
# plt.show()

# ---------------------------------------------------------------------------------
# Gráfico de distribución de LotFrontage vinculado al precio:
# pts = alt.selection(type="interval", encodings=["x"])
# chrt = alt.Chart(dt_train).mark_bar().encode(x='LotFrontage',
#                                        y='count(LotFrontage)',
#                                        tooltip='count(LotFrontage)'
#                                        ).transform_filter(pts).properties(width=600, height=450).interactive()

# chrt2 = alt.Chart(dt_train).mark_point().encode(x='LotFrontage',
#                                           y='SalePrice:Q',
#                                           tooltip='SalePrice:Q'
#                                           ).properties(width=600, height=450).add_selection(pts)
# alt.hconcat(chrt, chrt2).display()
# ---------------------------------------------------------------------------------

# Observo que hay dos observaciones muy por encima de la media y que no están correlacionadas con la variable objetivo,
# las expulso del dataset

outlier = dt_train.LotFrontage.max()
out_index = list(dt_train.loc[dt_train['LotFrontage'] == outlier].index)
dt_train = dt_train.drop(out_index, axis=0)

# Quedan 259 NaN's en LotFrontage, vamos a asignarles el valor 0 asumiendo que son pisos interiores
dt_train.LotFrontage.fillna(0, inplace=True)
dt_test.LotFrontage.fillna(0, inplace=True)

# Ahora vamos a tratar la variable FireplaceQu (calidad de la chimenea)
# La cantidad de NaNs corresponde a que para las casas sin chimenea se ha dejado el valor en blanco
# Creamos una variable que resulta de multiplicar el número de chimeneas por un valor de 0 a 5

for c, i in enumerate(list(dt_train.FireplaceQu.value_counts().index)):
    dt_train['FireplaceQu'] = dt_train['FireplaceQu'].apply(lambda x: c + 1 if x == i else x)

for c, i in enumerate(list(dt_test.FireplaceQu.value_counts().index)):
    dt_test['FireplaceQu'] = dt_test['FireplaceQu'].apply(lambda x: c + 1 if x == i else x)

dt_train['FireplaceQu'].fillna(0, inplace=True)
dt_test['FireplaceQu'].fillna(0, inplace=True)

dt_train['FireplaceT'] = dt_train['Fireplaces'] * dt_train['FireplaceQu']
dt_test['FireplaceT'] = dt_test['Fireplaces'] * dt_test['FireplaceQu']

dt_train.drop(['Fireplaces', 'FireplaceQu'], axis=1, inplace=True)
dt_test.drop(['Fireplaces', 'FireplaceQu'], axis=1, inplace=True)

# Ninguna variable tiene más de un 10% de nans, veamos cuántas observaciones totales eliminaríamos en caso de quitarlas:
# len(nans_row_index(dt_train)) / len(dt_train)
# len(nans_row_index(dt_test)) / len(dt_test)

# Eliminaríamos cerca de un 10% de la información, vamos a intentar dar tratamiento para mantener información
# A través de la función nans_per_row vemos cuántos nans hay por fila

# nans_per_row(dt_test)['NaNs_Ammount'].value_counts()
# nans_per_row(dt_train)['NaNs_Ammount'].value_counts()

# Hay al menos 5 variables muy correlacionadas la mayor parte de filas con nans tiene 5 variables

# msno.matrix(dt_train)
# msno.matrix(dt_test)

# msno.heatmap(dt_train)
# msno.heatmap(dt_test)

# Todas la variables de atributos del garage o del sótano están correlacionadas.
# Los nans corresponden a las casas sin garage o sin sótano, vamos a crear una categoría para ellas

for i in dt_train.columns:
    if i.startswith('Bsmt') or i.startswith('Garage'):
        dt_train[i].fillna('NO', inplace=True)
        dt_test.fillna('NO', inplace=True)

# Las variables MasVnrType y MasVnrArea tienen los mismos NaNs.
# Son pocas filas y no tenemos forma de aproximar la información, las descartamos
dt_train.drop(list(nans_per_row(dt_train).index), axis=0, inplace=True)

# Dividimos las variables entre contínuas y categóricas
categoricas = []
numericas = []
for i in dt_train.columns:
    if dt_train.dtypes.loc[i] == 'object':
        categoricas.append(i)
    else:
        numericas.append(i)

# Ploteo de las variables categóricas
dt_cat = dt_train[categoricas]

# graph = []
# color_= alt.Color('count()', scale=alt.Scale(scheme='darkmulti'))

# for i in range(0, len(categoricas), 7):
#     g1 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i], type='nominal'),
#                                    alt.Y(categoricas[i], type='nominal', aggregate='count'), color=color_)
#     g2 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 1], type='nominal'),
#                                    alt.Y(categoricas[i + 1], type='nominal', aggregate='count'), color=color_)
#     g3 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 2], type='nominal'),
#                                    alt.Y(categoricas[i + 2], type='nominal', aggregate='count'), color=color_)  
#     g4 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 3], type='nominal'),
#                                    alt.Y(categoricas[i + 3], type='nominal', aggregate='count'), color=color_)
#     g5 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 4], type='nominal'),
#                                    alt.Y(categoricas[i + 4], type='nominal', aggregate='count'), color=color_)
#     g6 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 5], type='nominal'),
#                                    alt.Y(categoricas[i + 5], type='nominal', aggregate='count'), color=color_)
#     g7 = alt.Chart(dt_cat).mark_bar().encode(alt.X(categoricas[i + 6], type='nominal'),
#                                    alt.Y(categoricas[i + 6], type='nominal', aggregate='count'), color=color_)
    
#     alt.hconcat(g1, g2, g3, g4, g5, g6).display()

# Vemos las variables sin representación y las agrupamos:
rep, unq = representative(dt_cat, 0.02)
rep.head()

# Mediante unaa agrupación del dataset ordenado sacamos el índice en forma de lista y lo subdividimos en las zonas:
nbhoods = list(dt_train[['Neighborhood', 'SalePrice']].groupby(['Neighborhood']).mean().sort_values(by='SalePrice', ascending=False).index)
nbhoods_A = nbhoods[:3]
nbhoods_B = nbhoods[3:13]
nbhoods_C = nbhoods[13:22]
nbhoods_D = nbhoods[-3:]

# Definimos el bucle para crear la nueva variable:
dt_train['Areas'] = dt_train['Neighborhood'].apply(lambda x: 'A' if x in nbhoods_A else 'B' if x in nbhoods_B else 'C' if x in nbhoods_C else 'D')
dt_test['Areas'] = dt_test['Neighborhood'].apply(lambda x: 'A' if x in nbhoods_A else 'B' if x in nbhoods_B else 'C' if x in nbhoods_C else 'D')

dt_train.drop('Neighborhood', axis=1, inplace=True)

# Actualizamos la lista de categóricas y numéricas ya que hay nuevas variables a tener en cuenta:
categoricas = []
numericas = []
for i in dt_train.columns:
    if dt_train.dtypes.loc[i] == 'object':
        categoricas.append(i)
    else:
        numericas.append(i)

dt_cat = dt_train[categoricas]
        
rep, unq = representative(dt_cat, 0.05)

# Aplicamos la agrupación de categorías con baja representación
# Aplicamos el bucle de la agrupación de categorías con baja representación:

for i in range(len(rep)):
    feature = rep['var'].iloc[i]
    dt_train[feature] = dt_train[feature].apply(lambda x: 'grouped_' + feature if x == rep['value'].iloc[i] else x)
    dt_test[feature] = dt_test[feature].apply(lambda x: 'grouped_' + feature if x == rep['value'].iloc[i] else x) 