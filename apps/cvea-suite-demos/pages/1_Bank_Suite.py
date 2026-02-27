# CVEA Bank Suite — Credit & Market Risk (NIIF 9, SUDEBAN)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from theme import cvea_header

st.set_page_config(page_title="CVEA Bank Suite (CVEA-BS)", page_icon="🏦", layout="wide")
cvea_header(
    "CVEA Bank Suite (CVEA-BS)",
    "Credit & Market Risk Desk — NIIF 9 · Datos simulados",
)

@st.cache_data
def get_credit_portfolio(n=10_000):
    rng = np.random.default_rng(42)
    ids = np.arange(1, n + 1)
    score = rng.integers(300, 851, size=n)
    ingreso = np.clip(rng.lognormal(8, 0.8, n) * 500, 200, 50000)
    monto = np.clip(rng.lognormal(9, 0.9, n) * 300, 500, 200000)
    tasa = 0.04 + (850 - score) / 10000 + rng.uniform(-0.005, 0.01, n)
    dias_mora = np.where(rng.random(n) < 0.92, 0, rng.exponential(45, n).astype(int))
    # PD aproximada por score
    pd_val = np.clip(1 / (1 + np.exp((score - 600) / 80)) * 0.15 + rng.uniform(0, 0.02, n), 0.001, 0.95)
    estrato = pd.cut(ingreso, bins=[0, 500, 1500, 5000, 100000], labels=["Bajo", "Medio", "Medio-Alto", "Alto"])
    return pd.DataFrame({
        "id_cliente": ids,
        "score_crediticio": score,
        "ingreso_mensual_usd": ingreso,
        "monto_credito": monto,
        "tasa_interes": tasa,
        "dias_mora": dias_mora,
        "probabilidad_default": pd_val,
        "estrato_ingreso": estrato,
    })

@st.cache_data
def get_series_bimonetarias(months=12):
    rng = np.random.default_rng(123)
    dates = pd.date_range(pd.Timestamp.now() - pd.DateOffset(months=months), periods=months, freq="MS")
    pasiva_me = 0.0419 + np.cumsum(rng.normal(0, 0.002, months))
    activa_me = pasiva_me + 0.02 + rng.uniform(0, 0.01, months)
    liquidez = 0.30 + np.cumsum(rng.normal(0, 0.01, months))
    return pd.DataFrame({
        "fecha": dates,
        "tasa_pasiva_me": np.clip(pasiva_me, 0.02, 0.12),
        "tasa_activa_me": np.clip(activa_me, 0.04, 0.18),
        "liquidez_ratio": np.clip(liquidez, 0.1, 0.6),
        "captaciones_mn": 1e6 * (80 + np.cumsum(rng.normal(2, 5, months))),
        "cartera_bruta_mn": 1e6 * (70 + np.cumsum(rng.normal(1, 4, months))),
    })

@st.cache_data
def get_candlestick_data(days=60):
    rng = np.random.default_rng(99)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq="B")
    close = 100 * np.exp(np.cumsum(rng.normal(0.0005, 0.015, days)))
    open_ = np.roll(close, 1)
    open_[0] = 100
    high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.01, days)))
    low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.01, days)))
    return pd.DataFrame({"fecha": dates, "open": open_, "high": high, "low": low, "close": close})

@st.cache_data
def get_correlation_matrix():
    rng = np.random.default_rng(7)
    n = 6
    rets = rng.standard_normal((120, n)) * 0.01
    rets[:, 0] += 0.0005
    corr = np.corrcoef(rets.T)
    return pd.DataFrame(corr, index=[f"Cartera {i+1}" for i in range(n)], columns=[f"Cartera {i+1}" for i in range(n)])

# Sidebar
st.sidebar.header("Controles globales")
choque_macro = st.sidebar.slider("Choque macroeconómico (% impacto inflación/devaluación)", -15.0, 15.0, 0.0, 0.5) / 100
moneda = st.sidebar.selectbox("Vista", ["Moneda Nacional (MN)", "Moneda Extranjera (ME)"], index=1)

df_cred = get_credit_portfolio()
series = get_series_bimonetarias()
# Aplicar choque a ratios
series["liquidez_ratio"] = series["liquidez_ratio"] * (1 - choque_macro)
liquidez_actual = float(series["liquidez_ratio"].iloc[-1])
solvencia_sim = 0.1628 * (1 - choque_macro * 0.5)
morosidad_sim = 0.0244 * (1 + choque_macro * 2)
intermed_sim = 0.65 * (1 - choque_macro * 0.3)

tab1, tab2, tab3 = st.tabs(["Visión general", "Riesgo de crédito (NIIF 9)", "Riesgo de mercado y tesorería"])

with tab1:
    st.subheader("Panel de indicadores")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Liquidez", f"{liquidez_actual:.2%}", f"{choque_macro*100:+.1f}% choque")
    c2.metric("Solvencia", f"{solvencia_sim:.2%}", "—")
    c3.metric("Índice de morosidad", f"{morosidad_sim:.2%}", "—")
    c4.metric("Nivel intermediación financiera", f"{intermed_sim:.1%}", "—")
    st.subheader("Evolución del fondeo (últimos 12 meses)")
    fig_fondo = go.Figure()
    fig_fondo.add_trace(go.Scatter(x=series["fecha"], y=series["captaciones_mn"], name="Captaciones", line=dict(color="blue")))
    fig_fondo.add_trace(go.Scatter(x=series["fecha"], y=series["cartera_bruta_mn"], name="Cartera bruta", line=dict(color="green")))
    fig_fondo.update_layout(xaxis_title="Fecha", yaxis_title="Monto (MN)", height=400)
    st.plotly_chart(fig_fondo, use_container_width=True)

with tab2:
    st.subheader("Migración de cartera (NIIF 9 — Stages)")
    # Stages: 1 Normal, 2 Riesgo significativo, 3 Default
    df_cred["stage"] = np.where(df_cred["dias_mora"] > 90, "Stage 3: Default",
                         np.where((df_cred["dias_mora"] > 30) | (df_cred["probabilidad_default"] > 0.15), "Stage 2: Riesgo significativo", "Stage 1: Normal"))
    stage_counts = df_cred["stage"].value_counts()
    # Sankey: Stage1 -> Stage2 -> Stage3 (simplificado con flujos simulados)
    s1, s2, s3 = stage_counts.get("Stage 1: Normal", 0), stage_counts.get("Stage 2: Riesgo significativo", 0), stage_counts.get("Stage 3: Default", 0)
    nodes = ["Stage 1\nNormal", "Stage 2\nRiesgo sign.", "Stage 3\nDefault"]
    source = [0, 0, 1]
    target = [1, 2, 2]
    value = [int(s1 * 0.08), int(s1 * 0.02), int(s2 * 0.25)]
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(label=nodes, pad=15, thickness=20),
        link=dict(source=source, target=target, value=value),
    )])
    fig_sankey.update_layout(title="Migración entre estadios de riesgo", height=400)
    st.plotly_chart(fig_sankey, use_container_width=True)

    st.subheader("Score crediticio vs Probabilidad de incumplimiento (PD)")
    fig_scatter = px.scatter(df_cred.sample(min(2000, len(df_cred))), x="score_crediticio", y="probabilidad_default", color="estrato_ingreso",
                             title="Credit Score vs PD (por estrato de ingreso)", opacity=0.6)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Cálculo ECL (Pérdida esperada) — EAD × PD × LGD")
    lgd_default = 0.45
    lgd = st.data_editor(pd.DataFrame([{"LGD (Loss Given Default)": lgd_default}]), use_container_width=True, hide_index=True)
    lgd_val = float(lgd.iloc[0].iloc[0])
    if lgd_val < 0 or lgd_val > 1:
        lgd_val = 0.45
    ead = df_cred["monto_credito"].sum()
    pd_avg = df_cred["probabilidad_default"].mean()
    ecl = ead * pd_avg * lgd_val
    st.metric("Pérdida esperada (ECL) USD", f"{ecl:,.0f}", f"LGD = {lgd_val:.0%}")
    st.latex(r"ECL = EAD \times PD \times LGD")

with tab3:
    st.subheader("Índice bursátil / bonos (velas japonesas)")
    cand = get_candlestick_data()
    fig_candle = go.Figure(data=[go.Candlestick(x=cand["fecha"], open=cand["open"], high=cand["high"], low=cand["low"], close=cand["close"])])
    fig_candle.update_layout(xaxis_rangeslider_visible=False, height=400)
    st.plotly_chart(fig_candle, use_container_width=True)
    st.subheader("Mapa de calor de correlaciones entre carteras")
    corr_df = get_correlation_matrix()
    fig_corr = px.imshow(corr_df, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    st.plotly_chart(fig_corr, use_container_width=True)
