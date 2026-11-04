"""Excepciones propias de la red de transporte."""


class RedTransporteError(Exception):
    """Clase base de los errores del dominio."""


class NodoNoExisteError(RedTransporteError):
    """El nodo solicitado no forma parte del grafo."""


class SinRutaError(RedTransporteError):
    """No existe camino entre el origen y el destino."""


class ArchivoInvalidoError(RedTransporteError):
    """El archivo CSV no se pudo leer o tiene un formato incorrecto."""
