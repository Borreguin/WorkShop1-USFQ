# WorkShop-USFQ
## Taller 3 de inteligencia artificial

- **Nombre del grupo**: G5
- **Integrantes del grupo**:
  * Felipe Toscano
  * José Asitimbay
  * Brayan Lechón
  * Christian Hernandez

**Participación en el taller:**
  * **Felipe Toscano**: Desarollo principal P1 
    del 
    literal A al C, apoyo en los literales D y E
  * **José Asitimbay**: Desarollo principal P1 
    literal D y E apoyo en la redaccion del readme
  * **Brayan Lechón**: Participacion en P1 
    literales A, D, E y F. Participacion en 
    estructuracion del directorio del 
    proyecto y redaccion del readme resultados P1.
  * **Christian Hernandez**: Desarollo y 
    redaccion de resultados del P2.

## GLPK package:
The GLPK (GNU Linear Programming Kit) package is intended for solving large-scale linear programming (LP), mixed integer programming (MIP), and other related problems. It is a set of routines written in ANSI C and organized in the form of a callable library.
This project uses this Linear Programming Kit to solve large-scale problems related to Logistics, the installation
depends on the Operating System:

Windows: https://winglpk.sourceforge.net/

Linux: apt-get install -y -qq glpk-utils

Mac:  brew install glpk

# 1. Uso de Aprendizaje no Supervisado

## A. Plotear las variables
Presentar un gráfico por cada variable que muestre sus valores superpuestos por cada día. Para propósito de explicación, la gráfica anterior muestra un ejemplo de una
2  variable de presencia solar que no corresponde a este set de datos, pero sirve de ilustración.
### CO2 Ventilación NE
**Grafico agrupado por dia y hora**
![](Taller3/P1_UML/images/CO2%20Ventilation%20NE_diario.png)
**Grafico agrupado por Semana del año vs Dia y Hora**
![](Taller3/P1_UML/images/CO2%20Ventilation%20NE_heatmap.png)

### C02 Ventilacion SW
**Grafico agrupado por dia y hora**
![](Taller3/P1_UML/images/CO2%20Ventilation%20SW_diario.png)
**Grafico agrupado por Semana del año vs Dia y Hora**
![](Taller3/P1_UML/images/CO2%20Ventilation%20SW_heatmap.png)

### Temperatura NE
**Grafico agrupado por dia y hora**
![](Taller3/P1_UML/images/Temp.%20Vent.%20NE%20Out_diario.png)
**Grafico agrupado por Semana del año vs Dia y Hora**
![](Taller3/P1_UML/images/Temp.%20Vent.%20NE%20Out_heatmap.png)

### Temperatura SW 
**Grafico agrupado por dia y hora**
![](Taller3/P1_UML/images/Temp.%20Vent.%20SW%20Out_diario.png)
**Grafico agrupado por Semana del año vs Dia y Hora**
![](Taller3/P1_UML/images/Temp.%20Vent.%20SW%20Out_heatmap.png)

## B. Encontrar patrones – análisis univariable
Utilizando cualquier técnica de aprendizaje no supervisado, encontrar los patrones diarios que existen en el data set, para cada variable individual. Utilizar al menos dos técnicas para verificar su consistencia entre las dos técnicas.

### CO2 Ventilación NE
![](Taller3/P1_UML/images/CO2%20Ventilation%20NE_clustered_heatmap.png)

### C02 Ventilacion SW
![](Taller3/P1_UML/images/CO2%20Ventilation%20SW_clustered_heatmap.png)


### Temperatura NE
![](Taller3/P1_UML/images/Temp.%20Vent.%20NE%20Out_clustered_heatmap.png)

### Temperatura SW
![](Taller3/P1_UML/images/Temp.%20Vent.%20SW%20Out_clustered_heatmap.png)

## C. Encontrar anomalías – análisis univariable
Es posible que ciertos perfiles diarios en el set de datos no pertenezcan a los patrones diarios descubiertos en el literal B. ¿Cómo detectarlos?
## D. Encontrar patrones – análisis multivariable
De manera similar al literal B, encontrar los patrones diarios que existen en el data set, para cada par de variables, es decir, las dos de la parte Norte Este y las dos de la parte Sur Oeste. Utilizar al menos dos técnicas para verificar su consistencia entre las dos técnicas.


### C02 Ventilacion NE vs Temperatura NE
![](Taller3/P1_UML/images/Temp.%20Vent.%20NE%20Out_vs_CO2%20Ventilation%20NE_weekday_cycle.png)

### C02 Ventilacion SW vs Temperatura SW
![](Taller3/P1_UML/images/Temp.%20Vent.%20SW%20Out_vs_CO2%20Ventilation%20SW_weekday_cycle.png)
## E. Encontrar anomalías – análisis multivariable
De manera similar al literal C, encontrar anomalías, pero de los dos pares de variables.

### C02 Ventilacion NE vs Temperatura NE
**Agrupacion por Hora**
![](Taller3/P1_UML/images/Cluster_V005_vent01_CO2_vs_V006_vent01_temp_out_hour.gif)
**Agrupacion por Dia de la Semana**
![](Taller3/P1_UML/images/Cluster_V005_vent01_CO2_vs_V006_vent01_temp_out_weekday.gif)

### C02 Ventilacion SW vs Temperatura SW
**Agrupacion por Hora**
![](Taller3/P1_UML/images/Cluster_V022_vent02_CO2_vs_V023_vent02_temp_out_hour.gif)

**Agrupacion por Dia de la Semana**
![](Taller3/P1_UML/images/Cluster_V022_vent02_CO2_vs_V023_vent02_temp_out_weekday.gif)


## F. Conclusiones
Se podrá encontrar alguna relación entre la parte Norte Este y Sur Oeste del edificio, ¿Qué pudieran sugerir los patrones y las anomalías encontradas?




## Investigacion Operativa

### Analiza el codigo propuesto

En la carpeta Taller3/P2_TSP se coloca el código del modelado del TSP usando LP, 
correr el caso 1, con una tolerancia de 0.20 y tiempo límite de 120 segundos, marcar los 
tiempos que se demora para 10, 20, 30, 40 y 50 ciudades. 
Subjetivamente, 
#### ¿qué tal te parece las soluciones que ha arrojado el modelo sin aplicar todavía una heurística que ayude al modelo? 

|    |   n_cities |   distance |   distancia_minima_nodos |   distancia_maxima_nodos |   distancia_promedio_nodos |   distancia_total_minima_posible |   distancia_total_maxima_posible |
|---:|-----------:|-----------:|-------------------------:|-------------------------:|---------------------------:|---------------------------------:|---------------------------------:|
|  0 |         10 |    570.7   |                13.8578   |                  196.88  |                    109.712 |                          216.246 |                          308.923 |
|  1 |         20 |    816.339 |                 3.80132  |                  231.421 |                    108.609 |                          373.766 |                          533.951 |
|  2 |         30 |    992.891 |                 3.00666  |                  231.762 |                    103.791 |                          541.997 |                          774.281 |
|  3 |         40 |   1230.5   |                 0.894427 |                  258.558 |                    107.687 |                          741.065 |                         1058.66  |
|  4 |         50 |   1316.64  |                 2.06155  |                  234.784 |                    114.33  |                          916.586 |                         1309.41  |


#### 10 ciudades
![](/Taller3/P2_TSP/images/SC1_10.png)

#### 20 ciudades
![](/Taller3/P2_TSP/images/SC1_20.png)

#### 30 ciudades
![](/Taller3/P2_TSP/images/SC1_30.png)

#### 40 ciudades
![](/Taller3/P2_TSP/images/SC1_40.png)

#### 50 ciudades
![](/Taller3/P2_TSP/images/SC1_50.png)

Las soluciones del modelo TSP sin heurísticas muestran un aumento lógico en la distancia total a medida que crece el número de ciudades, lo que es esperado. Para valorar la eficacia de estas 
soluciones, sería ideal compararlas contra soluciones heurísticas. Las heurísticas podrían ofrecer un buen equilibrio entre calidad de solución y eficiencia computacional.


### Analizar el parámetro tee 
 
El parámetro tee determina si los detalles de la ejecución del solver se imprimen en la consola. Con tee=True, se visualiza la salida del proceso de optimización; tee=False mantiene la operación 
en silencio, sin imprimir nada.

### Aplicar heurística de límites a la función objetivo 

|   distancia_minima_nodos |   distancia_maxima_nodos |   distancia_promedio_nodos |   distancia_total_minima_posible |   distancia_total_maxima_posible |   n_cities |   distance | with_heuristics   |
|-------------------------:|-------------------------:|---------------------------:|---------------------------------:|---------------------------------:|-----------:|-----------:|:------------------|
|                  2.1     |                  251.941 |                    106.548 |                          1121.79 |                          1602.56 |         70 |    1482.02 | False             |
|                  2.72029 |                  235.996 |                    109.339 |                          1235.45 |                          1764.93 |         70 |    1587.48 | True              |

#### USANDO HEURISTICA

![](/Taller3/P2_TSP/images/SC2_H.png)

#### SIN USAR HEURISTICA

![](/Taller3/P2_TSP/images/SC2_NO_H.png)


En este caso específico, la heurística no parece haber mejorado la solución del problema TSP. Esto podría deberse a la estructura específica del conjunto de datos o a que la heurística no está alineada con las características del problema. 
#### *¿Cuál es la diferencia entre los dos casos?* 

La diferencia entre los dos casos se manifiesta en la distancia total recorrida. Con heurística activa, la ruta es más larga (1587.48) comparada con la ruta sin heurística (1482.02). 
Esto sugiere que la heurística utilizada puede no estar optimizando la ruta de la manera esperada para este conjunto de datos.

#### *¿Sirve esta heurística para cualquier caso? ¿Cuál pudiera ser una razón?* 

No necesariamente todas las heurísticas son aplicables o mejoran el rendimiento en todos los casos. Una heurística que funciona bien en un conjunto de instancias puede no ser efectiva en otra, dependiendo de la naturaleza del problema y las características específicas de los datos. 
Por ejemplo, si la heurística está diseñada para favorecer conexiones cercanas y las ciudades están distribuidas de manera uniforme, puede que no ofrezca una ventaja significativa y podría llevar a soluciones que no son las optimas.


### Aplicar heurística de vecinos cercanos  

|   n_cities |   distance | with_heuristic   |   distancia_minima_nodos |   distancia_maxima_nodos |   distancia_promedio_nodos |   distancia_total_minima_posible |   distancia_total_maxima_posible |
|-----------:|-----------:|:-----------------|-------------------------:|-------------------------:|---------------------------:|---------------------------------:|---------------------------------:|
|        100 |    1915.74 | False            |                 0.894427 |                  268.63  |                    106.204 |                          1536.87 |                          2195.53 |
|        100 |    1702.73 | True             |                 2.06155  |                  254.005 |                    109.107 |                          1673.09 |                          2390.13 |

#### USANDO HEURISTICA

![](/Taller3/P2_TSP/images/SC3_H.png)

#### SIN USAR HEURISTICA

![](/Taller3/P2_TSP/images/SC3_NO_H.png)



#### *¿Cuál es la diferencia entre los dos casos?* 

La diferencia entre los dos casos es que la heurística 'vecino cercano' redujo la distancia total recorrida de 1915.74 a 1702.73. Esto indica que la heurística fue efectiva en este escenario particular, generando una ruta más corta.

#### *¿Sirve esta heurística para cualquier caso? ¿Cuál pudiera ser una razón?* 

No, esta heurística no necesariamente funcionará para todos los casos. Su efectividad puede variar según la disposición geográfica de las ciudades, la distribución de las distancias u otros factores o caracteristicas propios del problema o de la data.
En este caso, parece ser adecuada ya que logró una mejora significativa.


## Conclusiones

- Las heurísticas tienen un impacto notable en la solución del problema del viajante de comercio (TSP), donde pueden mejorar o deteriorar las soluciones en comparación con métodos que no utilizan heurísticas, lo que se evidencia en los diferentes casos de estudio analizados.
- La efectividad de las heurísticas puede variar según la naturaleza del problema y las características específicas de los datos, por lo que es importante evaluar su rendimiento en diferentes escenarios.
- la elección de la heurística más adecuada requiere un enfoque basado en el conocimiento profundo del problema y la experimentación para identificar la heurística que proporciona los mejores resultados para un conjunto de datos.
- Las heurísticas proporcionan un equilibrio valioso entre la precisión y la eficiencia computacional, permitiendo obtener soluciones aceptables en un tiempo razonable


