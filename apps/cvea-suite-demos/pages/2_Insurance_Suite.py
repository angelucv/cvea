# CVEA Insurance Suite — Reservas, NIIF 17, Estrés, Cumplimiento
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="CVEA Insurance Suite", page_icon="🛡️", layout="wide")
st.title("CVEA Insurance Suite")
st.caption("Reservas, NIIF 17, estrés inflacionario y cumplimiento LC/FT — Datos simulados")

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
medicion_niff17 = st.sidebar.selectbox("Modelo de medición NIIF 17", ["BBA (Bloques de Construcción / GMM)", "PAA (Asignación de Primas)"], index=0)
risk_adj = st.sidebar.selectbox("Ajuste por riesgo no financiero", ["Costo de capital", "Valor en Riesgo (VaR)"], index=0)
choque_infl = st.sidebar.slider("Choque inflacionario exógeno (%)", -10.0, 10.0, 0.0, 0.5) / 100

tab1, tab2, tab3, tab4 = st.tabs(["Reservas y siniestralidad histórica", "Motor NIIF 17", "Simulador de estrés inflacionario", "Cumplimiento LC/FT"])

with tab1:
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

with tab2:
    st.subheader("Puente contable NIIF 17 (Waterfall)")
    # Valores simulados para el waterfall
    opening = 1_200_000
    new_business = 180_000
    change_supuestos = -45_000
    unwinds = 30_000
    exp_adj = -20_000
    release_pl = 85_000
    closing = opening + new_business + change_supuestos + unwinds + exp_adj + release_pl
    x = ["Saldo inicial", "Nuevos negocios", "Cambios supuestos", "Descuento fin.", "Ajuste experiencia", "Liberación P&L", "Cierre"]
    y = [opening, new_business, change_supuestos, unwinds, exp_adj, release_pl, closing]
    colors = ["blue" if v >= 0 else "red" for v in y]
    fig_w = go.Figure(go.Bar(x=x, y=y, marker_color=colors, text=[f"{v:,.0f}" for v in y], textposition="outside"))
    fig_w.update_layout(title=f"Enfoque: {medicion_niff17} · Risk Adj: {risk_adj}", yaxis_title="Monto", height=400)
    st.plotly_chart(fig_w, use_container_width=True)

with tab3:
    st.subheader("Prueba de estrés sobre patrimonio")
    st.slider("Choque inflacionario (%)", -10.0, 10.0, float(choque_infl * 100), 0.5, key="stress_slider")
    # Métricas que reaccionan al choque
    base_ratio = 0.734
    new_ratio = base_ratio * (1 + choque_infl * 0.5)
    c1, c2, c3 = st.columns(3)
    c1.metric("Ratio IBNR/costos (base)", f"{base_ratio:.3f}", "—")
    c2.metric("Ratio IBNR/costos (post-choque)", f"{new_ratio:.3f}", f"{(new_ratio - base_ratio) / base_ratio * 100:+.1f}%")
    c3.metric("Choque aplicado", f"{choque_infl * 100:+.1f}%", "—")
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
