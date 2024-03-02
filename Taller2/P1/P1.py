import os, sys
project_path = os.path.dirname(__file__)
sys.path.append(project_path)
import matplotlib
matplotlib.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg\bin\ffmpeg.exe'
from P1_MazeLoader import MazeLoader
from queue import PriorityQueue
from queue import Queue
import time
from collections import deque
import pandas as pd


def study_case_1():
    print("This is study case 1")
    maze_file = 'laberinto1.txt'
    
    # Lista para almacenar los resultados
    resultados_df = pd.DataFrame(columns=['Laberinto', 'Nodos del Grafo', 'Algoritmo', 'Nodos visitados (distancia visitas)', 'Nodos de la ruta (distancia ruta)', 'Tiempo de ejecucion'])
    
      
    #Carga del laberinto
    maze = MazeLoader(maze_file).load_Maze()
    
    # Generamos el grafo del algoritmo
    grafo, inicio, fin = maze.get_graph()
    
    #Ejecutamos para los algoritmos BFS, A_estrella y Búsqueda Bidereccional
    algoritmos =['BFS','A_estrella','Busqueda_Bidireccional']
        
    for algoritmo in algoritmos:
        funcion = getattr(__import__("__main__"), algoritmo, None)  # Obtiene la función por su nombre

        # Iniciar el temporizador antes de ejecutar algoritmo
        start_time = time.time()
        # Ejecuta cada algoritmo
        ruta, visitados = funcion(grafo, inicio, fin)
        # Detener el temporizador después de la ejecución del algoritmo
        end_time = time.time()

        # Calcular la diferencia
        tiempo_ejecucion = round(end_time - start_time,5)
        print(f"El algoritmo {algoritmo} se ejecutó en {tiempo_ejecucion} segundos.")
    
        # Encuentra la solución y la respectiva animación GIF de requerirse
        maze.set_solution(ruta, visitados, tiempo_ejecucion, algoritmo)
        maze.animate_solution(gif=True)
        
        # Añade los resultados al DataFrame
        resultados_df.loc[len(resultados_df)] = {'Laberinto': maze_file, 'Nodos del Grafo': len(grafo), 'Algoritmo': algoritmo, 'Nodos visitados (distancia visitas)': len(visitados), 'Nodos de la ruta (distancia ruta)': len(ruta), 'Tiempo de ejecucion': tiempo_ejecucion}
  
    return resultados_df


def study_case_2():
    print("This is study case 2")
    maze_file = 'laberinto2.txt'
    
    # Lista para almacenar los resultados
    resultados_df = pd.DataFrame(columns=['Laberinto', 'Nodos del Grafo', 'Algoritmo', 'Nodos visitados (distancia visitas)', 'Nodos de la ruta (distancia ruta)', 'Tiempo de ejecucion'])
    
      
    #Carga del laberinto
    maze = MazeLoader(maze_file).load_Maze()
    
    # Generamos el grafo del algoritmo
    grafo, inicio, fin = maze.get_graph()
    
    #Ejecutamos para los algoritmos BFS, A_estrella y Búsqueda Bidereccional
    algoritmos =['BFS','A_estrella','Busqueda_Bidireccional']
        
    for algoritmo in algoritmos:
        funcion = getattr(__import__("__main__"), algoritmo, None)  # Obtiene la función por su nombre

        # Iniciar el temporizador antes de ejecutar algoritmo
        start_time = time.time()
        # Ejecuta cada algoritmo
        ruta, visitados = funcion(grafo, inicio, fin)
        # Detener el temporizador después de la ejecución del algoritmo
        end_time = time.time()

        # Calcular la diferencia
        tiempo_ejecucion = round(end_time - start_time,5)
        print(f"El algoritmo {algoritmo} se ejecutó en {tiempo_ejecucion} segundos.")
    
        # Encuentra la solución y la respectiva animación GIF de requerirse
        maze.set_solution(ruta, visitados, tiempo_ejecucion, algoritmo)
        maze.animate_solution(gif=True)
        
        # Añade los resultados al DataFrame
        resultados_df.loc[len(resultados_df)] = {'Laberinto': maze_file, 'Nodos del Grafo': len(grafo), 'Algoritmo': algoritmo, 'Nodos visitados (distancia visitas)': len(visitados), 'Nodos de la ruta (distancia ruta)': len(ruta), 'Tiempo de ejecucion': tiempo_ejecucion}
  
    return resultados_df

def study_case_3():

    print("This is study case 3")
    maze_file = 'laberinto3.txt'
    
    # Lista para almacenar los resultados
    resultados_df = pd.DataFrame(columns=['Laberinto', 'Nodos del Grafo', 'Algoritmo', 'Nodos visitados (distancia visitas)', 'Nodos de la ruta (distancia ruta)', 'Tiempo de ejecucion'])
    
      
    #Carga del laberinto
    maze = MazeLoader(maze_file).load_Maze()
    
    # Generamos el grafo del algoritmo
    grafo, inicio, fin = maze.get_graph()
    
    #Ejecutamos para los algoritmos BFS, A_estrella y Búsqueda Bidereccional
    algoritmos =['BFS','A_estrella','Busqueda_Bidireccional']
        
    for algoritmo in algoritmos:
        funcion = getattr(__import__("__main__"), algoritmo, None)  # Obtiene la función por su nombre

        # Iniciar el temporizador antes de ejecutar algoritmo
        start_time = time.time()
        # Ejecuta cada algoritmo
        ruta, visitados = funcion(grafo, inicio, fin)
        # Detener el temporizador después de la ejecución del algoritmo
        end_time = time.time()

        # Calcular la diferencia
        tiempo_ejecucion = round(end_time - start_time,5)
        print(f"El algoritmo {algoritmo} se ejecutó en {tiempo_ejecucion} segundos.")
    
        # Encuentra la solución y la respectiva animación GIF de requerirse
        maze.set_solution(ruta, visitados, tiempo_ejecucion, algoritmo)
        maze.animate_solution(gif=True)
        
        # Añade los resultados al DataFrame
        resultados_df.loc[len(resultados_df)] = {'Laberinto': maze_file, 'Nodos del Grafo': len(grafo), 'Algoritmo': algoritmo, 'Nodos visitados (distancia visitas)': len(visitados), 'Nodos de la ruta (distancia ruta)': len(ruta), 'Tiempo de ejecucion': tiempo_ejecucion}
  
    return resultados_df

#Búsquedas empleadas

#BFS

# Búsqueda en anchura para encontrar la ruta
def BFS(grafo, inicio, fin):
    cola = Queue()
    cola.put([inicio])  # Cola de rutas a explorar
    visitados = list([inicio])
    while not cola.empty():
        ruta = cola.get()
        ultima_pos = ruta[-1]
        if ultima_pos == fin:
            print("\nLista de nodos visitados:")
            print(visitados)
            print("\nLista de la ruta encontrada:")
            print(ruta)
            print(f"\nNúmero de nodos visitados: {len(visitados)}")
            print(f"Número de nodos de la ruta: {len(ruta)}\n")
            return list(ruta), list(visitados)  # Retornar la ruta cuando se encuentra el fin
        for next_pos in grafo[ultima_pos]:
            if next_pos not in visitados:
                visitados.append(next_pos)
                nueva_ruta = list(ruta)
                nueva_ruta.append(next_pos)
                cola.put(nueva_ruta)

#A estrella

def heuristica(a, b):
    """Calcula la distancia de Manhattan entre dos puntos a y b"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def A_estrella(grafo, inicio, fin):
    frontera = PriorityQueue()
    frontera.put((0, inicio))
    procedencia = {inicio: None}
    costo_actual = {inicio: 0}

    while not frontera.empty():
        actual = frontera.get()[1]

        if actual == fin:
            break

        for siguiente in grafo[actual]:
            nuevo_costo = costo_actual[actual] + 1  # Costo constante de 1 por movimiento
            if siguiente not in costo_actual or nuevo_costo < costo_actual[siguiente]:
                costo_actual[siguiente] = nuevo_costo
                prioridad = nuevo_costo + heuristica(fin, siguiente)
                frontera.put((prioridad, siguiente))
                procedencia[siguiente] = actual

    # Reconstruir el camino
    actual = fin
    ruta = []
    while actual != inicio:
        ruta.append(actual)
        actual = procedencia[actual]
    ruta.append(inicio)
    ruta.reverse()

    visitados = list(procedencia.keys())
                     
    print("\nLista de nodos visitados:")
    print(visitados)
    print("\nLista de la ruta encontrada:")
    print(ruta)
    print(f"\nNúmero de nodos visitados: {len(visitados)}")
    print(f"Número de nodos de la ruta: {len(ruta)}\n")

    return ruta, visitados


# Búsqueda Bidireccional

def Busqueda_Bidireccional(grafo, inicio, fin):
    # Caso base: si el inicio y el fin son el mismo.
    if inicio == fin:
        return [inicio], [inicio]

    # Inicializa conjuntos de nodos visitados desde ambos extremos.
    visitados_desde_inicio = {inicio}
    visitados_desde_fin = {fin}

    # Diccionarios para rastrear el nodo previo (padre) desde cada extremo.
    padre_desde_inicio = {inicio: None}
    padre_desde_fin = {fin: None}

    # Colas para los nodos a explorar desde ambos extremos.
    cola_desde_inicio = deque([inicio])
    cola_desde_fin = deque([fin])

    # Lista para registrar el orden en que se visitan los nodos.
    orden_visitados = []

    # Función interna para reconstruir el camino encontrando el punto de encuentro.
    def reconstruir_camino(punto_encuentro, padre_desde_inicio, padre_desde_fin):
        # Reconstruir el camino desde el inicio hasta el punto de encuentro.
        camino_desde_inicio = []
        actual = punto_encuentro
        while actual in padre_desde_inicio:  # Asegura que actual exista en padre_desde_inicio
            camino_desde_inicio.insert(0, actual)
            actual = padre_desde_inicio.get(actual)

        # Reconstruir el camino desde el punto de encuentro hasta el fin.
        # Comenzamos con el siguiente nodo después del punto de encuentro para evitar duplicarlo.
        camino_desde_fin = []
        actual = padre_desde_fin.get(punto_encuentro)  # Usamos get() para manejar el caso de None de forma segura.
        while actual:
            camino_desde_fin.append(actual)
            actual = padre_desde_fin.get(actual)

        # Invertimos el camino desde el fin para que esté en el orden correcto y unimos los caminos.
        # No incluimos el punto de encuentro al final para evitar duplicados.
        camino_completo = camino_desde_inicio + camino_desde_fin

        return camino_completo


    # Mientras haya nodos por explorar desde ambos extremos.
    while cola_desde_inicio and cola_desde_fin:
        
        # Expansión desde el inicio.
        if cola_desde_inicio:
            actual_desde_inicio = cola_desde_inicio.popleft()
            orden_visitados.append(actual_desde_inicio)
            for vecino in grafo[actual_desde_inicio]:
                if vecino in visitados_desde_fin:
                    orden_visitados.append(vecino)
                    padre_desde_inicio[vecino] = actual_desde_inicio
                    # Punto de encuentro encontrado.
                    ruta = reconstruir_camino(vecino, padre_desde_inicio, padre_desde_fin)
                    print("\nLista de nodos visitados:")
                    print(orden_visitados)
                    print("\nLista de la ruta encontrada:")
                    print(ruta)
                    print(f"\nNúmero de nodos visitados: {len(orden_visitados)}")
                    print(f"Número de nodos de la ruta: {len(ruta)}\n")

                    return ruta, orden_visitados
                
                if vecino not in visitados_desde_inicio:
                    visitados_desde_inicio.add(vecino)
                    padre_desde_inicio[vecino] = actual_desde_inicio
                    cola_desde_inicio.append(vecino)

        # Expansión desde el fin.
        if cola_desde_fin:
            actual_desde_fin = cola_desde_fin.popleft()
            orden_visitados.append(actual_desde_fin)
            for vecino in grafo[actual_desde_fin]:
                if vecino in visitados_desde_inicio:
                    orden_visitados.append(vecino)
                    padre_desde_fin[vecino] = actual_desde_fin
                    # Punto de encuentro encontrado.
                    ruta = reconstruir_camino(vecino, padre_desde_inicio, padre_desde_fin)
                    print("\nLista de nodos visitados:")
                    print(orden_visitados)
                    print("\nLista de la ruta encontrada:")
                    print(ruta)
                    print(f"\nNúmero de nodos visitados: {len(orden_visitados)}")
                    print(f"Número de nodos de la ruta: {len(ruta)}\n")

                    return ruta, orden_visitados
                
                if vecino not in visitados_desde_fin:
                    visitados_desde_fin.add(vecino)
                    padre_desde_fin[vecino] = actual_desde_fin
                    cola_desde_fin.append(vecino)

    # Si no se encuentra un camino.
    return [], orden_visitados



if __name__ == '__main__':
    resultado_lab1=study_case_1()
    resultado_lab2=study_case_2()
    resultado_lab3=study_case_3()

    print(resultado_lab1)
    print(resultado_lab2)
    print(resultado_lab3)

    resultado_lab1.to_excel('resultado_lab1.xlsx', index=False) 
    resultado_lab2.to_excel('resultado_lab2.xlsx', index=False) 
    resultado_lab3.to_excel('resultado_lab3.xlsx', index=False) 
 

