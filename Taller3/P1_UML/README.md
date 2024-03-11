# WorkShop-USFQ
## Taller 3 de inteligencia artificial

- **Nombre del grupo**: Grupo 1
- **Integrantes del grupo**:
  * Kuntur: 

### USO DE APRENDIZAJE NO SUPERVISADO

Para el presente estudio se usa el dataset en [https://github.com/Borreguin/WorkShop1-USFQ](https://github.com/Borreguin/WorkShop1-USFQ) que tiene 4 varaibles y su descripción se presenta a continuación:

| Tag_name  | Alias | Descripción |
|--------------|--------------|--------------|
| *V005_vent01_CO2* | *CO2 Ventilation NE* | Cantidad de CO2 en ppm de la salida del sistema de ventilación en la parte Norte Este |
| *V022_vent02_CO2* | *CO2 Ventilation SW* | Cantidad de CO2 en ppm de la salida del sistema de ventilación en la parte Sur Oeste |
| *V006_vent01_temp_out* | *Temp. Vent. NE Out* | Temperatura de salida del sistema de ventilación en $^oC de$ la parte Norte Este |
| *V023_vent02_temp_out* | *Temp. Vent. SW Out* | Temperatura de salida del sistema de ventilación en C de la parte Sur Oeste |

#### A. Plotear Variables

Para cada variable se presenta un gráfico de box plot con sus valores superpuestos de horas por dia.

![Boxplot_V005_vent01_CO2](graficas\\Boxplot_V005_vent01_CO2.png)
![Boxplot_V006_vent01_temp_out](graficas\\Boxplot_V006_vent01_temp_out.png)
![Boxplot_V022_vent02_CO2](graficas\\Boxplot_V022_vent02_CO2.png)
![Boxplot_V023_vent02_temp_out](graficas\\Boxplot_V023_vent02_temp_out.png)

En los boxplot se puede ver que existe algun patrón por horas, además que en algunas horas existen valores con anomalías, por eso realizaremos un análisis univariable y multivariable para ver los patrones y anomalías de los datos.

#### B. Patrones - Análisis univariable

Para realizar el análisis univariado, se observa que los datos tienen valores vacios, específicamente las columnas `Boxplot_V006_vent01_temp_out` y  `Boxplot_V023_vent02_temp_out`, tiene un valor vacío cada una, por lo que se decide rellenar el valor vacío con la media de cada columna. 

Después se realiza el modelo de kmeans en cada variable para encontrar patrones diarios en los datos. Primero se analiza con el método del codo cual sería la mejor agrupacion por variables obteniendo los siguientes resultados.

![elbow_method_univariable](graficas\\elbow_method_univariable.png)

Como se puede ver en la gráfica para las columnas del ventilador 01, el método sugiere k=3, y para las columnas del ventilador 02 el método sugiere k=2, por lo que se realizó esta agrupación obteniendo los resultados a continuación.

![kmeans_method_univariable](graficas\\kmeans_method_univariable.png)

Como se puede ver es difícil ver los patrones de la segmentación propuesta por kmeans, porque cada día es un eje en el espacio multidimensional, por ejemplo para la salida de temperatura del ventilador 01, tenemos la hora 19 cerca de un centroide que no es de su grupo, por esta razón vamos a realizar la técnica de PCA (análisis de componenetes principales) para visualizar todos los días en una sola gráfica de 2 dimensiones:

Las sigueintes gráficas representa el método de codo con la segmentación de kmenas para cada variable utilizando la técnica de PCA.

![elbow_method_univariable_pca](graficas\\elbow_method_univariable.png)
![kmeans_method_univariable_pca](graficas\\kmeans_method_univariable.png)

Con la técnica de PCA se puede visualizar una mejor agrupación, donde cada grupo se encuentra alrededor de su propio centroide, sin embargo aún tenemos algunos puntos alejados de sus centroidos por lo que posiblemente sean anomalías, por eso con el rango intercuartilico hallaremos los valores atípicos.

#### C. Anomalías – Análisis univariable

Según el rango intercuartilico de cada grupo tenemos las siguinetes anomalías:

| hours |	PC1 |	PC2 |	variables |
|--------------|--------------|--------------|--------------|
| 8 |	-4.278174 |	-9.823595 |	vent_01_co2 |
| 17 | 20.814538 | 8.980539 | vent_01_co2 |
|	8 |	4.343456 | -12.591591 | vent_02_co2 |
| 18 | -25.400655 |	21.250618 |	vent_01_temp |
| 19 | -2.045363 | 26.104500 | vent_01_temp |

Como vimos en la gráfica de cluster con PCA los valores más alejados de sus centros son anomalías detectadas por el rango intercuartil, el único punto que se visualiza alejado de su centroido es la hora 19 en la salida de la temperatura del ventilador 02 no se detecta como una anomalía, esto es debido a que los puntos de ese grupo se encuentran en una buena distribución que indican que la hora 19 a pesar de estar distanciada de su centroide si pertenezca a su distribución.

#### D Patrones – Análisis multivariable

Para el EDA, es importante un análisis multivariado, por lo que combinaremos las variables del ventilador 01 y ventilador 02 para el método de kmeans, obteniendo los siguientes resultados.

![elbow_method_bivariable](graficas\\elbow_method_univariable.png)
![kmeans_method_bivariable](graficas\\kmeans_method_univariable.png)

Como se puede ver cuando se juntan las columnas de CO2 y temperatura de cada ventilador obtenemos otros patrones de los datos, por lo que el método de kmeans sugiere agrupar con k=4, y resulta mas difícil ver para una gráfica de 2 dimensiones. Por lo que realizando la técnica de PCA podemos obtener nuevos patrones que no visualizamos antes.

Ahora aplicamos la técnica del PCA para el análisis multivariable, obteniendo los resultados siguientes.

![elbow_method_bivariable_pca](graficas\\elbow_method_univariable.png)
![kmeans_method_bivariable_pca](graficas\\kmeans_method_univariable.png)

Como podemos ver en la gráfica parece que los puntos ya no estan alejados de sus centroidos, indicando una mejor agrupación, pero es necesario descartar las anomalías de este análisis.

#### Anomalías – Análisis multivariable


Según el rango intercuartilico de cada grupo tenemos las siguientes anomalias:

| hours	| PC1 |	PC2 |	variables |
|--------------|--------------|--------------|--------------|
| 18 | 15.071131 | 29.257638 | vent_01_NE |
|	18 | 10.529579 | 22.521862 | vent_02_SW |

Ahora tenemos menos anomalías en comparación con el análisis univariado, sin embargo tenemos un valor que es interesante analizarlo, la hora 18 del ventilador 01 parece que se encuentra mas cerca del centroide del grupo verde que del centroide del grupo morado, sin embargo eso no significa una mala segmentación esto puede deberse a la proyección multidimensional, porque si visualizaramos las múltiples dimensiones podría pasar que el punto 18 este más cerca a su grupo morado que al grupo verde, este es un problema de la tecnica PCA que tenemos que ser cuidadosos al momento de interpretar los datos.

#### Conclusiones

Basándonos en los hallazgos, parece haber una relación entre las partes Norte Este (NE) y Sur Oeste (SW) del edificio, ya que ambas muestran anomalías durante horas específicas del día.

Además, las anomalías detectadas en las áreas NE y SW muestran patrones similares en horarios, con puntos anómalos identificados a las 18 horas tanto en NE como en SW.  Esto sugiere una posible relación entre las anomalías en estas áreas y factores como la ocupación del edificio y el funcionamiento de los sistemas de aire acondicionado,  que también pueden influir en variables como el nivel de CO2 y la temperatura, como se refleja en el análisis de componentes principales.

En resumen, los patrones y anomalías encontradas mediante el análisis de componentes principales (PCA) combinado con técnicas de agrupación resaltan  la importancia de monitorear de cerca las condiciones ambientales en diferentes áreas del edificio durante distintos momentos del día.  Esto permite identificar y abordar rápidamente posibles problemas en los sistemas de ventilación, asegurando así un ambiente interior saludable  y confortable para los ocupantes.

Lo que podemos concluir al finalizar el análisis multivariado, es que los valores sí parecen tener una similitud entre los grupos de las horas del ventilador NE y el ventilador SW, a diferencia del grupo morado que a pesar de estar cerca de los mismos valores vemos que en el ventilador uno tiene más tendencia al componente principal 2, un siguiente análisis es ver que variables tienen peso en el eje del componenete principal 2. Sin embargo esta similaridad no se visualiza en el análisis univariado, esto puede deberse a que exista una correlación entre el CO2 y la temperatura de cada ventilador.

Ahora visualizamos el resultado del análisis en las series de los ventiladores obteniendo el siguiente resultado.

##### Cluster del Análisis univariado en data principal
![data_analisis_univariado_time](graficas\\data_analisis_univariado_time.png)
![data_analisis_univariado_hour](graficas\\data_analisis_univariado_hour.png)

##### Cluster del Análisis Multivariado en data principal
![data_analisis_bivariado_time](graficas\\data_analisis_bivariado_time.png)
![data_analisis_bivariado_hour](graficas\\data_analisis_bivariado_hour.png)