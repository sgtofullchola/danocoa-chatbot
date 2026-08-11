import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Bot DANOCOA - Farmacia & Supermercado", page_icon="💊")

st.title("DANOCOA INTELLIGENCE BUSINESS UNIT")
st.caption("Asistente Virtual — Farmacia & Supermercado 'Todo en Uno'")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Bienvenido a Farmacia-Supermercado Todo en Uno. 🛒💊\n\n¿En qué puedo ayudarte hoy? Puedes consultarme por medicamentos, productos de cuidado personal o abarrotes."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def procesar_respuesta(user_input):
    txt = user_input.lower()
    ahora = datetime.now()
    es_happy_hour = 13 <= ahora.hour < 16

    if "medicina" in txt or "losartan" in txt or "medicamento" in txt:
        desc = "10% de descuento Happy Hour" if es_happy_hour else "precio regular"
        precio = "$10.80" if es_happy_hour else "$12.00"
        return f"¡Claro! El **Losartán 50mg** se encuentra disponible a **{precio}** ({desc}).\n\n💡 **Sugerencia de Canasta (Regla B):** Clientes que llevan este tratamiento habitualmente agregan **Metformina 850mg** para control metabólico o artículos de cuidado personal. ¿Deseas incluir alguno a tu orden?"
    elif "champu" in txt or "champú" in txt or "jabon" in txt:
        desc = "15% de descuento Happy Hour" if es_happy_hour else "precio regular"
        precio = "$6.80" if es_happy_hour else "$8.00"
        return f"El **Champú Cuidado Total** tiene un costo de **{precio}** ({desc}).\n\n💡 **Sugerencia de Canasta (Regla B):** Quienes llevan este producto suelen agregar **Crema para Peinar 300ml** con el mismo 15% de descuento. ¿Te gustaría sumarlo?"
    elif "andina" in txt or "analgesico" in txt:
        return "El **Analgésico Plus de Lab Andina** cuenta con una promoción especial de Co-Marketing (Regla D):\n- Precio Regular: $12.00\n- Descuento Especial: -12%\n- **Precio Final: $10.56**\n\n¿Deseas reservarlo para retiro en caja o envío?"
    else:
        return "Con gusto te atiendo. Actualmente tenemos ofertas activas en Abarrotes (5%), Farmacia (10%) y Cuidado Personal (15%) durante nuestra franja Happy Hour. ¿Qué producto específico buscas hoy?"

if user_input := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    bot_response = procesar_respuesta(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.write(bot_response)