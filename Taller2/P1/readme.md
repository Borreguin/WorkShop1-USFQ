# WorkShop1-USFQ
## Taller 2 de inteligencia artificial
## EJERCICIO 1

Nombre del grupo: Grupo-3

Integrantes del grupo:

Bryan Calisto
Daniel Marín
Bryan Núñez
Francisco Roh

Para este ejercicio se generaron grafos, en las cuales cada baldosa recorrible representa un nodo.

Se utilizó 3 algoritmos de busqueda para encontrar la ruta de salida de cada laberinto, estos son:
- BFS
- A estrella
- Busqueda Bidireccional



# Resultados

## Laberinto 1

### BFS
![lab1BFS](/Taller2/images/laberinto1.txt_BFS.gif)
### A Estrella
![lab1AE](/Taller2/images/laberinto1.txt_A_estrella.gif)
### Busqueda Bidireccional
![lab1BB](/Taller2/images/laberinto1.txt_Busqueda_Bidireccional.gif)

## Laberinto 2

### BFS
![lab2BFS](/Taller2/images/laberinto2.txt_BFS.gif)
### A Estrella
![lab2AE](/Taller2/images/laberinto2.txt_A_estrella.gif)
### Busqueda Bidireccional
![lab2BB](/Taller2/images/laberinto2.txt_Busqueda_Bidireccional.gif)

## Laberinto 3

### BFS
![lab3BFS](/Taller2/images/laberinto3.txt_BFS.gif)
### A Estrella
![lab3AE](/Taller2/images/laberinto3.txt_A_estrella.gif)
### Busqueda Bidireccional
![lab3BB](/Taller2/images/laberinto3.txt_Busqueda_Bidireccional.gif)

# CONCLUSIONES
Para comparar el comportamiento, efectividad y rapidez establecimos las siguientes metricas para evaluar los algoritmos:
- Nodos de la ruta (distancia de la ruta).
- Nodos visitados (distancia de las visitas).
- Tiempo de ejecucion de las busquedas.

Se manejan laberintos de diferente profundidad, el mas pequeño cuenta con 43 nodos , el mediano cuenta con 201 nodos y el mas grande cuenta con 1270 nodos. 

![resulF](/Taller2/images/Resultados_P1.jpg)

- Todos los algoritmos encontraron la misma ruta, a excepción del laberinto 1, donde la busqueda bidireccional generó una ruta con una baldosa adicional, ya que el punto de encuentro no se localizó en la ruta de los otros algoritmos, la cual es la mas corta.

- En tiempos de ejecucion, de manera general la busqueda bidireccional es el algoritmo mas rapido, inclusive en casos donde este no encontró la ruta mas corta como en el laberinto 1. Igualmente fue el mas rapido en el laberinto 3, a pesar de que visitó mas nodos (1104 nodos visitados)

- Con respecto a los nodos visitados (procesamiento de la ruta), 

 