import matplotlib.pyplot as plt
import missingno as msno
import pandas as pd
import seaborn as sns

from functions import nans, drop_nans, nans_row_index, nans_per_row

sns.set(style='darkgrid')

dt_train = pd.read_csv('train.csv')
dt_test = pd.read_csv('test.csv')

# Hay 81 columnas en el dataset, vamos a evaluar tanto % de nans, outliers, correlaciones...
dt_train.dtypes

# NaNs
plt.figure(figsize=(15, 8))
sns.barplot(nans(dt_train)['index'], nans(dt_train)['%_nans'])
plt.xticks(rotation=45)
plt.title('Nans train')
plt.show()

plt.figure(figsize=(15, 8))
sns.barplot(nans(dt_test)['index'], nans(dt_test)['%_nans'])
plt.xticks(rotation=45)
plt.title('Nans test')
plt.show()

# Variables como 'Alley', 'PoolQC', 'Fence' o 'MiscFeature' tienen un % de nans muy alto
# Llenamos los NaN's de la variable Alley, Fence y Misc con una nueva categoría ('NO')

no = ['Alley', 'Fence', 'MiscFeature']
for i in no:
    dt_train[i].fillna('NO', inplace=True)
    dt_test[i].fillna('NO', inplace=True)

dt = drop_nans(dt_train, 0.5)
plt.figure(figsize=(15, 8))
sns.barplot(nans(dt)['index'], nans(dt)['%_nans'])
plt.xticks(rotation=45)
plt.title('Nans')
plt.show()

dt_test = drop_nans(dt_test, 0.51)
plt.figure(figsize=(15, 8))
sns.barplot(nans(dt_test)['index'], nans(dt_test)['%_nans'])
plt.xticks(rotation=45)
plt.title('Nans')
plt.show()

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

outlier = dt.LotFrontage.max()
out_index = list(dt.loc[dt['LotFrontage'] == outlier].index)
dt = dt.drop(out_index, axis=0)
dt_test = dt_test.drop(out_index, axis=0)

# Quedan 259 NaN's en LotFrontage, vamos a asignarles el valor 0 asumiendo que son pisos interiores
dt.LotFrontage.fillna(0, inplace=True)
dt_test.LotFrontage.fillna(0, inplace=True)

# Ahora vamos a tratar la variable FireplaceQu (calidad de la chimenea)
# La cantidad de NaNs corresponde a que para las casas sin chimenea se ha dejado el valor en blanco
# Creamos una variable que resulta de multiplicar el número de chimeneas por un valor de 0 a 5

for c, i in enumerate(list(dt.FireplaceQu.value_counts().index)):
    dt['FireplaceQu'] = dt['FireplaceQu'].apply(lambda x: c + 1 if x == i else x)

for c, i in enumerate(list(dt_test.FireplaceQu.value_counts().index)):
    dt_test['FireplaceQu'] = dt_test['FireplaceQu'].apply(lambda x: c + 1 if x == i else x)

dt['FireplaceQu'].fillna(0, inplace=True)
dt_test['FireplaceQu'].fillna(0, inplace=True)

dt['FireplaceT'] = dt['Fireplaces'] * dt['FireplaceQu']
dt_test['FireplaceT'] = dt_test['Fireplaces'] * dt_test['FireplaceQu']

dt.drop(['Fireplaces', 'FireplaceQu'], axis=1, inplace=True)
dt_test.drop(['Fireplaces', 'FireplaceQu'], axis=1, inplace=True)

# Ninguna variable tiene más de un 10% de nans, veamos cuántas observaciones totales eliminaríamos en caso de quitarlas:
len(nans_row_index(dt)) / len(dt)
len(nans_row_index(dt_test)) / len(dt_test)

# Eliminaríamos cerca de un 10% de la información, vamos a intentar dar tratamiento para mantener información
# A través de la función nans_per_row vemos cuántos nans hay por fila

nans_per_row(dt_test)['NaNs_Ammount'].value_counts()
nans_per_row(dt)['NaNs_Ammount'].value_counts()

# Hay al menos 5 variables muy correlacionadas la mayor parte de filas con nans tiene 5 variables

msno.matrix(dt)
msno.matrix(dt_test)

msno.heatmap(dt)
msno.heatmap(dt_test)

# Todas la variables de atributos del garage o del sótano están correlacionadas.
# Los nans corresponden a las casas sin garage o sin sótano, vamos a crear una categoría para ellas

for i in dt.columns:
    if i.startswith('Bsmt') or i.startswith('Garage'):
        dt[i].fillna('NO', inplace=True)
        dt_test.fillna('NO', inplace=True)

# Las variables MasVnrType y MasVnrArea tienen los mismos NaNs.
# Son pocas filas y no tenemos forma de aproximar la información, las descartamos

dt.drop(list(nans_per_row(dt).index), axis=0, inplace=True)

# Ahora que no tenemos NaNs, vamos a observar los outliers para cada variable,

categoricas = []
numericas = []
for i in dt.columns:
    if dt.dtypes.loc[i] == 'object':
        categoricas.append(i)
    else:
        numericas.append(i)

for i in numericas:
    sns.distplot(dt[i])
    plt.title(i)
    plt.show()

for i in categoricas:
    sns.countplot(dt[i])
    plt.title(i)
    plt.show()
