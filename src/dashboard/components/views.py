"""
views.py — Componentes de visualización del dashboard de Mora BCRA.
Versión para Data Mart (Liviana): Lee `datamart_bancos.parquet` directamente con pandas.
(Sin DuckDB y sin datos de Nivel-Cliente, apto para Streamlit Cloud).
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE DATOS (DATA MART)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Cargando Data Mart optimizado...")
def load_datamart_data():
    """Lee el Parquet agregado del Data Mart para la web."""
    base_dir = Path(__file__).parent.parent.parent.parent
    datamart_path = base_dir / "data" / "dwh" / "datamart_bancos.parquet"

    if not datamart_path.exists():
        st.warning("⚠️ Data Mart no encontrado. Ejecutá export_datamart_web.py.")
        return pd.DataFrame()

    df = pd.read_parquet(datamart_path, engine="pyarrow")
    
    # Asegurar que nulos numéricos vengan en 0 si es que los hubiera
    num_cols = ["deuda_total_sum", "registros_count", "deudores_unicos", "previsiones_sum",
                "sum_flag_refinanciado", "sum_flag_proceso_judicial", "sum_flag_recategorizacion",
                "sum_flag_sit_juridica", "sum_flag_deuda_cubierta", "dias_atraso"]
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    return df


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

SITUACION_COLORES = {
    1: "#2ecc71",   # Normal — verde
    2: "#f1c40f",   # Seguimiento especial — amarillo
    3: "#e67e22",   # Con problemas — naranja
    4: "#e74c3c",   # Alto riesgo — rojo
    5: "#8e44ad",   # Irrecuperable — violeta
    11: "#3498db",  # Cubierto — azul
}

def _sit_label(sit: int) -> str:
    return {
        1: "1 — Normal", 2: "2 — Seg. especial", 3: "3 — Con problemas",
        4: "4 — Alto riesgo", 5: "5 — Irrecuperable", 11: "11 — Cubierto",
    }.get(sit, str(sit))


def _kpi_row(df: pd.DataFrame):
    """Fila de KPIs genéricos usando datos agrupados."""
    c1, c2, c3, c4 = st.columns(4)
    total_registros = df["registros_count"].sum()
    deuda_total = df["deuda_total_sum"].sum()
    
    deuda_irregular = df[df["situacion_bcra"] >= 3]["deuda_total_sum"].sum()
    tasa_irregular = (deuda_irregular / deuda_total * 100) if deuda_total > 0 else 0

    c1.metric("Casos Crédito/Deuda", f"{total_registros:,.0f}")
    c2.metric("Monto total (miles $)", f"${deuda_total:,.0f}")
    c3.metric(
        "Monto promedio (miles $)", 
        f"${(deuda_total / total_registros):,.0f}" if total_registros > 0 else "$0"
    )
    c4.metric("Cartera irregular ($)", f"{tasa_irregular:.1f}%")


# ─────────────────────────────────────────────────────────────────────────────
# VISTA 1 — ENTIDADES FINANCIERAS
# ─────────────────────────────────────────────────────────────────────────────

def render_vista_entidades(df: pd.DataFrame):
    if df.empty:
        st.info("Sin datos con los filtros actuales.")
        return

    _kpi_row(df)
    st.divider()

    # ── Gráfico 1: Casos por banco y situación (top 20, apilado) ──
    st.subheader("Volumen de casos por entidad y situación crediticia")
    st.caption("Top 20 entidades por número de casos registrados")

    # Obtener el top 20 por cantidad de registros
    top_ents_df = df.groupby("nombre_entidad")["registros_count"].sum().nlargest(20)
    top20_ents = top_ents_df.index.tolist()

    df_top20 = df[df["nombre_entidad"].isin(top20_ents)].copy()
    df_top20["sit_label"] = df_top20["situacion_bcra"].map(_sit_label)

    agg_top20 = (
        df_top20.groupby(["nombre_entidad", "sit_label", "situacion_bcra"])["registros_count"]
        .sum()
        .reset_index(name="casos")
        .sort_values("situacion_bcra")
    )

    orden = top_ents_df.index.tolist()

    color_map = {_sit_label(k): v for k, v in SITUACION_COLORES.items()}
    fig_apilado = px.bar(
        agg_top20,
        x="nombre_entidad",
        y="casos",
        color="sit_label",
        color_discrete_map=color_map,
        category_orders={"nombre_entidad": orden},
        labels={"nombre_entidad": "Entidad", "casos": "Casos", "sit_label": "Situación"},
        height=420,
    )
    fig_apilado.update_layout(
        xaxis_tickangle=-40,
        legend_title_text="Situación",
        barmode="stack",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_apilado, use_container_width=True)

    st.divider()

    # ── Gráfico 2: Top 20 / Tail 20 por volumen de deuda ─────────────────────
    st.subheader("Top 20 y Tail 20 — Volumen de deuda por entidad")

    deuda_ent = (
        df.groupby("nombre_entidad")["deuda_total_sum"]
        .sum()
        .reset_index(name="deuda_total_miles")
        .sort_values("deuda_total_miles", ascending=False)
    )

    col_top, col_tail = st.columns(2)

    with col_top:
        st.markdown("**🔺 Top 20 — Mayor volumen**")
        top20 = deuda_ent.head(20)
        fig_top = px.bar(
            top20, x="deuda_total_miles", y="nombre_entidad",
            orientation="h",
            color="deuda_total_miles",
            color_continuous_scale="Reds",
            labels={"deuda_total_miles": "Deuda (miles $)", "nombre_entidad": ""},
            height=500,
        )
        fig_top.update_layout(
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col_tail:
        st.markdown("**🔻 Tail 20 — Menor volumen**")
        tail20 = deuda_ent[deuda_ent["deuda_total_miles"] > 0].tail(20)
        fig_tail = px.bar(
            tail20, x="deuda_total_miles", y="nombre_entidad",
            orientation="h",
            color="deuda_total_miles",
            color_continuous_scale="Blues",
            labels={"deuda_total_miles": "Deuda (miles $)", "nombre_entidad": ""},
            height=500,
        )
        fig_tail.update_layout(
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_tail, use_container_width=True)

    st.divider()

    # ── Gráfico 3: Scatter 3D — clasificación de entidades ───────────────────
    st.subheader("🔭 Clasificación de entidades — Scatter 3D")
    st.caption("Cada punto es una entidad financiera. Ejes: tasa irregular / cobertura de previsiones / log₁₀(deuda total)")

    # Agrupamos los sumados a nivel banco
    df["n_irregular_count"] = np.where(df["situacion_bcra"] >= 3, df["registros_count"], 0)

    ent_agg = df.groupby("nombre_entidad").agg(
        deuda_total=("deuda_total_sum", "sum"),
        previsiones=("previsiones_sum", "sum"),
        registros=("registros_count", "sum"),
        n_irregular=("n_irregular_count", "sum"),
    ).reset_index()

    ent_agg["tasa_irregular_%"] = (ent_agg["n_irregular"] / ent_agg["registros"] * 100).round(1)
    ent_agg["ratio_previsiones_%"] = (ent_agg["previsiones"] / ent_agg["deuda_total"].replace(0, np.nan) * 100).round(1)
    ent_agg["log_deuda"] = np.log10(ent_agg["deuda_total"].clip(lower=1))
    ent_agg = ent_agg[ent_agg["deuda_total"] > 0].dropna(subset=["ratio_previsiones_%"])

    fig_3d = px.scatter_3d(
        ent_agg,
        x="tasa_irregular_%",
        y="ratio_previsiones_%",
        z="log_deuda",
        color="tasa_irregular_%",
        color_continuous_scale="RdYlGn_r",
        hover_name="nombre_entidad",
        hover_data={"deuda_total": ":,.0f", "tasa_irregular_%": True},
        labels={
            "tasa_irregular_%": "Tasa irregular (%)",
            "ratio_previsiones_%": "Previsiones / Deuda (%)",
            "log_deuda": "log₁₀(Deuda total)",
        },
        height=580,
    )
    fig_3d.update_traces(marker=dict(size=5, opacity=0.85))
    fig_3d.update_layout(
        coloraxis_colorbar_title="Irregular %",
        scene=dict(
            xaxis_title="Tasa irregular (%)",
            yaxis_title="Previsiones / Deuda (%)",
            zaxis_title="log₁₀(Deuda total)",
        ),
    )
    st.plotly_chart(fig_3d, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# VISTA 2 — PERSPECTIVA TEMPORAL
# ─────────────────────────────────────────────────────────────────────────────

def render_vista_temporal(df: pd.DataFrame):
    if df.empty:
        st.info("Sin datos con los filtros actuales.")
        return

    st.subheader("📅 Distribución de Días de Atraso")
    st.info(
        "**Nota metodológica:** El 97.9% de los registros tiene `dias_atraso = 0` porque el BCRA "
        "permite clasificar la situación crediticia por criterio qualitativo sin mora.",
        icon="ℹ️"
    )

    df_con_atraso = df[df["dias_atraso"] > 0].copy()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Casos con atraso > 0 por situación**")
        atraso_sit = (
            df_con_atraso.groupby(["situacion_bcra", "desc_situacion"])
            .agg(registros=("registros_count", "sum"))
            .reset_index()
        )
        atraso_sit["sit_label"] = atraso_sit["situacion_bcra"].map(_sit_label)
        color_map = {_sit_label(k): v for k, v in SITUACION_COLORES.items()}
        fig_con_atraso = px.bar(
            atraso_sit, x="sit_label", y="registros",
            color="sit_label", color_discrete_map=color_map,
            labels={"sit_label": "Situación", "registros": "Casos"},
            height=320,
        )
        fig_con_atraso.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_con_atraso, use_container_width=True)

    with col2:
        st.markdown("**Distribución de días de atraso**")
        # El datamart agrupa. Multiplicamos "registros_count" como el weight del histograma
        filtered_atraso = df_con_atraso[df_con_atraso["dias_atraso"] <= 730]
        fig_hist = px.histogram(
            filtered_atraso,
            x="dias_atraso",
            y="registros_count",
            color="desc_situacion",
            nbins=50,
            labels={"dias_atraso": "Días de atraso", "registros_count": "Casos con atraso"},
            height=320,
            histfunc="sum"
        )
        fig_hist.update_layout(barmode="overlay", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()

    # ── Carga datamart_fechas_origen para vista de antigüedad ─────────────────
    st.subheader("📆 Antigüedad en Situación Normal (Padrón 1DSF)")

    base_dir = Path(__file__).parent.parent.parent.parent
    datamart_fechas_path = base_dir / "data" / "dwh" / "datamart_fechas_origen.parquet"

    if datamart_fechas_path.exists():
        s1 = pd.read_parquet(datamart_fechas_path)
        if not s1.empty and "fecha_origen_situacion1" in s1.columns:
            s1["fecha_str"] = s1["fecha_origen_situacion1"].astype(str)
            s1["anio"] = s1["fecha_str"].str[:4]
            dist_anio = s1.groupby("anio")["deudores_count"].sum().reset_index()
            dist_anio.columns = ["Año de origen en sit. 1", "Deudores"]
            fig_anio = px.bar(
                dist_anio, x="Año de origen en sit. 1", y="Deudores",
                color="Deudores", color_continuous_scale="Blues",
                labels={"Año de origen en sit. 1": "Año de inicio en sit. normal", "Deudores": "Deudores"},
                height=320,
            )
            fig_anio.update_layout(coloraxis_showscale=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_anio, use_container_width=True)
            st.caption(f"Total deudores con fecha de origen conocida: {s1['deudores_count'].sum():,}")
        else:
            st.info("Los datos de fecha de origen están vacíos.")
    else:
        st.info("datamart_fechas_origen.parquet no encontrado.")


# ─────────────────────────────────────────────────────────────────────────────
# VISTA 3 — MAPA DE ARGENTINA
# ─────────────────────────────────────────────────────────────────────────────

def render_vista_mapa(df: pd.DataFrame):
    if df.empty:
        st.info("Sin datos con los filtros actuales.")
        return

    # Comprobar si hay provincias reales en el dataset
    tiene_provincia = "provincia" in df.columns and (df["provincia"].notna() & (df["provincia"] != "Desconocida")).sum() > 0

    if not tiene_provincia:
        st.warning(
            "⚠️ **El Padrón ARCA aún no fue cargado en el DWH o no hay datos geográficos**."
        )
        return

    df["n_irregular_count"] = np.where(df["situacion_bcra"] >= 3, df["registros_count"], 0)

    prov_agg = df.groupby("provincia").agg(
        deuda_total=("deuda_total_sum", "sum"),
        registros=("registros_count", "sum"),
        n_irregular=("n_irregular_count", "sum"),
    ).reset_index()

    prov_agg["tasa_irregular"] = (prov_agg["n_irregular"] / prov_agg["registros"] * 100).replace(np.inf, np.nan).fillna(0)

    import requests
    geojson_url = "https://raw.githubusercontent.com/gonzalo-mena/argentina-geojson/master/provincias.geojson"
    try:
        geojson = requests.get(geojson_url, timeout=5).json()
        fig_mapa = px.choropleth(
            prov_agg,
            geojson=geojson,
            locations="provincia",
            featureidkey="properties.NAME_1",
            color="tasa_irregular",
            hover_data={"registros": True, "deuda_total": ":,.0f"},
            color_continuous_scale="RdYlGn_r",
            labels={"tasa_irregular": "Tasa irregular (%)", "registros": "Casos", "deuda_total": "Deuda ($)"},
            title="Tasa de cartera irregular por provincia",
            fitbounds="locations",
            height=550,
        )
        fig_mapa.update_geos(visible=False)
        st.plotly_chart(fig_mapa, use_container_width=True)
    except Exception:
        # Fallback: barras horizontales
        fig_bar = px.bar(
            prov_agg.sort_values("deuda_total", ascending=False),
            x="deuda_total", y="provincia", orientation="h",
            color="tasa_irregular", color_continuous_scale="RdYlGn_r",
            labels={"deuda_total": "Deuda (miles $)", "provincia": "Provincia"},
            height=600,
        )
        st.plotly_chart(fig_bar, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# VISTA 4 — DEUDORES Y FLAGS
# ─────────────────────────────────────────────────────────────────────────────

def render_vista_deudores(df: pd.DataFrame, tipo_persona: str = "todos"):
    if df.empty:
        st.info("Sin datos.")
        return

    _kpi_row(df)
    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Casos por situación crediticia**")
        sit = df.groupby("desc_situacion")["registros_count"].sum().reset_index()
        fig_sit = px.pie(
            sit, values="registros_count", names="desc_situacion", height=320,
            color_discrete_sequence=px.colors.sequential.RdPu,
        )
        fig_sit.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_sit, use_container_width=True)

    with col_b:
        st.markdown("**Deuda M$ por situación crediticia**")
        sit_d = df.groupby("desc_situacion")["deuda_total_sum"].sum().reset_index()
        fig_sit_d = px.pie(
            sit_d, values="deuda_total_sum", names="desc_situacion", height=320,
            color_discrete_sequence=px.colors.sequential.Blues,
        )
        fig_sit_d.update_traces(textposition="inside", textinfo="percent")
        st.plotly_chart(fig_sit_d, use_container_width=True)

    st.divider()
    st.markdown("**Flags de Riesgo — Instancias**")
    flags = {
        "Refinanciados":                   int(df["sum_flag_refinanciado"].sum()),
        "Proceso judicial activo":         int(df["sum_flag_proceso_judicial"].sum()),
        "Recategorización obligatoria":    int(df["sum_flag_recategorizacion"].sum()),
        "Situación jurídica activa":       int(df["sum_flag_sit_juridica"].sum()),
        "Deuda totalmente cubierta":       int(df["sum_flag_deuda_cubierta"].sum()),
    }
    flags_df = pd.DataFrame.from_dict(flags, orient="index", columns=["Casos"])
    total_registros = df["registros_count"].sum()
    flags_df["% del total"] = (flags_df["Casos"] / total_registros * 100).round(2) if total_registros > 0 else 0
    fig_flags = px.bar(
        flags_df.reset_index(), x="index", y="Casos",
        color="Casos", color_continuous_scale="Oranges",
        labels={"index": "Flag", "Casos": "Casos"},
        height=320,
    )
    fig_flags.update_layout(coloraxis_showscale=False, xaxis_tickangle=-20, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_flags, use_container_width=True)

