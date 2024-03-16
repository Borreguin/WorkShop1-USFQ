# WorkShop-USFQ
## Taller 4 de inteligencia artificial

- **Nombre del grupo**: G5
- **Integrantes del grupo**:
  * Felipe Toscano
  * José Asitimbay
  * Brayan Lechón
  * Christian Hernandez

**Participación en el taller:**
  * **Felipe Toscano**: 
  * **José Asitimbay**: 
  * **Brayan Lechón**: 
  * **Christian Hernandez**: 


## ALGORTIMOS GENÉTICOS
El taller contine el código para la ejecución 
de un Algoritmo Genético, el objetivo de este algoritmo es llegar a generar la frase objetivo: “GA Workshop! USFQ” que tiene 17 letras. El
proceso de generación lo realizará a partir de 
una población de 100 frases aleatorias (individuos) de tamaño de 17 letras. Las poblaciones generadas deberán interactuar cada una
hasta llegar a producir la frase objetivo. Una 
vez alcanzado un individuo que sea igual a la frase objetivo, el algoritmo genético se detendrá.
Posibles resultados de ejecución:
1. El algoritmo llega a producir el individuo deseado en el número de interacciones que se le
ha definido, en este caso, el algoritmo ha convergido a una solución óptima.
2. El algoritmo no logra producir el individuo deseado en el número de interacciones que se
le ha definido, en este caso ocurren dos 
   situaciones: 
a) el algoritmo puede que este cerca del objetivo y le falta más iteraciones para llegar a una solución óptima, 
b) el algoritmo nunca puede converger y en lugar de acercarse al objetivo se aleja.



## Resolucion
1. Ejecute los dos casos de estudio y explique los resultados de ejecución de cada caso de
estudio.
2. ¿Cuál sería una posible explicación para que el caso 2 no finalice como lo hace el caso 1?
Revisar el archivo util.py función distance.
3. Realice una correcta implementación para 
   obtener la distancia/diferencia correcta entre dos individuos en el archivo util.py función distance.
4. ¿Sin alterar el parámetro de mutación mutation_rate, se puede implementar algo para
mejorar la convergencia y que esta sea más rápida? Implemente cualquier mejora que
permita una rápida convergencia. Pista: ¿Tal vez elegir de manera diferente los padres?
¿Realizar otro tipo de mutación o cruce?
5. Cree un nuevo caso de estudio 3. Altere el parámetro de mutación mutation_rate, ¿ha beneficiado en algo la convergencia? Qué valores son los más adecuados para este
parámetro. ¿Qué conclusión se puede obtener de este cambio?
6. Cree un nuevo caso de estudio 4. Altere el tamaño de la población, ¿es beneficioso o no
aumentar la población?
Como se puede observar que al aumentar la population vemos que el número de generaciones disminuye y converge más rápidamente.

![](Taller4/AlgoritmosGeneticos/images/population_vs_ngenerations.png)

Aquí vemos la performance en tiempo y número de generations para diferentes tamaños de población.


| population_size | n_generations | execution_time |
|-----------------|---------------|----------------|
|             100 |            93 |       0.159570 |
|             200 |           119 |       0.421872 |
|             300 |            36 |       0.197471 |
|             400 |            21 |       0.155585 |
|             500 |            20 |       0.176497 |
|             600 |            19 |       0.207475 |
|             700 |            16 |       0.200449 |
|             800 |            30 |       0.441833 |
|             900 |            22 |       0.367986 |


7. De todo lo aprendido, cree el caso de estudio definitivo (caso de estudio 5) el cual tiene lo
mejor de los ítems 4, 5, 6.


