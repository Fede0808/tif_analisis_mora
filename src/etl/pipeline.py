"""
pipeline.py — ETL Out-of-Core con DuckDB para datos del BCRA y ARCA.

Fuentes:
  BCRA: deudores.txt, inf_ret.txt, inf_retparc.txt, morexent.txt,
        nomdeu.txt, nommor.txt, maeent.txt, 1DSF.txt, 24DSF.txt
  ARCA: Padron_ARCA.txt, Actividades_ARCA.txt

Nota metodológica:
  Los importes están expresados en miles de pesos con un decimal.
  El campo `nro_identificacion` (CUIT/CUIL/CDI) es el punto de enlace
  entre la Central de Deudores del BCRA y el Padrón ARCA.

ADVERTENCIA DE GOBERNANZA:
  El `nro_identificacion` se mantiene temporalmente en el DWH local
  para posibilitar el join entre fuentes. DEBE ser reemplazado por
  `hash_id` y eliminado antes de cualquier deploy web o publicación.
  Ver sección "Anonimización" en TODO.md.
"""

import duckdb
import os
import pandas as pd
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES DE ANCHO POSICIONAL (FWF — Fixed-Width Format)
# ─────────────────────────────────────────────────────────────────────────────

# deudores.txt: 24 campos, ancho total = 171 caracteres
DEUDORES_WIDTHS = [5, 6, 2, 11, 3, 2, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 1, 1, 1, 1, 1, 1, 4]
DEUDORES_COLS = [
    "cod_entidad", "fecha_informacion", "tipo_identificacion", "nro_identificacion",
    "cod_actividad", "situacion",
    "prestamos_garantias_afrontadas", "sin_uso",
    "garantias_otorgadas", "otros_conceptos",
    "garantias_pref_a", "garantias_pref_b", "sin_garantias_pref",
    "contragarantias_pref_a", "contragarantias_pref_b", "sin_contragarantias_pref",
    "previsiones",
    "deuda_cubierta", "proceso_judicial_revision",
    "refinanciaciones", "recategorizacion_obligatoria",
    "situacion_juridica", "irrecuperables_ultimo_parrafo",
    "dias_atraso",
]

# inf_ret.txt / inf_retparc.txt: 7 campos
RECTIF_WIDTHS = [5, 6, 2, 11, 55, 2, 12]
RECTIF_COLS = [
    "cod_entidad", "fecha_informacion", "tipo_identificacion",
    "nro_identificacion", "denominacion", "situacion", "monto",
]

# morexent.txt: 5 campos
MOREX_WIDTHS = [6, 120, 2, 11, 1]
MOREX_COLS = [
    "fecha_informacion", "denominacion_ente_residual",
    "tipo_identificacion", "nro_identificacion", "proceso_judicial_revision",
]

# nomdeu.txt / nommor.txt: 2 campos
NOMALT_WIDTHS = [11, 55]
NOMALT_COLS = ["nro_identificacion", "denominacion"]

# maeent.txt: 2 campos
MAEENT_WIDTHS = [5, 70]
MAEENT_COLS = ["cod_entidad", "nombre_entidad"]

# 1DSF.txt: 3 campos
DSF1_WIDTHS = [2, 11, 6]
DSF1_COLS = ["tipo_identificacion", "nro_identificacion", "fecha_origen_situacion1"]

# 24DSF.txt: 3 campos fijos + 24 x 3 repeating = 75 campos totales
DSF24_FIXED_WIDTHS = [5, 2, 11]
DSF24_FIXED_COLS = ["cod_entidad", "tipo_identificacion", "nro_identificacion"]
DSF24_REPEAT_WIDTHS = [2, 12, 1]  # situacion, monto, proceso_judicial por mes

# Padron_ARCA.txt: 10 campos
PADRON_WIDTHS = [11, 160, 6, 1, 11, 10, 1, 10, 2, 8]
PADRON_COLS = [
    "cuit_cuil_cdi", "denominacion", "cod_actividad_arca",
    "marca_baja", "cuit_reemplazo",
    "fecha_nac_contrato", "sexo", "codigo_postal",
    "cod_provincia", "fecha_fallecimiento",
]

# Actividades_ARCA.txt: 2 campos
ACTIVIDADES_WIDTHS = [6, 254]
ACTIVIDADES_COLS = ["cod_actividad_arca", "descripcion"]

# Provincias (dominio estático según LEAME PADRON)
PROVINCIAS = {
    "00": "Ciudad Autónoma de Buenos Aires",
    "01": "Buenos Aires",
    "02": "Catamarca",
    "03": "Córdoba",
    "04": "Corrientes",
    "05": "Entre Ríos",
    "06": "Jujuy",
    "07": "Mendoza",
    "08": "La Rioja",
    "09": "Salta",
    "10": "San Juan",
    "11": "San Luis",
    "12": "Santa Fe",
    "13": "Santiago del Estero",
    "14": "Tucumán",
    "16": "Chaco",
    "17": "Chubut",
    "18": "Formosa",
    "19": "Misiones",
    "20": "Neuquén",
    "21": "La Pampa",
    "22": "Río Negro",
    "23": "Santa Cruz",
    "24": "Tierra del Fuego",
}


class BCRA_ETL:
    """
    Pipeline ETL Out-of-Core con DuckDB.
    Lee archivos de ancho fijo del BCRA/ARCA y genera un Star Schema en DuckDB + Parquet.

    Fuentes BCRA: deudores.txt, inf_ret.txt, inf_retparc.txt, morexent.txt,
                  nomdeu.txt, nommor.txt, maeent.txt, 1DSF.txt, 24DSF.txt
    Fuentes ARCA: Padron_ARCA.txt, Actividades_ARCA.txt
    """

    def __init__(self, raw_data_dir: str, dwh_dir: str):
        self.raw_data_dir = Path(raw_data_dir)
        self.dwh_dir = Path(dwh_dir)
        self.dwh_dir.mkdir(parents=True, exist_ok=True)

        db_path = str(self.dwh_dir / "bcra_dwh.duckdb")
        self.con = duckdb.connect(db_path)
        print(f"[INFO] DuckDB Data Warehouse conectado en: {db_path}")

    # ─────────────────────────────────────────────────────────────────────────
    # ESQUEMA
    # ─────────────────────────────────────────────────────────────────────────

    def _create_schema(self):
        """Define la estructura completa del Data Warehouse (Star Schema)."""
        print("[INFO] Creando/verificando esquema completo del DWH...")

        # ── DIMENSIONES ──────────────────────────────────────────────────────

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS dim_entidad (
                cod_entidad VARCHAR PRIMARY KEY,
                nombre_entidad VARCHAR
            )
        """)

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS dim_situacion (
                id_situacion INTEGER PRIMARY KEY,
                descripcion VARCHAR,
                is_default BOOLEAN
            )
        """)
        self.con.execute("""
            INSERT OR IGNORE INTO dim_situacion VALUES
            (1,  'Normal',                                          FALSE),
            (2,  'Con seguimiento especial / Riesgo bajo',          FALSE),
            (3,  'Con problemas / Riesgo medio',                    TRUE),
            (4,  'Con alto riesgo de insolvencia / Riesgo alto',    TRUE),
            (5,  'Irrecuperable',                                   TRUE),
            (11, 'Cubierto totalmente por garantías preferidas A',  FALSE)
        """)

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS dim_provincia (
                cod_provincia VARCHAR PRIMARY KEY,
                nombre_provincia VARCHAR
            )
        """)
        for cod, nombre in PROVINCIAS.items():
            self.con.execute(
                "INSERT OR IGNORE INTO dim_provincia VALUES (?, ?)", [cod, nombre]
            )

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS dim_actividad (
                cod_actividad_arca VARCHAR PRIMARY KEY,
                descripcion VARCHAR
            )
        """)

        # ⚠ GOBERNANZA: nro_identificacion temporal — destruir antes de publicación web
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS dim_persona (
                hash_id VARCHAR PRIMARY KEY,
                nro_identificacion VARCHAR,          -- PII: eliminar antes de publicación
                tipo_persona VARCHAR,                -- Física / Jurídica
                denominacion VARCHAR,                -- PII: eliminar antes de publicación
                cod_actividad_arca VARCHAR,
                marca_baja VARCHAR,
                cuit_reemplazo VARCHAR,              -- PII: eliminar antes de publicación
                fecha_nac_contrato VARCHAR,          -- PII: eliminar antes de publicación
                sexo VARCHAR,
                codigo_postal VARCHAR,
                cod_provincia VARCHAR,
                fecha_fallecimiento VARCHAR          -- PII: eliminar antes de publicación
            )
        """)

        # Tabla auxiliar: deudores sin padrón (BCRA empadronamiento propio)
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS dim_no_empadronados (
                nro_identificacion VARCHAR PRIMARY KEY,
                denominacion VARCHAR,
                origen VARCHAR    -- 'deudor' o 'moroso'
            )
        """)

        # Tabla auxiliar: fecha de inicio en situación normal
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS dim_situacion1_origen (
                nro_identificacion VARCHAR PRIMARY KEY,
                tipo_identificacion VARCHAR,
                fecha_origen_situacion1 INTEGER
            )
        """)

        # ── TABLAS DE HECHOS ─────────────────────────────────────────────────

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS fact_deuda_mensual (
                hash_id                         VARCHAR,
                periodo_yyyymm                  INTEGER,
                cod_entidad                     VARCHAR,
                id_situacion                    INTEGER,
                -- Montos (miles de pesos con 1 decimal)
                prestamos_garantias_afrontadas  DECIMAL(12,1),
                sin_uso                         DECIMAL(12,1),
                garantias_otorgadas             DECIMAL(12,1),
                otros_conceptos                 DECIMAL(12,1),
                garantias_pref_a                DECIMAL(12,1),
                garantias_pref_b                DECIMAL(12,1),
                sin_garantias_pref              DECIMAL(12,1),
                contragarantias_pref_a          DECIMAL(12,1),
                contragarantias_pref_b          DECIMAL(12,1),
                sin_contragarantias_pref        DECIMAL(12,1),
                previsiones                     DECIMAL(12,1),
                -- Flags
                deuda_cubierta                  TINYINT,
                proceso_judicial_revision       TINYINT,
                refinanciaciones                TINYINT,
                recategorizacion_obligatoria    TINYINT,
                situacion_juridica              TINYINT,
                irrecuperables_ultimo_parrafo   TINYINT,
                dias_atraso                     INTEGER
            )
        """)

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS fact_historial_24 (
                cod_entidad         VARCHAR,
                nro_identificacion  VARCHAR,
                mes_n               INTEGER,    -- 0 = período actual, 23 = más antiguo
                periodo_yyyymm      INTEGER,    -- calculado externamente si disponible
                situacion           INTEGER,
                monto               DECIMAL(12,1),
                proceso_judicial    TINYINT
            )
        """)

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS fact_rectificativas (
                tipo_rectif         VARCHAR,    -- 'completa' o 'parcial'
                cod_entidad         VARCHAR,
                fecha_informacion   INTEGER,
                tipo_identificacion VARCHAR,
                nro_identificacion  VARCHAR,    -- PII: eliminar antes de publicación
                denominacion        VARCHAR,    -- PII: eliminar antes de publicación
                situacion           INTEGER,
                monto               DECIMAL(12,1)
            )
        """)

        self.con.execute("""
            CREATE TABLE IF NOT EXISTS fact_morosos_exentidades (
                fecha_informacion           INTEGER,
                denominacion_ente_residual  VARCHAR,
                tipo_identificacion         VARCHAR,
                nro_identificacion          VARCHAR,   -- PII: eliminar antes de publicación
                proceso_judicial_revision   TINYINT
            )
        """)

        print("[OK] Esquema creado/verificado correctamente.")

    # ─────────────────────────────────────────────────────────────────────────
    # MÉTODOS ETL — DIMENSIONES
    # ─────────────────────────────────────────────────────────────────────────

    def load_entities(self, maeent_path: str):
        """Carga el Maestro de Entidades BCRA (maeent.txt)."""
        if not os.path.exists(maeent_path):
            print(f"[WARN] Archivo no encontrado: {maeent_path}")
            return
        print(f"[INFO] Ingestando Maestro de Entidades: {maeent_path}")
        df = pd.read_fwf(
            maeent_path, widths=MAEENT_WIDTHS, header=None,
            names=MAEENT_COLS, encoding="latin1", dtype=str
        )
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        self.con.register("df_entidades", df)
        self.con.execute("INSERT OR IGNORE INTO dim_entidad SELECT cod_entidad, nombre_entidad FROM df_entidades")
        self.con.unregister("df_entidades")
        print(f"[OK] Entidades cargadas: {len(df)}")

    def load_actividades_arca(self, actividades_path: str):
        """Carga el catálogo de actividades ARCA (Actividades_ARCA.txt)."""
        if not os.path.exists(actividades_path):
            print(f"[WARN] Archivo no encontrado: {actividades_path}")
            return
        print(f"[INFO] Ingestando Actividades ARCA: {actividades_path}")
        df = pd.read_fwf(
            actividades_path, widths=ACTIVIDADES_WIDTHS, header=None,
            names=ACTIVIDADES_COLS, encoding="latin1", dtype=str
        )
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        df.dropna(subset=["cod_actividad_arca"], inplace=True)
        self.con.register("df_actividades", df)
        self.con.execute("INSERT OR IGNORE INTO dim_actividad SELECT cod_actividad_arca, descripcion FROM df_actividades")
        self.con.unregister("df_actividades")
        print(f"[OK] Actividades ARCA cargadas: {len(df)}")

    def load_padron_arca(self, padron_path: str):
        """
        Carga el Padrón ARCA (Padron_ARCA.txt) en dim_persona.
        Genera hash_id = sha256(nro_identificacion) directamente en DuckDB.

        ⚠ GOBERNANZA: nro_identificacion se almacena temporalmente para el ETL.
        Debe eliminarse antes de la publicación web.
        """
        if not os.path.exists(padron_path):
            print(f"[WARN] Archivo no encontrado: {padron_path}")
            return
        print(f"[INFO] Ingestando Padrón ARCA: {padron_path} (archivo grande, puede demorar...)")
        # Leer en chunks para manejo de archivos grandes (>14 GB)
        chunk_size = 500_000
        reader = pd.read_fwf(
            padron_path, widths=PADRON_WIDTHS, header=None,
            names=PADRON_COLS, encoding="latin1", dtype=str,
            chunksize=chunk_size
        )
        total = 0
        for chunk in reader:
            chunk = chunk.map(lambda x: x.strip() if isinstance(x, str) else x)
            chunk.dropna(subset=["cuit_cuil_cdi"], inplace=True)
            # Derivar tipo_persona desde prefijo CUIT
            chunk["tipo_persona"] = chunk["cuit_cuil_cdi"].str[:2].apply(
                lambda p: "Física" if p in ("20", "23", "24", "27")
                else ("Jurídica" if p in ("30", "33", "34") else "Otra/Desconocida")
            )
            chunk = chunk.rename(columns={"cuit_cuil_cdi": "nro_identificacion"})
            self.con.register("df_padron_chunk", chunk)
            self.con.execute("""
                INSERT OR IGNORE INTO dim_persona
                SELECT
                    sha256(nro_identificacion) AS hash_id,
                    nro_identificacion,
                    tipo_persona,
                    denominacion,
                    cod_actividad_arca,
                    marca_baja,
                    cuit_reemplazo,
                    fecha_nac_contrato,
                    sexo,
                    codigo_postal,
                    cod_provincia,
                    fecha_fallecimiento
                FROM df_padron_chunk
            """)
            self.con.unregister("df_padron_chunk")
            total += len(chunk)
            print(f"  → Procesados {total:,} registros ARCA...")
        print(f"[OK] Padrón ARCA cargado: {total:,} personas.")

    def load_situacion1_origen(self, dsf1_path: str):
        """Carga la fecha de inicio en situación 1 (1DSF.txt)."""
        if not os.path.exists(dsf1_path):
            print(f"[WARN] Archivo no encontrado: {dsf1_path}")
            return
        print(f"[INFO] Ingestando 1DSF (origen situación 1): {dsf1_path}")
        df = pd.read_fwf(
            dsf1_path, widths=DSF1_WIDTHS, header=None,
            names=DSF1_COLS, encoding="latin1", dtype=str
        )
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        df.dropna(subset=["nro_identificacion"], inplace=True)
        df["fecha_origen_situacion1"] = pd.to_numeric(df["fecha_origen_situacion1"], errors="coerce")
        self.con.register("df_dsf1", df)
        self.con.execute("""
            INSERT OR IGNORE INTO dim_situacion1_origen
            SELECT tipo_identificacion, nro_identificacion, fecha_origen_situacion1
            FROM df_dsf1
        """)
        self.con.unregister("df_dsf1")
        print(f"[OK] 1DSF cargado: {len(df)} registros.")

    def load_no_empadronados(self, path: str, origen: str = "deudor"):
        """
        Carga denominaciones de deudores/morosos no empadronados.
        origen: 'deudor' (nomdeu.txt) o 'moroso' (nommor.txt)
        """
        if not os.path.exists(path):
            print(f"[WARN] Archivo no encontrado: {path}")
            return
        print(f"[INFO] Ingestando no-empadronados ({origen}): {path}")
        df = pd.read_fwf(
            path, widths=NOMALT_WIDTHS, header=None,
            names=NOMALT_COLS, encoding="latin1", dtype=str
        )
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        df["origen"] = origen
        self.con.register("df_noalt", df)
        self.con.execute("""
            INSERT OR IGNORE INTO dim_no_empadronados
            SELECT nro_identificacion, denominacion, origen FROM df_noalt
        """)
        self.con.unregister("df_noalt")
        print(f"[OK] No-empadronados ({origen}) cargados: {len(df)}")

    # ─────────────────────────────────────────────────────────────────────────
    # MÉTODOS ETL — TABLAS DE HECHOS
    # ─────────────────────────────────────────────────────────────────────────

    def extract_and_load_monthly_file(self, txt_path: str, periodo_yyyymm: int):
        """
        Ingesta del archivo posicional principal de la Central de Deudores (deudores.txt).
        Carga los 24 campos completos según el diseño de registro del BCRA.

        Offsets posicionales:
          1-5   cod_entidad (5)           6-11  fecha_informacion (6)
          12-13 tipo_identificacion (2)   14-24 nro_identificacion (11)
          25-27 cod_actividad (3)         28-29 situacion (2)
          30-41 prestamos_garantias (12)  42-53 sin_uso (12)
          54-65 garantias_otorgadas (12)  66-77 otros_conceptos (12)
          78-89 garantias_pref_a (12)     90-101 garantias_pref_b (12)
          102-113 sin_garantias_pref (12) 114-125 contragarantias_pref_a (12)
          126-137 contragarantias_pref_b (12) 138-149 sin_contragarantias_pref (12)
          150-161 previsiones (12)        162 deuda_cubierta (1)
          163 proceso_judicial (1)        164 refinanciaciones (1)
          165 recategorizacion_obl (1)    166 situacion_juridica (1)
          167 irrecuperables (1)          168-171 dias_atraso (4)
        """
        if not os.path.exists(txt_path):
            print(f"[WARN] Archivo no encontrado: {txt_path}")
            return

        print(f"[INFO] Ingestando Hechos Mensuales (deudores.txt): {txt_path}")

        # Usando DuckDB directamente para máxima performance out-of-core
        # NOTA: El BCRA usa coma como separador decimal (ej: "88,0"), no punto.
        #       Se aplica replace(',', '.') en cada campo monetario antes del CAST.
        def monto(pos, largo=12):
            """Helper: extrae campo monetario, normaliza decimal y castea."""
            return (
                f"try_cast(replace(trim(substring(linea, {pos}, {largo})), ',', '.') "
                f"AS DECIMAL(12,1))"
            )

        query = f"""
            INSERT INTO fact_deuda_mensual
            SELECT
                sha256(trim(substring(linea, 14, 11)))  AS hash_id,
                {periodo_yyyymm}                        AS periodo_yyyymm,
                trim(substring(linea, 1,  5))           AS cod_entidad,
                try_cast(trim(substring(linea, 28, 2))  AS INTEGER)  AS id_situacion,
                -- Montos (miles de pesos con 1 decimal; el BCRA usa coma decimal)
                {monto(30)}  AS prestamos_garantias_afrontadas,
                {monto(42)}  AS sin_uso,
                {monto(54)}  AS garantias_otorgadas,
                {monto(66)}  AS otros_conceptos,
                {monto(78)}  AS garantias_pref_a,
                {monto(90)}  AS garantias_pref_b,
                {monto(102)} AS sin_garantias_pref,
                {monto(114)} AS contragarantias_pref_a,
                {monto(126)} AS contragarantias_pref_b,
                {monto(138)} AS sin_contragarantias_pref,
                {monto(150)} AS previsiones,
                -- Flags (un único dígito, sin coma)
                try_cast(trim(substring(linea,162, 1)) AS TINYINT) AS deuda_cubierta,
                try_cast(trim(substring(linea,163, 1)) AS TINYINT) AS proceso_judicial_revision,
                try_cast(trim(substring(linea,164, 1)) AS TINYINT) AS refinanciaciones,
                try_cast(trim(substring(linea,165, 1)) AS TINYINT) AS recategorizacion_obligatoria,
                try_cast(trim(substring(linea,166, 1)) AS TINYINT) AS situacion_juridica,
                try_cast(trim(substring(linea,167, 1)) AS TINYINT) AS irrecuperables_ultimo_parrafo,
                try_cast(trim(substring(linea,168, 4)) AS INTEGER)  AS dias_atraso
            FROM read_csv('{txt_path}', columns={{'linea': 'VARCHAR'}}, sep='\\0', header=False, null_padding=True)
            WHERE try_cast(trim(substring(linea, 28, 2)) AS INTEGER) IN (1, 2, 3, 4, 5, 11)
        """

        try:
            self.con.execute(query)
            count = self.con.execute("SELECT COUNT(*) FROM fact_deuda_mensual").fetchone()[0]
            print(f"[OK] Hechos mensuales cargados. Total acumulado en fact_deuda_mensual: {count:,}")
        except Exception as e:
            print(f"[ERROR] Fallo la carga de {txt_path}: {e}")

    def load_rectificativas(self, path: str, tipo: str = "completa"):
        """
        Carga archivos de rectificativas (inf_ret.txt o inf_retparc.txt).
        tipo: 'completa' o 'parcial'
        Situacion y monto en ceros = registro eliminado de la Central.
        """
        if not os.path.exists(path):
            print(f"[WARN] Archivo no encontrado (rectificativas {tipo}): {path}")
            return
        print(f"[INFO] Ingestando Rectificativas ({tipo}): {path}")
        df = pd.read_fwf(
            path, widths=RECTIF_WIDTHS, header=None,
            names=RECTIF_COLS, encoding="latin1", dtype=str
        )
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        df["tipo_rectif"] = tipo
        df["situacion"] = pd.to_numeric(df["situacion"], errors="coerce")
        df["monto"] = pd.to_numeric(df["monto"], errors="coerce")
        self.con.register("df_rectif", df)
        self.con.execute("""
            INSERT INTO fact_rectificativas
            SELECT tipo_rectif, cod_entidad, CAST(fecha_informacion AS INTEGER),
                   tipo_identificacion, nro_identificacion, denominacion,
                   CAST(situacion AS INTEGER), monto
            FROM df_rectif
        """)
        self.con.unregister("df_rectif")
        print(f"[OK] Rectificativas ({tipo}) cargadas: {len(df)}")

    def load_morosos_exentidades(self, morex_path: str):
        """
        Carga morosos de ex-entidades financieras (morexent.txt).
        Este archivo solo se publica si hay datos disponibles.
        """
        if not os.path.exists(morex_path):
            print(f"[WARN] Archivo no encontrado (morexent.txt): {morex_path}")
            return
        print(f"[INFO] Ingestando Morosos de Ex-Entidades: {morex_path}")
        df = pd.read_fwf(
            morex_path, widths=MOREX_WIDTHS, header=None,
            names=MOREX_COLS, encoding="latin1", dtype=str
        )
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        df["fecha_informacion"] = pd.to_numeric(df["fecha_informacion"], errors="coerce")
        df["proceso_judicial_revision"] = pd.to_numeric(df["proceso_judicial_revision"], errors="coerce")
        self.con.register("df_morex", df)
        self.con.execute("""
            INSERT INTO fact_morosos_exentidades
            SELECT CAST(fecha_informacion AS INTEGER), denominacion_ente_residual,
                   tipo_identificacion, nro_identificacion,
                   CAST(proceso_judicial_revision AS TINYINT)
            FROM df_morex
        """)
        self.con.unregister("df_morex")
        print(f"[OK] Morosos de ex-entidades cargados: {len(df)}")

    def load_historial_24(self, dsf24_path: str):
        """
        Carga el historial de los últimos 24 meses (24DSF.txt).
        Estructura: 3 campos fijos + 24 repeticiones de (situacion[2], monto[12], proc_judicial[1]).
        Ancho total del registro = 3 + (5) + 24*(2+12+1) = 3+5+24*15 = 368 chars.

        Este archivo puede ser muy grande. Se procesa en chunks con pandas.
        """
        if not os.path.exists(dsf24_path):
            print(f"[WARN] Archivo no encontrado (24DSF.txt): {dsf24_path}")
            return
        print(f"[INFO] Ingestando Historial 24 meses: {dsf24_path}")

        # Construir widths completos
        repeat_cols = []
        for n in range(24):
            repeat_cols.extend([
                f"sit_m{n:02d}", f"monto_m{n:02d}", f"proc_m{n:02d}"
            ])
        all_widths = DSF24_FIXED_WIDTHS + DSF24_REPEAT_WIDTHS * 24
        all_cols = DSF24_FIXED_COLS + repeat_cols

        chunk_size = 200_000
        reader = pd.read_fwf(
            dsf24_path, widths=all_widths, header=None,
            names=all_cols, encoding="latin1", dtype=str,
            chunksize=chunk_size
        )
        total = 0
        for chunk in reader:
            chunk = chunk.map(lambda x: x.strip() if isinstance(x, str) else x)
            # Unpivot: transformar en formato largo (1 fila por mes)
            rows = []
            for _, row in chunk.iterrows():
                for n in range(24):
                    rows.append({
                        "cod_entidad": row["cod_entidad"],
                        "nro_identificacion": row["nro_identificacion"],
                        "mes_n": n,
                        "periodo_yyyymm": None,  # requeire cálculo externo
                        "situacion": pd.to_numeric(row.get(f"sit_m{n:02d}"), errors="coerce"),
                        "monto": pd.to_numeric(row.get(f"monto_m{n:02d}"), errors="coerce"),
                        "proceso_judicial": pd.to_numeric(row.get(f"proc_m{n:02d}"), errors="coerce"),
                    })
            df_long = pd.DataFrame(rows)
            df_long.dropna(subset=["situacion"], inplace=True)
            if not df_long.empty:
                self.con.register("df_hist", df_long)
                self.con.execute("""
                    INSERT INTO fact_historial_24
                    SELECT cod_entidad, nro_identificacion, mes_n, periodo_yyyymm,
                           CAST(situacion AS INTEGER), monto,
                           CAST(proceso_judicial AS TINYINT)
                    FROM df_hist
                """)
                self.con.unregister("df_hist")
            total += len(chunk)
            print(f"  → Historial 24: procesados {total:,} registros base...")
        print(f"[OK] Historial 24 meses cargado ({total:,} registros base).")

    # ─────────────────────────────────────────────────────────────────────────
    # EXPORTACIÓN Y CALIDAD
    # ─────────────────────────────────────────────────────────────────────────

    def export_to_parquet(self):
        """
        Exporta todas las tablas del DWH a formato Parquet (compresión ZSTD).
        Los archivos de hechos grandes usan ZSTD; las dimensiones usan Snappy por defecto.
        """
        print("[INFO] Exportando modelo dimensional a Parquet...")
        parquet_dir = self.dwh_dir / "parquet"
        parquet_dir.mkdir(exist_ok=True)

        tablas_hechos = [
            "fact_deuda_mensual", "fact_historial_24",
            "fact_rectificativas", "fact_morosos_exentidades",
        ]
        tablas_dims = [
            "dim_entidad", "dim_situacion", "dim_persona",
            "dim_actividad", "dim_provincia",
            "dim_situacion1_origen", "dim_no_empadronados",
        ]

        for tabla in tablas_hechos:
            try:
                out = f"{parquet_dir}/{tabla}.parquet"
                self.con.execute(f"COPY (SELECT * FROM {tabla}) TO '{out}' (FORMAT PARQUET, COMPRESSION ZSTD)")
                print(f"  → {tabla}.parquet exportado.")
            except Exception as e:
                print(f"  [WARN] No se pudo exportar {tabla}: {e}")

        for tabla in tablas_dims:
            try:
                out = f"{parquet_dir}/{tabla}.parquet"
                self.con.execute(f"COPY (SELECT * FROM {tabla}) TO '{out}' (FORMAT PARQUET)")
                print(f"  → {tabla}.parquet exportado.")
            except Exception as e:
                print(f"  [WARN] No se pudo exportar {tabla}: {e}")

        print(f"[OK] Exportación Parquet finalizada en: {parquet_dir}")

    def validate_data_quality(self):
        """Ejecuta aserciones de calidad de datos sobre el modelo dimensional."""
        print("[INFO] Ejecutando Data Quality Checks...")

        checks = [
            (
                "fact_deuda_mensual — Sin hash_id nulos",
                "SELECT COUNT(*) FROM fact_deuda_mensual WHERE hash_id IS NULL",
                lambda n: n == 0,
                "Existen registros sin hash_id en fact_deuda_mensual."
            ),
            (
                "fact_deuda_mensual — Sin montos negativos",
                "SELECT COUNT(*) FROM fact_deuda_mensual WHERE prestamos_garantias_afrontadas < 0",
                lambda n: n == 0,
                "Existen registros con deuda (prestamos) negativa."
            ),
            (
                "dim_persona — Tipos de persona válidos",
                "SELECT COUNT(*) FROM dim_persona WHERE tipo_persona IN ('Física', 'Jurídica')",
                lambda n: n > 0,
                "No se detectaron personas físicas ni jurídicas en dim_persona (posible schema drift)."
            ),
            (
                "dim_entidad — Con registros",
                "SELECT COUNT(*) FROM dim_entidad",
                lambda n: n > 0,
                "dim_entidad está vacía."
            ),
        ]

        passed = 0
        for name, query, assertion, msg in checks:
            result = self.con.execute(query).fetchone()[0]
            if assertion(result):
                print(f"  [✓] {name}")
                passed += 1
            else:
                print(f"  [✗] QA Falló: {msg} (valor={result})")

        if passed == len(checks):
            print(f"[OK] Todos los {passed} Quality Checks pasaron con éxito.")
        else:
            print(f"[WARN] {len(checks) - passed} de {len(checks)} checks fallaron.")

    def get_summary_metrics(self):
        """Imprime un resumen del modelo cargado."""
        print("[INFO] Resumen de Tablas en el DWH:")
        tablas = [
            "fact_deuda_mensual", "fact_historial_24",
            "fact_rectificativas", "fact_morosos_exentidades",
            "dim_persona", "dim_entidad", "dim_situacion",
            "dim_actividad", "dim_provincia",
            "dim_situacion1_origen", "dim_no_empadronados",
        ]
        for t in tablas:
            try:
                n = self.con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                print(f"  {t:<40} {n:>15,} filas")
            except Exception:
                print(f"  {t:<40} (no existe o vacía)")

    def close(self):
        self.con.close()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN — Ejecución del pipeline completo
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import glob
    print("─" * 60)
    print("  BCRA ETL — Pipeline Completo (DuckDB)")
    print("─" * 60)

    base_dir = Path(__file__).parent.parent.parent
    raw_dir = base_dir / "data" / "descarga_manual"
    dwh_dir = base_dir / "data" / "dwh"

    etl = BCRA_ETL(raw_data_dir=str(raw_dir), dwh_dir=str(dwh_dir))
    etl._create_schema()

    # ── ARCA ─────────────────────────────────────────────────────────────────
    padron_dir = raw_dir / "20260131PADRON"
    etl.load_actividades_arca(str(padron_dir / "Actividades_ARCA.txt"))
    # Padrón ARCA (14 GB — puede tardar varios minutos)
    etl.load_padron_arca(str(padron_dir / "Padron_ARCA.txt"))

    # ── BCRA — Situación 1 (1DSF202512) ──────────────────────────────────────
    # 1DSF.txt: fecha de inicio ininterrumpido en situación 1 (3 campos)
    dsf1_dir = raw_dir / "1DSF202512"
    etl.load_situacion1_origen(str(dsf1_dir / "1DSF.txt"))

    # ── BCRA — Archivos Mensuales de Deudores ────────────────────────────────
    # Busca deudores.txt en cualquier subdirectorio (ej: 202512DEUDORES/)
    deudores_encontrados = sorted(glob.glob(str(raw_dir / "**" / "deudores.txt"), recursive=True))
    if deudores_encontrados:
        for deudores_path in deudores_encontrados:
            carpeta = Path(deudores_path).parent
            try:
                periodo = int(carpeta.name[:6])
            except ValueError:
                periodo = 202512
            etl.load_entities(str(carpeta / "maeent.txt"))
            etl.extract_and_load_monthly_file(deudores_path, periodo)
            etl.load_rectificativas(str(carpeta / "inf_ret.txt"), tipo="completa")
            etl.load_rectificativas(str(carpeta / "inf_retparc.txt"), tipo="parcial")
            etl.load_morosos_exentidades(str(carpeta / "morexent.txt"))
            etl.load_no_empadronados(str(carpeta / "nomdeu.txt"), origen="deudor")
            etl.load_no_empadronados(str(carpeta / "nommor.txt"), origen="moroso")
    else:
        print("[WARN] No se encontró ningún archivo deudores.txt en descarga_manual/.")
        print("       Descargue los archivos mensuales del BCRA y re-ejecute el pipeline.")

    # ── Calidad / Exportación ─────────────────────────────────────────────────
    etl.validate_data_quality()
    etl.export_to_parquet()
    etl.get_summary_metrics()
    etl.close()

