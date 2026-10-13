import customtkinter as ctk
import math

from modelos import calcular_eoq


# CONFIGURACIÓN GENERAL

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("Sistema de Inventarios")
app.geometry("900x700")


# FUNCIONES DE NAVEGACIÓN

def abrir_eoq():
    inicio.pack_forget()
    pantalla_eoq.pack(fill="both", expand=True)

def volver_inicio():
    pantalla_eoq.pack_forget()
    inicio.pack(fill="both", expand=True)


# FUNCIÓN DEL BOTÓN CALCULAR

def ejecutar_eoq():

    try:
        demanda = float(entrada_demanda.get())
        costo = float(entrada_costo.get())
        almacenamiento = float(entrada_almacenamiento.get())
        dias = float(entrada_dias.get())

        valores = [demanda, costo, almacenamiento, dias]

        if not all(math.isfinite(valor) and valor > 0 for valor in valores):
            raise ValueError

        # Enviar variables de entrada al modelo
        datos = calcular_eoq(
            demanda,
            costo,
            almacenamiento,
            dias
        )

        proceso_eoq.configure(
    text=(
        "EOQ = √((2 × D × S) / H)\n\n"
        f"EOQ = √((2 × {demanda:g} × {costo:g}) / {almacenamiento:g})\n\n"
        f"EOQ = {datos['eoq']:.2f} unidades"
    )
)

        # Mostrar variables de salida
        resultado.configure(
            text=(
                f"Cantidad óptima: {datos['eoq']:.2f} unidades\n\n"
                f"Pedidos anuales: {datos['pedidos_anuales']:.2f}\n\n"
                f"Tiempo entre pedidos: {datos['tiempo_pedidos']:.2f} días\n\n"
                f"Costo de ordenar: ${datos['costo_ordenar']:,.2f}\n\n"
                f"Costo de almacenar: ${datos['costo_almacenar']:,.2f}\n\n"
                f"Costo anual relevante: ${datos['costo_total']:,.2f}"
            )
        )

    except ValueError:
        resultado.configure(
            text="Introduce números válidos mayores que cero."
        )


# PANTALLA PRINCIPAL

inicio = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

inicio.pack(fill="both", expand=True)


titulo = ctk.CTkLabel(
    inicio,
    text="Sistema de Modelos de Inventario",
    font=("Arial", 28, "bold")
)

titulo.pack(pady=40)


boton_eoq = ctk.CTkButton(
    inicio,
    text="Modelo EOQ",
    width=220,
    height=45,
    command=abrir_eoq
)

boton_eoq.pack(pady=15)


# PANTALLA EOQ

pantalla_eoq = ctk.CTkScrollableFrame(
    app,
    fg_color="transparent"
)

def desplazar_touchpad(event):

    if not pantalla_eoq.winfo_ismapped():
        return

    canvas = pantalla_eoq._parent_canvas

    delta_x, delta_y = app.tk.call(
        "tk::PreciseScrollDeltas",
        event.delta
    )

    delta_y = float(delta_y)

    if delta_y == 0:
        return

    canvas.update_idletasks()

    # Obtener el tamaño total del contenido
    zona = canvas.bbox("all")

    if zona is None:
        return

    altura_total = zona[3] - zona[1]
    altura_visible = canvas.winfo_height()

    # Si todo cabe en pantalla, no hay nada que desplazar
    if altura_total <= altura_visible:
        return

    # Posición actual del scroll
    posicion_actual = canvas.yview()[0]

    # Mover proporcionalmente al gesto del touchpad
    nueva_posicion = posicion_actual - (delta_y / altura_total)

    # Evitar salirnos de los límites
    nueva_posicion = max(0.0, min(1.0, nueva_posicion))

    canvas.yview_moveto(nueva_posicion)


app.bind_all(
    "<TouchpadScroll>",
    desplazar_touchpad,
    add="+"
)
        
def controlar_barra_eoq(inicio_scroll, fin_scroll):
    barra = pantalla_eoq._scrollbar

    barra.set(inicio_scroll, fin_scroll)

    inicio_scroll = float(inicio_scroll)
    fin_scroll = float(fin_scroll)

    if inicio_scroll <= 0.0 and fin_scroll >= 1.0:
        barra.grid_remove()
    else:
        barra.grid()


pantalla_eoq._parent_canvas.configure(
    yscrollcommand=controlar_barra_eoq
)


titulo_eoq = ctk.CTkLabel(
    pantalla_eoq,
    text="Cantidad Económica de Pedido (EOQ)",
    font=("Arial", 25, "bold")
)
titulo_eoq.pack(pady=20)

# VARIABLES DE ENTRADA

frame_entradas = ctk.CTkFrame(pantalla_eoq)
frame_entradas.pack(padx=30, pady=10, fill="x")

titulo_entradas = ctk.CTkLabel(
    frame_entradas,
    text="Variables de entrada",
    font=("Arial", 18, "bold")
)
titulo_entradas.grid(
    row=0,
    column=0,
    columnspan=2,
    pady=15
)


ctk.CTkLabel(
    frame_entradas,
    text="Demanda anual (D):"
).grid(row=1, column=0, padx=20, pady=8, sticky="w")

entrada_demanda = ctk.CTkEntry(
    frame_entradas,
    width=250
)
entrada_demanda.grid(row=1, column=1, padx=20, pady=8)


ctk.CTkLabel(
    frame_entradas,
    text="Costo por pedido (S):"
).grid(row=2, column=0, padx=20, pady=8, sticky="w")

entrada_costo = ctk.CTkEntry(
    frame_entradas,
    width=250
)
entrada_costo.grid(row=2, column=1, padx=20, pady=8)


ctk.CTkLabel(
    frame_entradas,
    text="Costo de almacenamiento anual (H):"
).grid(row=3, column=0, padx=20, pady=8, sticky="w")

entrada_almacenamiento = ctk.CTkEntry(
    frame_entradas,
    width=250
)
entrada_almacenamiento.grid(row=3, column=1, padx=20, pady=8)


ctk.CTkLabel(
    frame_entradas,
    text="Días de operación al año:"
).grid(row=4, column=0, padx=20, pady=8, sticky="w")

entrada_dias = ctk.CTkEntry(
    frame_entradas,
    width=250
)
entrada_dias.grid(row=4, column=1, padx=20, pady=8)


boton_calcular = ctk.CTkButton(
    frame_entradas,
    text="CALCULAR",
    command=ejecutar_eoq
)
boton_calcular.grid(
    row=5,
    column=0,
    columnspan=2,
    pady=15
)

# PROCESO

frame_proceso = ctk.CTkFrame(pantalla_eoq)
frame_proceso.pack(padx=30, pady=10, fill="x")

titulo_proceso = ctk.CTkLabel(
    frame_proceso,
    text="Proceso",
    font=("Arial", 18, "bold")
)
titulo_proceso.pack(pady=10)

proceso_eoq = ctk.CTkLabel(
    frame_proceso,
    text="EOQ = √((2 × D × S) / H)",
    font=("Arial", 14)
)
proceso_eoq.pack(pady=10)

# VARIABLES DE SALIDA

frame_salidas = ctk.CTkFrame(pantalla_eoq)
frame_salidas.pack(padx=30, pady=10, fill="x")

titulo_salidas = ctk.CTkLabel(
    frame_salidas,
    text="Variables de salida",
    font=("Arial", 18, "bold")
)
titulo_salidas.pack(pady=10)

resultado = ctk.CTkLabel(
    frame_salidas,
    text="Introduce los datos para calcular.",
    font=("Arial", 14),
    justify="left"
)
resultado.pack(pady=10)

# BOTÓN VOLVER

boton_volver = ctk.CTkButton(
    pantalla_eoq,
    text="Volver al inicio",
    command=volver_inicio
)
boton_volver.pack(pady=15)
app.mainloop()
