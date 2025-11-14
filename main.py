import random
# import pickle  # <- se usará en el futuro cuando carguemos modelo.pkl


# ============================================================
#   RESPUESTAS FALSAS (SIMULACIÓN DE CHATBOT UAdeC)
# ============================================================
FAKE_INTENTS = {
    "saludo": [
        "¡Hola! Soy el asistente virtual de la Universidad Autónoma de Coahuila. ¿En qué trámite te ayudo hoy?",
        "Bienvenido al chatbot de la UAdeC 🙌. Cuéntame, ¿qué trámite necesitas hacer?"
    ],
    "despedida": [
        "¡Hasta luego! Espero haberte ayudado con tus trámites de la UAdeC.",
        "Gracias por usar el asistente de la Universidad Autónoma de Coahuila. ¡Que tengas un excelente día!"
    ],
    "pago_semestre": [
        "Para pagar tu semestre en la UAdeC, normalmente debes entrar al portal de alumnos, generar tu ficha de pago y acudir al banco o hacer pago en línea. Verifica siempre las fechas límite en el calendario escolar.",
        "El pago de semestre se realiza generando la referencia de pago en el sistema de la UAdeC y cubriéndola en los bancos autorizados o en línea. Si tienes dudas específicas, te recomiendo contactar a Escolar o Finanzas."
    ],
    "solicitar_creditos_educativos": [
        "Los créditos educativos suelen gestionarse a través del área de Servicios Estudiantiles o Finanzas. Revisa los requisitos en la página de la UAdeC o pregunta por los convenios de crédito y becas.",
        "Para solicitar créditos educativos, consulta primero la convocatoria vigente y junta documentos como historial académico, identificación y comprobante de ingresos. Después se entrega la solicitud en el departamento correspondiente."
    ],
    "pago_cuota_mantenimiento": [
        "La cuota de mantenimiento normalmente se incluye en tu estado de cuenta o se genera como concepto aparte en el portal de pagos. Revisa tu referencia de pago y asegúrate de cubrirla antes de la fecha límite.",
        "Para pagar la cuota de mantenimiento, verifica en tu estado de cuenta el concepto y el monto exacto. Después puedes pagarlo en los bancos autorizados o mediante pago en línea según indique la UAdeC."
    ],
    "consulta_estado_cuenta": [
        "Para consultar tu estado de cuenta, entra al portal de alumnos de la UAdeC con tu matrícula y revisa la sección de Finanzas o Pagos. Ahí verás los cargos pendientes y los pagos registrados.",
        "Tu estado de cuenta se visualiza normalmente en el sistema de la UAdeC, en el apartado de pagos. Si no puedes acceder, acude a Escolar o Finanzas para que te apoyen."
    ],
    "ayuda_horario": [
        "Para la selección de horario, revisa primero el calendario de reinscripción y las materias ofertadas. Después, en el sistema de la UAdeC, podrás elegir grupos según tu avance y disponibilidad.",
        "La selección de horario se hace en línea, en las fechas indicadas por la UAdeC. Te recomiendo tener un horario tentativo con varias opciones de grupo por si alguno aparece lleno."
    ],
    "consulta_calendario_escolar": [
        "El calendario escolar de la UAdeC está disponible en la página oficial. Ahí encontrarás fechas de inscripciones, pagos, inicios de semestre, exámenes y vacaciones.",
        "Puedes consultar el calendario escolar buscando en la página de la Universidad Autónoma de Coahuila la sección de 'Calendario escolar' o 'Fechas importantes'."
    ],
    "consulta_creditos_escolares": [
        "Para revisar tus créditos escolares, entra al portal de alumnos y consulta tu historial académico o tu avance de plan de estudios. Ahí verás cuántos créditos llevas y cuántos te faltan.",
        "Tus créditos acumulados se muestran en tu historial académico dentro del sistema de la UAdeC. Si ves algo raro, acude con Escolar para aclararlo."
    ],
    "info_contacto_escolar": [
        "Para contactar al departamento escolar, revisa la página de tu facultad dentro de la UAdeC. Normalmente ahí aparecen correos, teléfonos y horarios de atención.",
        "Puedes comunicarte con Escolar mediante los teléfonos y correos oficiales publicados por la UAdeC. Te recomiendo anotar el correo institucional de tu facultad para futuras dudas."
    ],
    "ayuda_general": [
        "Puedo ayudarte con trámites como pago de semestre, créditos educativos, cuota de mantenimiento, estado de cuenta, horarios, calendario y créditos escolares. Intenta preguntar algo específico 😉.",
        "Soy el asistente de trámites de la UAdeC. Pregúntame sobre pagos, estado de cuenta, horarios, créditos o calendario escolar y haré lo posible por orientarte."
    ],
    "desconocido": [
        "No estoy seguro de cómo ayudarte con eso. ¿Puedes explicarlo con otras palabras o mencionar si es sobre pagos, horarios, créditos o calendario?",
        "Mmm… esa parte no la tengo registrada. Intenta decirme si tu duda es sobre pagos, créditos, horarios, calendario escolar o contacto con Escolar."
    ],
}


# ============================================================
#   DETECCIÓN DE INTENT FALSO (REGLAS SIMPLES)
#   LUEGO SE REEMPLAZARÁ POR EL MODELO REAL
# ============================================================
def detectar_intent_falso(texto_usuario: str) -> str:
    """
    Asigna una 'intención' falsa usando reglas súper simples.
    Más adelante, esta función se reemplazará por una
    predicción real basada en modelo ML.
    """
    texto = texto_usuario.lower()

    if any(p in texto for p in ["hola", "buenas", "qué onda", "buen dia", "buen día", "hey"]):
        return "saludo"

    if any(p in texto for p in ["adiós", "bye", "nos vemos", "hasta luego", "gracias, eso es todo"]):
        return "despedida"

    if any(p in texto for p in ["pagar semestre", "pago semestre", "colegiatura", "inscripción", "inscripcion"]):
        return "pago_semestre"

    if any(p in texto for p in ["crédito educativo", "credito educativo", "créditos educativos", "financiamiento", "prestamo para estudiar", "beca crédito"]):
        return "solicitar_creditos_educativos"

    if any(p in texto for p in ["cuota de mantenimiento", "mantenimiento", "cuota escolar", "cuota anual"]):
        return "pago_cuota_mantenimiento"

    if any(p in texto for p in ["estado de cuenta", "cuánto debo", "cuanto debo", "saldo pendiente", "adeudo"]):
        return "consulta_estado_cuenta"

    if any(p in texto for p in ["horario", "selección de horario", "seleccion de horario", "inscribir materias", "cargar materias", "clases"]):
        return "ayuda_horario"

    if any(p in texto for p in ["calendario escolar", "fechas importantes", "fechas de pago", "cuando inicia el semestre", "cuando empieza el semestre"]):
        return "consulta_calendario_escolar"

    if any(p in texto for p in ["créditos escolares", "creditos escolares", "créditos acumulados", "avance curricular", "porcentaje de la carrera"]):
        return "consulta_creditos_escolares"

    if any(p in texto for p in ["contacto escolar", "correo escolar", "teléfono escolar", "telefono escolar", "donde pregunto", "ventanilla"]):
        return "info_contacto_escolar"

    if any(p in texto for p in ["ayuda", "qué puedes hacer", "que puedes hacer", "no sé qué preguntar", "no se que preguntar"]):
        return "ayuda_general"

    return "desconocido"


def obtener_respuesta(intent: str) -> str:
    """
    Elige una respuesta aleatoria de la lista de respuestas para ese intent.
    """
    respuestas = FAKE_INTENTS.get(intent, FAKE_INTENTS["desconocido"])
    return random.choice(respuestas)


# ============================================================
#   (FUTURO) INTEGRACIÓN CON MODELO REAL
# ============================================================
USAR_MODELO_REAL = False  # Cambiar a True cuando A tenga modelo.pkl listo


def cargar_modelo_real():
    """
    FUTURO:
    Aquí se cargará el modelo entrenado (modelo.pkl)
    """
    # global modelo, vectorizer, tags
    # with open("models/modelo.pkl", "rb") as f:
    #     data = pickle.load(f)
    # modelo = data["model"]
    # vectorizer = data["vectorizer"]
    # tags = data["tags"]
    pass


def predecir_intent_real(texto_usuario: str) -> str:
    """
    FUTURO:
    Usará el modelo cargado para predecir el intent.
    """
    # X = vectorizer.transform([texto_usuario])
    # pred = modelo.predict(X)[0]
    # return pred
    return "desconocido"


# ============================================================
#   PROGRAMA PRINCIPAL
# ============================================================
def main():
    print("================================================")
    print("   CHATBOT DE TRÁMITES - UNIVERSIDAD AUTÓNOMA   ")
    print("                 DE COAHUILA (UAdeC)            ")
    print("================================================")
    print("Puedo orientarte en temas de pagos, créditos,")
    print("horarios, calendario escolar y contacto con Escolar.")
    print("Escribe 'salir' para terminar.\n")

    if USAR_MODELO_REAL:
        cargar_modelo_real()

    while True:
        texto_usuario = input("Tú: ")

        if texto_usuario.strip().lower() in ["salir", "exit", "quit"]:
            print("Chatbot: ¡Hasta luego! 👋")
            break

        if USAR_MODELO_REAL:
            intent = predecir_intent_real(texto_usuario)
        else:
            intent = detectar_intent_falso(texto_usuario)

        respuesta = obtener_respuesta(intent)
        print(f"Chatbot: {respuesta}")


if __name__ == "__main__":
    main()