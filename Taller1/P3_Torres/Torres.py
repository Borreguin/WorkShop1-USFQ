def print_towers(towers):
    """Imprime las torres de Hanoi de manera visual en texto."""
    max_height = max(len(tower) for tower in towers.values())
    for level in range(max_height, 0, -1):
        for tower in ['A', 'B', 'C']:
            if level <= len(towers[tower]):
                print(f" {towers[tower][level-1]} ", end="")
            else:
                print(" | ", end="")
        print()  # Nueva línea después de cada nivel
    print("---" * 3)  # Base de las torres

def move_disk(towers, origen, destino):
    """Mueve un disco de la torre de origen a la torre de destino."""
    disk = towers[origen].pop()
    towers[destino].append(disk)

def hanoi_visual(n, origen, destino, auxiliar, towers):
    """Versión visual del algoritmo de Hanoi."""
    if n == 1:
        move_disk(towers, origen, destino)
        print(f"\nMoviendo disco de {origen} a {destino}:")
        print_towers(towers)
        return
    hanoi_visual(n-1, origen, auxiliar, destino, towers)
    move_disk(towers, origen, destino)
    print(f"\nMoviendo disco de {origen} a {destino}:")
    print_towers(towers)
    hanoi_visual(n-1, auxiliar, destino, origen, towers)

n = 3  # Número de discos
towers = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}

# Imprimir estado inicial
print("Estado inicial:")
print_towers(towers)

# Resolver visualmente el problema
hanoi_visual(n, 'A', 'C', 'B', towers)