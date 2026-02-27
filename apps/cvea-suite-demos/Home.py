# CVEA Suite — Demos interactivos
# Ejecutar: streamlit run Home.py

import streamlit as st

st.set_page_config(
    page_title="CVEA Suite Demos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("CVEA Suite — Demos interactivos")
st.markdown("""
Ecosistema tecnológico integral del **Centro Venezolano de Estudios Actuariales (CVEA)** para actuarios, 
estadísticos y tomadores de decisiones. Los demos utilizan **datos simulados** con fines pedagógicos y de demostración.
""")

st.subheader("Demos por sector")
st.markdown("""
Use el **menú lateral** para navegar a cada demo:

| Demo | Descripción |
|------|-------------|
| **1. Bank Suite** | Credit & Market Risk (NIIF 9), liquidez, Sankey de migración, ECL, velas y correlaciones. |
| **2. Insurance Suite** | Reservas (Chain Ladder, BF, IACL), NIIF 17 (waterfall), estrés inflacionario, cumplimiento LC/FT. |
| **3. Retail Suite** | POS, treemap de participación, elasticidad de precios, reglas de asociación, PyGWalker. |
| **4. Health Suite** | Morbilidad, auditoría clínica vs baremos, Monte Carlo reservas, tarificación y telemedicina. |
| **5. Control Suite** | Flotas, OEE, mantenimiento predictivo, cascada de gastos, análisis exploratorio. |
""")

st.info("Para ejecutar en local: `pip install -r requirements.txt` y luego `streamlit run Home.py`.")
