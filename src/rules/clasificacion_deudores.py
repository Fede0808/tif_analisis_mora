\"\"\"
Módulo de Regulación BCRA - Texto Ordenado de Clasificación de Deudores
Implementa los criterios técnicos para las Situaciones 1 a 6.

Referencias:
- Situación 1: Normal (atraso <= 31 días)
- Situación 2: Con seguimiento especial/Riesgo potencial (atraso 32 a 90 días)
- Situación 3: Con problemas (atraso 91 a 180 días)
- Situación 4: Con alto riesgo de insolvencia (atraso 181 a 365 días)
- Situación 5: Irrecuperable (atraso > 365 días)
- Situación 6: Irrecuperable por disposición técnica.
\"\"\"

class BCRADebtorClassification:
    SIT_1_NORMAL = 1
    SIT_2_SEGUIMIENTO_ESPECIAL = 2
    SIT_3_PROBLEMAS = 3
    SIT_4_ALTO_RIESGO = 4
    SIT_5_IRRECUPERABLE = 5
    SIT_6_TECNICA = 6

    @classmethod
    def classify_by_days_late(cls, days_late: int, is_technical_default: bool = False) -> int:
        \"\"\"
        Clasifica al deudor en función de los días de atraso en el pago,
        según el TO de Clasificación de Deudores del BCRA.
        \"\"\"
        if is_technical_default:
            return cls.SIT_6_TECNICA

        if days_late <= 31:
            return cls.SIT_1_NORMAL
        elif 32 <= days_late <= 90:
            return cls.SIT_2_SEGUIMIENTO_ESPECIAL
        elif 91 <= days_late <= 180:
            return cls.SIT_3_PROBLEMAS
        elif 181 <= days_late <= 365:
            return cls.SIT_4_ALTO_RIESGO
        else:
            return cls.SIT_5_IRRECUPERABLE

    @classmethod
    def is_default(cls, situation: int) -> bool:
        \"\"\"
        Define el umbral de 'default' estricto para modelos de supervivencia.
        Se asume default técnico o empírico a partir de la Situación 3 (cartera con problemas / atraso > 90 días).
        Basile II / NIIF 9 standard aproxima > 90 días como credit-impaired.
        \"\"\"
        return situation >= cls.SIT_3_PROBLEMAS

    @classmethod
    def get_situation_description(cls, situation: int) -> str:
        descriptions = {
            1: "Normal",
            2: "Con seguimiento especial",
            3: "Con problemas",
            4: "Con alto riesgo de insolvencia",
            5: "Irrecuperable",
            6: "Irrecuperable por disposición técnica"
        }
        return descriptions.get(situation, "Desconocida")
