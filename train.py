import json
import os
import string
import pickle

import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.linear_model import LogisticRegression


#  CONFIGURACIÓN DE RUTAS
try:
    ruta_script = os.path.dirname(os.path.abspath(__file__))
except NameError:
    ruta_script = os.path.abspath(os.getcwd())

ruta_json = os.path.join(ruta_script, "intents.json")
ruta_models = os.path.join(ruta_script, "models")
os.makedirs(ruta_models, exist_ok=True)
ruta_modelo_pkl = os.path.join(ruta_models, "modelo.pkl")

#  CARGAR JSON
lemmatizer = WordNetLemmatizer()

try:
    with open(ruta_json, "r", encoding="utf-8") as file:
        datos = json.load(file)
except FileNotFoundError:
    print("Error: No se encontró el archivo 'intents.json' en la ruta:")
    print(ruta_json)
    raise SystemExit

palabras = []    # vocabulario
clases = []      # etiquetas (intents)
documentos = []  # lista de (tokens, etiqueta)

print("Iniciando procesamiento de texto...")

for intencion in datos["intenciones"]:
    etiqueta = intencion["etiqueta"]

    # registrar etiqueta si no está
    if etiqueta not in clases:
        clases.append(etiqueta)

    for patron in intencion["patrones"]:
        # tokenizar
        tokens = nltk.word_tokenize(patron)

        # limpiar y lematizar
        tokens_limpios = []
        for t in tokens:
            if t not in string.punctuation:
                tokens_limpios.append(lemmatizer.lemmatize(t.lower()))

        palabras.extend(tokens_limpios)
        documentos.append((tokens_limpios, etiqueta))

# quitar duplicados y ordenar
palabras = sorted(list(set(palabras)))
clases = sorted(list(set(clases)))

print("-" * 50)
print(f"Proceso completado.")
print(f" {len(documentos)} documentos (patrones) encontrados.")
print(f" {len(clases)} clases (etiquetas) encontradas: {clases}")
print(f" {len(palabras)} palabras únicas (vocabulario) encontradas.")
print("-" * 50)

#  CREAR VECTORES
def crear_bolsa_de_palabras(tokens, vocabulario):
    """Convierte una lista de tokens en un vector BoW según el vocabulario."""
    bag = []
    for w in vocabulario:
        bag.append(1 if w in tokens else 0)
    return np.array(bag, dtype=np.float32)

X = []
y = []

for tokens, etiqueta in documentos:
    bow = crear_bolsa_de_palabras(tokens, palabras)
    X.append(bow)

    # usamos índice de la etiqueta como clase numérica
    indice_clase = clases.index(etiqueta)
    y.append(indice_clase)

X = np.array(X)
y = np.array(y)

print("Tamaño de X (patrones):", X.shape)
print("Tamaño de y (clases):  ", y.shape)

#  ENTRENAR MODELO
print("\nEntrenando modelo de clasificación (LogisticRegression)...")

modelo = LogisticRegression(max_iter=1000)
modelo.fit(X, y)

print("Entrenamiento completado.")

#  GUARDAR MODELO
data = {
    "model": modelo,
    "palabras": palabras,
    "clases": clases
}

with open(ruta_modelo_pkl, "wb") as f:
    pickle.dump(data, f)

print("\nModelo guardado en:", ruta_modelo_pkl)
print("¡Listo! Ahora puedes usar este modelo desde main.py.")