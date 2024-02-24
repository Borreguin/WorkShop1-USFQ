import matplotlib.pyplot as plt

def mostrar_estado(estado):
    orilla_inicio, orilla_destino = estado
    print("\nOrilla de inicio: " + ", ".join(orilla_inicio) + " | Orilla de destino: " + ", ".join(orilla_destino))
    print("\n")

def es_movimiento_valido(estado, eleccion, desde, hacia):
    if eleccion != "granjero" and eleccion not in desde:
        return False  # La elección debe estar en la misma orilla que el granjero para moverse
    
    # Simula el movimiento para verificar las condiciones después del movimiento
    desde_simulado = desde.copy()
    hacia_simulado = hacia.copy()
    if eleccion != "granjero":
        desde_simulado.remove(eleccion)
        hacia_simulado.append(eleccion)
    
    if "granjero" in desde_simulado:
        desde_simulado.remove("granjero")
    hacia_simulado.append("granjero")
    
    # Verificar las condiciones de peligro en ambas orillas
    for orilla in [desde_simulado, hacia_simulado]:
        if "lobo" in orilla and "cabra" in orilla and "granjero" not in orilla:
            return False
        if "cabra" in orilla and "col" in orilla and "granjero" not in orilla:
            return False
    return True

def realizar_movimiento(estado, eleccion, desde, hacia):
    if eleccion != "granjero":
        desde.remove(eleccion)
        hacia.append(eleccion)
    if "granjero" in desde:
        desde.remove("granjero")
    else:
        hacia.remove("granjero")
    hacia.append("granjero")
    return (estado[0], estado[1])

elementos_posiciones = {
    "granjero": (1, 1),
    "lobo": (2, 1),
    "cabra": (3, 1),
    "col": (4, 1)
}

def mostrar_grafico(estado):
    plt.figure(figsize=(6, 4))
    plt.clf()  # Limpia el gráfico actual para evitar superposiciones
    orilla_inicio, orilla_destino = estado
    for elemento, pos in elementos_posiciones.items():
        if elemento in orilla_inicio:
            plt.scatter(pos[0], 1, label=elemento, s=100)  # Orilla de inicio
        if elemento in orilla_destino:
            plt.scatter(pos[0], 2, label=elemento, s=100)  # Orilla de destino
    plt.ylim(0, 3)
    plt.yticks([1, 2], ["Orilla Inicio", "Orilla Destino"])
    plt.xticks([])
    plt.legend()
    plt.draw()
    plt.pause(0.1)  # Pausa para permitir la visualización del gráfico antes de continuar

def juego():
    estado = (["granjero", "lobo", "cabra", "col"], [])
    plt.ion()  # Activa el modo interactivo de matplotlib
    while True:
        mostrar_estado(estado)
        mostrar_grafico(estado)
        if len(estado[1]) == 4:  # Todos han cruzado al destino
            print("¡Felicidades! Todos han cruzado el río con éxito.")
            break
        eleccion = input("¿Quién cruzará el río con el granjero? (lobo, cabra, col, ninguno): ").strip().lower()
        if eleccion == "ninguno":
            eleccion = "granjero"
        
        desde, hacia = (estado[0], estado[1]) if "granjero" in estado[0] else (estado[1], estado[0])
        
        if es_movimiento_valido(estado, eleccion, desde, hacia):
            estado = realizar_movimiento(estado, eleccion, desde, hacia)
        else:
            print("Movimiento inválido. Intenta de nuevo.")
    plt.ioff()  # Desactiva el modo interactivo
    mostrar_grafico(estado)  # Muestra el estado final
    plt.show()

juego()
