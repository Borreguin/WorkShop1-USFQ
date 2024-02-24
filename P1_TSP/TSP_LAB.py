import numpy as np
import matplotlib.pyplot as plt



# Función para calcular la distancia total de una ruta
def calcular_distancia_ruta(ruta, matriz_distancias):
    distancia_total = 0
    numero_ciudades = len(ruta)
    for i in range(numero_ciudades):
        distancia_total += matriz_distancias[ruta[i - 1]][ruta[i]]
    return distancia_total

# Heurística del vecino más cercano para una aproximación rápida
def vecino_mas_cercano(matriz_distancias):
    numero_ciudades = len(matriz_distancias)
    no_visitadas = list(range(1, numero_ciudades))
    ruta = [0]  # Comenzamos por la ciudad 0
    while no_visitadas:
        siguiente_ciudad = min(no_visitadas, key=lambda ciudad: matriz_distancias[ruta[-1]][ciudad])
        ruta.append(siguiente_ciudad)
        no_visitadas.remove(siguiente_ciudad)
    ruta.append(0) # Regresar a la ciudad origen
    return ruta

# Función para generar las coordenadas de las ciudades
def generar_coordenadas_ciudades(n):
    np.random.seed(0)
    return np.random.rand(n, 2)

# Función para visualizar la ruta
def visualizar_ruta(ruta, coordenadas):
    plt.figure(figsize=(10, 5))
    # Dibujar las líneas de la ruta
    for i in range(1, len(ruta)):
        ciudad_anterior = coordenadas[ruta[i - 1]]
        ciudad_actual = coordenadas[ruta[i]]
        plt.plot([ciudad_anterior[0], ciudad_actual[0]], [ciudad_anterior[1], ciudad_actual[1]], 'b')
    # Dibujar un punto para cada ciudad
    plt.scatter(coordenadas[:, 0], coordenadas[:, 1], c='red', label='Ciudad')
    # Nombrar las ciudades
    for i, coord in enumerate(coordenadas):
        plt.text(coord[0], coord[1], f' {i}', fontsize=12)
    plt.title('Ruta del vendedor viajero')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.legend()
    plt.grid(True)
    plt.show()

# Supongamos que queremos resolver para 5 ciudades
numero_ciudades = 1000
coordenadas_ciudades = generar_coordenadas_ciudades(numero_ciudades)

# Calcular la matriz de distancias a partir de las coordenadas
matriz_distancias = np.zeros((numero_ciudades, numero_ciudades))
for i in range(numero_ciudades):
    for j in range(numero_ciudades):
        matriz_distancias[i][j] = np.linalg.norm(coordenadas_ciudades[i] - coordenadas_ciudades[j])

# Encontrar la ruta usando vecino más cercano
ruta = vecino_mas_cercano(matriz_distancias)
distancia_total = calcular_distancia_ruta(ruta, matriz_distancias)

# Visualizar la ruta
visualizar_ruta(ruta, coordenadas_ciudades)

# Imprimir la ruta y la distancia total
print("Ruta sugerida:", ruta)
print("Distancia total:", distancia_total)
