# Auditoría de estructura de datos para el TIF

Actuá como científico de datos y revisor metodológico.

## Objetivo

Determinar si los datos disponibles permiten sostener un análisis temporal de mora o si conviene reformular el TIF hacia una segmentación no supervisada.

## Debés revisar

1. unidad de análisis;
2. identificadores persistentes;
3. variable temporal;
4. periodicidad;
5. cantidad de períodos disponibles;
6. variable de situación crediticia, mora o deterioro;
7. variables explicativas disponibles;
8. granularidad;
9. presencia de duplicados;
10. consistencia temporal;
11. datos faltantes;
12. riesgos de privacidad;
13. factibilidad de construir transiciones.

## Pregunta central

¿La estructura de datos permite reconstruir trayectorias temporales confiables?

## Salida esperada

Devolvé:

1. diagnóstico de viabilidad de Ruta A: análisis temporal;
2. diagnóstico de viabilidad de Ruta B: segmentación no supervisada;
3. evidencia requerida;
4. supuestos no validados;
5. riesgos metodológicos;
6. recomendación preliminar;
7. próximos pasos para validar la recomendación.

## Restricciones

- No mostrar registros individuales sensibles.
- No asumir longitudinalidad sin evidencia.
- No recomendar modelos complejos si los datos no lo justifican.
