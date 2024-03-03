import matplotlib.pyplot as plt
import numpy as np

def dibujar_torres(torres, paso):
    plt.clf()  # Limpia el gráfico actual
    n = sum(len(torre) for torre in torres)  # Número total de discos
    colores = plt.cm.viridis(np.linspace(0, 1, n))  # Genera colores únicos para cada disco
    for i, torre in enumerate(torres):
        for j, disco in enumerate(torre):
            # Ajusta el dibujo de cada disco para que el más pequeño esté arriba
            plt.gca().add_patch(plt.Rectangle((3*i - disco/2, j), disco, 0.5, edgecolor='black', facecolor=colores[disco-1]))
        plt.text(3*i, len(torre), f'Torre {i+1}', ha='center', va='bottom', fontsize=10)
    plt.title(f'Paso {paso}')
    plt.xlim(-2, 8)  # Ajustado para proporcionar más espacio a la derecha
    plt.ylim(0, n+1)
    plt.axis('off')
    plt.pause(0.5)  # Pausa para visualizar el estado antes de continuar

def torre_de_hanoi_grafico(n, origen=0, destino=2, auxiliar=1, torres=None, paso=[1]):
    if torres is None:
        torres = [list(range(n, 0, -1)), [], []]
        dibujar_torres(torres, paso[0])
    if n == 1:
        torres[destino].append(torres[origen].pop())
        paso[0] += 1
        dibujar_torres(torres, paso[0])
        return
    torre_de_hanoi_grafico(n-1, origen, auxiliar, destino, torres, paso)
    torres[destino].append(torres[origen].pop())
    paso[0] += 1
    dibujar_torres(torres, paso[0])
    torre_de_hanoi_grafico(n-1, auxiliar, destino, origen, torres, paso)

# Configura la visualización
plt.figure(figsize=(10, 6))
n_discos = 3  # Ajusta este valor para cambiar el número de discos
torre_de_hanoi_grafico(n_discos)
plt.show()