import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Bot DANOCOA - Farmacia & Supermercado", page_icon="💊")

# Estilos limpios
st.title("DANOCOA INTELLIGENCE BUSINESS UNIT")
st.caption("Asistente Virtual — Farmacia & Supermercado 'Todo en Uno'")

# Base de datos simulada de inventario con Regla B (Asociaciones de Canasta)
INVENTARIO = {
    "acetaminofen": {
        "nombre": "Acetaminofén 500mg (10 comp.)",
        "precio": 3.50,
        "categoria": "Farmacia",
        "sugerencias": [
            {"nombre": "Vitamina C 1000mg", "precio": 4.00, "razon": "Refuerzo inmunológico habitual"},
            {"nombre": "Termómetro Digital", "precio": 6.50, "razon": "Control de temperatura"}
        ]
    },
    "losartan": {
        "nombre": "Losartán 50mg (30 comp.)",
        "precio": 12.00,
        "categoria": "Farmacia",
        "sugerencias": [
            {"nombre": "Metformina 850mg", "precio": 8.50, "razon": "Control metabólico integral (109 coinc. históricas)"},
            {"nombre": "Suavizante de Ropa 1L", "precio": 4.50, "razon": "Abarrotes en oferta Happy Hour"}
        ]
    },
    "champu": {
        "nombre": "Champú Cuidado Total 400ml",
        "precio": 8.00,
        "categoria": "Cuidado Personal",
        "sugerencias": [
            {"nombre": "Crema para Peinar 300ml", "precio": 6.00, "razon": "15% desc. adicional por Cuidado Personal"}
        ]
    },
    "analgesico": {
        "nombre": "Analgésico Plus (Lab Andina)",
        "precio": 12.00,
        "categoria": "Laboratorio",
        "sugerencias": []
    }
}

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Bienvenido a Farmacia-Supermercado Todo en Uno. 🛒💊\n\n¿En qué puedo ayudarte hoy? Puedes preguntarme por cualquier medicamento (ej. Acetaminofén, Losartán) o producto."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def procesar_respuesta(user_input):
    txt = user_input.lower()
    ahora = datetime.now()
    # Evalúa si la hora actual está entre 1:00 PM y 4:00 PM
    es_happy_hour = 13 <= ahora.hour < 16

    # Buscar coincidencia en la base de datos
    producto_encontrado = None
    for clave in INVENTARIO:
        if clave in txt:
            producto_encontrado = INVENTARIO[clave]
            break

    if producto_encontrado:
        cat = producto_encontrado["categoria"]
        precio_orig = producto_encontrado["precio"]
        
        # Regla D: Co-Marketing Laboratorios (12% Descuento)
        if cat == "Laboratorio":
            precio_final = precio_orig * 0.88
            return f"El **{producto_encontrado['nombre']}** cuenta con promoción de Co-Marketing (Lab Andina):\n- Precio Regular: ${precio_orig:.2f}\n- Descuento Especial: -12%\n- **Precio Final: ${precio_final:.2f}**\n\n¿Deseas reservarlo para retiro en caja o envío?"

        # Regla C: Precios Dinámicos (Happy Hour)
        desc_porcentaje = 0
        if es_happy_hour:
            if cat == "Abarrotes": desc_porcentaje = 5
            elif cat == "Farmacia": desc_porcentaje = 10
            elif cat == "Cuidado Personal": desc_porcentaje = 15

        precio_final = precio_orig * (1 - desc_porcentaje/100)
        
        txt_desc = f"({desc_porcentaje}% desc. Happy Hour aplicado)" if desc_porcentaje > 0 else "(Precio Regular)"
        res = f"¡Claro! El **{producto_encontrado['nombre']}** tiene un precio de **${precio_final:.2f}** {txt_desc}.\n"

        # Regla B: Venta Cruzada (Canasta Agregada)
        if producto_encontrado["sugerencias"]:
            res += "\n💡 **Sugerencia de Canasta (Regla B):**\n"
            for sug in producto_encontrado["sugerencias"]:
                p_sug = sug['precio'] * (1 - desc_porcentaje/100) if es_happy_hour else sug['precio']
                res += f"• **{sug['nombre']}**: ${p_sug:.2f} — *{sug['razon']}*\n"
            res += "\n¿Te gustaría agregar alguno a tu orden?"
        return res

    return "Con gusto te atiendo. Puedes consultar productos como **Acetaminofén**, **Losartán**, **Champú** o promociones de **Lab Andina**. ¿Qué producto deseas buscar?"

if user_input := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    bot_response = procesar_respuesta(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.write(bot_response)