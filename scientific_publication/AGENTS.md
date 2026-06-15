# SCIENTIFIC PUBLICATION

**Dominio**: Manuscrito formal de la teoría del Universo Centrífugo.

## OVERVIEW

Documentación científica estructurada en secciones que conforman el manuscrito formal. Actualmente contiene fundamentos teóricos, desarrollo matemático, predicciones observacionales y verificación experimental.

## ⚠️ ESTADO REAL (post-reorganización junio 2026)

Este directorio contiene el **manuscrito formal** para publicación. Para documentación de trabajo, metodologías, informes de simulación y material auxiliar, ver `docs/`.

La validación numérica completa del solver FFT está documentada en:
- `docs/05_informe_simulacion_numerica.md`
- `docs/07_fase2_ejecucion_simulacion_completada.md`
- `docs/08_fase3_analisis_resultados_completada.md`
- `docs/12_validacion_plan_256cubed_completado.md`

## STRUCTURE REAL

```
scientific_publication/
├── AGENTS.md                              # Este archivo
├── README.md                              # Índice general de la publicación
├── 01_theoretical_foundations/
│   └── core_hypothesis.md                 # Hipótesis central (33KB)
├── 02_mathematical_development/
│   └── 4d_rotation_dynamics.md            # Dinámica rotación 4D (33KB)
├── 04_observational_predictions/
│   └── cosmological_parameters.md         # Predicciones cuantitativas (36KB)
└── 05_experimental_verification/
    ├── desi_2024_validation.md            # Validación con datos DESI (13KB)
    └── falsifiability_criteria.md         # Criterios de falsabilidad (22KB)
```

## ESTADO DE SECCIONES

| Sección | Archivos | Estado | Notas |
|---------|----------|--------|-------|
| `01_theoretical_foundations/` | 1 | ✅ Consolidado | Solo `core_hypothesis.md` |
| `02_mathematical_development/` | 1 | ✅ Completo | Solo `4d_rotation_dynamics.md` |
| `03_numerical_validation/` | 0 | ❌ NO EXISTE | Ver `docs/` para validación numérica FFT |
| `04_observational_predictions/` | 1 | ✅ Predicciones desarrolladas | Solo `cosmological_parameters.md` |
| `05_experimental_verification/` | 2 | ✅ Criterios + validación DESI | `desi_2024_validation.md`, `falsifiability_criteria.md` |
| `06_implications_and_conclusions/` | 0 | ❌ NO EXISTE | Pendiente de desarrollo |
| `appendices/` | 0 | ❌ ELIMINADO | Eliminado en reorganización junio 2026 |

## SECUENCIA DE LECTURA RECOMENDADA

1. `01_theoretical_foundations/core_hypothesis.md` — Punto de entrada conceptual
2. `02_mathematical_development/4d_rotation_dynamics.md` — Formalismo matemático riguroso
3. `04_observational_predictions/cosmological_parameters.md` — Predicciones testables
4. `05_experimental_verification/falsifiability_criteria.md` — Criterios de refutación
5. `05_experimental_verification/desi_2024_validation.md` — Validación con datos reales

## CONCEPTOS CLAVE

- **Rotación isoclínica 4D**: Universo como 3-esfera en ℝ⁴ rotando con velocidad angular ω₄D
- **Ley de Hubble emergente**: H₀ = ω₄D × R₄D / (2π) × f_geométrico
- **Tensor energía-momento proyectado**: T_μν(efectivo) = P_μ^α × P_ν^β × T_αβ
- **Gravedad emergente**: Deformación elástica de brana por empuje centrífugo
- **Materia oscura explicada**: Aceleración inercial del Bulk (a_c ≈ 4.8×10⁻¹⁰ m/s²)
- **Energía oscura**: Rotación isoclínica + tensión de brana (sin Λ cosmológica)

## RELACIÓN CON docs/

| scientific_publication/ | docs/ (material de trabajo) |
|---|---|
| `01_theoretical_foundations/core_hypothesis.md` | `01_marco_teorico.md`, `02_propuesta_investigacion.md` |
| `02_mathematical_development/4d_rotation_dynamics.md` | `formulacion_matematica_rotacion_4d.md`, `ecuaciones_movimiento_rotacion_4d.md` |
| `04_observational_predictions/cosmological_parameters.md` | `comparacion_curvas_expansion.md`, `informe_materia_oscura_elastica.md` |
| `05_experimental_verification/*` | `informe_precesion_perihelio.md`, `fuerza_coriolis_4d_trayectorias.md` |
| (validación numérica no incluida aquí) | `05_informe_simulacion_numerica.md` → `12_validacion_plan_256cubed_completado.md` |

## ANTI-PATTERNS

- **No referenciar archivos inexistentes**: Las secciones 03, 06 y appendices fueron eliminadas del esquema documentado. No crear enlaces a ellas.
- **No confundir con `docs/`**: Aquí va el manuscrito final para publicación; allí va material de trabajo, metodologías e informes intermedios.
- **No commitear resultados preliminares**: Solo resultados validados van en `05_experimental_verification/`.
- **Sección 03 pendiente**: Si se desarrolla validación numérica formal para el paper, crear `03_numerical_validation/` con contenido nuevo (no copiar de `docs/`).

## ÚLTIMA ACTUALIZACIÓN

Junio 2026 — Reorganización integral del proyecto. Estructura documentada refleja exactamente el contenido real del directorio.
