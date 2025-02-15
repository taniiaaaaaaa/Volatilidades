# -*- coding: utf-8 -*-
"""Calculo_Volatilidades.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QKPzq8mHiIWiv5b55gQkyKazAHxaUjo5
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import openpyxl

# Identificador
tickerV = ["AC.MX", "ALSEA.MX", "ALFAA.MX", "BBAJIOO.MX", "BIMBOA.MX", "CEMEXCPO.MX",
           "CHDRAUIB.MX", "FUNO11.MX", "GENTERA.MX", "GMEXICOB.MX", "GFINBURO.MX",
           "GFNORTEO.MX", "GMXT.MX", "KIMBERA.MX", "LACOMERUBC.MX",
           "PINFRA.MX", "SORIANAB.MX", "WALMEX.MX"]

# Fecha desde empleando la fecha actual menos 500 días
deD = (datetime.now() - timedelta(days=1080)).strftime('%Y-%m-%d')

# Fecha hasta, empleando la fecha actual en el sistema
hastaD = datetime.now().strftime('%Y-%m-%d')

# Descargando los datos
def descargar_datos(tickers, fx_rate, start, end, interval):
    # Descargar precios de las acciones
    precios_acciones = yf.download(tickers, start=start, end=end, interval=interval)

    # Descargar tasa de cambio
    precios_fx = yf.download(fx_rate, start=start, end=end, interval=interval)['Adj Close']

    # Calcular rendimientos
    rendimientos_acciones = precios_acciones['Adj Close'].pct_change().dropna()

    return precios_acciones, rendimientos_acciones, precios_fx

# Periodicidad de los datos
periodicidad = '1d'

# Descargando precios y rendimientos
precios_acciones, rendimientos_acciones, precios_fx = descargar_datos(tickerV, 'USDMXN=X', deD, hastaD, periodicidad)

rendimientos_acciones

"""##Volatilidad convencional"""

# En Python:
import statistics
# Se calcula la desviación estándar:
sigmas=[statistics.stdev(rendimientos_acciones[i]) for i in rendimientos_acciones.columns[1:]]
print(sigmas)

"""##volatilidad con suavizamineto exponencial

"""

import numpy as np
import pandas as pd

# Simulando un DataFrame con rendimientos de múltiples series
# Asumiendo que la columna 'Date' contiene las fechas y las demás columnas son rendimientos de diferentes activos
rendimientosEjemplo1 = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'AC.MX': np.random.randn(100),
    'ALFAA.MX' : np.random.randn(100),
    'BBAJIOO.MX': np.random.randn(100),
    'BIMBOA.MX': np.random.randn(100),
    'CEMEXCPO.MX': np.random.randn(100),
    'CHDRAUIB.MX': np.random.randn(100),
    'FUNO11.MX': np.random.randn(100),
    'GENTERA.MX': np.random.randn(100),
    'GMEXICOB.MX': np.random.randn(100),
    'GFINBURO.MX': np.random.randn(100),
    'GFNORTEO.MX': np.random.randn(100),
    'GMXT.MX': np.random.randn(100),
    'KIMBERA.MX': np.random.randn(100),
    'PINFRA.MX': np.random.randn(100),
    'SORIANAB.MX': np.random.randn(100),
    'WALMEX.MX': np.random.randn(100)
})

# Lambda con el valor deseado:
lambdaS = 0.98

# Inicializamos una lista para almacenar tablas suavizadas de cada columna de rendimientos
tablasSuavizadas = []

# Aplicamos el suavizamiento exponencial a cada columna de rendimientos, excepto la columna 'Date'
for col in rendimientosEjemplo1.columns[1:]:
    # Obtenemos la serie de rendimientos de la columna actual
    rendimientosIPC = rendimientosEjemplo1[col]

    # Generamos la secuencia de T a t0 (la más reciente a la más antigua)
    seqT = np.arange(rendimientosIPC.shape[0], 0, -1)

    # Elevamos lambdaS a la potencia de t-1
    lambdaT = lambdaS**seqT

    # Calculamos rendimientos cuadráticos suavizados
    rendimientosCuadraticos = (rendimientosIPC**2) * lambdaT
    rendimientosSuavizados = rendimientosCuadraticos * lambdaT

    # Creamos la tabla de salida para esta serie de rendimientos
    tablaSuavizada = pd.DataFrame({
        'Fecha': rendimientosEjemplo1['Date'],
        'Lambda': lambdaT,
        'Rendimientos Cuadráticos': rendimientosCuadraticos,
        'Rendimientos Suavizados': rendimientosSuavizados
    })

    # Añadimos el nombre del activo como un identificador en el DataFrame
    tablaSuavizada['Activo'] = col

    # Añadimos la tabla suavizada a la lista de tablas
    tablasSuavizadas.append(tablaSuavizada)

# Concatenamos todas las tablas suavizadas en un solo DataFrame
tablaSuavizamientoExponencial = pd.concat(tablasSuavizadas)

# Mostramos la tabla suavizada
print(tablaSuavizamientoExponencial)

import numpy as np
import pandas as pd

# Simulando un DataFrame con rendimientos de múltiples series
# Asumiendo que la columna 'Date' contiene las fechas y las demás columnas son rendimientos de diferentes activos
rendimientosEjemplo1 = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'AC.MX': np.random.randn(100),
    'ALFAA.MX' : np.random.randn(100),
    'BBAJIOO.MX': np.random.randn(100),
    'BIMBOA.MX': np.random.randn(100),
    'CEMEXCPO.MX': np.random.randn(100),
    'CHDRAUIB.MX': np.random.randn(100),
    'FUNO11.MX': np.random.randn(100),
    'GENTERA.MX': np.random.randn(100),
    'GMEXICOB.MX': np.random.randn(100),
    'GFINBURO.MX': np.random.randn(100),
    'GFNORTEO.MX': np.random.randn(100),
    'GMXT.MX': np.random.randn(100),
    'KIMBERA.MX': np.random.randn(100),
    'PINFRA.MX': np.random.randn(100),
    'SORIANAB.MX': np.random.randn(100),
    'WALMEX.MX': np.random.randn(100)
})

# Lambda con el valor deseado:
lambdaS = 0.95

# Inicializamos una lista para almacenar tablas suavizadas de cada columna de rendimientos
tablasSuavizadas = []

# Aplicamos el suavizamiento exponencial a cada columna de rendimientos, excepto la columna 'Date'
for col in rendimientosEjemplo1.columns[1:]:
    # Obtenemos la serie de rendimientos de la columna actual
    rendimientosIPC = rendimientosEjemplo1[col]

    # Generamos la secuencia de T a t0 (la más reciente a la más antigua)
    seqT = np.arange(rendimientosIPC.shape[0], 0, -1)

    # Elevamos lambdaS a la potencia de t-1
    lambdaT = lambdaS**seqT

    # Calculamos rendimientos cuadráticos suavizados
    rendimientosCuadraticos = (rendimientosIPC**2) * lambdaT
    rendimientosSuavizados = rendimientosCuadraticos * lambdaT

    # Creamos la tabla de salida para esta serie de rendimientos
    tablaSuavizada = pd.DataFrame({
        'Fecha': rendimientosEjemplo1['Date'],
        'Lambda': lambdaT,
        'Rendimientos Cuadráticos': rendimientosCuadraticos,
        'Rendimientos Suavizados': rendimientosSuavizados
    })

    # Añadimos el nombre del activo como un identificador en el DataFrame
    tablaSuavizada['Activo'] = col

    # Añadimos la tabla suavizada a la lista de tablas
    tablasSuavizadas.append(tablaSuavizada)

# Concatenamos todas las tablas suavizadas en un solo DataFrame
tablaSuavizamientoExponencial = pd.concat(tablasSuavizadas)

# Mostramos la tabla suavizada
print(tablaSuavizamientoExponencial)