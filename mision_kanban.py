import streamlit as st
import random
import time
import pandas as pd

# ----------------------------
# CONFIGURACIÓN INICIAL
# ----------------------------
st.set_page_config(page_title="Misión Kanban", page_icon="🚀", layout="wide")

# Estilo visual
st.markdown("""
    <style>
    body { background-color: #F9FAFB; color: #1F2937; }
    .stButton>button {
        background-color: #3B82F6;
        color: white;
        border-radius: 10px;
        padding: 0.6em 1em;
        font-weight: bold;
    }
    .stProgress > div > div {
        background-color: #10B981;
    }
    .block-container {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# DATOS DE JUEGO
# ----------------------------
if "jugadores" not in st.session_state:
    st.session_state.jugadores = {}
if "jugador_actual" not in st.session_state:
    st.session_state.jugador_actual = None
if "pregunta_actual" not in st.session_state:
    st.session_state.pregunta_actual = 0
if "inicio_tiempo" not in st.session_state:
    st.session_state.inicio_tiempo = None

# Preguntas / retos (puedes ampliarlas fácilmente)
preguntas = [
    {
        "nivel": "🟢 Aprendiz",
        "texto": "¿Cuál es el propósito principal del método Kanban?",
        "opciones": [
            "Aumentar el trabajo en curso",
            "Visualizar el flujo de trabajo y limitar el WIP",
            "Eliminar reuniones",
            "Asignar más tareas por persona"
        ],
        "respuesta": "Visualizar el flujo de trabajo y limitar el WIP"
    },
    {
        "nivel": "🔵 Colaborador",
        "texto": "En Kanban, el límite WIP (Work In Progress) sirve para...",
        "opciones": [
            "Evitar que las tareas se acumulen",
            "Aumentar el ritmo de trabajo",
            "Permitir multitareas simultáneas",
            "Reducir la comunicación"
        ],
        "respuesta": "Evitar que las tareas se acumulen"
    },
    {
        "nivel": "🟣 Líder",
        "texto": "Un equipo detecta un cuello de botella en la columna 'En progreso'. ¿Qué debería hacer primero?",
        "opciones": [
            "Ignorarlo hasta el final del sprint",
            "Reducir el WIP o reasignar recursos",
            "Agregar más tareas",
            "Aumentar la velocidad de entrega"
        ],
        "respuesta": "Reducir el WIP o reasignar recursos"
    },
    {
        "nivel": "🟠 Sensei",
        "texto": "En Kanban, ¿qué principio fomenta la mejora continua?",
        "opciones": [
            "Kaizen",
            "Muda",
            "Takt Time",
            "Scrum"
        ],
        "respuesta": "Kaizen"
    },
    {
        "nivel": "🔴 Maestro",
        "texto": "El indicador 'Lead Time' mide...",
        "opciones": [
            "El tiempo que tarda una tarea desde que se inicia hasta que se entrega",
            "La cantidad de tareas asignadas por persona",
            "El costo por tarea completada",
            "La eficiencia del Scrum Master"
        ],
        "respuesta": "El tiempo que tarda una tarea desde que se inicia hasta que se entrega"
    }
]

# ----------------------------
# FUNCIÓN PARA MOSTRAR TABLERO KANBAN
# ----------------------------
def mostrar_tablero(pregunta_actual):
    st.markdown("### 🧩 Tablero Kanban del Progreso")
    kanban = {
        "Por hacer": [f"Desafío {i+1}" for i in range(pregunta_actual, len(preguntas))],
        "En progreso": [f"Desafío {pregunta_actual + 1}"] if pregunta_actual < len(preguntas) else [],
        "Hecho": [f"Desafío {i+1}" for i in range(pregunta_actual)]
    }
    cols = st.columns(3)
    for i, col_name in enumerate(kanban):
        with cols[i]:
            st.subheader(col_name)
            for tarea in kanban[col_name]:
                st.markdown(f"✅ {tarea}" if col_name == "Hecho" else f"🔹 {tarea}")

# ----------------------------
# INICIO DEL JUEGO
# ----------------------------
st.title("🚀 Misión Kanban 2.0")
st.markdown("Bienvenido al desafío interactivo sobre la metodología **Kanban Ágil**. Supera los retos, gana puntos y demuestra tu dominio del flujo continuo 💪.")

jugador = st.text_input("Ingresa tu nombre para comenzar:")

if jugador:
    st.session_state.jugador_actual = jugador
    if jugador not in st.session_state.jugadores:
        st.session_state.jugadores[jugador] = {"puntos": 0, "tiempo": 0}
    
    mostrar_tablero(st.session_state.pregunta_actual)
    
    # Avance de preguntas
    if st.session_state.pregunta_actual < len(preguntas):
        pregunta = preguntas[st.session_state.pregunta_actual]
        st.subheader(f"Nivel {pregunta['nivel']}")
        st.markdown(f"**{pregunta['texto']}**")
        
        st.session_state.inicio_tiempo = time.time()
        respuesta = st.radio("Selecciona una respuesta:", pregunta["opciones"])
        
        if st.button("Responder"):
            tiempo_respuesta = time.time() - st.session_state.inicio_tiempo
            jugador_data = st.session_state.jugadores[jugador]
            
            # Evento aleatorio
            eventos = [
                ("⚠️ Un bloqueo detiene el flujo, pierdes 3 segundos", -3),
                ("🚀 Trabajo urgente completado, +10 puntos", 10),
                ("💡 Mejora continua: respuesta rápida vale doble", 2)
            ]
            if random.random() < 0.25:
                evento, efecto = random.choice(eventos)
                st.warning(evento)
                if efecto == 2:
                    multiplicador = 2
                elif efecto > 0:
                    jugador_data["puntos"] += efecto
                    multiplicador = 1
                else:
                    tiempo_respuesta -= efecto  # penalización en tiempo
                    multiplicador = 1
            else:
                multiplicador = 1
            
            # Verificar respuesta
            if respuesta == pregunta["respuesta"]:
                puntos = int(max(5, 20 - tiempo_respuesta)) * multiplicador
                jugador_data["puntos"] += puntos
                st.success(f"✅ ¡Correcto! +{puntos} puntos")
            else:
                st.error("❌ Incorrecto. Sigue aprendiendo del flujo Kanban.")
            
            jugador_data["tiempo"] += tiempo_respuesta
            st.session_state.pregunta_actual += 1
            st.rerun()
    
    else:
        # Final del juego
        st.balloons()
        st.header("🎉 ¡Misión completada!")
        st.write("Has terminado todos los desafíos Kanban.")
        
        # Mostrar ranking
        st.subheader("🏆 Ranking Final")
        ranking = sorted(st.session_state.jugadores.items(), key=lambda x: (x[1]["puntos"], -x[1]["tiempo"]), reverse=True)
        for i, (nombre, datos) in enumerate(ranking, 1):
            st.write(f"{i}. {nombre} — {datos['puntos']} pts — ⏱️ {round(datos['tiempo'],1)} s")
        
        # Descargar resultados
        ranking_df = pd.DataFrame([
            {"Jugador": n, "Puntos": d["puntos"], "Tiempo": round(d["tiempo"], 2)}
            for n, d in ranking
        ])
        st.download_button("⬇️ Descargar resultados", ranking_df.to_csv(index=False), "ranking_kanban.csv")

