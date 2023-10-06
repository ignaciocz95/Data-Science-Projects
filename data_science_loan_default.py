# -*- coding: utf-8 -*-
"""Data Science Loan Default.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10ggAHm_zcY-NQe8MszXfxGNHOWP3k-2r

# **Proyecto Loan Default - Curso Data Science 2023**

#Contexto

En el presente proyecto analizaremos un dataset que nos permitira identificar las probabilidades certeras si un prestamo sera defaulteado, entiendiendo default, como el no pago del prestamo. Mediante la utilizacion de Machine Learning, identificaremos ciertas variables que nos permitiran intentar predicir si un prestamo sera defaulteado

El dataset que utilizaremos en este proyecto fue obtenido de la pagina web Kaggle.

El link en el cual se podra obtener el dataset utilizado es el siguiente:

https://www.kaggle.com/datasets/joebeachcapital/loan-default

# Hipotesis del trabajo

Poder determinar, en base a los datos obtenidos, si un prestamo va a ser defaulteado o no con cierto grado de precision para de esta forma lograr prevenirlos y evitar perdidas de dinero.

# Carga del dataset
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
df = pd.DataFrame()
df = pd.read_csv ('/content/drive/MyDrive/Cursos/UTN/Data Science/Dataset/Anonymize_Loan_Default_data.csv', encoding="ISO-8859-1")

"""# Exploracion del Dataset"""

df.head(38480)

"""Informacion del Dataset"""

df.info()

"""Podemos identificar la existencia de 36 columnas en el dataset. El total de filas son 38480. En algunas columnas presentan datos nulos, aquellas que no llegan a 38480. En otras no presentan datos nulos. Aquellas columnas que presentan 38480 datos non-null.
Tambien podemos identificar 3 tipos de objetos en el dataset.
Object: presente en 14 columnas. Esto representa texto.
Float64: presente en 19 columnas. Esto representa numeros con decimales.
Int64: presente en 4 columnas. Esto representa numeros enteros'

Estadistica descriptiva
"""

df.describe()

"""En el cuadro anterior podemos observar en la primer fila, el numero total de valores no nulos de cada una de las columnas.
En el segundo renglon se presenta la media de cada una de las columnas. A partir de esto podemos determinar, por ejemplo que la media de la cantidad prestada es de 11094 dolares o que la tasa de interes media es de 12.16 % El tercer renglon representa el desvio estandard de cada una de las columnas.
Min, el cuarto renglon, representa el valor minimo de cada una de las columans. El valor minimo prestado es 0 dolares y por ende la tasa de interes tambien es de 0 %.
El quinto renglon representa el percentil 25 de cada una de las columnas. Un ejemplo para representar esto es la columna de 'total payment'. Esta muestra que el 25 % de la muestra paga menos de 5463 dolares. El sexto renglon representa el percentil 50 de cada una de las columnas. El 'total payment' asciende a casi el dolble, 9673 dolares. El septimo renglon representa el percentil 75 de cada una de las columnas. Esto se puede ver en la colmuna de la tasa de interes paga donde el 25 % de la poblacion que mayor prestamo tomo, paga una tasa de interes de; 14.7%.
El percentil se utiliza para obtener un valor el cual representa la proporcion de la serie de datos que queda debajo de cierto valor.
El ultimo renglon, el octavo, representa el maximo valor de la columna. Por ejemplo, el prestamo mas grande es de 35000 dolares.

Dimensiones del DataFrame
"""

df.shape

"""Nombres de las columnas"""

df.columns

"""Conteo de valores únicos en una columna"""

df['purpose'].value_counts()

"""Agrupación y promedio por valores únicos de una columna"""

df.groupby('purpose').mean()

"""Conteo de valores nulos en cada columna"""

df.isnull().sum()

"""# Preparacion y limpieza del dataset

Deteccion y gestion de datos faltantes
"""

# Datos no numericos por columna
non_numeric_cols = df.select_dtypes(exclude=['number']).columns
non_numeric_cols
df[non_numeric_cols].info()

"""El datset esta compuesto por 38480 filas algunas de las cuales estan compuestas por valores nulos.

Porcentaje de valores nulos por columna
"""

num_missing = df.isna().sum()

total_columns = df.shape[0]
percentage_missing = (num_missing / total_columns) * 100
print(percentage_missing)

"""# Eliminacion de columnas

Columnas con mas del 30 % de los datos faltantes
"""

columns_with_high_missing = num_missing[num_missing / len(df) > 0.30]
print(columns_with_high_missing)

df_cleaned = df.drop(columns=columns_with_high_missing.index)
print(df_cleaned)

"""Chequeo que ambas columnas fueron eliminadas"""

df_cleaned.shape

"""Pasamos de 37 columnas a 35, por lo tanto ambas columnas con un porcentaje de nulos mayores al 30 % fueron eliminadas del dataset. Aunque estas columnas aumentaban la cantidad de informacion disponible para analizar, el porcentaje de valores nulos hacia que las conclusiones que podemos llegar a sacar de estas era imprecisa y por lo tanto se decidio eliminarlas del dataset.

Identifico cual es el valor mas frecuente y uso este para reemplazar los valores nulos para que al analizar estos atributos del dataset no se vean afectadas las conclusiones.
"""

df_copy = df.copy()
most_freq = df_copy[non_numeric_cols].describe().loc['top']
most_freq
df_copy[non_numeric_cols] = df_copy[non_numeric_cols].fillna(most_freq)

"""# Deteción de datos duplicados

**Datos duplicados**
"""

df[df.duplicated()]

"""No hay filas duplicadas.

# Deteción y transformación de datos inconsistentes

Los datos inconsistentes, como por ejemplo los datos NaN, que estan presentes en el dataset seran eliminados mas adelante

# Visualización
"""

import seaborn as sns
import matplotlib.pyplot as plt

sns.scatterplot(
    x="annual_inc",
    y="loan_amnt",
    alpha=.3,
    data=df.sample(1000)
)

"""En el scatterplot se puede visualizar que existe una clara concentracion de datos en la parte superior izquierda. A pesar de la existencia de algunos outliers, se podria decir que es probable que exista una correlacion positiva entre los ingresos anuales mas bajos y la toma de prestamos, especialmente de cantidades inferiores a los 20 mil dolares. Esto puede visualizarse ya que se pueden apreciar la mayor cantidad de puntos entre los sueldos anuales inferiores a 100 mil dolares anuales y los prestamos inferiores a 20 mil dolares anuales"""

categoria_propositos = df['purpose'].value_counts() / len(df) * 100
categoria_propositos

plt.figure(figsize=(10, 5))
plt.bar(categoria_propositos.index, categoria_propositos.values)
plt.xlabel('Purpose')
plt.ylabel('Percentage')
plt.title('Propositos de prestamos')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""El grafico de barras muestra como claramente se puede ver que la mayoria de los prestamos son destinados a deuda y el pago de tarjeta de credito. Entre estos dos motivos se encuentran mas de la mitad de los motivos por los cuales los individuos toman un credito.
En menor cuantia se puede visualizar que los otros motivos, de forma descendente en proporsion, son: mejoras del hogar, alguna compra grande, para financiar un emprendimiento o negocio pequeño, por alguna cuestion relacionada al auto, para realizar un casamiento, por algun tema medico, por una mudanza, por la compra de una casa, para financiar educacion, vacaciones o para financiar la adquisicion de algun metodo de generacion de eneregia renovable.

# Modelos de Machine Learning

El tipo de modelo que se utilizara sera un modelo de aprendizaje supervisado. Utilizaremos este para poder identificar significatividad entre variable independientes y dependientes.
Tambien se utilizara el mismo para evitar que las variables utilizadas no esten correlacionadas. De esta forma evitaremos afirmar descubrimientos o confirmar hipotesis que deberian ser descartadas y no lo fueron por la correlacion de sus variables, es decir, evitar un error de tipo II
Dentro de los modelos de aprendizaje supervisado, el modelo que se utilizara sera el modelo de Regresion logistica. La decision de usar este tipo de modelo y no otro se basa principalmente en que la variable dependiente del modelo es una variable binaria, repay_fail. Esto significa que la variable adopta solo dos posibles valores, 0 y 1. Adopatar 0 cuando no se realiza el pago total del prestamo, adoptando 1 caso contrario.
"""

# Librerias utilizadas para el modelado
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

"""Intento de aplicar booleano"""

#Codificación de variables categoricas: no tienen un orden son categoricas nominales, las otras ordinales como el estado fisico y nivel de uso ya estan codificadas en numeros. Aca usamos ONE HOT
df_encoded = pd.get_dummies(df, columns=['emp_length', 'home_ownership', 'verification_status', 'last_credit_pull_d', 'last_pymnt_d', 'earliest_cr_line','issue_d', 'loan_status', 'purpose', 'zip_code', 'addr_state', 'revol_util'])

"""# Eliminacion de columnas object y filas con valores NaN"""

# Elimino porque no lo puedo convertir en valores que puedan interpretarse como dummy
df = df.drop(columns=['emp_length'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['home_ownership'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['verification_status'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['last_credit_pull_d'])

# Eliminado del dataset por presencia de valores NaN
df = df.drop(columns=['next_pymnt_d'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['last_pymnt_d'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['earliest_cr_line'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['issue_d'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['loan_status'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['purpose'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['zip_code'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['addr_state'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['revol_util'])

# Elimino porque no se lo puede convertir en una variable dummy
df = df.drop(columns=['Unnamed: 0'])

#Esta columna no esta presente en el dataset
df = df.drop(columns=['term'])

# Eliminado del dataset por presencia de valores NaN
df = df.drop(columns=['mths_since_last_delinq'])

#Elimino filas que contengan NaN
df = df.dropna()

df.shape

df.columns

"""# Division entre Train y Test set"""

X = df.iloc[1:37359,1:20].values
y = df.iloc[1:37359,20].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=0)

"""# Funcion Sigmoid"""

model = LogisticRegression()
model.fit(X_train,y_train)
lr_prediction = model.predict(X_test)

print("Prediccion",lr_prediction)
print("Etiquetas reales",y_test)

# Crear un DataFrame con las predicciones y las etiquetas reales
data = {'Predicción': lr_prediction, 'Etiquetas Reales': y_test}

# Crear un DataFrame para verificar si son iguales o diferentes
resultado = pd.DataFrame(data)

# Agregar una columna que indique si son iguales o diferentes
resultado['Comparación'] = resultado['Predicción'] == resultado['Etiquetas Reales']

# Imprimir el DataFrame
resultado.head()

resultado['Comparación'].value_counts()

print('Logistic Regression accuracy = ', metrics.accuracy_score(lr_prediction,y_test))

"""Tiene un 99.1% de precisión para clasificar

En el primer caso voy a usar un ejemplo presente en el dataset. En el seguno uno totalmente aleatorio. Realizo esto para comprobar que el modelo este gerenando predicciones certeras
"""

import numpy as np
# Supongamos que tienes nuevos ejemplos en una matriz X_nuevos
X_nuevos = np.array([[ 98954, 3500, 3500, 1025, 10.91, 114.44, 15000, 11.52, 0, 0, 8, 0, 3570, 9, 4139.500493, 1212.28, 3500, 609.5, 565.92],
                     [ 127463, 2400, 2400, 875, 15.96, 84.34, 23000, 15.86, 0, 2, 3, 0, 231, 3, 599.36, 218.08, 324.62, 180.59, 84.34],
                     [ 234027, 5000, 5000, 0.001123457, 14.82, 172.89, 42000, 18.51, 0, 8, 6, 0, 9792, 23, 1556, 0, 928.41, 454.55, 172.89]])

# Realiza predicciones en los nuevos ejemplos
predicciones_nuevos = model.predict(X_nuevos)

# Imprime las predicciones para los nuevos ejemplos
for i, prediccion in enumerate(predicciones_nuevos):
    print(f"Nuevo ejemplo {i + 1}: Predicción de precio = {prediccion:.2f}")

import numpy as np
# Supongamos que tienes nuevos ejemplos en una matriz X_nuevos
X_nuevos = np.array([[ 93454, 3700, 3700, 1925, 10.51, 454.44, 15450, 61.52, 0, 0, 4, 0, 3573, 30, 4239.500493, 1312.28, 3450, 639.5, 545.92],
                     [ 127423, 2490, 2490, 675, 55.96, 34.34, 23040, 65.86, 0, 1, 2, 0, 271, 2, 799.36, 118.08, 334.62, 190.59, 87.34],
                     [ 233427, 5030, 5030, 0.0013223457, 54.82, 672.89, 43000, 15.51, 0, 9, 5, 0, 9492, 93, 1356, 0, 924.41, 456.55, 182.89]])

# Realiza predicciones en los nuevos ejemplos
predicciones_nuevos = model.predict(X_nuevos)

# Imprime las predicciones para los nuevos ejemplos
for i, prediccion in enumerate(predicciones_nuevos):
    print(f"Nuevo ejemplo {i + 1}: Predicción de precio = {prediccion:.2f}")

"""# Metricas de evaluacion"""

from sklearn.metrics import mean_squared_error, r2_score

# Realizar predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Evaluar el rendimiento del modelo
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Error cuadrático medio (MSE): {mse}")
print(f"Coeficiente de determinación (R²): {r2}")

# Visualizar los coeficientes de la regresión
print("Coeficientes de la regresión:")
print(f"Intercepto: {model.intercept_}")
print(f"Coeficientes: {model.coef_}")

"""El coeficiente de determinacion (R2) muestra cuan bien se ajusta nuestro modelo a los datos. En este caso tenemos un buen R2. El coeficiente de determinacion de este modelo es del 93 %.
En relacion a los coeficientes del modelo, no hay coeficientes mayores a 1 que podrian considerarse medianamente altos.
El error cuadratico medio (MSE) mide el promedio de los errores al cuadrado, entendiendo al error como la diferencia entre el valor predicho y el valor original.
En este caso el error es 0.009. Es un error muy bajo
"""

# Matriz de Confusion
from sklearn.metrics import confusion_matrix
matriz = confusion_matrix(y_test, y_pred)
print(matriz)

"""Los valores de la diagonal principal representan los valores estimados correctamente por el modelo. Tanto los valores negativos a11 (9457) como los valores negativos b22 (1551).
La otra diagonal representa los valores en que el modelo se ha equivocado. Los falsos negativos o error de tipo II se encuentran en a12 (12) y los falsos positivos o error de tipo I en b12 (88).

"""

#Exactitud
from sklearn.metrics import accuracy_score
exactitud = accuracy_score(y_test, y_pred)
print(exactitud)

"""Esta metrica representa el porcentaje de predicciones correctas sobre el total de predicciones. Al tener un porcentaje tan alto, podria indicar que los datos estan poco equilibrados.
Es por eso que se pueden utilizar otras metricas de medicion como sensibilidad
"""

#Sensibilidad
from sklearn.metrics import recall_score
sensibilidad = recall_score(y_test, y_pred)
print(sensibilidad)

"""La sensibilidad representa la tasa de verdaderos positivos. Es la cantidad de positivos bien calificados por el modelo respecto al total de positivos.
Es decir, este modelo tiene una sensibilidad del 95 % que es lo mismo que decir que este modelo califica correctamente al 95 % de sus positivos.
"""

#Precision
from sklearn.metrics import precision_score
precision = precision_score(y_test, y_pred)
print(precision)

"""La precision del modelo hace referencia a cuan cercano es el valor predicho del valor real. En este caso particular, la predicion es del 99 %. El valor predicho es muy cercano al valor actual."""

#Puntaje de F1
from sklearn.metrics import f1_score
puntaje = f1_score(y_test, y_pred)
print(puntaje)

"""El puntaje F1 es el promedio ponderado de precision y la sensibilidad. Este puntaje tiene en cuenta no solo los falsos positivos sino tambien los falsos negativos, siendo asi una metrica mas completa.\
El puntaje F1 de este modelo es del 97 %.

# Conclusiones del modelo

El modelo de aprendizaje supervisado utilizado nos permite llegar a la conclusion si un prestamo va a ser defaulteado o no.
El modelo cuenta con resultados muy buenos en cuanto a las distintas metricas analizadas previamente.
El R2, el error cuadratico medio, la matriz de confusion, la exactitud, sensibilidad, presicion y puntaje F1, arrojan resultados muy optimistas en cuanto al funcionamiento del modelo y su capacidad predictora.
Alguna recomendacion o mejora a futuro para el modelo podria ser determinar cual de las distintas variables tiene mayor peso a la hora de determinar si un prestamo va a ser defaulteado o no. Con esto se podria iterar eliminando las de menor peso y ver si el modelo sigue manteniendo resultados similares en las metricas previamente mencionadas para de esta forma disminuir la cantidad de informacion necesaria para lograr un prediccion acertada.
La ventaja de lograr esto no solo es disminuir la cantidad de tiempo en el que modelo esta corriendo. Tambien en almacenamiento, ya que al necesitar menos datos, la cantidad de informacion necesaria es menor y por ende el espacio fisico y digital para almacenar tal informacion.
Por ultimo el tiempo tanto de los usuarios al completar la informacion y del individuo que procese tal informacion.
"""