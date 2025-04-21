import streamlit as st
import telegram
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

df = pd.read_excel("camino_etapas_limpio.xlsx")
fecha_inicio = datetime(2025, 5, 5)
df["Fecha"] = [fecha_inicio + timedelta(days=i) for i in range(len(df))]

mañana = datetime.now().date() + timedelta(days=1)
etapa_m = df[df["Fecha"].dt.date == mañana]

if not etapa_m.empty:
    etapa = etapa_m.iloc[0]
    mensaje = f"""
🕊️ *Anticipo de la etapa de mañana*

📅 *{mañana.strftime('%A %d de %B de %Y')}*

🏁 *Etapa {etapa['Etapa']} – {etapa['Localidad']}*
📏 Distancia estimada: {etapa['Distancia_km']} km
📝 Notas: {etapa['Notas']}

🙏 Buen descanso, peregrino. Lenny estará contigo mañana 🌄
""".strip()
else:
    mensaje = "Mañana no hay etapa programada. Disfruta tu descanso. 🛌"

try:
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensaje, parse_mode=telegram.constants.ParseMode.MARKDOWN)
    st.success("✅ Mensaje enviado correctamente a Telegram.")
except Exception as e:
    st.error("❌ No se pudo enviar el mensaje.")
    st.text(str(e))

