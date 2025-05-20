import pandas as pd
import streamlit as st
import pywhatkit as kit
import datetime
import os

# Configuración de archivo de stock
STOCK_FILE = "stock_ejemplo.xlsx"

# Cargar datos de stock o inicializar
if os.path.exists(STOCK_FILE):
    df = pd.read_excel(STOCK_FILE)
else:
    df = pd.DataFrame(columns=["Producto", "Stock_actual", "Stock_mínimo"])

st.set_page_config(page_title="Gestor de Stock", layout="centered")
st.title("📦 Gestor Simple de Stock + WhatsApp")

# Mostrar tabla
st.subheader("Estado actual del stock")
st.dataframe(df, use_container_width=True)

# Identificar alertas
alertas = df[df["Stock_actual"] < df["Stock_mínimo"]]

# Mostrar alertas
if not alertas.empty:
    st.warning("Productos por debajo del stock mínimo:")
    for _, row in alertas.iterrows():
        st.write(f"- {row['Producto']} ({row['Stock_actual']} unidades)")
else:
    st.success("Todo en orden. No hay productos en alerta.")

# Agregar nuevo producto
st.subheader("Agregar o actualizar producto")
with st.form("form_producto"):
    nombre = st.text_input("Nombre del producto")
    stock_actual = st.number_input("Stock actual", min_value=0, step=1)
    stock_minimo = st.number_input("Stock mínimo", min_value=0, step=1)
    enviado = st.form_submit_button("Guardar")

if enviado:
    df.loc[df["Producto"] == nombre, ["Stock_actual", "Stock_mínimo"]] = [stock_actual, stock_minimo]
    if nombre not in df["Producto"].values:
        df.loc[len(df)] = [nombre, stock_actual, stock_minimo]
    df.to_excel(STOCK_FILE, index=False)
    st.success(f"Producto '{nombre}' actualizado.")
    st.experimental_rerun()

# Enviar alerta por WhatsApp
st.subheader("Enviar alerta por WhatsApp")
numero = st.text_input("Número de WhatsApp (con +59899749614)")
if st.button("Enviar alerta"):
    if not alertas.empty and numero:
        mensaje = "⚠️ ¡Atención!\nLos siguientes productos están por debajo del stock mínimo:\n"
        for _, row in alertas.iterrows():
            mensaje += f"- {row['Producto']} ({row['Stock_actual']} unidades)\n"

        ahora = datetime.datetime.now() + datetime.timedelta(minutes=2)
        hora = ahora.hour
        minuto = ahora.minute
        kit.sendwhatmsg(numero, mensaje, hora, minuto, wait_time=10, tab_close=True)
        st.info("Mensaje programado para enviarse en 2 minutos")
    else:
        st.error("No hay productos en alerta o no se ingresó un número válido.")
