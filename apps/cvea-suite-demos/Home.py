# CVEA Suite — Demos interactivos
# Ejecutar: streamlit run Home.py

import streamlit as st
from theme import cvea_header

st.set_page_config(
    page_title="CVEA Suite Demos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

cvea_header(
    "CVEA Suite — Demos interactivos",
    "Aplicativos demostrativos con datos simulados para banca, seguros, retail, salud e industria.",
)

st.image("../../assets/logos/Logo-CVEA-horizontal-grande-letrascolor.png", use_column_width=True)
st.markdown(
    "Todas las funcionalidades mostradas en cada módulo son **adaptables** a las necesidades y procesos específicos de cada organización usuaria."
)

st.subheader("Demos por sector")
st.markdown("""
Use el **menú lateral** para navegar a cada demo:

| Demo | Descripción |
|------|-------------|
| **1. Bank Suite** | Credit & Market Risk (NIIF 9), liquidez, visión 360 de la cartera y tesorería. |
| **2. Insurance Suite** | Reservas técnicas, siniestralidad por ramo, monitoreo de reservas y análisis por productos. |
| **3. Retail Suite** | POS, participación de mercado, elasticidad de precios, reglas de asociación, PyGWalker. |
| **4. Health Suite** | Morbilidad, auditoría clínica vs baremos, Monte Carlo de reservas de salud, tarificación. |
| **5. Control Suite** | Flotas, OEE, mantenimiento predictivo, cascada de gastos, análisis exploratorio. |
""")
