import streamlit as st
from theme import apply_cvea_theme, LOGO_HORIZONTAL_COLOR

st.set_page_config(
    page_title="CVEA Suite Demos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_cvea_theme()

st.markdown("<div class='cvea-topbar'>CVEA Suite — Demos interactivos</div>", unsafe_allow_html=True)
st.markdown("<a href='../../cvea-suite.html' class='cvea-back'>Volver a CVEA Suite</a>", unsafe_allow_html=True)
st.image(LOGO_HORIZONTAL_COLOR)
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
