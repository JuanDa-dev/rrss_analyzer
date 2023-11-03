
import os
import networkx as nx 

def find_files(directory, filename):
    """
    Busca archivos con el nombre especificado en el directorio y sus subdirectorios.
    Devuelve una lista con las rutas de los archivos encontrados.
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for file in filenames:
            if file == filename:
                files.append(os.path.join(root, file))
    return files


