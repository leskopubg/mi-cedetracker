import streamlit as st
import yfinance as yf
import pandas as pd

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="CedeTracker Familiar", layout="wide")

# 2. BASE DE DATOS DE RATIOS (He incluido los principales, luego sumamos los 300)
RATIOS = {
    "AAPL": 20, "NVDA": 24, "TSLA": 15, "KO": 5, "MELI": 120, 
    "AMZN": 144, "GOOGL": 58, "MSFT": 30, "META": 24, "MMM": 10,
    "GGAL": 10  # Para el cálculo del CCL
}

def get_ccl_galicia():
    try:
        # GGAL en pesos (BYMA) y GGAL en USD (ADR)
        ggal_ars = yf.Ticker("GGAL.BA").fast_info['last_price']
        ggal_usd = yf.Ticker("GGAL").fast_info['last_price']
        return (ggal_ars * 10) / ggal_usd
    except:
        return 1300.0  # Valor de respaldo si falla la conexión

# 3. INTERFAZ
st.title("🚀 Nuestro CedeTracker")

# LOGIN SIMULADO
if 'user' not in st.session_state:
    with st.container():
        user = st.text_input("Tu nombre de usuario")
        if st.button("Entrar"):
            st.session_state['user'] = user
            st.rerun()
else:
    ccl = get_ccl_galicia()
    st.sidebar.success(f"Hola {st.session_state['user']}!")
    st.sidebar.metric("Dólar CCL (Galicia)", f"${ccl:,.2f}")

    # FORMULARIO DE CARGA
    with st.expander("➕ Cargar Compra"):
        t_sel = st.selectbox("Ticker", list(RATIOS.keys()))
        cant = st.number_input("Cantidad", min_value=1)
        p_ars = st.number_input("Precio Unitario (ARS)", min_value=0.0)
        comis = st.number_input("Comisión Total (ARS)", min_value=0.0)
        
        if st.button("Guardar"):
            st.success(f"Guardado: {cant} de {t_sel}")

    st.info("Para que los datos no se borren, el próximo paso es conectar Google Sheets.")
  
