# CVEA Insurance Suite — Reservas, siniestralidad, cumplimiento
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from theme import cvea_header

st.set_page_config(page_title="CVEA Insurance Suite (CVEA-IS)", page_icon="🛡️", layout="wide")
cvea_header(
    "CVEA Insurance Suite (CVEA-IS)",
    "Reservas técnicas, siniestralidad por ramo y cumplimiento LC/FT — Datos simulados",
)

@st.cache_data
def get_runoff_triangle(years=10):
    rng = np.random.default_rng(33)
    # Triángulo de desarrollo: filas = año ocurrencia, columnas = año desarrollo
    tri = np.zeros((years, years))
    for i in range(years):
        for j in range(years - i):
            tri[i, j] = max(0, rng.lognormal(8 + i * 0.1, 0.5) * (1 + j * 0.15))
    return pd.DataFrame(tri, index=[f"Año {y}" for y in range(1, years + 1)], columns=[f"Dev {d}" for d in range(1, years + 1)])

@st.cache_data
def get_inflation_vector(years=10):
    return np.cumprod(1 + np.random.RandomState(44).uniform(0.05, 0.35, years))

def chain_ladder(tri):
    tri = tri.copy()
    n = len(tri)
    for j in range(1, n):
        for i in range(n - j):
            if tri.iloc[i, j - 1] > 0:
                factor = tri.iloc[: n - j, j].sum() / tri.iloc[: n - j, j - 1].sum()
                tri.iloc[n - j - 1, j] = tri.iloc[n - j - 1, j - 1] * factor
    return tri

def bornhuetter_ferguson(tri, loss_ratio=0.72):
    tri = tri.copy()
    n = len(tri)
    premium = np.random.RandomState(55).uniform(1e6, 2e6, n)
    for j in range(1, n):
        denom = tri.iloc[: n - j, j - 1].sum()
        if denom <= 0:
            continue
        dev_fact = tri.iloc[: n - j, j].sum() / denom
        dev_fact = max(dev_fact, 0.5)
        i = n - j - 1
        expected = premium[i] * loss_ratio
        tri.iloc[i, j] = tri.iloc[i, j - 1] * dev_fact + expected * (1 - 1 / dev_fact)
    return tri

triangle_raw = get_runoff_triangle()
infl_vec = get_inflation_vector()

st.sidebar.header("Controles")
modelo_reserva = st.sidebar.radio("Modelo de proyección IBNR", ["Chain Ladder", "Bornhuetter-Ferguson", "Chain Ladder Ajustado por Inflación (IACL)"], index=0)
choque_infl = st.sidebar.slider("Choque inflacionario exógeno (%)", -10.0, 10.0, 0.0, 0.5) / 100

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Visión general",
        "Monitoreo de reservas (SUDEASEG)",
        "Ramos y productos",
        "Cumplimiento y estrés",
    ]
)

with tab1:
    st.subheader("Visión general — primas y siniestralidad por ramo")
    ramos = ["Automóviles", "Salud", "Personas", "Patrimoniales", "Fianzas"]
    rng_vis = np.random.default_rng(123)
    primas = rng_vis.uniform(1e6, 5e6, len(ramos))
    siniestros = primas * rng_vis.uniform(0.4, 0.9, len(ramos))
    df_vs = pd.DataFrame({"Ramo": ramos, "Primas_cobradas": primas, "Siniestros_pagados": siniestros})
    df_vs["Siniestralidad"] = df_vs["Siniestros_pagados"] / df_vs["Primas_cobradas"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Primas totales (USD)", f"{df_vs['Primas_cobradas'].sum():,.0f}")
    c2.metric("Siniestros totales (USD)", f"{df_vs['Siniestros_pagados'].sum():,.0f}")
    c3.metric("Siniestralidad promedio", f"{df_vs['Siniestralidad'].mean():.1%}")
    c4.metric("Número de ramos", f"{len(ramos)}")

    st.subheader("Primas cobradas por ramo")
    fig_primas = px.bar(df_vs, x="Ramo", y="Primas_cobradas", title="Primas cobradas por ramo")
    st.plotly_chart(fig_primas, use_container_width=True)

    st.subheader("Siniestralidad por ramo")
    fig_sin = px.bar(df_vs, x="Ramo", y="Siniestralidad", text="Siniestralidad", range_y=[0, 1])
    fig_sin.update_traces(texttemplate="%{text:.1%}", textposition="outside")
    fig_sin.update_layout(title="Siniestralidad por ramo")
    st.plotly_chart(fig_sin, use_container_width=True)

    meta_sin = st.sidebar.slider("Meta de siniestralidad técnica (%)", 30.0, 90.0, 65.0, 1.0) / 100
    sin_prom = float(df_vs["Siniestralidad"].mean())
    fig_g = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=sin_prom * 100,
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#38666A"},
                "steps": [
                    {"range": [0, meta_sin * 100], "color": "#d9ead3"},
                    {"range": [meta_sin * 100, 100], "color": "#f4cccc"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "value": meta_sin * 100},
            },
            title={"text": "Siniestralidad promedio vs meta"},
        )
    )
    st.plotly_chart(fig_g, use_container_width=True)

with tab2:
    st.subheader("Monitoreo de reservas — marco SUDEASEG")
    reservas = [
        ("Reserva de riesgos en curso", "Cobertura de la parte no devengada de las primas."),
        ("Reserva de siniestros reportados", "Siniestros ocurridos y reportados, pendientes de pago."),
        ("Reserva IBNR", "Siniestros ocurridos y no reportados."),
        ("Reserva de desviación de siniestralidad", "Suavizar volatilidad de la siniestralidad futura."),
        ("Reserva catastrófica", "Eventos de baja frecuencia y alta severidad."),
        ("Reserva matemática de vida", "Compromisos de largo plazo en seguros de vida."),
        ("Reserva de previsión", "Otras contingencias y ajustes prudenciales."),
    ]
    df_res = pd.DataFrame(reservas, columns=["Reserva", "Descripción resumida"])
    st.table(df_res)

    st.subheader("Triángulo de desarrollo de siniestros (pagados)")
    tri_display = triangle_raw.copy()
    tri_display = tri_display.style.background_gradient(axis=None, cmap="YlOrRd")
    st.dataframe(tri_display, use_container_width=True)
    if modelo_reserva == "Chain Ladder":
        tri_proj = chain_ladder(triangle_raw)
    elif modelo_reserva == "Bornhuetter-Ferguson":
        tri_proj = bornhuetter_ferguson(triangle_raw)
    else:
        tri_ajust = triangle_raw.copy()
        for j in range(10):
            tri_ajust.iloc[:, j] = tri_ajust.iloc[:, j] / (infl_vec[j] if j < len(infl_vec) else infl_vec[-1])
        tri_proj = chain_ladder(tri_ajust)
        for j in range(10):
            tri_proj.iloc[:, j] = tri_proj.iloc[:, j] * (infl_vec[j] if j < len(infl_vec) else infl_vec[-1])
    ibnr = tri_proj.sum().sum() - triangle_raw.sum().sum()
    st.metric("Reserva IBNR proyectada (simulada)", f"{max(0, ibnr):,.0f}", f"Modelo: {modelo_reserva}")

with tab3:
    st.subheader("Ramos y productos — indicadores de siniestralidad")
    ramos = ["Automóviles", "Salud", "Personas", "Patrimoniales", "Fianzas"]
    productos = {
        "Automóviles": ["Auto individual", "Flotas empresariales", "Taxis"],
        "Salud": ["Plan individual", "Plan colectivo", "Ambulatorio"],
        "Personas": ["Vida riesgo", "Accidentes personales", "Vida colectivo"],
        "Patrimoniales": ["Incendio", "Robo", "RC General"],
        "Fianzas": ["Fiel cumplimiento", "Anticipo", "Laboral"],
    }
    filas = []
    rng_det = np.random.default_rng(456)
    for ramo in ramos:
        for prod in productos[ramo]:
            prima = rng_det.uniform(100_000, 900_000)
            sin_pago = prima * rng_det.uniform(0.3, 0.95)
            filas.append(
                {
                    "Ramo": ramo,
                    "Producto": prod,
                    "Primas": prima,
                    "Siniestros_pagados": sin_pago,
                    "Siniestralidad": sin_pago / prima,
                }
            )
    df_prod = pd.DataFrame(filas)

    ramo_sel = st.selectbox("Ramo", ramos)
    df_sel = df_prod[df_prod["Ramo"] == ramo_sel]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Primas (ramo)", f"{df_sel['Primas'].sum():,.0f}")
    c2.metric("Siniestros (ramo)", f"{df_sel['Siniestros_pagados'].sum():,.0f}")
    c3.metric("Siniestralidad media", f"{df_sel['Siniestralidad'].mean():.1%}")
    c4.metric("Nº productos", f"{df_sel['Producto'].nunique()}")

    fig_prod = px.bar(df_sel, x="Producto", y="Siniestralidad", text="Siniestralidad", range_y=[0, 1])
    fig_prod.update_traces(texttemplate="%{text:.1%}", textposition="outside")
    fig_prod.update_layout(title=f"Siniestralidad por producto — {ramo_sel}")
    st.plotly_chart(fig_prod, use_container_width=True)

with tab4:
    st.subheader("Cumplimiento SUDEASEG y prueba de estrés")
    st.subheader("Prueba de estrés sobre patrimonio")
    choque_central = st.slider("Choque inflacionario (%)", -10.0, 10.0, float(choque_infl * 100), 0.5, key="stress_slider") / 100
    # Métricas que reaccionan al choque
    base_ratio = 0.734
    new_ratio = base_ratio * (1 + choque_central * 0.5)
    c1, c2, c3 = st.columns(3)
    c1.metric("Ratio IBNR/costos (base)", f"{base_ratio:.3f}", "—")
    c2.metric("Ratio IBNR/costos (post-choque)", f"{new_ratio:.3f}", f"{(new_ratio - base_ratio) / base_ratio * 100:+.1f}%")
    c3.metric("Choque aplicado", f"{choque_central * 100:+.1f}%", "—")
    # Fan chart simulado
    periods = 60
    rng = np.random.RandomState(77)
    base = 100 * np.exp(np.cumsum(rng.normal(0.002, 0.02, periods)))
    p75_lo = base * 0.85
    p75_hi = base * 1.15
    p95_lo = base * 0.70
    p95_hi = base * 1.35
    x = list(range(periods))
    fig_fan = go.Figure()
    fig_fan.add_trace(go.Scatter(x=x, y=p95_hi, fill=None, line=dict(color="lightblue")))
    fig_fan.add_trace(go.Scatter(x=x, y=p95_lo, fill="tonexty", line=dict(color="lightblue")))
    fig_fan.add_trace(go.Scatter(x=x, y=p75_hi, fill=None, line=dict(color="blue")))
    fig_fan.add_trace(go.Scatter(x=x, y=p75_lo, fill="tonexty", line=dict(color="blue")))
    fig_fan.add_trace(go.Scatter(x=x, y=base, line=dict(color="darkblue", width=2), name="Central"))
    fig_fan.update_layout(title="Trayectoria probable de pagos futuros (IC 75% y 95%)", height=400)
    st.plotly_chart(fig_fan, use_container_width=True)

with tab4:
    st.subheader("Cumplimiento SUDEASEG — LC/FT/FPADM")
    # Radar: Conozca a su cliente, Intermediarios, Reportes sistemáticos
    categorias = ["Conozca a su cliente", "Intermediarios", "Reportes sistemáticos", "Formación", "Debida diligencia"]
    rng = np.random.RandomState(88)
    valores = rng.uniform(60, 95, 5)
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=list(valores) + [valores[0]], theta=categorias + [categorias[0]], fill="toself", name="Calificación"))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=450)
    st.plotly_chart(fig_radar, use_container_width=True)
    score = np.mean(valores)
    if score >= 80:
        st.success("Calificación: Riesgo bajo — Cumplimiento adecuado.")
    elif score >= 60:
        st.warning("Calificación: Riesgo medio — Revisar políticas.")
    else:
        st.error("Calificación: Riesgo alto — Acción correctiva requerida.")
