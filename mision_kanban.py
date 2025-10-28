import streamlit as st
import time, random

st.set_page_config(page_title="🎯 Misión Kanban", page_icon="🧠", layout="centered")

st.title("🎯 Misión Kanban – Competencia Ágil")
st.write("¡Bienvenido! Compite en tiempo real respondiendo preguntas sobre Kanban. Gana puntos según tu rapidez y precisión.")

if "jugadores" not in st.session_state:
    st.session_state.jugadores = {}
if "started" not in st.session_state:
    st.session_state.started = False
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = 0

preguntas = [
    {"nivel": "1️⃣ Aprendiz Kanban","pregunta": "¿Qué representa una tarjeta en Kanban?","opciones": ["Una tarea o trabajo","Un equipo de trabajo","Un tablero completo","Un sprint"],"respuesta": 0},
    {"nivel": "2️⃣ Colaborador Kanban","pregunta": "¿Qué busca limitar el WIP (Work In Progress)?","opciones": ["La cantidad de tareas activas","El número de personas","La calidad del producto","La duración del sprint"],"respuesta": 0},
    {"nivel": "3️⃣ Líder de Flujo","pregunta": "Un cuello de botella ocurre cuando...","opciones": ["Hay más tareas que capacidad en una etapa","El equipo trabaja más rápido","Se termina todo el trabajo","El tablero está vacío"],"respuesta": 0},
    {"nivel": "4️⃣ Sensei Kanban","pregunta": "Si una etapa está siempre llena, ¿qué deberías hacer?","opciones": ["Reducir el WIP o mejorar esa etapa","Ignorarla","Mover tareas sin analizar","Eliminar esa columna"],"respuesta": 0},
    {"nivel": "5️⃣ Maestro Ágil","pregunta": "El objetivo principal de Kanban es...","opciones": ["Mejorar el flujo de trabajo","Planificar más rápido","Agregar tareas constantemente","Evitar reuniones"],"respuesta": 0},
]

if not st.session_state.started:
    nombre = st.text_input("Ingresa tu nombre para unirte a la misión:")
    if st.button("Unirme al juego 🚀") and nombre:
        if nombre not in st.session_state.jugadores:
            st.session_state.jugadores[nombre] = {"puntos": 0, "tiempo": 0}
            st.success(f"Bienvenido, {nombre}! Espera a que inicie la misión.")
        else:
            st.warning("Ya estás registrado.")
    st.write(f"Jugadores conectados: {len(st.session_state.jugadores)}")
    st.write(list(st.session_state.jugadores.keys()))

if st.button("Iniciar misión (solo el organizador) 🧭"):
    st.session_state.started = True
    st.session_state.pregunta_actual = 0
    st.success("¡La misión ha comenzado!")

if st.session_state.started:
    actual = st.session_state.pregunta_actual
    if actual < len(preguntas):
        q = preguntas[actual]
        st.subheader(q["nivel"])
        st.markdown(f"### {q['pregunta']}")

        start_time = time.time()
        opcion = st.radio("Selecciona tu respuesta:", q["opciones"], key=f"resp_{actual}")
        if st.button("Enviar respuesta ✅", key=f"btn_{actual}"):
            tiempo = time.time() - start_time
            correcto = q["opciones"].index(opcion) == q["respuesta"]
            puntos = max(0, int(100 - tiempo * 10)) if correcto else 0

            usuario = list(st.session_state.jugadores.keys())[-1]
            st.session_state.jugadores[usuario]["puntos"] += puntos
            st.session_state.jugadores[usuario]["tiempo"] += tiempo

            if correcto:
                st.success(f"✅ ¡Correcto! +{puntos} puntos.")
            else:
                st.error("❌ Incorrecto.")

            st.session_state.pregunta_actual += 1
            time.sleep(1)
            st.rerun()
    else:
        st.header("🏁 ¡Misión completada!")
        ranking = sorted(st.session_state.jugadores.items(), key=lambda x: x[1]["puntos"], reverse=True)
        st.subheader("🏆 Ranking Final")
        for i, (nombre, datos) in enumerate(ranking, 1):
            st.write(f"**{i}. {nombre}** – {datos['puntos']} pts ⏱ {round(datos['tiempo'], 2)} s")
