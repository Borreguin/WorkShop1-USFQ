import matplotlib.pyplot as plt

class Estado:
    def __init__(self, lado_granjero, lado_lobo, lado_cabra, lado_col):
        self.lado_granjero = lado_granjero
        self.lado_lobo = lado_lobo
        self.lado_cabra = lado_cabra
        self.lado_col = lado_col

    def __eq__(self, otro_estado):
        return (
            self.lado_granjero == otro_estado.lado_granjero and
            self.lado_lobo == otro_estado.lado_lobo and
            self.lado_cabra == otro_estado.lado_cabra and
            self.lado_col == otro_estado.lado_col
        )

    def __hash__(self):
        return hash((self.lado_granjero, self.lado_lobo, self.lado_cabra, self.lado_col))


def es_estado_valido(estado):
    # Verificar si el lobo se come a la cabra o la cabra se come la col
    if (estado.lado_lobo == estado.lado_cabra and estado.lado_granjero != estado.lado_lobo) or \
       (estado.lado_cabra == estado.lado_col and estado.lado_granjero != estado.lado_cabra):
        return False
    return True


def dibujar_estado(estado):
    plt.figure()
    plt.title("Estado Actual")
    plt.bar(['Granjero', 'Lobo', 'Cabra', 'Col'],
            [estado.lado_granjero, estado.lado_lobo, estado.lado_cabra, estado.lado_col])
    plt.ylim(0, 1)
    plt.show()


def cruzar_river(estado, acciones, visitados, callback):
    if estado not in visitados and es_estado_valido(estado):
        visitados.add(estado)
        dibujar_estado(estado)  # Dibujar el estado actual

        if all(valor == 1 for valor in estado.__dict__.values()):
            # Hemos llegado al estado objetivo, llamamos al callback
            callback(acciones)
            return

        # Intentar llevar al lobo
        cruzar_river(Estado(1 - estado.lado_granjero, 1 - estado.lado_lobo, estado.lado_cabra, estado.lado_col),
                     acciones + [('Lobo', '->')], visitados, callback)

        # Intentar llevar a la cabra
        cruzar_river(Estado(1 - estado.lado_granjero, estado.lado_lobo, 1 - estado.lado_cabra, estado.lado_col),
                     acciones + [('Cabra', '->')], visitados, callback)

        # Intentar llevar la col
        cruzar_river(Estado(1 - estado.lado_granjero, estado.lado_lobo, estado.lado_cabra, 1 - estado.lado_col),
                     acciones + [('Col', '->')], visitados, callback)

        # Intentar cruzar solo
        cruzar_river(Estado(1 - estado.lado_granjero, estado.lado_lobo, estado.lado_cabra, estado.lado_col),
                     acciones + [('Granja', '->')], visitados, callback)


if __name__ == "__main__":
    # Estado inicial
    estado_inicial = Estado(0, 0, 0, 0)

    # Obtener soluciones
    soluciones = []
    cruzar_river(estado_inicial, [], set(), soluciones.append)
