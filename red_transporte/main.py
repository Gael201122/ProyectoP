"""Programa principal: red de transporte con ruta minima (Dijkstra)."""

from typing import List

from almacenamiento import (
    cargar_conexiones,
    construir_grafo,
    guardar_conexion,
)
from dijkstra import dijkstra
from entrada import pedir_nodo, pedir_opcion, pedir_peso
from excepciones import RedTransporteError
from modelos import Conexion

ARCHIVO_CSV: str = "conexiones.csv"

MENU: str = """
=== RED DE TRANSPORTE ===
1. Agregar conexion
2. Listar conexiones
3. Calcular ruta mas corta (Dijkstra)
4. Salir
"""


def opcion_agregar() -> None:
    """Captura una conexion nueva y la guarda en el CSV."""
    origen = pedir_nodo("Nodo origen: ")
    destino = pedir_nodo("Nodo destino: ")
    if origen == destino:
        print("  El origen y el destino no pueden ser el mismo nodo.")
        return
    peso = pedir_peso("Peso (distancia/costo): ")
    guardar_conexion(ARCHIVO_CSV, Conexion(origen, destino, peso))
    print(f"  Conexion guardada: {origen} <-> {destino} ({peso:g})")


def opcion_listar() -> None:
    """Muestra las conexiones almacenadas."""
    conexiones: List[Conexion] = cargar_conexiones(ARCHIVO_CSV)
    if not conexiones:
        print("  Aun no hay conexiones registradas.")
        return
    for c in conexiones:
        print(f"  {c.origen} <-> {c.destino}: {c.peso:g}")


def opcion_ruta() -> None:
    """Carga el grafo desde el CSV y ejecuta Dijkstra."""
    grafo = construir_grafo(cargar_conexiones(ARCHIVO_CSV))
    if not grafo.nodos():
        print("  Primero agrega conexiones.")
        return
    print("  Nodos disponibles:", ", ".join(grafo.nodos()))
    origen = pedir_nodo("Nodo origen: ")
    destino = pedir_nodo("Nodo destino: ")
    distancia, ruta = dijkstra(grafo, origen, destino)
    print(f"  Distancia total: {distancia:g}")
    print("  Ruta: " + " -> ".join(ruta))


def main() -> None:
    """Ciclo principal del menu."""
    acciones = {1: opcion_agregar, 2: opcion_listar, 3: opcion_ruta}
    while True:
        print(MENU)
        try:
            opcion = pedir_opcion("Opcion: ", range(1, 5))
            if opcion == 4:
                print("Hasta luego.")
                break
            acciones[opcion]()
        except RedTransporteError as error:
            print(f"  Error: {error}")
        except (KeyboardInterrupt, EOFError):
            print("\nPrograma interrumpido. Hasta luego.")
            break


if __name__ == "__main__":
    main()
