import random
import os
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import string

lemmatizer = WordNetLemmatizer()

def limpiar_y_tokenizar(texto: str):
    """
    Convierte el texto en minúsculas, lo tokeniza,
    quita signos de puntuación y lematiza cada palabra.
    """
    tokens_crudos = nltk.word_tokenize(texto.lower())
    tokens_limpios = []
    for t in tokens_crudos:
        if t not in string.punctuation:
            tokens_limpios.append(lemmatizer.lemmatize(t))
    return tokens_limpios

def bolsa_de_palabras(tokens, vocabulario):
    """
    Convierte una lista de tokens en un vector de bolsa de palabras (BoW),
    usando el mismo vocabulario que se usó en train.py.
    """
    bag = []
    for w in vocabulario:
        bag.append(1 if w in tokens else 0)
    return np.array(bag, dtype=np.float32)

# ============================================================
#   RESPUESTAS FALSAS (SIMULACIÓN CHATBOT UAdeC)
# ============================================================
FAKE_INTENTS = {
    "saludo": [
        "¡Hola! Soy el asistente virtual de la Universidad Autónoma de Coahuila. ¿En qué trámite te ayudo hoy?",
        "Bienvenido al chatbot de la UAdeC. Cuéntame, ¿qué trámite necesitas hacer?"
    ],
    "despedida": [
        "¡Hasta luego! Espero haberte ayudado con tus trámites de la UAdeC.",
        "Gracias por usar el asistente de la Universidad Autónoma de Coahuila. ¡Que tengas un excelente día!"
    ],
    "pago_semestre": [
        "Para pagar tu semestre en la UAdeC, debes entrar al Portal de Servicios Administrativos, generar tu boleta de pago UAdeC y cubrirla en línea o en bancos autorizados.",
        "El pago de reinscripción o semestre se realiza generando la boleta de pago UAdeC que se encuentra en el Portal de Servicios Administrativos. Consulta siempre fechas y montos actualizados."
    ],
    #"solicitar_creditos_educativos": [
    #    "Para créditos educativos, revisa la convocatoria vigente en Servicios Estudiantiles. Ahí verás requisitos y documentos.",
    #    "Los créditos educativos se solicitan en el área correspondiente dentro de la UAdeC. Prepara documentación como historial académico e identificación."
    #],
    "pago_cuota_mantenimiento": [
        "La cuota de mantenimiento aparece reflejada en la boleta de pago escuela. Puedes pagarla en línea o en los bancos autorizados.",
        "Para pagar la cuota de mantenimiento, debes entrar al Portal de Servicios Administrativos, generar tu boleta de pago escuela y cubrirla en línea o en bancos autorizados."
    ],
    "consulta_estado_cuenta": [
        "Si quieres checar tu estado de cuenta universitario: se consulta en el Portal de Servicios Administrativos, en el apartado de Estado de Cuenta UAdeC pero si quieres checar tu estado de cuenta facultativo entonces es en el apartado de Estado de Cuenta Escuela. Ahí verás cargos y pagos.  ",
        "Para revisar tus estados de cuenta, entra a la SIIA UAdeC y accede a los apartados de Estado de Cuenta UAdeC o Estado de Cuenta Escuela, dependiendo de cual es tu motivo."
    ],
    "consulta_estado_cuenta_escuela": [
        "Tu estado de cuenta se consulta en el Portal de Servicios Administrativos, en el apartado de Estado de Cuenta Escuela. Ahí verás cargos y pagos.",
        "Para revisar tu estado de cuenta de tu facultad, entra a la SIIA UAdeC y accede al apartado de Estado de Cuenta Escuela."
    ],
    "consulta_estado_cuenta_uadec": [
        "Tu estado de cuenta de la UAdeC se consulta en el Portal de Servicios Administrativos, en el apartado de Estado de Cuenta UAdeC. Ahí verás cargos y pagos.",
        "Para revisar tu estado de cuenta de la universidad, entra a la SIIA UAdeC y accede al apartado de Estado de Cuenta UAdeC."
    ],
    "ayuda_horario": [
        "La selección de horario se hace en línea, en las fechas señaladas por tu facultad. Revisa la oferta de materias antes.",
        "Para inscribir materias, verifica las fechas de selección de horario y genera tu horario en el Sistema de Inscripción Académica."
    ],
    "consulta_calendario_universitario": [
        "Puedes consultar el calendario universitario en la página oficial de la UAdeC, sección Acerca De y en Calendario.",
        "El calendario escolar incluye pagos, exámenes e inicios de semestre. Está disponible en la página oficial de la UAdeC."
    #],
    #"consulta_creditos_escolares": [
    #    "Tus créditos escolares están en tu historial académico dentro del portal de alumnos.",
    #    "Para ver tus créditos acumulados, entra al sistema UAdeC y consulta tu avance del plan de estudios."
    ],
    "info_contacto_escolar": [
        "Puedes contactar al departamento escolar mediante los correos y teléfonos oficiales listados en la página oficial de la UAdeC de tu facultad.",
        "Para atención escolar, revisa el directorio de tu facultad en la página de la UAdeC. Ahí están los correos institucionales.",
        "Para atención dentro de tu facultad, sigue las redes sociales de tu facultad. Y en Teams contacta al personal de tu facultad."
    ],
    "ayuda_general": [
        "Puedo ayudarte con pagos, horarios, calendario, estado de cuenta y contacto escolar. Pregunta algo específico.",
        "Soy el asistente virtual de trámites UAdeC. Dime si tu duda es sobre pagos, horarios, calendarios o contacto con Escolar."
    ],
    "desconocido": [
        "No estoy seguro de cómo ayudarte con eso. ¿Puedes explicarlo con más detalle?",
        "Mmm… no entiendo esa parte. ¿Tu duda es sobre pagos, horario, calendario o estado de cuenta?"
    ],
}


# ============================================================
#   DETECCIÓN DE INTENTS (MEJORADA: PALABRAS CLAVE)
# ============================================================
def detectar_intent_falso(texto_usuario: str) -> str:
    texto = texto_usuario.lower()

    # ---- SALUDO ----
    if any(p in texto for p in ["hola", "buenas", "qué onda", "que onda", "hey", "buen día", "buen dia"]):
        return "saludo"

    # ---- DESPEDIDA ----
    if any(p in texto for p in ["adios", "adiós", "bye", "hasta luego", "nos vemos", "gracias eso es todo"]):
        return "despedida"

    # ---- PAGO DE SEMESTRE / REINSCRIPCIÓN ----
    if ("pago" in texto or "pagar" in texto or "colegiatura" in texto) and \
       ("semestre" in texto or "inscripción" in texto or "inscripcion" in texto or "reinscripcion" in texto):
        return "pago_semestre"

    # ---- CRÉDITOS EDUCATIVOS ----
    #if ("crédito" in texto or "credito" in texto or "financiamiento" in texto or "préstamo" in texto or "prestamo" in texto) and \
    #   ("educativo" in texto or "beca" in texto or "estudiantil" in texto):
    #    return "solicitar_creditos_educativos"

    # ---- CUOTA DE MANTENIMIENTO ----
    if ("cuota" in texto or "mantenimiento" in texto) and ("pago" in texto or "pagar" in texto):
        return "pago_cuota_mantenimiento"

    # ---- ESTADO DE CUENTA ----
    if ("estado" in texto and "cuenta" in texto) or \
       ("adeudo" in texto) or \
       ("saldo pendiente" in texto):
        return "consulta_estado_cuenta"

    # ---- HORARIO / INSCRIPCIÓN DE MATERIAS ----
    if ("horario" in texto) or \
       ("inscribir" in texto and "materias" in texto) or \
       ("cargar" in texto and "clases" in texto):
        return "ayuda_horario"

    # ---- CALENDARIO ESCOLAR ----
    if ("calendario" in texto) or \
       ("fechas importantes" in texto) or \
       ("cuando inicia" in texto and "semestre" in texto):
        return "consulta_calendario_universitario"

    # ---- CRÉDITOS ESCOLARES ----
    #if ("créditos" in texto or "creditos" in texto or "avance" in texto) and \
    #   ("escolares" in texto or "curricular" in texto or "plan de estudios" in texto):
    #    return "consulta_creditos_escolares"

    # ---- CONTACTO ESCOLAR ----
    if ("contacto" in texto or "correo" in texto or "teléfono" in texto or "telefono" in texto) and \
       ("escolar" in texto or "ventanilla" in texto):
        return "info_contacto_escolar"

    # ---- AYUDA GENERAL ----
    if any(p in texto for p in ["ayuda","ayudar"]):
        return "ayuda_general"

    # ---- SI NO COINCIDE NADA ----
    return "desconocido"


# ============================================================
#   RESPUESTAS
# ============================================================
def obtener_respuesta(intent: str, texto_usuario: str = "") -> str:
    """
    Devuelve una respuesta dependiendo del intent.
    Maneja caso especial de estado de cuenta (escuela / UAdeC)
    y regresa 'desconocido' si no hay una coincidencia válida.
    """
    texto = (texto_usuario or "").lower()

    if intent == "consulta_estado_cuenta":

        if "escuela" in texto or "facultad" in texto:
            respuestas = FAKE_INTENTS.get("consulta_estado_cuenta_escuela")

        elif "uadec" in texto or "universidad" in texto:
            respuestas = FAKE_INTENTS.get("consulta_estado_cuenta_uadec")

        else:
            respuestas = FAKE_INTENTS.get("consulta_estado_cuenta")

    else:
        respuestas = FAKE_INTENTS.get(intent)

    if not respuestas:
        respuestas = FAKE_INTENTS["desconocido"]

    return random.choice(respuestas)


# ============================================================
#   FUTURO: INTEGRAR MODELO REAL
# ============================================================
USAR_MODELO_REAL = True  # usamos el modelo entrenado

# variables globales donde guardaremos lo que carguemos del .pkl
modelo = None
palabras_vocab = []
clases = []

def cargar_modelo_real():
    """
    Carga el modelo entrenado y el vocabulario desde models/modelo.pkl.
    Debe coincidir con lo que guardamos en train.py.
    """
    global modelo, palabras_vocab, clases

    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_modelo = os.path.join(ruta_script, "models", "modelo.pkl")

    with open(ruta_modelo, "rb") as f:
        data = pickle.load(f)

    modelo = data["model"]
    palabras_vocab = data["palabras"]
    clases = data["clases"]

    #print("Modelo cargado correctamente. Clases disponibles:", clases)

def predecir_intent_real(texto_usuario: str) -> str:
    """
    Usa el modelo real para predecir la intención del usuario.
    1) Limpia y tokeniza el texto
    2) Lo convierte a bolsa de palabras
    3) Predice con el modelo
    4) Regresa la etiqueta (intent) correspondiente
    """
    if modelo is None:
        # por seguridad, si alguien llama a esto sin cargar el modelo
        cargar_modelo_real()

    tokens = limpiar_y_tokenizar(texto_usuario)
    bow = bolsa_de_palabras(tokens, palabras_vocab).reshape(1, -1)

    indice_predicho = modelo.predict(bow)[0]  # es un número (índice)
    intent = clases[indice_predicho]          # lo convertimos a etiqueta

    return intent

def contiene_palabra_credito(texto: str) -> bool:
    """Detecta si el usuario está hablando de créditos."""
    texto = texto.lower()
    palabras_credito = ["credito", "crédito", "creditos", "créditos"]
    return any(p in texto for p in palabras_credito)

# ============================================================
#   PROGRAMA PRINCIPAL
# ============================================================
def main():
    print("================================================")
    print("   CHATBOT DE TRÁMITES - UNIVERSIDAD AUTÓNOMA   ")
    print("               DE COAHUILA (UAdeC)              ")
    print("================================================")
    print("Puedo orientarte en pagos,")
    print("estado de cuenta, horarios, calendario y escolar.")
    print("Escribe 'salir' para terminar.\n")

    if USAR_MODELO_REAL:
        cargar_modelo_real()

    while True:
        texto_usuario = input("Tú: ")
        texto_lower = texto_usuario.strip().lower()
        if texto_lower in ["salir", "exit", "quit"]:
            print("Chatbot: ¡Hasta luego!")
            break

        if contiene_palabra_credito(texto_lower):
            intent = "desconocido"
        else:
            if USAR_MODELO_REAL:
                intent = predecir_intent_real(texto_usuario)
            else:
                intent = detectar_intent_falso(texto_usuario)

        print("Chatbot:", obtener_respuesta(intent, texto_usuario))


if __name__ == "__main__":
    main()