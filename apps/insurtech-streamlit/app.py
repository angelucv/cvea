import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


@st.cache_data
def simulate_market_data(n_companies: int = 15, n_months: int = 36):
    rng = np.random.default_rng(123)
    dates = pd.date_range("2023-01-01", periods=n_months, freq="MS")
    companies = ["Mi Compañía"] + [f"Aseguradora {chr(65+i)}" for i in range(1, n_companies)]

    records = []
    for comp in companies:
        capital = rng.normal(5_000_000, 1_000_000)
        patrimonio = rng.normal(8_000_000, 2_000_000)
        activos = rng.normal(20_000_000, 5_000_000)
        for d in dates:
            pnc = abs(rng.normal(60_000, 25_000))
            sin_paid = abs(rng.normal(35_000, 12_000))
            gastos = abs(rng.normal(18_000, 6_000))
            resultado = rng.normal(25_000, 12_000)
            reservas = abs(rng.normal(11_000_000, 3_000_000))
            records.append(
                dict(
                    Empresa=comp,
                    Fecha=d,
                    PNC_USD=pnc,
                    Siniestros_Pagados_Netos_USD=sin_paid,
                    Gastos_Generales_USD=gastos,
                    Resultado_Neto_USD=resultado,
                    Capital_Social_Suscrito_USD=capital,
                    Activos_Totales_USD=activos,
                    Reservas_Tecnicas_Netas_USD=reservas,
                    Patrimonio_USD=patrimonio,
                )
            )

    df = pd.DataFrame.from_records(records)
    df["Siniestralidad_Pagada"] = df["Siniestros_Pagados_Netos_USD"] / df["PNC_USD"]
    df["ROE"] = df["Resultado_Neto_USD"] / df["Patrimonio_USD"]
    df["Ratio_Gastos"] = df["Gastos_Generales_USD"] / df["PNC_USD"]
    df["Ratio_Capital"] = df["Patrimonio_USD"] / df["Activos_Totales_USD"]
    return df


@st.cache_data
def simulate_portfolio(n_policies: int = 4000, start="2023-01-01", end="2025-12-31"):
    rng = np.random.default_rng(456)
    dates = pd.date_range(start, end, freq="D")
    ramos = ["Automóvil", "Salud", "Personas", "Patrimoniales", "Fianzas"]
    canales = ["Corredor", "Agente", "Bancaseguros", "Web"]

    pol_dates = rng.choice(dates, size=n_policies)
    primas = abs(rng.normal(800, 300, size=n_policies))

    pol = pd.DataFrame(
        dict(
            ID_Poliza=np.arange(1, n_policies + 1),
            Ramo=rng.choice(ramos, size=n_policies, p=[0.4, 0.3, 0.15, 0.1, 0.05]),
            Prima_Neta_USD=primas,
            Canal_Distribucion=rng.choice(canales, size=n_policies),
            Fecha_Emision=pol_dates,
        )
    )

    n_claims = int(n_policies * 0.25)
    sin = pd.DataFrame(
        dict(
            ID_Poliza=rng.choice(pol["ID_Poliza"], size=n_claims),
            Fecha_Ocurrencia=rng.choice(dates, size=n_claims),
            Monto_Pagado_USD=abs(rng.normal(1200, 900, size=n_claims)),
            Estado=rng.choice(
                ["Pagado", "En Proceso", "Rechazado"],
                size=n_claims,
                p=[0.7, 0.2, 0.1],
            ),
        )
    )
    sin = sin.merge(pol[["ID_Poliza", "Ramo", "Canal_Distribucion"]], on="ID_Poliza", how="left")
    return pol, sin


def layout_header():
    st.title("Actuarial Insurtech – CVEA Suite Demo")
    st.caption(
        "Versión demostrativa en **Python / Streamlit** inspirada en ActuarialInsurtechCARAMELS. "
        "Los datos son simulados con fines pedagógicos."
    )


def sidebar_filters(df_market: pd.DataFrame):
    st.sidebar.header("Filtros globales")
    min_date, max_date = df_market["Fecha"].min(), df_market["Fecha"].max()
    date_range = st.sidebar.date_input(
        "Periodo de análisis",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    if not isinstance(date_range, (list, tuple)) or len(date_range) != 2:
        date_range = (min_date, max_date)

    empresas = df_market["Empresa"].unique().tolist()
    default_company = "Mi Compañía" if "Mi Compañía" in empresas else empresas[0]
    empresa_sel = st.sidebar.selectbox("Compañía de referencia", empresas, index=empresas.index(default_company))

    return date_range, empresa_sel


def page_market_overview(df: pd.DataFrame, date_range):
    st.subheader("1. Visión general del mercado")
    df_period = df[(df["Fecha"] >= pd.to_datetime(date_range[0])) & (df["Fecha"] <= pd.to_datetime(date_range[1]))]

    kpi = (
        df_period.groupby("Fecha")[["PNC_USD", "Siniestros_Pagados_Netos_USD", "Resultado_Neto_USD"]]
        .sum()
        .reset_index()
    )
    kpi["Siniestralidad_Pagada"] = kpi["Siniestros_Pagados_Netos_USD"] / kpi["PNC_USD"]

    col1, col2, col3 = st.columns(3)
    col1.metric("PNC promedio mensual (USD)", f"{kpi['PNC_USD'].mean():,.0f}")
    col2.metric("Siniestralidad pagada promedio", f"{kpi['Siniestralidad_Pagada'].mean():.1%}")
    col3.metric("Resultado neto promedio (USD)", f"{kpi['Resultado_Neto_USD'].mean():,.0f}")

    fig_pnc = px.line(kpi, x="Fecha", y="PNC_USD", title="PNC mensual – mercado")
    fig_sin = px.line(kpi, x="Fecha", y="Siniestralidad_Pagada", title="Siniestralidad pagada – mercado")
    col_a, col_b = st.columns(2)
    col_a.plotly_chart(fig_pnc, use_container_width=True)
    col_b.plotly_chart(fig_sin, use_container_width=True)


def page_company_vs_market(df: pd.DataFrame, date_range, empresa_sel: str):
    st.subheader("2. Mi compañía vs mercado")
    df_period = df[(df["Fecha"] >= pd.to_datetime(date_range[0])) & (df["Fecha"] <= pd.to_datetime(date_range[1]))]

    df_market = df_period.groupby("Fecha")[["PNC_USD", "Siniestros_Pagados_Netos_USD"]].sum().reset_index()
    df_market["Siniestralidad_Pagada"] = df_market["Siniestros_Pagados_Netos_USD"] / df_market["PNC_USD"]
    df_comp = (
        df_period[df_period["Empresa"] == empresa_sel]
        .groupby("Fecha")[["PNC_USD", "Siniestros_Pagados_Netos_USD"]]
        .sum()
        .reset_index()
    )
    df_comp["Siniestralidad_Pagada"] = df_comp["Siniestros_Pagados_Netos_USD"] / df_comp["PNC_USD"]

    df_comp["Tipo"] = empresa_sel
    df_market["Tipo"] = "Mercado"
    df_long = pd.concat(
        [
            df_comp[["Fecha", "Siniestralidad_Pagada", "Tipo"]],
            df_market[["Fecha", "Siniestralidad_Pagada", "Tipo"]],
        ]
    )

    fig = px.line(
        df_long,
        x="Fecha",
        y="Siniestralidad_Pagada",
        color="Tipo",
        title="Siniestralidad pagada – Mi compañía vs mercado",
    )
    st.plotly_chart(fig, use_container_width=True)

    tabla_resumen = (
        df_period.groupby("Empresa")[["PNC_USD", "Siniestros_Pagados_Netos_USD", "Resultado_Neto_USD"]]
        .sum()
        .assign(Siniestralidad=lambda x: x["Siniestros_Pagados_Netos_USD"] / x["PNC_USD"])
        .reset_index()
    )
    st.dataframe(tabla_resumen.style.format({"PNC_USD": "{:,.0f}", "Siniestros_Pagados_Netos_USD": "{:,.0f}", "Resultado_Neto_USD": "{:,.0f}", "Siniestralidad": "{:.1%}"}))


def page_portfolio(pol: pd.DataFrame, sin: pd.DataFrame):
    st.subheader("3. Cartera técnica simulada")

    col1, col2 = st.columns(2)
    ramo_sel = col1.multiselect("Ramos", sorted(pol["Ramo"].unique()), default=sorted(pol["Ramo"].unique()))
    canal_sel = col2.multiselect(
        "Canales de distribución",
        sorted(pol["Canal_Distribucion"].unique()),
        default=sorted(pol["Canal_Distribucion"].unique()),
    )

    pol_f = pol[pol["Ramo"].isin(ramo_sel) & pol["Canal_Distribucion"].isin(canal_sel)]
    sin_f = sin[sin["Ramo"].isin(ramo_sel) & sin["Canal_Distribucion"].isin(canal_sel)]

    st.metric("Número de pólizas", f"{len(pol_f):,}")
    st.metric("Número de siniestros", f"{len(sin_f):,}")

    primas_ramo = pol_f.groupby("Ramo")["Prima_Neta_USD"].sum().reset_index()
    fig_primas = px.bar(primas_ramo, x="Ramo", y="Prima_Neta_USD", title="Prima neta por ramo")
    st.plotly_chart(fig_primas, use_container_width=True)

    if not sin_f.empty:
        sin_ramo = sin_f.groupby("Ramo")["Monto_Pagado_USD"].sum().reset_index()
        fig_sin = px.bar(sin_ramo, x="Ramo", y="Monto_Pagado_USD", title="Monto pagado por ramo")
        st.plotly_chart(fig_sin, use_container_width=True)


def main():
    layout_header()

    df_market = simulate_market_data()
    pol, sin = simulate_portfolio()

    date_range, empresa_sel = sidebar_filters(df_market)

    tab1, tab2, tab3 = st.tabs(
        [
            "Visión general mercado",
            "Mi compañía vs mercado",
            "Cartera técnica simulada",
        ]
    )

    with tab1:
        page_market_overview(df_market, date_range)
    with tab2:
        page_company_vs_market(df_market, date_range, empresa_sel)
    with tab3:
        page_portfolio(pol, sin)


if __name__ == "__main__":
    main()

