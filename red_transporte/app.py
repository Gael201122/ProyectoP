"""Interfaz web (Streamlit) para la red de transporte.

Ejecutar desde la carpeta del proyecto:
    streamlit run app.py
"""

import os
from typing import List

import streamlit as st

from almacenamiento import (
    cargar_conexiones,
    construir_grafo,
    guardar_conexion,
)
from dijkstra import dijkstra
from excepciones import RedTransporteError
from modelos import Conexion

ARCHIVO_CSV: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "conexiones.csv"
)


def limpiar(texto: str) -> str:
    """Quita espacios sobrantes de un nombre de nodo."""
    return " ".join(texto.split())


def validar_conexion(origen: str, destino: str, peso: float) -> None:
    """Lanza ValueError si los datos de la conexion no son validos."""
    if not origen or not destino:
        raise ValueError("Origen y destino no pueden estar vacios.")
    if "," in origen or "," in destino:
        raise ValueError("Los nombres no pueden contener comas.")
    if origen == destino:
        raise ValueError("Origen y destino no pueden ser el mismo nodo.")
    if peso <= 0:
        raise ValueError("El peso debe ser un numero mayor a 0.")


def pestana_agregar() -> None:
    """Formulario para registrar una conexion nueva."""
    st.subheader("Agregar conexión")
    with st.form("form_conexion", clear_on_submit=True):
        origen = limpiar(st.text_input("Nodo origen"))
        destino = limpiar(st.text_input("Nodo destino"))
        peso = st.number_input(
            "Peso (distancia/costo)", min_value=0.0, value=1.0, step=1.0
        )
        enviado = st.form_submit_button("Guardar")
    if not enviado:
        return
    try:
        validar_conexion(origen, destino, float(peso))
        guardar_conexion(
            ARCHIVO_CSV, Conexion(origen, destino, float(peso))
        )
    except (ValueError, RedTransporteError) as error:
        st.error(str(error))
    else:
        st.success(f"Conexión guardada: {origen} ↔ {destino} ({peso:g})")


def pestana_listar() -> None:
    """Tabla con las conexiones almacenadas en el CSV."""
    st.subheader("Conexiones registradas")
    try:
        conexiones: List[Conexion] = cargar_conexiones(ARCHIVO_CSV)
    except RedTransporteError as error:
        st.error(str(error))
        return
    if not conexiones:
        st.info("Aún no hay conexiones registradas.")
        return
    st.dataframe(
        [
            {"Origen": c.origen, "Destino": c.destino, "Peso": c.peso}
            for c in conexiones
        ],
        use_container_width=True,
    )


def pestana_ruta() -> None:
    """Calcula la ruta mas corta con Dijkstra."""
    st.subheader("Ruta más corta (Dijkstra)")
    try:
        grafo = construir_grafo(cargar_conexiones(ARCHIVO_CSV))
    except RedTransporteError as error:
        st.error(str(error))
        return
    nodos = grafo.nodos()
    if len(nodos) < 2:
        st.info("Agrega al menos una conexión para calcular rutas.")
        return
    origen = st.selectbox("Nodo origen", nodos, key="ruta_origen")
    destino = st.selectbox("Nodo destino", nodos, key="ruta_destino")
    if st.button("Calcular ruta"):
        try:
            distancia, ruta = dijkstra(grafo, origen, destino)
        except RedTransporteError as error:
            st.error(str(error))
        else:
            st.metric("Distancia total", f"{distancia:g}")
            st.write("**Ruta:** " + " → ".join(ruta))


def main() -> None:
    """Arma la pagina con tres pestanas."""
    st.set_page_config(page_title="Red de transporte", page_icon="🚌")
    st.title("Red de transporte")
    agregar, listar, ruta = st.tabs(
        ["Agregar conexión", "Conexiones", "Ruta más corta"]
    )
    with agregar:
        pestana_agregar()
    with listar:
        pestana_listar()
    with ruta:
        pestana_ruta()


main()
