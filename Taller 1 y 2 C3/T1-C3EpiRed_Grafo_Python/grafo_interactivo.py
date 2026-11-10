"""Ejecutar junto a welsh_powell.py. Solo usa Tkinter, incluido con Python."""
import tkinter as tk
from welsh_powell import grafo_conflictos, welsh_powell

# PASO 1. Reutilizar el algoritmo del taller y ubicar las ocho zonas.
grados, orden, colores = welsh_powell(grafo_conflictos)
inicio = {"Centro": (380, 60), "Norte": (160, 145), "Sur": (680, 280),
          "Oriente": (600, 145), "Occidente": (380, 240), "Suba": (80, 280),
          "Kennedy": (540, 360), "Engativá": (220, 360)}
posiciones = inicio.copy()
paleta = {1: "#93c5fd", 2: "#fdba74", 3: "#c4b5fd"}
seleccionada = None


# PASO 2. Dibujar cada conflicto una vez y colorear las zonas por turno.
def dibujar():
    lienzo.delete("all")
    for zona, vecinos in grafo_conflictos.items():
        for vecino in vecinos:
            if zona < vecino:  # Evita dibujar dos veces una misma conexión.
                activa = seleccionada in (zona, vecino)
                lienzo.create_line(*posiciones[zona], *posiciones[vecino],
                                   fill="#dc2626" if activa else "#94a3b8",
                                   width=3 if activa else 2, tags="arista")
    for zona, (x, y) in posiciones.items():
        fondo = paleta[colores[zona]] if mostrar.get() else "#e2e8f0"
        lienzo.create_oval(x-42, y-42, x+42, y+42, fill=fondo,
                           outline="#0f172a", width=3 if zona == seleccionada else 1,
                           tags="vertice")
        etiqueta = f"{zona}\nTurno {colores[zona]}" if mostrar.get() else zona
        lienzo.create_text(x, y, text=etiqueta, font=("Arial", 10, "bold"))


# PASO 3. Al hacer clic, seleccionar una zona y mostrar sus conflictos.
def seleccionar(evento):
    global seleccionada
    seleccionada = None
    for zona, (x, y) in posiciones.items():
        if (evento.x-x)**2 + (evento.y-y)**2 <= 42**2:
            seleccionada = zona
            break
    if seleccionada:
        z = seleccionada
        detalle.set(f"{z} | Grado: {grados[z]} | Turno: {colores[z]}\n"
                    f"Conflictos: {', '.join(grafo_conflictos[z])}")
    else:
        detalle.set("Haz clic en una zona para consultar sus conflictos.")
    dibujar()


# PASO 4. Arrastrar cambia la posición del dibujo, no los conflictos ni turnos.
def arrastrar(evento):
    if seleccionada:
        posiciones[seleccionada] = (max(45, min(715, evento.x)),
                                    max(45, min(375, evento.y)))
        dibujar()


def restablecer():
    global seleccionada
    posiciones.update(inicio)
    seleccionada = None
    detalle.set("Haz clic en una zona para consultar sus conflictos.")
    dibujar()


# PASO 5. Crear la ventana y conectar el ratón con las funciones anteriores.
if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.title("EpiRed - Grafo de conflictos y turnos")
    ventana.geometry("+20+20")
    ventana.resizable(False, False)
    tk.Label(ventana, text="EpiRed | Welsh-Powell", font=("Arial", 19, "bold")).pack(pady=8)
    tk.Label(ventana, text="Una línea es un conflicto. Haz clic o arrastra una zona.").pack()
    controles = tk.Frame(ventana)
    controles.pack(pady=6)
    mostrar = tk.BooleanVar(value=True)
    tk.Checkbutton(controles, text="Mostrar turnos", variable=mostrar,
                   command=dibujar).pack(side="left", padx=10)
    tk.Button(controles, text="Restablecer posiciones", command=restablecer).pack(side="left")
    lienzo = tk.Canvas(ventana, width=760, height=420, bg="white", highlightthickness=0)
    lienzo.pack()
    leyenda = tk.Frame(ventana)
    leyenda.pack(pady=6)
    for turno in sorted(paleta):
        tk.Label(leyenda, text=f"Turno {turno}", bg=paleta[turno],
                 padx=15, pady=4).pack(side="left", padx=8)
    detalle = tk.StringVar(value="Haz clic en una zona para consultar sus conflictos.")
    tk.Label(ventana, textvariable=detalle, height=3, font=("Arial", 10)).pack()
    lienzo.bind("<Button-1>", seleccionar)
    lienzo.bind("<B1-Motion>", arrastrar)
    dibujar()
    ventana.mainloop()
