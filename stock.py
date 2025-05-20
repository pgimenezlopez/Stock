import pandas as pd
import pywhatkit as kit
import datetime

# 📁 Ruta al Excel
EXCEL_PATH = "stock_ejemplo.xlsx"

# ☎️ Número de WhatsApp (formato internacional)
NUMERO_DESTINO = "+59899749614"  # Cambiar por el número real

# 🕒 Cuántos minutos en el futuro querés enviar el mensaje
MINUTOS_A_FUTURO = 2

# 📊 Leer archivo Excel
df = pd.read_excel(EXCEL_PATH)

# 📉 Detectar alertas
alertas = df[df["Stock_actual"] < df["Stock_mínimo"]]

# 📨 Armar mensaje
if not alertas.empty:
    mensaje = "⚠️ ¡Atención!\nLos siguientes productos están por debajo del stock mínimo:\n"
    for _, row in alertas.iterrows():
        mensaje += f"- {row['Producto']} ({row['Stock_actual']} unidades)\n"
else:
    mensaje = "✅ Todo en orden. No hay productos por debajo del stock mínimo."

# 🕓 Calcular hora de envío válida
ahora = datetime.datetime.now() + datetime.timedelta(minutes=MINUTOS_A_FUTURO)
hora = ahora.hour
minuto = ahora.minute

# 📲 Enviar mensaje por WhatsApp
kit.sendwhatmsg(NUMERO_DESTINO, mensaje, hora, minuto, wait_time=10, tab_close=True)

print("📬 Mensaje programado correctamente.")
