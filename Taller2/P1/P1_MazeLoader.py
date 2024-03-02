import matplotlib.pyplot as plt
import os, sys
project_path = os.path.dirname(__file__)
sys.path.append(project_path)
from P1_util import define_color
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np
class MazeLoader:
    def __init__(self, filename):
        self.filename = filename
        self.maze = None
        # Añadir atributos para almacenar la ruta y los pasos
        self.path = []
        self.steps = []
        self.tiempo_ejecucion = 0
        self.len_path = 0
        self.len_steps = 0
        self.algoritmo =""
        self.nodos_grafo=0
        self.inicio=0
        self.fin=0
                
    def load_Maze(self):
        _maze = []
        file_path = os.path.join(project_path, self.filename)
        print("Loading Maze from", file_path)
        with open(file_path, 'r') as file:
            for line in file:
                _maze.append(list(line.strip()))
        self.maze = _maze
        return self


    # Establecer la ruta y los pasos antes de animar
    def set_solution(self, path, steps, tiempo_ejecucion, algoritmo):
        self.path = path
        self.steps = steps
        self.tiempo_ejecucion = tiempo_ejecucion
        self.len_path = len(path)
        self.len_steps = len(steps)
        self.algoritmo = algoritmo

    def plot_maze(self):
        height = len(self.maze)
        width = len(self.maze[0])

        fig, ax = plt.subplots(figsize=(max(7,width/3), max(4,height/3.6)))  # Ajusta el tamaño de la figura según el tamaño del Maze
        for y in range(height):
            for x in range(width):
                cell = self.maze[y][x]
                color = define_color(cell)
                ax.fill([x, x+1, x+1, x], [y, y, y+1, y+1], color=color, edgecolor='black')
            
        plt.xlim(0, width)
        plt.ylim(0, height)
        plt.gca().invert_yaxis()  # Invierte el eje y para que el origen esté en la esquina inferior izquierda
        plt.xticks([])
        plt.yticks([]) 
        fig.tight_layout()
        plt.text(0.5, max(0.4,height/30), f"Laberinto: {self.filename}, Nodos:{self.nodos_grafo} - Algoritmo: {self.algoritmo}.",fontsize=8, fontweight='bold', color= 'white')
        plt.text(0.5, max(0.7,height/17), f"Nodos visitados: {self.len_steps}, Nodos en la ruta: {self.len_path}, Tiempo de ejecución: {self.tiempo_ejecucion} segundos.",fontsize=8, fontweight='bold', color= 'white')
        
        # Crear parches para la leyenda
        salida_patch = patches.Patch(color='green', label='Salida')
        llegada_patch = patches.Patch(color='red', label='Llegada')
        visitados_patch = patches.Patch(color='orange', label='Lugares Visitados')
        ruta_patch = patches.Patch(color='blue', alpha= 0.5, label='Ruta Encontrada')

        # Añadir la leyenda al gráfico
        plt.legend(handles=[salida_patch, llegada_patch, visitados_patch, ruta_patch], loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.01), fontsize=9)

        
        #plt.show()
        return fig, ax


    def animate_solution(self, gif=True):
   
        fig, ax = self.plot_maze()  # Esto configura el laberinto y obtiene la figura y los ejes

        # Lista para mantener un registro de las celdas iluminadas (patches)
        iluminados = [] 
              
        # Función de actualización para cada frame de la animación
        def update(frame):
            # Dibujar los pasos y la ruta
            if (self.len_steps+self.len_path) < 13:   #Por la cantidad de nodos visitados y de ruta se elige marcar siempre todos los nodos visitados o solo el paso a paso. Al crear el GIF se despliega siempre todos los nodos acumulados
                if frame <= len(self.steps)-1:
                    step = self.steps[frame]
                    if step not in [self.inicio, self.fin]:
                        patch=ax.fill([step[1], step[1]+1, step[1]+1, step[1]], [step[0], step[0], step[0]+1, step[0]+1], color='orange', alpha=0.5)
                        iluminados.extend(patch)
                else:
                    point = self.path[frame+1 - len(self.steps)]
                    if point not in [self.inicio, self.fin]:
                        patch=ax.fill([point[1], point[1]+1, point[1]+1, point[1]], [point[0], point[0], point[0]+1, point[0]+1], color='blue', alpha=0.7)
                        iluminados.extend(patch)
            else:
                if frame <= len(self.steps)-1:
                    step = self.steps[frame]
                    if step not in [self.inicio, self.fin]:
                        patch=ax.fill([step[1], step[1]+1, step[1]+1, step[1]], [step[0], step[0], step[0]+1, step[0]+1], color='orange', alpha=0.5)
                        iluminados.clear()
                        iluminados.extend(patch)
                else:
                    point = self.path[frame+1 - len(self.steps)]
                    if point not in [self.inicio, self.fin]:
                        patch=ax.fill([point[1], point[1]+1, point[1]+1, point[1]], [point[0], point[0], point[0]+1, point[0]+1], color='blue', alpha=0.7)
                        iluminados.extend(patch)                
            
            return iluminados  # Retorna los objetos artísticos actualizados

            # Función de inicialización para la animación
        def init():
        #  Aquí podrías configurar el estado inicial si es necesario, por ahora solo retorna una lista vacía
            return []

        # Crea y ejecuta la animación
        frames = np.append(np.arange(0,len(self.steps) + len(self.path)-2), [len(self.steps) + len(self.path)-3] * 20)  # Repite el último cuadro 20 veces
        ani = animation.FuncAnimation(fig, update, frames=frames, repeat=False, init_func=init, interval=0, blit=True)
        
        if gif:
            # Guardar la animación
            nombre_archivo = f'{self.filename}_{self.algoritmo}.gif'
            ani.save(nombre_archivo, writer='ffmpeg', fps=50)
        
        plt.show()
        #plt.close()

    def get_graph(self):
        # Implementar la creación del grafo a partir del laberinto
        filas = len(self.maze)
        columnas = len(self.maze[0]) if filas > 0 else 0
        grafo = {}
                
        for i in range(filas):
            for j in range(columnas):
                if self.maze[i][j] not in ['#']:  # Si no es una pared
                    nodo = (i, j)
                    grafo[nodo] = []
                    
                    # Buscar vecinos
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (1,1), (1,-1), (-1,1), (-1,-1)]:
                        x, y = i + dx, j + dy
                        if 0 <= x < filas and 0 <= y < columnas and self.maze[x][y] not in ['#']:
                            grafo[nodo].append((x, y))
                    
                    if self.maze[i][j] == 'E':
                        inicio = (i, j)
                    elif self.maze[i][j] == 'S':
                        fin = (i, j)
        
        # Asegurarse de que tanto inicio como fin están definidos
        if inicio is None or fin is None:
            raise ValueError("El laberinto debe tener un punto de inicio (E) y un punto final (S)")
        print(f"\nNúmero de nodos del laberinto: {len(grafo)}")
        self.inicio = inicio
        self.fin = fin
        self.nodos_grafo= len(grafo)
        return grafo, inicio, fin







