"""
filters.py — Sidebar de filtros interactivos del dashboard de Mora BCRA.
Adaptado al schema del DWH v2.
"""
import streamlit as st
import pandas as pd


def render_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("🔍 Filtros")

    if df.empty:
        return {
            "situaciones": list(range(1, 6)),
            "entidades": [],
            "monto_min": 0,
            "solo_con_prestamos": False,
        }

    # ── Situación crediticia ──────────────────────────────────────────────────
    sit_map = {
        1: "1 — Normal",
        2: "2 — Seguimiento especial",
        3: "3 — Con problemas",
        4: "4 — Alto riesgo",
        5: "5 — Irrecuperable",
        11: "11 — Cubierto (garantía pref. A)",
    }
    sits_disponibles = sorted(df["situacion_bcra"].dropna().unique())
    sit_labels = [sit_map.get(s, str(s)) for s in sits_disponibles]
    selected_labels = st.sidebar.multiselect(
        "Situación BCRA",
        options=sit_labels,
        default=sit_labels,
    )
    # Mapear etiquetas de vuelta a números
    inv_map = {v: k for k, v in sit_map.items()}
    selected_sits = [inv_map.get(l, int(l.split(" ")[0])) for l in selected_labels]

    # ── Entidades financieras ─────────────────────────────────────────────────
    entidades = sorted(df["nombre_entidad"].dropna().unique().tolist())
    selected_entidades = st.sidebar.multiselect(
        "Entidades financieras",
        options=entidades,
        default=entidades,
        help="Filtrá por entidad acreedora (banco, financiera, mutual, etc.)"
    )

    # ── Monto mínimo de deuda ─────────────────────────────────────────────────
    monto_max = int(df["deuda_total_sum"].max()) if df["deuda_total_sum"].max() > 0 else 1_000_000
    monto_min = st.sidebar.number_input(
        "Deuda total mínima (miles $)",
        min_value=0,
        max_value=monto_max,
        value=0,
        step=100,
        help="Filtrá registros con deuda total mayor a este valor (en miles de pesos)"
    )

    # ── Flags de riesgo ───────────────────────────────────────────────────────
    st.sidebar.subheader("Flags de Riesgo")
    solo_refinanciados = st.sidebar.checkbox("Solo refinanciados")
    solo_judicial = st.sidebar.checkbox("Solo en proceso judicial")
    solo_recategorizados = st.sidebar.checkbox("Solo recategorización obligatoria")

    return {
        "situaciones": selected_sits,
        "entidades": selected_entidades,
        "monto_min": monto_min,
        "solo_refinanciados": solo_refinanciados,
        "solo_judicial": solo_judicial,
        "solo_recategorizados": solo_recategorizados,
    }
