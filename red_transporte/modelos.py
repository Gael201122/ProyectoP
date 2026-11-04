"""Modelos del dominio: conexiones y grafo ponderado."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Conexion:
    """Arista entre dos nodos con un peso (distancia, tiempo o costo)."""

    origen: str
    destino: str
    peso: float


class Grafo:
    """Grafo ponderado representado con listas de adyacencia."""

    def __init__(self, dirigido: bool = False) -> None:
        self._dirigido: bool = dirigido
        self._adyacencia: Dict[str, Dict[str, float]] = {}

    def agregar_nodo(self, nodo: str) -> None:
        """Agrega un nodo si todavia no existe."""
        self._adyacencia.setdefault(nodo, {})

    def agregar_conexion(self, conexion: Conexion) -> None:
        """Agrega (o actualiza) una conexion entre dos nodos."""
        self.agregar_nodo(conexion.origen)
        self.agregar_nodo(conexion.destino)
        self._adyacencia[conexion.origen][conexion.destino] = conexion.peso
        if not self._dirigido:
            self._adyacencia[conexion.destino][conexion.origen] = (
                conexion.peso
            )

    def existe_nodo(self, nodo: str) -> bool:
        """Indica si el nodo pertenece al grafo."""
        return nodo in self._adyacencia

    def nodos(self) -> List[str]:
        """Devuelve los nodos ordenados alfabeticamente."""
        return sorted(self._adyacencia)

    def vecinos(self, nodo: str) -> Dict[str, float]:
        """Devuelve {vecino: peso} del nodo dado."""
        return self._adyacencia[nodo]
