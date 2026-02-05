import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración visual de la app
st.set_page_config(page_title="Nuestro CedeTracker", page_icon="🚀", layout="wide")

# Conexión con Google Sheets (usa los Secrets que ya configuraste)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
except Exception as e:
    st.error("Conectando con la base de datos...")
    df = pd.DataFrame(columns=["Usuario", "Ticker", "Cantidad", "Precio_ARS", "Fecha"])

st.title("🚀 Nuestro CedeTracker Familiar")

# --- SISTEMA DE LOGIN ---
if 'user' not in st.session_state:
    st.subheader("¡Bienvenido!")
    user_input = st.text_input("Ingresá tu nombre para empezar:")
    if st.button("Entrar"):
        if user_input:
            st.session_state['user'] = user_input
            st.rerun()
        else:
            st.warning("Por favor, escribí un nombre.")
else:
    user = st.session_state['user']
    st.sidebar.success(f"Sesión iniciada: {user}")
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state['user']
        st.rerun()

    # --- FORMULARIO DE CARGA ---
    with st.expander("➕ Cargar Nueva Operación", expanded=True):
        with st.form("form_carga"):
            col_t, col_c, col_p = st.columns(3)
            with col_t:
                ticker = st.text_input("Ticker (ej: AAPL, NVDA)").upper()
            with col_c:
                cant = st.number_input("Cantidad", min_value=1, step=1)
            with col_p:
                precio = st.number_input("Precio Unitario (ARS)", min_value=1.0, step=0.1)
            
            submit = st.form_submit_button("Guardar en la Nube")
            
            if submit:
                if ticker:
                    # Crear nueva fila de datos
                    nueva_fila = pd.DataFrame([{
                        "Usuario": user,
                        "Ticker": ticker,
                        "Cantidad": cant,
                        "Precio_ARS": precio,
                        "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
                    }])
                    # Actualizar planilla
                    df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
                    conn.update(data=df_actualizado)
                    st.success(f"✅ ¡{ticker} guardado correctamente!")
                    st.rerun()
                else:
                    st.error("Falta el nombre del Ticker.")

    # --- LISTADO Y BORRADO ---
    st.subheader("📋 Mi Historial de Compras")
    
    if not df.empty and "Usuario" in df.columns:
        # Filtramos para que cada uno solo vea lo suyo
        mis_datos = df[df['Usuario'] == user]
        
        if not mis_datos.empty:
            for i, row in mis_datos.iterrows():
                # Diseño de cada fila con botón de borrar
                with st.container():
                    c1, c2, c3 = st.columns([3, 2, 1])
                    c1.write(f"**{row['Ticker']}** ({row['Fecha']})")
                    c2.write(f"{row['Cantidad']} un. a ${row['Precio_ARS']:,.2f}")
                    
                    # El botón de borrar que buscabas
                    if c3.button("🗑️", key=f"del_{i}"):
                        df_borrado = df.drop(i)
                        conn.update(data=df_borrado)
                        st.warning(f"Eliminado: {row['Ticker']}")
                        st.rerun()
                st.divider()
        else:
            st.info("Aún no cargaste ninguna operación.")
    else:
        st.info("La base de datos está lista. ¡Cargá tu primera compra!")
        
