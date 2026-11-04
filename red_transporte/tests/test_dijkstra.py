"""Pruebas unitarias de Dijkstra (ejecutar: python -m unittest)."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from almacenamiento import (  # noqa: E402
    cargar_conexiones,
    construir_grafo,
    guardar_conexion,
)
from dijkstra import dijkstra  # noqa: E402
from excepciones import (  # noqa: E402
    ArchivoInvalidoError,
    NodoNoExisteError,
    SinRutaError,
)
from modelos import Conexion  # noqa: E402


def _grafo_base():
    conexiones = [
        Conexion("A", "B", 4),
        Conexion("A", "C", 1),
        Conexion("C", "B", 2),
        Conexion("B", "D", 5),
        Conexion("X", "Y", 1),
    ]
    return construir_grafo(conexiones)


class PruebasDijkstra(unittest.TestCase):
    def test_ruta_minima(self):
        distancia, ruta = dijkstra(_grafo_base(), "A", "D")
        self.assertEqual(distancia, 8)
        self.assertEqual(ruta, ["A", "C", "B", "D"])

    def test_nodo_inexistente(self):
        with self.assertRaises(NodoNoExisteError):
            dijkstra(_grafo_base(), "A", "Z")

    def test_sin_ruta(self):
        with self.assertRaises(SinRutaError):
            dijkstra(_grafo_base(), "A", "X")

    def test_csv_ida_y_vuelta(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "c.csv")
            guardar_conexion(ruta, Conexion("A", "B", 3.5))
            self.assertEqual(
                cargar_conexiones(ruta), [Conexion("A", "B", 3.5)]
            )

    def test_csv_corrupto(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "c.csv")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("origen,destino,peso\nA,B,abc\n")
            with self.assertRaises(ArchivoInvalidoError):
                cargar_conexiones(ruta)


if __name__ == "__main__":
    unittest.main()
