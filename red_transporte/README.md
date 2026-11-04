# Proyecto 1: Algoritmo de Dijkstra

**Alumno:** Roberto Gael Torres Cervantes
**Código:** 225361202
**Materia:** Programación III

Programa modular en Python 3 que registra conexiones entre nodos
(con peso), las guarda en `conexiones.csv` y calcula la ruta más
corta con el algoritmo de Dijkstra.

## Estructura
- `main.py`: menú interactivo
- `entrada.py`: captura validada con try/except
- `almacenamiento.py`: lectura/escritura del CSV y construcción del grafo
- `modelos.py`: clases `Conexion` y `Grafo` (POO)
- `dijkstra.py`: algoritmo con cola de prioridad (`heapq`)
- `excepciones.py`: excepciones propias
- `app.py`: interfaz web opcional con Streamlit
- `tests/`: pruebas unitarias

## Uso
    python main.py
    python -m unittest discover -s tests
    flake8

Interfaz web opcional (requiere `pip install -r requirements.txt`):

    streamlit run app.py

## Nota
La conexión A-B de `conexiones.csv` se agregó como prueba del
ingreso interactivo de datos.