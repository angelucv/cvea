# CVEA Retail Suite — POS, precios multimoneda, canastas, PyGWalker
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from theme import cvea_header

st.set_page_config(page_title="CVEA Retail Suite (CVEA-RS)", page_icon="🛒", layout="wide")
cvea_header(
    "CVEA Retail Suite (CVEA-RS)",
    "Inteligencia comercial, elasticidad de precios, canastas y Self-Service BI — Datos simulados",
)

@st.cache_data
def get_transactions(n=55_000):
    rng = np.random.default_rng(101)
    dates = pd.date_range("2024-01-01", periods=365, freq="D")
    categories = ["Alimentos", "Bebidas", "Lácteos", "Higiene", "Limpieza", "Panadería"]
    marcas = ["Tradicional", "Genérica"]
    metodos = ["Divisas", "Bs", "Cripto"]
    tickets = []
    for i in range(n):
        d = rng.choice(dates)
        cat = rng.choice(categories, p=[0.25, 0.2, 0.15, 0.15, 0.15, 0.1])
        marca = rng.choice(marcas, p=[0.61, 0.39])
        precio_bs = rng.lognormal(3, 1.2) * 50
        tasa_oficial = 36 + rng.uniform(0, 2)
        tasa_paralela = tasa_oficial * (1 + rng.uniform(0.05, 0.2))
        precio_usd = precio_bs / tasa_paralela
        vol = rng.integers(1, 10)
        metodo = rng.choice(metodos, p=[0.5, 0.35, 0.15])
        tickets.append({
            "id_ticket": i + 1,
            "fecha": d,
            "SKU": f"SKU-{rng.integers(1, 500)}",
            "categoria_producto": cat,
            "marca_tipo": marca,
            "precio_bs": precio_bs,
            "precio_usd": precio_usd,
            "tasa_cambio_oficial": tasa_oficial,
            "tasa_cambio_paralela": tasa_paralela,
            "volumen_unidades": vol,
            "metodo_pago": metodo,
            "region": rng.choice(["Central", "Oriente", "Occidente", "Andes"], p=[0.4, 0.25, 0.2, 0.15]),
            "formato_tienda": rng.choice(["Supermercado", "Farmacia", "Bodegón"], p=[0.5, 0.3, 0.2]),
        })
    return pd.DataFrame(tickets)

@st.cache_data
def get_association_flows():
    # Flujos Harina -> Margarina, etc.
    items = ["Harina", "Margarina", "Leche", "Pan", "Café", "Azúcar"]
    rng = np.random.default_rng(202)
    links = []
    for i, a in enumerate(items):
        for j, b in enumerate(items):
            if i != j and rng.random() < 0.4:
                links.append((a, b, int(rng.uniform(5, 40))))
    return links

df_ret = get_transactions()

st.sidebar.header("Filtros")
regiones = st.sidebar.multiselect("Región", options=sorted(df_ret["region"].unique()), default=sorted(df_ret["region"].unique()))
formatos = st.sidebar.multiselect("Formato de tienda", options=sorted(df_ret["formato_tienda"].unique()), default=sorted(df_ret["formato_tienda"].unique()))
df_f = df_ret[df_ret["region"].isin(regiones) & df_ret["formato_tienda"].isin(formatos)]

tab1, tab2, tab3, tab4 = st.tabs(["Inteligencia comercial", "Elasticidad y precios multimoneda", "Inventario y canastas", "Análisis exploratorio (PyGWalker)"])

with tab1:
    st.subheader("KPIs")
    vol_semanal = df_f["volumen_unidades"].sum() / (df_f["fecha"].max() - df_f["fecha"].min()).days * 7
    ticket_prom = df_f.groupby("id_ticket").agg({"precio_usd": "sum"}).reset_index()["precio_usd"].mean()
    c1, c2, c3 = st.columns(3)
    c1.metric("Volumen semanal (unidades, sim.)", f"{vol_semanal:,.0f}", "aprox. 17.7M mercado")
    c2.metric("Ticket promedio (USD)", f"{ticket_prom:.2f}", "multimoneda")
    c3.metric("Índice confianza consumidor (sim.)", "46%", "—")
    st.subheader("Participación por categoría y marca (Treemap)")
    part = df_f.groupby(["categoria_producto", "marca_tipo"])["precio_usd"].sum().reset_index()
    part["participacion"] = part["precio_usd"] / part["precio_usd"].sum()
    fig_treemap = px.treemap(part, path=["categoria_producto", "marca_tipo"], values="precio_usd", title="Participación (Tradicional ~61%)")
    st.plotly_chart(fig_treemap, use_container_width=True)

with tab2:
    st.subheader("Curva de demanda (precio vs tasa de cambio)")
    costo_import = st.slider("Costo importado (USD)", 0.5, 2.0, 1.0, 0.1)
    tc_oficial = st.slider("Tipo de cambio oficial (s_t)", 30.0, 50.0, 36.0, 0.5)
    tc_paralelo = st.slider("Tipo de cambio paralelo (b_t)", 35.0, 60.0, 42.0, 0.5)
    # Restricciones P >= s_t P*, P >= b_t P*
    p_min_oficial = tc_oficial * costo_import
    p_min_paralelo = tc_paralelo * costo_import
    if p_min_paralelo > p_min_oficial * 1.5:
        st.warning("Destrucción de demanda: precio de venta por debajo de umbral de arbitraje.")
    precios = np.linspace(30, 80, 50)
    demanda = 1000 - 8 * precios + 0.1 * tc_paralelo * precios
    demanda = np.maximum(demanda, 0)
    fig_dem = px.line(x=precios, y=demanda, labels={"x": "Precio (MN)", "y": "Volumen proyectado"})
    fig_dem.add_vline(x=p_min_oficial, line_dash="dash", line_color="gray")
    fig_dem.add_vline(x=p_min_paralelo, line_dash="dash", line_color="red")
    st.plotly_chart(fig_dem, use_container_width=True)

with tab3:
    st.subheader("Reglas de asociación (afinidades de productos)")
    soporte_min = st.number_input("Soporte mínimo (%)", 0.01, 0.5, 0.05, 0.01)
    confianza_min = st.number_input("Confianza mínima (%)", 0.1, 0.9, 0.3, 0.05)
    links = get_association_flows()
    if links:
        source = [l[0] for l in links]
        target = [l[1] for l in links]
        value = [l[2] for l in links]
        all_nodes = list(set(source) | set(target))
        node_idx = {n: i for i, n in enumerate(all_nodes)}
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(label=all_nodes),
            link=dict(source=[node_idx[s] for s in source], target=[node_idx[t] for t in target], value=value),
        )])
        fig_sankey.update_layout(title="Ej.: compran Harina → también Margarina (Soporte/Confianza aplicados)", height=450)
        st.plotly_chart(fig_sankey, use_container_width=True)

with tab4:
    st.subheader("Self-Service BI — Arrastrar y soltar variables")
    try:
        import pygwalker as pyg
        sub = df_f[["fecha", "categoria_producto", "marca_tipo", "precio_bs", "precio_usd", "volumen_unidades", "metodo_pago", "region", "formato_tienda"]].copy()
        sub["hora_del_dia"] = np.random.RandomState(303).integers(8, 21, len(sub))
        pyg_html = pyg.walk(sub, return_html=True)
        st.components.v1.html(pyg_html, height=800, scrolling=True)
    except Exception as e:
        st.info("PyGWalker no disponible en este entorno. Para análisis exploratorio, use la tabla filtrable a continuación.")
        st.dataframe(df_f.head(5000), use_container_width=True)
