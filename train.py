import json
import nltk
from nltk.stem import WordNetLemmatizer
import string
import os  # <-- Importamos la librería OS

# --- INICIO DE LA MODIFICACIÓN (Solución 2) ---
# Obtiene la ruta absoluta de la carpeta donde está ESTE SCRIPT
try:
    # __file__ existe si ejecutas el script directamente
    ruta_script = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Si __file__ no está definido (ej. en un intérprete interactivo)
    # usa el directorio de trabajo actual
    ruta_script = os.path.abspath(os.getcwd())

# Crea la ruta completa al archivo intents.json
ruta_json = os.path.join(ruta_script, 'intents.json')
# --- FIN DE LA MODIFICACIÓN ---


# 1. Inicializar el Lematizador (para reducir palabras a su raíz)
lemmatizer = WordNetLemmatizer()

# 2. Cargar el archivo JSON
try:
    # Usa la nueva variable 'ruta_json'
    with open(ruta_json, 'r', encoding='utf-8') as file:
        datos = json.load(file)
except FileNotFoundError:
    print(f"Error: No se encontró el archivo 'intents.json' en la ruta:")
    print(ruta_json)
    print("Asegúrate de haberlo creado en la misma carpeta que train.py.")
    exit()

# 3. Listas para almacenar nuestros datos procesados
palabras = []       # Todas las palabras (lematizadas)
clases = []         # Todas las etiquetas (intenciones)
documentos = []     # Pares (palabras, etiqueta)

print("Iniciando procesamiento de texto...")

# 4. Recorrer el JSON
for intencion in datos['intenciones']:
    for patron in intencion['patrones']:
        
        # 4.1. Tokenizar: Separar la oración en palabras
        lista_palabras = nltk.word_tokenize(patron)
        
        # 4.2. Lematizar y quitar puntuación
        palabras_procesadas = []
        for palabra in lista_palabras:
            # Si no es un signo de puntuación
            if palabra not in string.punctuation:
                # Convertir a minúscula y lematizar (reducir a raíz)
                palabras_procesadas.append(lemmatizer.lemmatize(palabra.lower()))
        
        # 4.3. Agregar a nuestras listas
        palabras.extend(palabras_procesadas)
        documentos.append((palabras_procesadas, intencion['etiqueta']))
        
        # 4.4. Agregar la etiqueta (si no está ya)
        if intencion['etiqueta'] not in clases:
            clases.append(intencion['etiqueta'])

# 5. Limpieza final: Quitar duplicados y ordenar
# Usamos set() para quitar duplicados automáticamente
palabras = sorted(list(set(palabras)))
clases = sorted(list(set(clases)))

print("-" * 50)
print(f"Proceso completado.")
print(f" {len(documentos)} documentos (patrones) encontrados.")
print(f" {len(clases)} clases (etiquetas) encontradas: {clases}")
print(f" {len(palabras)} palabras únicas (vocabulario) encontradas:")
print(palabras)
print("-" * 50)


