"""EpiRed: ejecutar python taller.py abre el grafo; --consola muestra solo texto."""
# 1. Herramientas incluidas en Python: no requieren instalación.
from collections import deque  # Cola para explorar por niveles con BFS.
import heapq  # Cola de prioridad para elegir el menor costo con UCS.

# 2. Datos del grafo: cada tupla contiene origen, destino y minutos ficticios.
# A Medellín, B Bello, C Itagüí, D Envigado, E Sabaneta, F Caldas,
# G Copacabana, H Girardota, I Barbosa y J Rionegro.
CONEXIONES = [
    ("A", "B", 20), ("A", "C", 15), ("A", "D", 30), ("B", "C", 30),
    ("C", "D", 10), ("D", "E", 12), ("E", "F", 20), ("C", "F", 35),
    ("A", "G", 35), ("B", "G", 20), ("G", "H", 15), ("H", "I", 20),
    ("G", "J", 40),
]
GRAFO = {nodo: {} for nodo in "ABCDEFGHIJ"}  # Un diccionario por municipio.
for a, b, minutos in CONEXIONES:
    GRAFO[a][b] = GRAFO[b][a] = minutos  # Guarda ida y vuelta con igual costo.


# 3. Función compartida: recupera la ruta desde la meta hasta el inicio.
def reconstruir(padres, destino):
    ruta = []
    while destino is not None:
        ruta.append(destino)
        destino = padres[destino]  # Retrocede al nodo desde el cual llegamos.
    return ruta[::-1]  # Invierte la lista para mostrar inicio -> meta.


# 4. BFS: busca primero los municipios que están a menos tramos.
def bfs(grafo, inicio, meta):
    cola = deque([inicio])  # Al principio solo está pendiente el origen.
    padres = {inicio: None}  # También sirve para reconocer nodos descubiertos.
    orden = []  # Guarda el orden de búsqueda, que puede diferir de la ruta.
    while cola:
        actual = cola.popleft()  # Primero en entrar, primero en salir.
        orden.append(actual)
        if actual == meta:
            return reconstruir(padres, meta), orden
        for vecino in sorted(grafo[actual]):  # Orden alfabético reproducible.
            if vecino not in padres:
                padres[vecino] = actual  # Marca el vecino antes de encolarlo.
                cola.append(vecino)
    return [], orden  # Cola agotada: no hay camino hacia la meta.


# 5. DFS: profundiza por una rama y retrocede si no llega a la meta.
def dfs(grafo, inicio, meta):
    padres = {inicio: None}
    orden = []

    def visitar(actual):  # Función recursiva: puede llamarse a sí misma.
        orden.append(actual)
        if actual == meta:
            return True
        for vecino in sorted(grafo[actual]):
            if vecino not in padres:
                padres[vecino] = actual  # Evita volver a entrar al mismo nodo.
                if visitar(vecino):  # Profundiza; si no llega, retrocede.
                    return True
        return False  # Esta rama no encontró la meta; permite retroceder.

    encontrada = visitar(inicio)  # Inicia la exploración recursiva.
    return (reconstruir(padres, meta) if encontrada else []), orden


# 6. UCS: busca el menor tiempo total, con pesos no negativos.
def ucs(grafo, inicio, meta):
    cola = [(0, inicio)]  # Cada entrada contiene (costo acumulado, nodo).
    costos, padres, orden = {inicio: 0}, {inicio: None}, []
    while cola:
        costo, actual = heapq.heappop(cola)  # Sale el menor costo.
        if costo != costos[actual]:
            continue  # Descarta un costo antiguo que ya fue mejorado.
        orden.append(actual)
        if actual == meta:  # Al salir con el menor costo, la ruta es óptima.
            return reconstruir(padres, meta), orden
        for vecino in sorted(grafo[actual]):
            nuevo = costo + grafo[actual][vecino]  # Suma el siguiente tramo.
            if nuevo < costos.get(vecino, float("inf")):  # ¿Mejora el costo?
                costos[vecino], padres[vecino] = nuevo, actual
                heapq.heappush(cola, (nuevo, vecino))  # Añade la mejor opción.
    return [], orden


# 7. Ejemplo de uso: ejecutar las búsquedas y comparar sus resultados.
if __name__ == "__main__":
    inicio, meta = "A", "E"  # Cambia estas letras para consultar otra ruta.
    print(f"EpiRed: ruta de {inicio} a {meta}. Tiempos ficticios en minutos.")
    for nombre, algoritmo in [("BFS", bfs), ("DFS", dfs), ("UCS", ucs)]:
        ruta, orden = algoritmo(GRAFO, inicio, meta)
        print(f"\n{nombre} | Orden de búsqueda: {' '.join(orden)}")
        if ruta:  # Solo suma costos si existe una ruta.
            # zip forma pares consecutivos: (A,C), (C,D), (D,E), por ejemplo.
            costo = sum(GRAFO[a][b] for a, b in zip(ruta, ruta[1:]))
            print(f"Ruta: {' -> '.join(ruta)} | {len(ruta)-1} tramos | {costo} min")
        else:
            print("No existe una ruta.")

    # 8. Abrir la vista sencilla usando estas mismas funciones y datos.
    import sys
    if "--consola" not in sys.argv:
        from grafo_interactivo import mostrar_grafo
        mostrar_grafo(GRAFO, {"BFS": bfs, "DFS": dfs, "UCS": ucs})
