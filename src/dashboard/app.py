"""
app.py — Dashboard principal de análisis de mora del sistema crediticio argentino.
"""
import streamlit as st
import pandas as pd
from components.auth import check_password
from components.filters import render_filters
from components.views import (
    load_datamart_data,
    render_vista_entidades,
    render_vista_deudores,
    render_vista_temporal,
    render_vista_mapa,
)

st.set_page_config(
    page_title="Mora BCRA — Dashboard Analítico",
    page_icon="🏦",
    layout="wide",
)


@st.cache_data(show_spinner="Cargando datos agregados...")
def get_cached_data() -> pd.DataFrame:
    return load_datamart_data()


def aplicar_filtros(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if df.empty:
        return df
    mask = pd.Series(True, index=df.index)
    if filters.get("situaciones"):
        mask &= df["situacion_bcra"].isin(filters["situaciones"])
    if filters.get("entidades"):
        mask &= df["nombre_entidad"].isin(filters["entidades"])
    if filters.get("monto_min", 0) > 0:
        mask &= df["deuda_total_sum"] >= filters["monto_min"]
    if filters.get("solo_refinanciados"):
        mask &= df["sum_flag_refinanciado"] > 0
    if filters.get("solo_judicial"):
        mask &= df["sum_flag_proceso_judicial"] > 0
    if filters.get("solo_recategorizados"):
        mask &= df["sum_flag_recategorizacion"] > 0
    return df[mask]


def main():
    if not check_password():
        st.stop()

    st.title("🏦 Análisis de Mora — Sistema Crediticio Argentino")
    st.markdown("Dashboard exploratorio interactivo | Datos: BCRA & ARCA | Período: **dic-2025**")
    st.info(
        "📌 **Nota metodológica:** Importes en **miles de pesos con 1 decimal** "
        "(ej.: `1234.5` = $1.234.500). "
        "El CUIT/CUIL/CDI se almacena como hash SHA-256 para anonimizar a los deudores. "
        "El 97.9% de los registros tiene `dias_atraso = 0` porque el BCRA permite clasificación "
        "cualitativa de riesgo sin mora acumulada.",
        icon="ℹ️",
    )

    df = get_cached_data()
    if df.empty:
        st.error("No se pudieron cargar los datos. Verificá que el pipeline ETL fue ejecutado.")
        st.stop()

    filters = render_filters(df)
    df_filtered = aplicar_filtros(df, filters)

    st.caption(
        f"Mostrando información agregada de **{df_filtered['registros_count'].sum():,.0f}** registros representativos, "
        f"de un total de {df['registros_count'].sum():,.0f} en el sistema."
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏦 Entidades Financieras",
        "👥 Deudores",
        "📅 Perspectiva Temporal",
        "🗺️ Mapa por Provincia",
        "👨‍👩‍👧‍👦 Personas Físicas",
    ])

    with tab1:
        render_vista_entidades(df_filtered)

    with tab2:
        render_vista_deudores(df_filtered)

    with tab3:
        render_vista_temporal(df_filtered)

    with tab4:
        render_vista_mapa(df_filtered)

    with tab5:
        st.header("Endeudamiento de Personas Físicas")
        if "tipo_persona" in df_filtered.columns and df_filtered["tipo_persona"].notna().any():
            df_fis = df_filtered[df_filtered["tipo_persona"] == "Física"]
            render_vista_deudores(df_fis, tipo_persona="Física")
        else:
            st.info("Requiere Padrón ARCA cargado para distinguir entre personas físicas y jurídicas.")
            render_vista_deudores(df_filtered)


if __name__ == "__main__":
    main()
