if __name__ == '__main__':
 from collections import deque

def obtener_sucesores(estado):
    """Genera todos los posibles sucesores válidos de un estado."""
    sucesores = []
    # Intenta mover cada personaje (incluido el granjero solo) y verifica si el nuevo estado es válido
    for i in range(4):
        if estado[i] == estado[0]:  # Solo se puede mover con el granjero
            nuevo_estado = list(estado)
            nuevo_estado[i] = not estado[i]  # Mover el personaje
            nuevo_estado[0] = not estado[0]  # Mover el granjero
            if es_estado_valido(nuevo_estado):
                sucesores.append(tuple(nuevo_estado))
    return sucesores

def es_estado_valido(estado):
    """Comprueba si un estado es válido según las reglas."""
    # El granjero no está presente y (lobo está con la cabra o cabra está con la col)
    return not ((estado[0] != estado[1] and estado[1] == estado[2]) or (estado[0] != estado[2] and estado[2] == estado[3]))

def resolver_granjero():
    estado_inicial = (True, True, True, True)
    estado_objetivo = (False, False, False, False)
    cola = deque([(estado_inicial, [])])  # Almacena estados y el camino hasta ellos
    visitados = set()

    while cola:
        estado_actual, camino = cola.popleft()
        if estado_actual in visitados:
            continue
        visitados.add(estado_actual)

        if estado_actual == estado_objetivo:
            return camino  # Retorna el camino cuando se alcanza el estado objetivo

        for sucesor in obtener_sucesores(estado_actual):
            if sucesor not in visitados:
                cola.append((sucesor, camino + [sucesor]))

    return None  # No se encontró solución

def traducir_solucion(solucion):
    """Traduce la solución a listas de salida y llegada."""
    salida, llegada = [], []
    personajes = ["Granjero", "  Lobo  ", " Cabra  ", "  Col   "]
    for estado in solucion:
        salida.append([personajes[i] if estado[i] else "        " for i in range(4)])
        llegada.append([personajes[i]  if not estado[i] else "        "  for i in range(4)])
    return salida, llegada

if __name__ == '__main__':
    # Resolver el acertijo y mostrar los pasos
    solucion = resolver_granjero()
    print(f"\nTrue = Orilla inicial, False = Orilla final\n")
    print(f"('Granjero', '  Lobo  ', ' Cabra  ', '  Col   '), Pasos a seguir:\n")
    for paso in solucion:
        print(paso)
        

    #Traducir los pasos a salida y llegada
    salida, llegada = traducir_solucion(solucion)
    print()
    print("Solución:\n")
    print("Paso 0: ['Granjero', '  Lobo  ', ' Cabra  ', '  Col   '] - Salida \\\u25BC~~~/ Llegada - ['        ', '        ', '        ', '        ']")
    for i, (s, l) in enumerate(zip(salida, llegada), start=1):
        if i % 2 == 0:
            print(f"Paso {i}: {s} - Salida \\\u25BC~~~/ Llegada - {l}")
        else:
            print(f"Paso {i}: {s} - Salida \~~~\u25BC/ Llegada - {l}")
