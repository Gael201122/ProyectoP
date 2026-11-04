"""Persistencia de las conexiones en un archivo CSV."""

import csv
import math
import os
from typing import List

from excepciones import ArchivoInvalidoError
from modelos import Conexion, Grafo

ENCABEZADO: List[str] = ["origen", "destino", "peso"]


def guardar_conexion(ruta: str, conexion: Conexion) -> None:
    """Agrega una conexion al CSV (crea el archivo y encabezado si falta)."""
    try:
        es_nuevo = (
            not os.path.exists(ruta) or os.path.getsize(ruta) == 0
        )
        with open(ruta, "a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            if es_nuevo:
                escritor.writerow(ENCABEZADO)
            escritor.writerow(
                [conexion.origen, conexion.destino, conexion.peso]
            )
    except OSError as error:
        raise ArchivoInvalidoError(
            f"No se pudo escribir en '{ruta}': {error}"
        ) from error


def _fila_a_conexion(fila: List[str], numero: int) -> Conexion:
    """Convierte una fila del CSV en Conexion validando su contenido."""
    if len(fila) != 3:
        raise ArchivoInvalidoError(
            f"Fila {numero}: se esperaban 3 columnas, hay {len(fila)}."
        )
    origen, destino, texto_peso = (campo.strip() for campo in fila)
    try:
        peso = float(texto_peso)
    except ValueError as error:
        raise ArchivoInvalidoError(
            f"Fila {numero}: peso invalido '{texto_peso}'."
        ) from error
    if not origen or not destino or peso <= 0 or not math.isfinite(peso):
        raise ArchivoInvalidoError(f"Fila {numero}: datos invalidos.")
    return Conexion(origen, destino, peso)


def cargar_conexiones(ruta: str) -> List[Conexion]:
    """Lee todas las conexiones del CSV. Si no existe, devuelve []."""
    if not os.path.exists(ruta):
        return []
    conexiones: List[Conexion] = []
    try:
        with open(ruta, newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            next(lector, None)  # se omite el encabezado
            for numero, fila in enumerate(lector, start=2):
                if fila:
                    conexiones.append(_fila_a_conexion(fila, numero))
    except OSError as error:
        raise ArchivoInvalidoError(
            f"No se pudo leer '{ruta}': {error}"
        ) from error
    return conexiones


def construir_grafo(conexiones: List[Conexion]) -> Grafo:
    """Instancia el grafo en memoria a partir de las conexiones."""
    grafo = Grafo()
    for conexion in conexiones:
        grafo.agregar_conexion(conexion)
    return grafo
