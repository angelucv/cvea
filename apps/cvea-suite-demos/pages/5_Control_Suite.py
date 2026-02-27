# CVEA Control Suite — Flotas, OEE, mantenimiento, gastos, PyGWalker
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from theme import cvea_header

st.set_page_config(page_title="CVEA Control Suite (CVEA-CS)", page_icon="⚙️", layout="wide")
cvea_header(
    "CVEA Control Suite (CVEA-CS)",
    "Cadena de suministro, mantenimiento predictivo, gastos operativos y análisis exploratorio — Datos simulados",
)

@st.cache_data
def get_logistics_data(n=12_000):
    rng = np.random.default_rng(333)
    # Venezuela bounds approx
    lat = 10.0 + rng.uniform(-2, 2, n)
    lon = -66.5 + rng.uniform(-3, 3, n)
    consumo = rng.lognormal(3, 0.5, n)
    km = rng.lognormal(6, 0.4, n)
    estado = rng.choice(["Activo", "En Mantenimiento", "Detenido"], n, p=[0.85, 0.10, 0.05])
    tiempo_ciclo = rng.lognormal(4, 0.6, n)
    costo = rng.lognormal(8, 0.5, n)
    ids = [f"V{i}" for i in range(1, n // 100 + 1)] * 100
    rng.shuffle(ids)
    ids = ids[:n]
    return pd.DataFrame({
        "id_vehiculo": ids,
        "lat": lat,
        "lon": lon,
        "consumo_combustible_litros": consumo,
        "kilometros_recorridos": km,
        "estado_operativo": estado,
        "tiempo_ciclo_produccion": tiempo_ciclo,
        "costo_operativo_usd": costo,
    })

df_log = get_logistics_data()

st.sidebar.header("Controles")
variabilidad_combustible = st.sidebar.slider("Variabilidad precio/disponibilidad combustible (%)", -20.0, 20.0, 0.0, 1.0) / 100
fecha_ini = st.sidebar.date_input("Fecha inicio auditoría", pd.Timestamp("2024-01-01"))
fecha_fin = st.sidebar.date_input("Fecha fin auditoría", pd.Timestamp("2024-12-31"))

tab1, tab2, tab3, tab4 = st.tabs(["Cadena de suministro y flotas", "Eficiencia industrial y mantenimiento", "Sostenibilidad y gastos", "Análisis exploratorio"])

with tab1:
    st.subheader("KPIs logísticos")
    costo_km = (df_log["costo_operativo_usd"].sum() / (df_log["kilometros_recorridos"].sum() + 1)) * (1 + variabilidad_combustible)
    rend_comb = df_log["kilometros_recorridos"].sum() / (df_log["consumo_combustible_litros"].sum() + 1)
    otif_sim = 0.88 + np.random.RandomState(1).uniform(0, 0.05)
    c1, c2, c3 = st.columns(3)
    c1.metric("Costo por kilómetro (USD/km)", f"{costo_km:.2f}", f"{variabilidad_combustible*100:+.0f}% comb.")
    c2.metric("Rendimiento combustible (km/L)", f"{rend_comb:.1f}", "—")
    c3.metric("OTIF (On Time In Full)", f"{otif_sim:.1%}", "—")
    st.subheader("Mapa de flota y rutas (centros → entregas)")
    try:
        import pydeck as pdk
        centro = df_log.groupby("id_vehiculo").agg({"lat": "mean", "lon": "mean"}).reset_index().head(200)
        view = pdk.ViewState(latitude=10.0, longitude=-66.5, zoom=5, pitch=40)
        layer1 = pdk.Layer("ScatterplotLayer", centro, get_position=["lon", "lat"], get_radius=5000, get_color=[100, 150, 200], pickable=True)
        r = pdk.Deck(layers=[layer1], initial_view_state=view, map_style="light")
        st.pydeck_chart(r)
    except Exception as e:
        st.info("Mapa PyDeck no disponible. Mostrando muestra de coordenadas.")
        st.dataframe(df_log[["id_vehiculo", "lat", "lon", "estado_operativo"]].drop_duplicates().head(100))

with tab2:
    st.subheader("OEE (Overall Equipment Effectiveness)")
    oee_val = 0.72 + np.random.RandomState(44).uniform(-0.05, 0.05)
    fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=oee_val * 100, number={"suffix": "%"}, gauge={"axis": {"range": [0, 100]}, "bar": {"color": "darkblue"}, "steps": [{"range": [0, 50], "color": "lightgray"}, {"range": [50, 75], "color": "gray"}, {"range": [75, 100], "color": "lightblue"}], "threshold": {"line": {"color": "red", "width": 4}, "value": 85}}))
    fig_gauge.update_layout(title="OEE en tiempo real (simulado)", height=350)
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.subheader("Frecuencia de fallas por zona/turno (heatmap)")
    df_log["zona"] = pd.cut(df_log["lat"], 5, labels=["Z1", "Z2", "Z3", "Z4", "Z5"])
    df_log["turno"] = np.random.RandomState(55).choice(["Mañana", "Tarde", "Noche"], len(df_log))
    fallas = df_log.groupby(["zona", "turno"]).size().unstack(fill_value=0)
    fig_heat = px.imshow(fallas, text_auto=True, aspect="auto", color_continuous_scale="Reds")
    st.plotly_chart(fig_heat, use_container_width=True)
    st.subheader("Curva de supervivencia — Probabilidad de falla a 30 días")
    t = np.linspace(0, 30, 100)
    # Weibull simplificado
    shape, scale = 1.5, 25
    surv = np.exp(-(t / scale) ** shape)
    prob_falla_30 = 1 - surv[-1]
    fig_surv = go.Figure()
    fig_surv.add_trace(go.Scatter(x=t, y=surv, mode="lines", name="P(sin falla)"))
    fig_surv.update_layout(xaxis_title="Días", yaxis_title="P(sin falla)", title=f"P(falla antes 30 días) ≈ {prob_falla_30:.1%}", height=350)
    st.plotly_chart(fig_surv, use_container_width=True)
    if st.button("Simular orden de mantenimiento preventivo"):
        st.success("Orden ejecutada. Probabilidad de falla reiniciada (simulación).")

with tab3:
    st.subheader("Desglose presupuesto operativo (Waterfall)")
    presupuesto = 2_500_000
    diesel = -600_000
    peajes = -80_000
    mantenimiento = -120_000
    depreciacion = -200_000
    margen = presupuesto + diesel + peajes + mantenimiento + depreciacion
    x = ["Presupuesto total", "Diesel", "Peajes", "Mantenimiento flota", "Depreciación", "Margen operativo neto"]
    y = [presupuesto, diesel, peajes, mantenimiento, depreciacion, margen]
    colors = ["blue" if v >= 0 else "red" for v in y]
    fig_w = go.Figure(go.Bar(x=x, y=y, marker_color=colors, text=[f"{v:,.0f}" for v in y], textposition="outside"))
    fig_w.update_layout(title="Cascada de gastos operativos", yaxis_title="USD", height=400)
    st.plotly_chart(fig_w, use_container_width=True)

with tab4:
    st.subheader("Self-Service Analytics")
    try:
        import pygwalker as pyg
        sub = df_log.copy()
        sub["mes"] = np.random.RandomState(404).integers(1, 13, len(sub))
        pyg_html = pyg.walk(sub, return_html=True)
        st.components.v1.html(pyg_html, height=700, scrolling=True)
    except Exception as e:
        st.info("PyGWalker no disponible. Use la tabla para cruzar estado_operativo, tiempo_ciclo_produccion, etc.")
        st.dataframe(df_log.head(2000), use_container_width=True)
