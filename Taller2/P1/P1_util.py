from collections import deque
import matplotlib.pyplot as plt
import numpy as np

def define_color(cell):
    if cell == '#':
        return 'black'
    elif cell == ' ':   # Espacio vacío
        return 'white'
    elif cell == 'E':   # Entrada
        return 'green'
    elif cell == 'S':   # Salida
        return 'red'
    

############################
# Reducción del laberinto  # FT
############################

def trasnformar_laberinto(archivo):
    """Carga un laberinto desde un archivo de texto y lo convierte en una matriz.
    
    Args:
    archivo (str): la ruta al archivo de texto que contiene el laberinto.
    
    Returns:
    list: una matriz que representa el laberinto, donde ' ' es 0, '#' es 1,
          'E' es el punto de inicio, y 'S' es el punto de salida.
    """
    # Inicializar una lista vacía para la matriz del laberinto
    matriz_laberinto = []
    
    # Abrir el archivo para leer
    with open(archivo, 'r') as file:
        # Iterar sobre cada línea en el archivo
        for linea in file:
            # Remover los saltos de línea y espacios extra al final
            linea = linea.rstrip()
            # Inicializar la fila de la matriz
            fila = []
            # Iterar sobre cada carácter en la línea
            for char in linea:
                if char == ' ':
                    fila.append(0)  # Espacio en blanco es 0
                elif char == '#':
                    fila.append(1)  # Pared es 1
                else:
                    fila.append(char)  # 'E' y 'S' se mantienen
            # Agregar la fila a la matriz del laberinto
            matriz_laberinto.append(fila)
    
    return matriz_laberinto


def count_open_neighbors(maze, row, col):
    """
    Count the number of open neighbors (value 0 or 'E' or 'S') around a given cell in the maze.

    Args:
    maze (list): The maze represented as a 2D list.
    row (int): The row index of the cell.
    col (int): The column index of the cell.

    Returns:
    int: The number of open neighbors.
    """
    open_neighbors = 0
    # List of potential neighbor positions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        # Check if neighbor is within bounds
        if 0 <= r < len(maze) and 0 <= c < len(maze[0]):
            # Check if neighbor is an open path or the start/end point
            if maze[r][c] in [0, 'E', 'S']:
                open_neighbors += 1
                
    return open_neighbors

def transform_maze(maze):
    """
    Transform the maze by changing 0s to 1s based on the number of open neighbors.
    A cell remains open (0) if it has at least two open neighbors.
    Otherwise, it becomes a wall (1). This process is repeated until no changes occur.

    Args:
    maze (list): The maze represented as a 2D list.

    Returns:
    list: The transformed maze.
    """
    changed = True
    while changed:
        changed = False
        # Create a copy of the maze to store changes
        new_maze = [row[:] for row in maze]
        
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 0:
                    if count_open_neighbors(maze, i, j) < 2:
                        new_maze[i][j] = 1
                        changed = True
                        
        # Check if there was any change in this iteration
        if changed:
            # Update maze for the next iteration
            maze = new_maze
            
    return maze


####################################
# Sección para el plot de matrices # FT
####################################

def plot_maze_before_after(original_maze, transformed_maze):
    """
    Plot a visual representation of the original and transformed mazes side by side using matplotlib.

    Args:
    original_maze (list): The original maze represented as a 2D list.
    transformed_maze (list): The transformed maze represented as a 2D list.
    """
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns for subplots

    # Map the 'E' and 'S' to numeric values for plotting purposes
    mapper = {' ': 0, '#': 1, 'E': 2, 'S': 3}
    
    # Convert the mazes to NumPy arrays for better handling
    original_maze_array = np.array([[mapper[cell] if cell in mapper else cell for cell in row] for row in original_maze])
    transformed_maze_array = np.array([[mapper[cell] if cell in mapper else cell for cell in row] for row in transformed_maze])

    # Plot the original maze
    cax1 = axes[0].matshow(original_maze_array, cmap=plt.cm.gray)
    axes[0].set_title('Original Maze')
    
    # Plot the transformed maze
    cax2 = axes[1].matshow(transformed_maze_array, cmap=plt.cm.gray)
    axes[1].set_title('Transformed Maze')

    # Hide the tick labels
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)

    # Add a color bar
    fig.colorbar(cax1, ax=axes[0], fraction=0.046, pad=0.04)
    fig.colorbar(cax2, ax=axes[1], fraction=0.046, pad=0.04)

    # Display the plots
    plt.tight_layout()
    plt.show()




###############################
# Sección de solución por BFS # FT
###############################

def bfs_find_path(maze, start, end):
    """
    Find the shortest path from start to end using BFS.

    Args:
    maze (list of list of int): The maze representation where 0 is a path and 1 is a wall.
    start (tuple): The starting position (row, col).
    end (tuple): The ending position (row, col).

    Returns:
    list: The path from start to end as a list of (row, col) tuples.
    """
    rows, cols = len(maze), len(maze[0])
    visited = [[False]*cols for _ in range(rows)]
    parent = {start: None}
    
    queue = deque([start])
    visited[start[0]][start[1]] = True
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        row, col = queue.popleft()
        if (row, col) == end:
            break
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols and maze[r][c] != 1 and not visited[r][c]:
                visited[r][c] = True
                parent[(r, c)] = (row, col)
                queue.append((r, c))
    
    # Backtrack from end to start to get the path
    path = []
    while end is not None:
        path.append(end)
        end = parent[end]
    path.reverse()
    
    return path if path[0] == start else []

def mark_path(maze, path, start_position, end_position):
    """
    Mark the path in the maze with 0 and set all other cells to 1, but preserve 'E' and 'S'.
    
    Args:
    maze (list of list of int/str): The maze to mark.
    path (list of tuple): The path to mark as 0.
    start_position (tuple): The position of 'E'.
    end_position (tuple): The position of 'S'.
    """
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if (r, c) == start_position:
                maze[r][c] = 'E'  # Preserve the start position
            elif (r, c) == end_position:
                maze[r][c] = 'S'  # Preserve the end position
            elif (r, c) in path:
                maze[r][c] = 0  # Mark the path
            else:
                maze[r][c] = 1  # Fill the rest with walls



