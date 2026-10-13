import math

def calcular_eoq(demanda, costo_pedido, almacenamiento, dias):
    # Cantidad económica de pedido
    eoq = math.sqrt(
        (2 * demanda * costo_pedido) / almacenamiento
    )

    # Número de pedidos al año
    pedidos_anuales = demanda / eoq

    # Tiempo entre pedidos
    tiempo_pedidos = dias / pedidos_anuales

    # Costos anuales
    costo_ordenar = (demanda / eoq) * costo_pedido
    costo_almacenar = (eoq / 2) * almacenamiento

    costo_total = costo_ordenar + costo_almacenar

    # Variables de salida
    return {
        "eoq": eoq,
        "pedidos_anuales": pedidos_anuales,
        "tiempo_pedidos": tiempo_pedidos,
        "costo_ordenar": costo_ordenar,
        "costo_almacenar": costo_almacenar,
        "costo_total": costo_total
    }
