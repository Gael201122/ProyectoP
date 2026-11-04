"""Captura interactiva y validada de datos del usuario."""

import math


def pedir_nodo(mensaje: str) -> str:
    """Pide el nombre de un nodo; repite hasta recibir texto valido."""
    while True:
        try:
            texto = " ".join(input(mensaje).split())
            if not texto:
                raise ValueError("El nombre no puede estar vacio.")
            if "," in texto:
                raise ValueError("El nombre no puede contener comas.")
            return texto
        except ValueError as error:
            print(f"  Entrada invalida: {error}")


def pedir_peso(mensaje: str) -> float:
    """Pide un peso numerico positivo y finito."""
    while True:
        try:
            peso = float(input(mensaje).strip())
            if not math.isfinite(peso) or peso <= 0:
                raise ValueError("El peso debe ser un numero mayor a 0.")
            return peso
        except ValueError as error:
            print(f"  Entrada invalida: {error}")


def pedir_opcion(mensaje: str, validas: range) -> int:
    """Pide una opcion entera dentro del rango dado."""
    while True:
        try:
            opcion = int(input(mensaje).strip())
            if opcion not in validas:
                raise ValueError(
                    f"Elige un numero entre {validas.start} "
                    f"y {validas.stop - 1}."
                )
            return opcion
        except ValueError as error:
            print(f"  Entrada invalida: {error}")
