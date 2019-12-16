# Proyecto NEOLAND

<p align="center">
  <img width="200" height="200" src=https://media.licdn.com/dms/image/C4E0BAQFZHsiCPsJdbw/company-logo_200_200/0?e=2159024400&v=beta&t=8pdnYbDLVLg1U-oWWOO88CcokkgK0TAW8L-nLw4Tf3c>
</p>

## Modelo de predicción del valor de inmuebles

El proyecto consiste en el tratamiento de datos, exploración gráfica y la elaboración de un modelo capaz de predecir el valor de un inmueble dadas unas variables de entrada.

***

### _Secciones_

+ [Dataset](#dataset)
+ [Algoritmos](#algoritmos)
+ [Visualización](#visualización)
+ [Presentación y estructura](#presentación-y-estructura)
+ [Proyecto final (Google Colab)](https://colab.research.google.com/github/MandarinoMcZumo/python/blob/master/Proyecto_Housing.ipynb)

***

## Dataset

[enlace_datos]: https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data
[enlace_concurso]: https://www.kaggle.com/c/house-prices-advanced-regression-techniques/overview

El dataset propuesto lo podemos encontrar en [este enlace][enlace_datos]. Además de proporcionarnos los datos, [en Kaggle se encuentra actualmente vigente un concurso en el que participaremos][enlace_concurso], para evaluar cómo ha funcionado nuestro modelo frente a otros competidores.

***

## Algoritmos

[random_forest]: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
[linear_regression]: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html?highlight=linear%20regression#sklearn.linear_model.LinearRegression
[SVR]: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html?highlight=svr#sklearn.svm.SVR
[Neural]: https://keras.io/getting-started/sequential-model-guide/

Emplearemos los siguientes algoritmos para realizar un modelo:
+ [Random Forest][random_forest]
+ [Linear Regression][linear_regression]
+ [XGBoost](https://xgboost.readthedocs.io/en/latest/)
+ [Neural Network][Neural]
+ [SVR][SVR]

Además de probar distintos métodos tras realizar PCA en el dataset y evaluar si compensa realizar la reducción de variables ara obtener un mejor resultado.

***

## Visualización

[enlace_seaborn]: https://seaborn.pydata.org/
[enlace_altair]: https://altair-viz.github.io/index.html

Las librerías para visualización de gráficos empleadas serán [Seaborn][enlace_seaborn] y [Altair][enlace_altair], con esta última además crearemos una serie de gráficos interactivos que nos permitirán modificar los datos visualizados y ayudarnos a la comprensión de los mismos.

***

## Presentación y estructura

Todo el código se estructura en distintos scripts:
+ functions.py, donde almacenamos todas las partes del código recurrente en forma de funciones, de forma que eliminamos líneas redundantes y facilitamos la lectura del mismo.
+ data_treatment.py, donde realizamos el estudio del dataset y modificaciones correspondientes.
+ Proyecto_Housing.ipynb, donde dejaremos presentado en forma de cuaderno de Jupyter tanto los distintos informes gráficos como los resultados obtenidos.
