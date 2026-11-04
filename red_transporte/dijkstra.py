"""Algoritmo de Dijkstra con cola de prioridad (heapq)."""

import heapq
from typing import Dict, List, Optional, Tuple

from excepciones import NodoNoExisteError, SinRutaError
from modelos import Grafo


def _reconstruir_ruta(
    previo: Dict[str, Optional[str]], destino: str
) -> List[str]:
    """Reconstruye la ruta origen -> destino siguiendo los previos."""
    ruta: List[str] = []
    actual: Optional[str] = destino
    while actual is not None:
        ruta.append(actual)
        actual = previo[actual]
    ruta.reverse()
    return ruta


def dijkstra(
    grafo: Grafo, origen: str, destino: str
) -> Tuple[float, List[str]]:
    """Calcula la distancia minima y la ruta completa origen -> destino.

    Raises:
        NodoNoExisteError: si origen o destino no estan en el grafo.
        SinRutaError: si no hay camino entre ambos nodos.
    """
    for nodo in (origen, destino):
        if not grafo.existe_nodo(nodo):
            raise NodoNoExisteError(f"El nodo '{nodo}' no existe.")

    distancias: Dict[str, float] = {origen: 0.0}
    previo: Dict[str, Optional[str]] = {origen: None}
    visitados: set = set()
    cola: List[Tuple[float, str]] = [(0.0, origen)]

    while cola:
        distancia_actual, actual = heapq.heappop(cola)
        if actual in visitados:
            continue
        visitados.add(actual)
        if actual == destino:
            return distancia_actual, _reconstruir_ruta(previo, destino)

        for vecino, peso in grafo.vecinos(actual).items():
            nueva = distancia_actual + peso
            if nueva < distancias.get(vecino, float("inf")):
                distancias[vecino] = nueva
                previo[vecino] = actual
                heapq.heappush(cola, (nueva, vecino))

    raise SinRutaError(f"No hay ruta entre '{origen}' y '{destino}'.")
