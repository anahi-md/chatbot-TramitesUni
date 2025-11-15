import random
# import pickle  # ← se usará cuando A genere modelo.pkl


# ============================================================
#   RESPUESTAS FALSAS (SIMULACIÓN CHATBOT UAdeC)
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
        "Para pagar tu semestre en la UAdeC, debes entrar al portal de alumnos, generar tu ficha de pago y cubrirla en línea o en bancos autorizados.",
        "El pago de reinscripción o semestre se realiza generando la referencia en el sistema de la UAdeC. Consulta siempre fechas y montos actualizados."
    ],
    "solicitar_creditos_educativos": [
        "Para créditos educativos, revisa la convocatoria vigente en Servicios Estudiantiles. Ahí verás requisitos y documentos.",
        "Los créditos educativos se solicitan en el área correspondiente dentro de la UAdeC. Prepara documentación como historial académico e identificación."
    ],
    "pago_cuota_mantenimiento": [
        "La cuota de mantenimiento aparece en tu estado de cuenta. Puedes pagarla en línea o en los bancos autorizados.",
        "Para pagar la cuota de mantenimiento, revisa tu estado de cuenta en el portal UAdeC y cubre el monto antes de la fecha límite."
    ],
    "consulta_estado_cuenta": [
        "Tu estado de cuenta se consulta en el portal de alumnos, en la sección de Finanzas. Ahí verás cargos y pagos.",
        "Para revisar tu estado de cuenta, entra al sistema UAdeC con tu matrícula y accede a la sección de Pagos."
    ],
    "ayuda_horario": [
        "La selección de horario se hace en línea, en las fechas señaladas por la UAdeC. Revisa la oferta de materias antes.",
        "Para inscribir materias, verifica las fechas de reinscripción y consulta disponibilidad de grupos en el portal UAdeC."
    ],
    "consulta_calendario_escolar": [
        "Puedes consultar el calendario escolar en la página oficial de la UAdeC, sección de Fechas importantes.",
        "El calendario escolar incluye pagos, exámenes e inicios de semestre. Está disponible en la web oficial de la UAdeC."
    ],
    "consulta_creditos_escolares": [
        "Tus créditos escolares están en tu historial académico dentro del portal de alumnos.",
        "Para ver tus créditos acumulados, entra al sistema UAdeC y consulta tu avance del plan de estudios."
    ],
    "info_contacto_escolar": [
        "Puedes contactar al departamento escolar mediante los correos y teléfonos oficiales listados en tu facultad.",
        "Para atención escolar, revisa el directorio de tu facultad en la página de la UAdeC. Ahí están los correos institucionales."
    ],
    "ayuda_general": [
        "Puedo ayudarte con pagos, créditos, horarios, calendario, estado de cuenta y contacto escolar. Pregunta algo específico 😉.",
        "Soy el asistente virtual de trámites UAdeC. Dime si tu duda es sobre pagos, horarios, créditos, calendarios o contacto con Escolar."
    ],
    "desconocido": [
        "No estoy seguro de cómo ayudarte con eso. ¿Puedes explicarlo con más detalle?",
        "Mmm… no entiendo esa parte. ¿Tu duda es sobre pagos, créditos, horario, calendario o estado de cuenta?"
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
    if ("crédito" in texto or "credito" in texto or "financiamiento" in texto or "préstamo" in texto or "prestamo" in texto) and \
       ("educativo" in texto or "beca" in texto or "estudiantil" in texto):
        return "solicitar_creditos_educativos"

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
        return "consulta_calendario_escolar"

    # ---- CRÉDITOS ESCOLARES ----
    if ("créditos" in texto or "creditos" in texto or "avance" in texto) and \
       ("escolares" in texto or "curricular" in texto or "plan de estudios" in texto):
        return "consulta_creditos_escolares"

    # ---- CONTACTO ESCOLAR ----
    if ("contacto" in texto or "correo" in texto or "teléfono" in texto or "telefono" in texto) and \
       ("escolar" in texto or "ventanilla" in texto):
        return "info_contacto_escolar"

    # ---- AYUDA GENERAL ----
    if "ayuda" in texto:
        return "ayuda_general"

    # ---- SI NO COINCIDE NADA ----
    return "desconocido"


# ============================================================
#   RESPUESTAS
# ============================================================
def obtener_respuesta(intent: str) -> str:
    respuestas = FAKE_INTENTS.get(intent, FAKE_INTENTS["desconocido"])
    return random.choice(respuestas)


# ============================================================
#   FUTURO: INTEGRAR MODELO REAL
# ============================================================
USAR_MODELO_REAL = False

def cargar_modelo_real():
    pass

def predecir_intent_real(texto_usuario: str) -> str:
    return "desconocido"


# ============================================================
#   PROGRAMA PRINCIPAL
# ============================================================
def main():
    print("================================================")
    print("   CHATBOT DE TRÁMITES - UNIVERSIDAD AUTÓNOMA   ")
    print("               DE COAHUILA (UAdeC)              ")
    print("================================================")
    print("Puedo orientarte en pagos, créditos educativos,")
    print("estado de cuenta, horarios, calendario y escolar.")
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

        print("Chatbot:", obtener_respuesta(intent))


if __name__ == "__main__":
    main()