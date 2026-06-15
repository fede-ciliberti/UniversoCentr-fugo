# Archivo: Paradigma BSSN (Obsoleto)

**Fecha de archivado**: Junio 2026  
**Motivo**: Cambio de paradigma hacia solver espectral FFT de membrana elástica

## Contexto Histórico

Estos documentos pertenecen al paradigma BSSN (Baumgarte-Shapiro-Shibata-Nakamura) que fue el enfoque inicial de simulación numérica del proyecto Universo Centrífugo.

En junio 2026, el proyecto abandonó el formalismo BSSN en favor del **solver espectral FFT de membrana elástica**. Este cambio se documenta en:

- `docs/simulacion_256cubed/README_256cubed.md` — Transición BSSN → FFT
- `docs/07_fase2_ejecucion_simulacion_completada.md` — Validación del solver FFT
- `docs/12_validacion_plan_256cubed_completado.md` — Plan 256³ completado con FFT

## Razones del Cambio

1. **Ineficiencia física**: BSSN evoluciona temporalmente un espacio-tiempo que es intrínsecamente estático en escalas de tiempo locales (órbitas planetarias, dinámica galáctica).
2. **Inestabilidades numéricas**: Diferencias finitas y ghost cells inducían vibraciones espurias que desestabilizaban la simulación a largo plazo.
3. **Costo computacional prohibitivo**: BSSN requería 128GB+ RAM y semanas de ejecución en supercomputadoras, vs segundos con FFT en workstation estándar.

## Documentos Archivados

| Archivo | Contenido | Estado |
|---------|-----------|--------|
| `plan_verificacion_algoritmo_completo.md` | Plan de simulación BSSN 256³ con convergencia 32³→256³ | Obsoleto |
| `RESUMEN_EJECUTIVO_256CUBED.md` | Arquitectura BSSN con chunks espaciales, memory mapping, 20 variables dinámicas | Obsoleto |
| `README_SIMULATION.md` | Sistema BSSN completo: orchestrator, GPU (CuPy/PyOpenCL), checkpoints SHA-256 | Obsoleto |
| `plan_reorganizacion_cientifica_completo.md` | Plan de reorganización de junio 2025 (parcialmente ejecutado) | Histórico |

## Estado Actual del Proyecto

El solver FFT está validado hasta resolución 256³ con correlación >99.8% contra el perfil de Schwarzschild. Ver:

- `docs/11_plan_estrategico_256cubed_completo.md` — Plan estratégico FFT
- `docs/12_validacion_plan_256cubed_completado.md` — Validación completada
- `notebooks/simulacion_membrana_elastica.py` — Motor FFT principal
- `results/membrana_elastica/{32,64,128,256}cubed/` — Resultados reales

## Nota para Investigadores

Estos documentos se conservan como registro histórico de la evolución metodológica del proyecto. No deben usarse como referencia para trabajo activo, ya que describen un paradigma abandonado.

Para entender la metodología actual, comenzar con:
1. `docs/03_metodologia_gravedad_emergente.md` — Derivación de gravedad desde elasticidad
2. `docs/plan_simulacion_elastica.md` — Plan maestro de simulación FFT
3. `docs/08_fase3_analisis_resultados_completada.md` — Análisis de resultados FFT
