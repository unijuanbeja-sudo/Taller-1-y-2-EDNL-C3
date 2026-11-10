"""EpiRed: organizar zonas en turnos sin conflictos. Explicar del paso 1 al 5."""

# PASO 1. Cada zona es un vértice; sus vecinos son zonas incompatibles.
# Es un grafo no dirigido: si Centro incluye a Norte, Norte incluye a Centro.
grafo_conflictos = {
    "Centro": ["Norte", "Oriente", "Occidente"],
    "Norte": ["Centro", "Suba", "Engativá"],
    "Sur": ["Oriente", "Kennedy"],
    "Oriente": ["Centro", "Sur", "Kennedy"],
    "Occidente": ["Centro", "Kennedy", "Engativá"],
    "Suba": ["Norte", "Engativá"],
    "Kennedy": ["Sur", "Oriente", "Occidente"],
    "Engativá": ["Norte", "Occidente", "Suba"]
}


def welsh_powell(grafo):
    """Recibe un grafo sin lazos y con vecinos recíprocos, sin repetidos."""
    # PASO 2. El grado es la cantidad de vecinos de cada zona.
    grados = {zona: len(vecinos) for zona, vecinos in grafo.items()}

    # PASO 3. Mayor grado primero; los empates conservan el orden del diccionario.
    orden = sorted(grafo, key=grados.get, reverse=True)

    # PASO 4. Llenar un turno con zonas compatibles antes de abrir el siguiente.
    colores = {}  # Guarda zona: número de turno.
    turno = 0
    while len(colores) < len(grafo):
        turno += 1
        for zona in orden:
            if zona in colores:
                continue  # Esta zona ya tiene turno.
            # Aceptar solo si ningún vecino tiene el turno actual.
            if all(colores.get(vecino) != turno for vecino in grafo[zona]):
                colores[zona] = turno
    return grados, orden, colores


# PASO 5. Ejecutar la función y mostrar los grados y las zonas de cada turno.
if __name__ == "__main__":
    grados, orden, colores = welsh_powell(grafo_conflictos)
    print("ORDEN DE MAYOR A MENOR GRADO")
    for zona in orden:
        print(f"{zona}: grado {grados[zona]}")

    print("\nAGRUPACIÓN POR TURNOS")
    for turno in sorted(set(colores.values())):
        zonas = [zona for zona in orden if colores[zona] == turno]
        print(f"Turno {turno}: {', '.join(zonas)}")
    print(f"\nTotal de turnos utilizados: {len(set(colores.values()))}")
