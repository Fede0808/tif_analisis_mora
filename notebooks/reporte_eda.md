# Reporte EDA Automático

**Archivo analizado:** `data/dwh/bcra_dwh.duckdb`

---

## Análisis de: dim_entidad

### 1. Visión General
- **Número de filas (vista):** 546
- **Número de columnas:** 2

### 2. Tipos de Datos y Valores Nulos
| Columna | Tipo de Dato | Nulos | % Nulos |
|---------|--------------|-------|----------|
| id_entidad | object | 0 | 0.00% |
| nombre_entidad | object | 0 | 0.00% |

### 3. Estadísticas Descriptivas (Variables Numéricas)
*No hay variables numéricas para calcular estadísticas.*

### 4. Variables Altamente Correlacionadas
*No hay suficientes variables numéricas para calcular correlaciones.*
---

## Análisis de: dim_situacion

### 1. Visión General
- **Número de filas (vista):** 6
- **Número de columnas:** 3

### 2. Tipos de Datos y Valores Nulos
| Columna | Tipo de Dato | Nulos | % Nulos |
|---------|--------------|-------|----------|
| id_situacion | int32 | 0 | 0.00% |
| descripcion | object | 0 | 0.00% |
| is_default | bool | 0 | 0.00% |

### 3. Estadísticas Descriptivas (Variables Numéricas)
```text
              count  mean       std  min   25%  50%   75%  max
id_situacion    6.0   3.5  1.870829  1.0  2.25  3.5  4.75  6.0
```

### 4. Variables Altamente Correlacionadas
*No hay suficientes variables numéricas para calcular correlaciones.*
---

## Análisis de: fact_deuda_mensual

### 1. Visión General
- **Número de filas (vista):** 1000000
- **Número de columnas:** 6

### 2. Tipos de Datos y Valores Nulos
| Columna | Tipo de Dato | Nulos | % Nulos |
|---------|--------------|-------|----------|
| hash_deudor | object | 0 | 0.00% |
| periodo_yyyymm | int32 | 0 | 0.00% |
| id_entidad | object | 0 | 0.00% |
| id_situacion | int32 | 0 | 0.00% |
| monto_deuda | float64 | 0 | 0.00% |
| dias_atraso | int32 | 0 | 0.00% |

### 3. Estadísticas Descriptivas (Variables Numéricas)
```text
                    count           mean         std       min       25%       50%       75%       max
periodo_yyyymm  1000000.0  202512.000000     0.00000  202512.0  202512.0  202512.0  202512.0  202512.0
id_situacion    1000000.0       3.547138     1.63452       1.0       2.0       4.0       5.0       6.0
monto_deuda     1000000.0     640.606259  4530.93819       0.0      26.0      93.0     541.0  973881.0
dias_atraso     1000000.0       0.000000     0.00000       0.0       0.0       0.0       0.0       0.0
```

### 4. Variables Altamente Correlacionadas
*No se encontraron correlaciones absolutas mayores a 0.8 entre variables numéricas.*
