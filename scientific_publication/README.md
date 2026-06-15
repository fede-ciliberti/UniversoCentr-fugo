# Universo Centrífugo: Publicación Científica

## Resumen Ejecutivo

Este directorio contiene el **manuscrito formal** de la Hipótesis del Universo Centrífugo, estructurado para publicación en revistas científicas de alto impacto (JCAP, Physical Review D, Classical and Quantum Gravity).

La teoría propone que el universo observable es una 3-esfera (S³) embebida en un espacio euclidiano 4D (ℝ⁴) que rota con velocidad angular ω₄D. La expansión cosmológica observada (Ley de Hubble) emerge como la proyección 3D de esta rotación hiperdimensional, proporcionando una explicación unificada para:

- **Energía oscura (~68%)**: Fuerza centrífuga de rotación isoclínica + tensión de brana
- **Materia oscura (~27%)**: Aceleración inercial del Bulk (a_c ≈ 4.8×10⁻¹⁰ m/s²)
- **Gravedad local**: Deformación elástica de brana por empuje centrífugo

**Estado actual (junio 2026)**: Marco teórico completo, validación numérica FFT hasta 256³ (>99.8% correlación con Schwarzschild), predicciones observacionales cuantitativas desarrolladas.

---

## Estructura del Manuscrito

### ✅ Secciones Completadas

| Sección | Archivo | Contenido | Tamaño |
|---------|---------|-----------|--------|
| **1. Fundamentos Teóricos** | `01_theoretical_foundations/core_hypothesis.md` | Hipótesis central, postulados G1/D1/O1, métrica S³ | 33 KB |
| **2. Desarrollo Matemático** | `02_mathematical_development/4d_rotation_dynamics.md` | Formalismo SO(4), rotación isoclínica, tensor T^μν | 33 KB |
| **4. Predicciones Observacionales** | `04_observational_predictions/cosmological_parameters.md` | H₀, Ω_rot, Ω_k, w_eff, anisotropías CMB | 36 KB |
| **5. Verificación Experimental** | `05_experimental_verification/falsifiability_criteria.md` | Criterios de refutación/confirmación | 22 KB |
| **5. Verificación Experimental** | `05_experimental_verification/desi_2024_validation.md` | Validación con datos DESI 2024 | 13 KB |

### ❌ Secciones No Desarrolladas

| Sección | Estado | Notas |
|---------|--------|-------|
| **3. Validación Numérica** | NO EXISTE | Para validación numérica FFT completa, ver `docs/05_informe_simulacion_numerica.md` → `docs/12_validacion_plan_256cubed_completado.md` |
| **6. Implicaciones y Conclusiones** | NO EXISTE | Pendiente de desarrollo para versión final del paper |
| **Apéndices** | ELIMINADO | Eliminado en reorganización junio 2026 |

---

## Secuencia de Lectura Recomendada

### Para Revisores / Lectores Nuevos

1. **Inicio conceptual**: [`01_theoretical_foundations/core_hypothesis.md`](01_theoretical_foundations/core_hypothesis.md)
   - Postulados fundamentales (G1, D1, O1)
   - Métrica de la 3-esfera en ℝ⁴
   - Diferenciación vs ΛCDM

2. **Formalismo matemático**: [`02_mathematical_development/4d_rotation_dynamics.md`](02_mathematical_development/4d_rotation_dynamics.md)
   - Grupo SO(4) ≅ SU(2) × SU(2)
   - Rotación isoclínica pura
   - Tensor energía-momento proyectado T_μν(efectivo)

3. **Predicciones testables**: [`04_observational_predictions/cosmological_parameters.md`](04_observational_predictions/cosmological_parameters.md)
   - Parámetros cosmológicos: H₀ = 70.2 ± 0.3 km/s/Mpc, Ω_rot = 0.274 ± 0.035
   - Anisotropías CMB cuádruples: A₄D = 26.2 ± 3.8
   - Escala de correlación fundamental: λ₄D = 1.53 ± 0.09 Gpc

4. **Criterios de falsabilidad**: [`05_experimental_verification/falsifiability_criteria.md`](05_experimental_verification/falsifiability_criteria.md)
   - Condiciones de refutación definitiva
   - Condiciones de confirmación definitiva
   - Cronograma de verificación (2025-2035)

5. **Validación con datos reales**: [`05_experimental_verification/desi_2024_validation.md`](05_experimental_verification/desi_2024_validation.md)
   - Comparación con datos DESI 2024
   - Restricciones observacionales

---

## Relación con docs/ (Material de Trabajo)

Este directorio (`scientific_publication/`) contiene el **manuscrito formal**. Para documentación de trabajo, metodologías detalladas e informes intermedios, ver `docs/`:

| Manuscrito Formal (aquí) | Material de Trabajo (docs/) |
|---|---|
| `01_theoretical_foundations/core_hypothesis.md` | `01_marco_teorico.md`, `02_propuesta_investigacion.md` |
| `02_mathematical_development/4d_rotation_dynamics.md` | `formulacion_matematica_rotacion_4d.md`, `ecuaciones_movimiento_rotacion_4d.md`, `conservacion_momento_inercia_geff.md` |
| (validación numérica no incluida aquí) | `05_informe_simulacion_numerica.md` → `12_validacion_plan_256cubed_completado.md` |
| `04_observational_predictions/cosmological_parameters.md` | `comparacion_curvas_expansion.md`, `informe_materia_oscura_elastica.md` |
| `05_experimental_verification/*` | `informe_precesion_perihelio.md`, `fuerza_coriolis_4d_trayectorias.md` |

**Documentación de apoyo** (ex-huérfanos integrados en junio 2026):
- `docs/formalismo_dbi_energia_oscura.md` — Acción DBI para w=-1 dinámico
- `docs/acoplamiento_masa_inercia_centrifuga.md` — Retroalimentación masa-vacío
- `docs/calculo_radio_tamano_universo.md` — Cálculo observacional de R₀

---

## Firmas Distintivas del Modelo

### Predicciones Únicas (no explicables por ΛCDM estándar)

1. **Simetría cuádruple universal**: Patrones cos(4θ), cos(8θ) en CMB, lensing y estructura a gran escala
2. **Escala física fundamental**: λ₄D = 1.53 ± 0.09 Gpc (periodicidad en velocidades peculiares)
3. **Eje preferencial multifenómeno**: Dirección común (l,b) = (264° ± 12°, -29° ± 8°) en CMB, estructura galáctica y flujos coherentes
4. **Curvatura espacial negativa**: Ω_k = -0.089 ± 0.014 (conectada directamente con geometría S³)

### Impacto Científico Potencial

**Si confirmado:**
- Primera evidencia directa de dimensiones espaciales extra
- Unificación de materia/energía oscura bajo un principio geométrico común
- Revolución en cosmología fundamental y gravedad cuántica

**Si refutado:**
- Fortalecimiento del modelo ΛCDM estándar
- Refinamiento de criterios de falsabilidad en cosmología teórica
- Metodología transferible a otros modelos emergentes

---

## Estado del Proyecto

### ✅ Completado (Junio 2026)

- Marco teórico riguroso y autoconsistente
- Cambio de paradigma BSSN → FFT espectral completado
- Solver FFT validado hasta 256³ (correlación >99.8% con Schwarzschild)
- Tests físicos implementados: precesión, lensing, materia oscura, expansión
- Predicciones observacionales cuantitativas desarrolladas
- Criterios de falsabilidad objetivos establecidos
- Reorganización integral del proyecto (consistencia total)

### 🔄 En Desarrollo

- Extensión a simulaciones multi-cuerpo y distribuciones galácticas completas
- Análisis comparativo con datos CMB Planck
- Cálculo del espectro de potencias P(k)
- Preparación de manuscrito final para submission

### 📅 Próximos Hitos

- **Q3 2026**: Sistemas binarios de membrana (ondas gravitacionales emergentes)
- **Q4 2026**: Simulación galáctica esférica (curvas de rotación con perfiles NFW)
- **Q1 2027**: Simulación cosmológica de estructura a gran escala S³
- **Q2 2027**: Análisis comparativo con datos CMB Planck
- **2027-2030**: Caracterización con nuevas observaciones (Euclid, CMB-S4)
- **2030-2035**: Decisión definitiva sobre validez del modelo

---

## Referencias Clave del Proyecto

### Documentación Base (docs/)

- [`docs/01_marco_teorico.md`](../docs/01_marco_teorico.md) — Marco teórico general
- [`docs/02_propuesta_investigacion.md`](../docs/02_propuesta_investigacion.md) — Propuesta formal e hipótesis
- [`docs/formulacion_matematica_rotacion_4d.md`](../docs/formulacion_matematica_rotacion_4d.md) — Formalismo SO(4) completo
- [`docs/conservacion_momento_inercia_geff.md`](../docs/conservacion_momento_inercia_geff.md) — Estabilidad de G_eff (HUB central)

### Validación Numérica (docs/)

- [`docs/05_informe_simulacion_numerica.md`](../docs/05_informe_simulacion_numerica.md) — Primer informe del solver FFT
- [`docs/11_plan_estrategico_256cubed_completo.md`](../docs/11_plan_estrategico_256cubed_completo.md) — Plan estratégico 256³
- [`docs/12_validacion_plan_256cubed_completado.md`](../docs/12_validacion_plan_256cubed_completado.md) — Validación completada

### Sistema de Notación

- **TF.X**: Ecuaciones de Fundamentos Teóricos
- **MD.X**: Ecuaciones de Desarrollo Matemático
- **OCP.X**: Ecuaciones de Predicciones Observacionales
- **G1, D1, O1**: Postulados fundamentales (Geométrico, Dinámico, Observacional)

---

## Licencia y Contribuciones

**Estado**: Investigación científica activa  
**Última actualización**: Junio 2026 (reorganización integral)  
**Próxima fase**: Extensión a sistemas multi-cuerpo y preparación de manuscripto final

**Licencia**: Disponible para uso académico y científico. Colaboraciones bienvenidas.

---

*"El universo es más extraño de lo que imaginamos, y más extraño de lo que podemos imaginar."*

La Conjetura del Universo Centrífugo sugiere que vivimos en una estructura hiperdimensional cuya verdadera naturaleza apenas comenzamos a vislumbrar.
