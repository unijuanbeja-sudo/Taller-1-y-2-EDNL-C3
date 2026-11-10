"""Vista del taller 2. Usa los algoritmos de taller.py y Tkinter de Python."""
import tkinter as tk
from tkinter import ttk

NOMBRES = dict(zip("ABCDEFGHIJ", ["Medellín", "Bello", "Itagüí", "Envigado",
    "Sabaneta", "Caldas", "Copacabana", "Girardota", "Barbosa", "Rionegro"]))
POSICIONES = {"A": (330, 125), "B": (160, 55), "C": (160, 235),
    "D": (335, 250), "E": (355, 375), "F": (80, 370), "G": (470, 60),
    "H": (650, 80), "I": (700, 250), "J": (520, 260)}


def mostrar_grafo(grafo, algoritmos):
    # 1. Preparar la ventana y guardar el resultado actual.
    ventana = tk.Tk()
    ventana.title("EpiRed - Taller 2 - BFS, DFS y UCS")
    ventana.geometry("+20+20")
    ventana.resizable(False, False)
    posiciones = POSICIONES.copy()
    estado = {"ruta": [], "seleccion": None}
    origen, destino = tk.StringVar(value="A"), tk.StringVar(value="E")
    metodo = tk.StringVar(value="BFS")
    tiempos = tk.BooleanVar(value=True)
    resultado, detalle = tk.StringVar(), tk.StringVar()

    # 2. Dibujar las conexiones, sus minutos y los municipios.
    def dibujar():
        lienzo.delete("all")
        ruta = estado["ruta"]
        tramos = {frozenset((a, b)) for a, b in zip(ruta, ruta[1:])}
        for a in grafo:
            for b, costo in grafo[a].items():
                if a >= b:
                    continue  # Cada conexión se dibuja una sola vez.
                x, y = posiciones[a]
                xx, yy = posiciones[b]
                en_ruta = frozenset((a, b)) in tramos
                color = "#ea580c" if en_ruta else "#94a3b8"
                if estado["seleccion"] in (a, b):
                    color = "#dc2626"
                lienzo.create_line(x, y, xx, yy, fill=color,
                                   width=4 if en_ruta else 2, tags="arista")
                if tiempos.get():
                    mx, my = (x+xx)/2, (y+yy)/2
                    lienzo.create_rectangle(mx-12, my-9, mx+12, my+9,
                                            fill="white", outline="")
                    lienzo.create_text(mx, my, text=costo, font=("Arial", 9))
        for nodo, (x, y) in posiciones.items():
            color = "#fdba74" if nodo in ruta else "#e2e8f0"
            if nodo == origen.get():
                color = "#86efac"
            if nodo == destino.get():
                color = "#c4b5fd"
            lienzo.create_oval(x-39, y-39, x+39, y+39, fill=color,
                outline="#0f172a", width=3 if nodo == estado["seleccion"] else 1,
                tags="vertice")
            lienzo.create_text(x, y, text=f"{nodo}\n{NOMBRES[nodo]}",
                               font=("Arial", 9, "bold"))

    # 3. Ejecutar la función del taller y distinguir búsqueda de ruta final.
    def calcular(evento=None):
        ruta, orden = algoritmos[metodo.get()](grafo, origen.get(), destino.get())
        estado.update(ruta=ruta, seleccion=None)
        costo = sum(grafo[a][b] for a, b in zip(ruta, ruta[1:]))
        descripcion = {"BFS": "menor cantidad de tramos",
                       "DFS": "primera ruta al profundizar, sin garantizar el mínimo",
                       "UCS": "menor tiempo total"}[metodo.get()]
        recorrido = " -> ".join(ruta) if ruta else "No existe ruta"
        resultado.set(f"{metodo.get()}: {descripcion}.\n"
            f"Ruta: {recorrido} | {max(0, len(ruta)-1)} tramos | {costo} min\n"
            f"Orden de búsqueda: {' -> '.join(orden)}")
        detalle.set("Haz clic en un municipio para consultar sus conexiones.")
        dibujar()

    # 4. Seleccionar y mover municipios sin cambiar sus conexiones o tiempos.
    def seleccionar(evento):
        estado["seleccion"] = None
        for nodo, (x, y) in posiciones.items():
            if (evento.x-x)**2 + (evento.y-y)**2 <= 39**2:
                estado["seleccion"] = nodo
                vecinos = ", ".join(f"{v}: {p} min" for v, p in grafo[nodo].items())
                detalle.set(f"{nodo} - {NOMBRES[nodo]} | Conexiones: {vecinos}")
                break
        if estado["seleccion"] is None:
            detalle.set("Haz clic en un municipio para consultar sus conexiones.")
        dibujar()

    def arrastrar(evento):
        if estado["seleccion"]:
            posiciones[estado["seleccion"]] = (max(42, min(718, evento.x)),
                                                max(42, min(378, evento.y)))
            dibujar()

    def restablecer():
        posiciones.update(POSICIONES)
        calcular()

    # 5. Controles sencillos para comparar los tres algoritmos.
    tk.Label(ventana, text="EpiRed | BFS, DFS y UCS", font=("Arial", 18, "bold")).pack(pady=6)
    tk.Label(ventana, text="Líneas: conexiones. Números: minutos ficticios. Puedes arrastrar los nodos.").pack()
    controles = tk.Frame(ventana)
    controles.pack(pady=6)
    for texto, variable, opciones in [("Algoritmo", metodo, list(algoritmos)),
            ("Origen", origen, list(grafo)), ("Destino", destino, list(grafo))]:
        tk.Label(controles, text=texto).pack(side="left", padx=4)
        lista = ttk.Combobox(controles, textvariable=variable, values=opciones,
                             state="readonly", width=5)
        lista.pack(side="left")
        lista.bind("<<ComboboxSelected>>", calcular)
    tk.Checkbutton(controles, text="Tiempos", variable=tiempos,
                   command=dibujar).pack(side="left", padx=5)
    tk.Button(controles, text="Restablecer posiciones", command=restablecer).pack(side="left")
    lienzo = tk.Canvas(ventana, width=760, height=420, bg="white", highlightthickness=0)
    lienzo.pack()
    tk.Label(ventana, text="Verde: origen | Morado: destino | Naranja: ruta | Rojo: conexiones seleccionadas").pack(pady=3)
    tk.Label(ventana, textvariable=resultado, font=("Arial", 10), height=3).pack()
    tk.Label(ventana, textvariable=detalle, wraplength=740, height=2).pack()
    lienzo.bind("<Button-1>", seleccionar)
    lienzo.bind("<B1-Motion>", arrastrar)
    calcular()
    ventana.mainloop()


if __name__ == "__main__":
    from taller import GRAFO, bfs, dfs, ucs
    mostrar_grafo(GRAFO, {"BFS": bfs, "DFS": dfs, "UCS": ucs})
