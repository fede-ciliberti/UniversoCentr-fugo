# Ejecución del Plan de Reorganización — Universo Centrífugo

**Fecha inicio**: 15 de junio de 2026
**Estado**: EN PROGRESO

## Decisiones Tomadas (por defecto, Fede no especificó)

1. ✅ **`simulation_256cubed_data/`**: MANTENER en ubicación actual (referenciado por 4 scripts activos). Documentar como legacy bulk data.
2. ✅ **Entry points de raíz**: MANTENER en raíz (opción conservadora).
3. ✅ **`downloads/`**: Mover datos observacionales a `data/observational/`, mantener PDF en `downloads/`.
4. ✅ **`publication_strategy/` stubs**: MANTENER como TODOs explícitos (no eliminar).
5. ✅ **Secciones faltantes de `scientific_publication/`**: ELIMINAR del esquema documentado (estructura debe ser real).

---

## FASE 1: Eliminación de Basura Inmediata ✅

### 1.1 Eliminar artefactos pip (=X.Y.Z)

```bash
cd /home/fciliberti/Trabajos/Lab/UniversoCentrífugo
rm -f "=0.56.0" "=1.21.0" "=1.7.0" "=3.5.0"
```

### 1.2 Eliminar archivos .backup y .original

```bash
# Backups en notebooks/
rm -f notebooks/run_256cubed_chunked_evolution.py.backup
rm -f notebooks/run_256cubed_chunked_evolution.py.original
rm -f notebooks/setup_256cubed_optimized_simulation.py.backup
rm -f notebooks/setup_256cubed_optimized_simulation.py.original

# Original en raíz
rm -f run_256cubed_complete_pipeline.py.original
```

### 1.3 Limpiar __pycache__

```bash
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
```

### Verificación Fase 1

```bash
ls -la | grep "^="                    # No debe mostrar nada
find . -name "*.backup" -o -name "*.original"  # No debe mostrar nada
find . -type d -name "__pycache__"    # No debe mostrar nada
```

---

## FASE 2: Archivado de Línea BSSN Obsoleta

### 2.1 Crear estructura de archive

```bash
mkdir -p archive/bssn_paradigm
mkdir -p archive/audits
mkdir -p archive/plans_legacy
mkdir -p archive/scripts_legacy
mkdir -p archive/empty_containers_snapshot
```

### 2.2 Crear README de bssn_paradigm

Crear archivo `archive/bssn_paradigm/README.md`:

```markdown
# Archivo: Paradigma BSSN (Obsoleto)

Estos documentos pertenecen al paradigma BSSN (Baumgarte-Shapiro-Shibata-Nakamura) que fue el enfoque inicial de simulación numérica del proyecto.

## Contexto Histórico

En junio 2026, el proyecto abandonó el formalismo BSSN en favor del **solver espectral FFT de membrana elástica**. El cambio se documenta en:
- `docs/simulacion_256cubed/README_256cubed.md` — Transición BSSN → FFT
- `docs/07_fase2_ejecucion_simulacion_completada.md` — Validación del solver FFT

## Razones del Cambio

1. **Ineficiencia física**: BSSN evoluciona temporalmente un espacio-tiempo que es intrínsecamente estático en escalas locales.
2. **Inestabilidades numéricas**: Diferencias finitas y ghost cells inducían vibraciones espurias.
3. **Costo computacional**: BSSN requería 128GB+ RAM y días de ejecución vs segundos con FFT.

## Documentos Archivados

- `plan_verificacion_algoritmo_completo.md` — Plan de simulación BSSN 256³
- `RESUMEN_EJECUTIVO_256CUBED.md` — Arquitectura BSSN con chunks/memory mapping
- `README_SIMULATION.md` — Sistema BSSN completo (orchestrator, GPU, checkpoints)
- `plan_reorganizacion_cientifica_completo.md` — Plan de reorganización de junio 2025 (parcialmente ejecutado)

## Estado Actual

El solver FFT está validado hasta 256³ con correlación >99.8% contra Schwarzschild. Ver:
- `docs/11_plan_estrategico_256cubed_completo.md`
- `docs/12_validacion_plan_256cubed_completado.md`
- `notebooks/simulacion_membrana_elastica.py` (motor principal)
```

### 2.3 Mover documentos BSSN a archive

```bash
mv plan_verificacion_algoritmo_completo.md archive/bssn_paradigm/
mv RESUMEN_EJECUTIVO_256CUBED.md archive/bssn_paradigm/
mv README_SIMULATION.md archive/bssn_paradigm/
mv plan_reorganizacion_cientifica_completo.md archive/bssn_paradigm/
```

### Verificación Fase 2

```bash
ls archive/bssn_paradigm/
# Debe mostrar: README.md + 4 archivos .md movidos
test -f plan_verificacion_algoritmo_completo.md && echo "ERROR: aún existe" || echo "OK: movido"
```

---

## FASE 3: Archivado de Material Complementario Obsoleto

### 3.1 Mover auditoría y planes legacy

```bash
mv docs/informe_resolucion_auditoria.md archive/audits/
mv plan_verificacion_completa.md archive/plans_legacy/
```

### 3.2 Mover scripts legacy de raíz

```bash
mv fix_parallelization_bottlenecks.py archive/scripts_legacy/
mv fix_parallelization_improved.py archive/scripts_legacy/
```

### 3.3 Documentar simulation_256cubed_data/

Crear archivo `simulation_256cubed_data/README.md`:

```markdown
# Legacy Bulk Data: Campos Tensoriales 256³

**Tamaño total**: ~1.7 GB  
**Formato**: Archivos `.dat` binarios (campos tensoriales en grilla 3D)  
**Origen**: Simulación 256³ con formalismo BSSN (junio 2025)  

## Contenido

23 archivos de campos tensoriales (`gamma_*.dat`, `K_*.dat`, `alpha.dat`, `beta_*.dat`, etc.) de 64 MB cada uno, más `stress_energy_tensor.dat` de 1 GB.

## Scripts que Referencian estos Datos

- `notebooks/setup_256cubed_optimized_simulation.py`
- `run_256cubed_complete_pipeline.py`
- `setup_256cubed_optimized_parallel.py`
- `fix_parallelization_bottlenecks.py` (archivado en `archive/scripts_legacy/`)

## Estado

**Legacy**: Estos datos corresponden al paradigma BSSN abandonado. No se regeneran con el solver FFT actual. Se conservan para referencia histórica y posible análisis comparativo futuro.

## Decisión de Archivado

No se mueven a `archive/` porque son referenciados por scripts activos. Si en el futuro se eliminan esas referencias, mover a `archive/legacy_data/simulation_256cubed_data/`.
```

### Verificación Fase 3

```bash
test -f docs/informe_resolucion_auditoria.md && echo "ERROR" || echo "OK: movido a archive/audits/"
ls archive/audits/
ls archive/plans_legacy/
ls archive/scripts_legacy/
cat simulation_256cubed_data/README.md
```

---

## FASE 4: Limpieza de Carpetas Muertas

### 4.1 Guardar AGENTS.md de carpetas muertas

```bash
cp computational_implementation/AGENTS.md archive/empty_containers_snapshot/computational_implementation_AGENTS.md
cp experimental_validation/AGENTS.md archive/empty_containers_snapshot/experimental_validation_AGENTS.md
cp ideas_descabelladas/AGENTS.md archive/empty_containers_snapshot/ideas_descabelladas_AGENTS.md
```

### 4.2 Mover contenido de output/ a results/

```bash
# Crear destino
mkdir -p results/simulation_256cubed
mkdir -p results/reports

# Mover contenido de output/simulation_256cubed/
mv output/simulation_256cubed/results/* results/simulation_256cubed/ 2>/dev/null || true
mv output/simulation_256cubed/checkpoints results/simulation_256cubed/ 2>/dev/null || true
mv output/simulation_256cubed/data results/simulation_256cubed/ 2>/dev/null || true
mv output/simulation_256cubed/visualizations results/simulation_256cubed/ 2>/dev/null || true

# Mover reportes científicos
mv results/local_gravity_32cubed/scientific_analysis_report_32cubed.txt results/reports/ 2>/dev/null || true
mv results/simulation_256cubed/scientific_analysis_report_256cubed.txt results/reports/ 2>/dev/null || true

# Eliminar carpeta output/ vacía
rm -rf output/
```

### 4.3 Eliminar carpetas muertas

```bash
rm -rf computational_implementation/
rm -rf experimental_validation/
rm -rf ideas_descabelladas/
rm -rf test_validation_figures/
rm -rf validation_figures/
rm -rf scientific_publication/appendices/
```

### Verificación Fase 4

```bash
# Estas carpetas NO deben existir
for dir in computational_implementation experimental_validation ideas_descabelladas test_validation_figures validation_figures output; do
  test -d "$dir" && echo "ERROR: $dir aún existe" || echo "OK: $dir eliminada"
done

# reports/ debe tener los 2 reportes
ls results/reports/
# Debe mostrar: scientific_analysis_report_32cubed.txt, scientific_analysis_report_256cubed.txt

# simulation_256cubed/ debe tener contenido
ls results/simulation_256cubed/
```

---

## FASE 5: Consolidación de Datos y Configuración

### 5.1 Crear estructura data/

```bash
mkdir -p data/configs
mkdir -p data/observational
mkdir -p data/initial_conditions
```

### 5.2 Mover configs JSON de raíz → data/configs/

```bash
mv config_64cubed.json data/configs/
mv manual_64cubed_config.json data/configs/
mv optimal_simulation_config.json data/configs/
mv parallelization_config_optimized.json data/configs/
mv parallel_optimization_config.json data/configs/
mv simulation_256cubed_config.json data/configs/
```

### 5.3 Mover datos observacionales de downloads/ → data/observational/

```bash
mv downloads/SPARC_Lelli2016c.mrt.txt data/observational/
mv downloads/Rotmod_LTG data/observational/
mv downloads/Rotmod_LTG.zip data/observational/
```

### 5.4 Mover datos binarios sueltos de raíz

```bash
mv simulation_initial_data.npz data/initial_conditions/
mv simulation_results_gpu.npz data/initial_conditions/
mv hubble_analysis_simulation_results_gpu.png results/
mv checkpoint_step_000000.npz checkpoints/
mv checkpoint_step_000010.npz checkpoints/
mv checkpoint_step_000020.npz checkpoints/
```

### Verificación Fase 5

```bash
# Raíz no debe tener .json, .npz, .png sueltos
ls *.json 2>/dev/null && echo "ERROR: hay JSONs en raíz" || echo "OK: no hay JSONs en raíz"
ls *.npz 2>/dev/null && echo "ERROR: hay NPZs en raíz" || echo "OK: no hay NPZs en raíz"
ls *.png 2>/dev/null && echo "ERROR: hay PNGs en raíz" || echo "OK: no hay PNGs en raíz"

# Estructura data/ correcta
tree data/ -L 2
```

---

## FASE 6: Actualización de AGENTS.md [CRÍTICO]

Esta es la fase más importante. Cada AGENTS.md debe reflejar la realidad post-reorganización.

### 6.1 docs/AGENTS.md — Actualizar STRUCTURE y WHERE TO LOOK

Editar `docs/AGENTS.md`:

**Agregar sección DOCUMENTACIÓN DE APOYO después de INFORMES TEMÁTICOS:**

```markdown
├── ── DOCUMENTACIÓN DE APOYO (ex-huérfanos integrados) ──
├── formalismo_dbi_energia_oscura.md        # Extensión DBI para energía oscura (w=-1)
├── acoplamiento_masa_inercia_centrifuga.md # Retroalimentación masa-vacío en momento angular
├── calculo_radio_tamano_universo.md        # Cálculo observacional de R₀ y volumen S³
```

**Corregir simulacion_256cubed/:**

```markdown
└── simulacion_256cubed/
    └── README_256cubed.md              # Único archivo real (transición BSSN→FFT)
```

**Agregar a tabla WHERE TO LOOK:**

```markdown
| **Energía oscura DBI** | `formalismo_dbi_energia_oscura.md` | Extensión teórica |
| **Acoplamiento masa-vacío** | `acoplamiento_masa_inercia_centrifuga.md` | Extensión teórica |
| **Radio del universo** | `calculo_radio_tamano_universo.md` | Cálculo observacional |
```

**Agregar nota sobre informe_resolucion_auditoria.md:**

```markdown
## NOTA HISTÓRICA

El archivo `informe_resolucion_auditoria.md` fue movido a `archive/audits/` tras la reorganización de junio 2026. Era un documento meta (respuesta a auditoría adversarial) que no alimentaba la investigación activa.
```

### 6.2 scientific_publication/AGENTS.md — Reflejar estructura real

Reescribir completamente `scientific_publication/AGENTS.md`:

```markdown
# SCIENTIFIC PUBLICATION

**Dominio**: Manuscrito formal de la teoría del Universo Centrífugo.

## OVERVIEW

Documentación científica estructurada en secciones que conforman el manuscrito formal. Actualmente contiene fundamentos teóricos, desarrollo matemático, predicciones observacionales y verificación experimental.

## STRUCTURE REAL (post-reorganización junio 2026)

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

| Sección | Archivos | Estado |
|---------|----------|--------|
| `01_theoretical_foundations/` | 1 | ✅ Consolidado |
| `02_mathematical_development/` | 1 | ✅ Completo |
| `03_numerical_validation/` | 0 | ❌ NO EXISTE (ver docs/ para validación numérica) |
| `04_observational_predictions/` | 1 | ✅ Predicciones desarrolladas |
| `05_experimental_verification/` | 2 | ✅ Criterios + validación DESI |
| `06_implications_and_conclusions/` | 0 | ❌ NO EXISTE |
| `appendices/` | 0 | ❌ ELIMINADO (junio 2026) |

## SECUENCIA DE LECTURA

1. `01_theoretical_foundations/core_hypothesis.md`
2. `02_mathematical_development/4d_rotation_dynamics.md`
3. `04_observational_predictions/cosmological_parameters.md`
4. `05_experimental_verification/falsifiability_criteria.md`
5. `05_experimental_verification/desi_2024_validation.md`

## RELACIÓN CON docs/

Este directorio contiene el manuscrito formal. Para documentación de trabajo, metodologías, informes de simulación y material auxiliar, ver `docs/`.

La validación numérica completa del solver FFT está en:
- `docs/05_informe_simulacion_numerica.md`
- `docs/07_fase2_ejecucion_simulacion_completada.md`
- `docs/08_fase3_analisis_resultados_completada.md`
- `docs/12_validacion_plan_256cubed_completado.md`

## ANTI-PATTERNS

- No referenciar archivos inexistentes (secciones 03, 06, appendices fueron eliminadas del esquema).
- No confundir con `docs/`: aquí va el manuscrito final, allí va material de trabajo.
```

### 6.3 scientific_publication/README.md — Eliminar referencias fantasma

Editar `scientific_publication/README.md`:

**Eliminar o marcar [NO EXISTE] las siguientes secciones:**
- Sección 3 (Validación Numérica): Marcar como "Ver docs/ para validación numérica FFT"
- Sección 6 (Implicaciones y Conclusiones): Marcar como "Pendiente de desarrollo"
- Sección 7 (Apéndices): Eliminar completely
- Todas las referencias a archivos inexistentes dentro de cada sección

**Actualizar sección "Referencias Clave del Proyecto":**

Eliminar referencias a:
- `../docs/conjetura_refundada.md` (no existe)
- `../docs/desarrollo_matematico_detallado_v2.md` (no existe)
- `../docs/predicciones_observacionales_4d.md` (no existe)

Reemplazar con referencias a docs reales:
- `../docs/01_marco_teorico.md`
- `../docs/formulacion_matematica_rotacion_4d.md`
- `../docs/conservacion_momento_inercia_geff.md`

### 6.4 publication_strategy/AGENTS.md — Marcar stubs

Agregar al inicio de `publication_strategy/AGENTS.md`:

```markdown
## ⚠️ ESTADO REAL (junio 2026)

**Solo `target_analysis/journal_selection_analysis.md` (19KB) tiene contenido desarrollado.**

Los restantes 15 archivos `.md` en este directorio son **stubs placeholders** (20-43 bytes cada uno) con títulos descriptivos pero sin contenido. Representan secciones planificadas pero no completadas de la estrategia editorial.

### Stubs pendientes de completar:

- `target_analysis/competitive_landscape.md`
- `target_analysis/conference_opportunities.md`
- `target_analysis/reviewer_identification.md`
- `communication_plan/presentation_materials.md`
- `communication_plan/press_release_template.md`
- `communication_plan/scientific_community_outreach.md`
- `communication_plan/social_media_strategy.md`
- `manuscript_preparation/executive_summary.md`
- `manuscript_preparation/figure_and_table_strategy.md`
- `manuscript_preparation/main_manuscript_outline.md`
- `manuscript_preparation/supplementary_materials.md`
- `risk_management/fallback_strategies.md`
- `risk_management/intellectual_property_considerations.md`
- `risk_management/potential_criticisms_analysis.md`
- `risk_management/response_preparation.md`
- `submission_strategy/cover_letter_templates.md`
- `submission_strategy/response_to_reviewers_framework.md`
- `submission_strategy/revision_strategy.md`
- `submission_strategy/submission_sequence.md`

### Acción recomendada

Completar estos stubs cuando se avance hacia la publicación, o eliminarlos si la estrategia editorial cambia.
```

### 6.5 notebooks/AGENTS.md — CREAR (nuevo)

Crear archivo `notebooks/AGENTS.md`:

```markdown
# NOTEBOOKS

**Dominio**: Scripts Python de simulación, cálculo teórico y análisis.

## ⚠️ NOTA IMPORTANTE

A pesar del nombre, este directorio contiene **scripts Python (.py)**, no Jupyter Notebooks. Se ejecutan con `python script.py`.

## STRUCTURE

```
notebooks/
│
├── ── MOTORES FÍSICOS (simulaciones principales) ──
├── simulacion_membrana_elastica.py        # Motor FFT de membrana elástica 3D (genera results/membrana_elastica/)
├── simulacion_orbita_precesion.py         # Simulación de órbita y precesión (Mercurio)
├── simulacion_desvio_luz_coriolis.py      # Desvío de luz por Coriolis 4D (lensing)
├── simulacion_evolucion_temporal_geff.py  # Evolución temporal de G_eff
├── analisis_materia_oscura.py             # Curvas de rotación galáctica sin materia oscura
├── comparacion_curvas_expansion.py        # Friedmann emergente vs ΛCDM
│
├── ── CÁLCULOS TEÓRICOS ──
├── calculate_4velocity_field.py           # Campo de 4-velocidad en rotación isoclínica
├── calculate_strain_tensor.py             # Tensor de deformación de brana
├── calculate_3d_projection.py             # Proyección 4D→3D
├── calculate_volume_average.py            # Promedio en volumen de la 3-esfera
├── solve_linearized_equations.py          # Ecuaciones de Einstein linealizadas
├── demo_basic_calculation.py              # Demo de cálculo básico
├── verify_hubble_relation.py              # Verificación relación de Hubble
│
├── ── SETUP / INSTALACIÓN ──
├── setup_numerical_simulation.py          # Setup parametrización numérica
├── setup_local_gravity_sources.py         # Setup fuentes de gravedad local
├── setup_256cubed_optimized_simulation.py # Setup simulación 256³ optimizada
├── install_simulation_deps.py             # Instalador de dependencias
│
├── ── ANÁLISIS / MONITOREO ──
├── analyze_256cubed_results.py            # Análisis resultados 256³
├── analyze_local_gravity_results.py       # Análisis gravedad local
├── monitor_local_gravity_simulation.py    # Monitor de simulación gravedad local
├── check_simulation_status.py             # Check de status de simulación
├── optimize_simulation_params.py          # Optimización de parámetros
├── test_performance.py                    # Test de performance
│
└── ── PIPELINES / RUNNERS ──
    ├── run_local_gravity_simulation.py    # Runner gravedad local
    ├── run_numerical_simulation.py        # Motor numérico (BSSN-like)
    └── run_256cubed_chunked_evolution.py  # Evolución 256³ por chunks
```

## MOTORES PRINCIPALES

### simulacion_membrana_elastica.py (Motor FFT)

**Rol**: Resolver ecuación de Poisson elástica ∇²h - λ²h = S(r) mediante FFT espectral.

**Uso**:
```bash
python notebooks/simulacion_membrana_elastica.py
```

**Output**: Genera archivos `.npy` en `results/membrana_elastica/{32,64,128,256}cubed/`.

**Validación**: Correlación >99.8% contra perfil de Schwarzschild en 256³. Ver `docs/12_validacion_plan_256cubed_completado.md`.

### Otros motores físicos

Cada motor corresponde a un test/predicción de la teoría:

| Script | Test/Predicción | Doc asociado |
|--------|----------------|--------------|
| `simulacion_orbita_precesion.py` | Precesión perihelio Mercurio | `docs/informe_precesion_perihelio.md` |
| `simulacion_desvio_luz_coriolis.py` | Lensing gravitacional | `docs/fuerza_coriolis_4d_trayectorias.md` |
| `analisis_materia_oscura.py` | Curvas rotación galáctica | `docs/informe_materia_oscura_elastica.md` |
| `comparacion_curvas_expansion.py` | Expansión cosmológica R(t) | `docs/comparacion_curvas_expansion.md` |
| `simulacion_evolucion_temporal_geff.py` | Estabilidad de G_eff | `docs/conservacion_momento_inercia_geff.md` |

## CONVENCIONES

- **Sin __init__.py**: Los directorios NO son paquetes Python. Imports por path relativo.
- **Scripts auto-ejecutables**: Cada archivo corre independientemente con `python script.py`.
- **Nomenclatura científica**: Variables con notación matemática en comentarios (omega_4D, R_0, etc.).
- **Outputs en results/**: Todos los datos generados van a `results/`, nunca en `notebooks/`.

## ANTI-PATTERNS

- No crear `__init__.py` ni convertir en paquete.
- No generar datos en `notebooks/` (siempre en `results/`).
- No commitear `.npz` grandes (agregar a `.gitignore`).
- No renombrar motores principales sin actualizar referencias en `docs/`.
```

### 6.6 Eliminar AGENTS.md de carpetas eliminadas

Ya se eliminaron en Fase 4:
- `computational_implementation/AGENTS.md` ✅ (guardado en archive)
- `experimental_validation/AGENTS.md` ✅ (guardado en archive)
- `ideas_descabelladas/AGENTS.md` ✅ (guardado en archive)

### Verificación Fase 6

```bash
# Cada AGENTS.md existente debe describir su directorio correctamente
cat docs/AGENTS.md | grep -A 5 "DOCUMENTACIÓN DE APOYO"
cat scientific_publication/AGENTS.md | grep "ESTADO REAL"
cat notebooks/AGENTS.md | head -20
cat publication_strategy/AGENTS.md | grep "ESTADO REAL"

# No deben existir AGENTS.md de carpetas eliminadas
test -f computational_implementation/AGENTS.md && echo "ERROR" || echo "OK"
test -f experimental_validation/AGENTS.md && echo "ERROR" || echo "OK"
test -f ideas_descabelladas/AGENTS.md && echo "ERROR" || echo "OK"
```

---

## FASE 7: Integración de Documentación de Apoyo

### 7.1 Agregar referencias cruzadas DESDE docs principales HACIA docs de apoyo

#### 7.1.1 formalismo_dbi_energia_oscura.md

**Referenciar desde `02_propuesta_investigacion.md`** (sección 3.1 Firma de Curvatura):

Agregar nota al pie:
```markdown
Para una formalización avanzada mediante la acción de Dirac-Born-Infeld (DBI) que reproduce w=-1 dinámicamente, ver [`formalismo_dbi_energia_oscura.md`](formalismo_dbi_energia_oscura.md).
```

**Referenciar desde `comparacion_curvas_expansion.md`** (sección 1 Friedmann Emergente):

Agregar nota:
```markdown
**Extensión DBI**: La acción de Dirac-Born-Infeld proporciona una derivación rigurosa de la ecuación de estado w=-1 a partir de la saturación relativista de la tensión de brana en el Bulk. Ver [`formalismo_dbi_energia_oscura.md`](formalismo_dbi_energia_oscura.md).
```

#### 7.1.2 acoplamiento_masa_inercia_centrifuga.md

**Referenciar desde `conservacion_momento_inercia_geff.md`** (sección de momento angular):

Agregar sección "Extensión Dinámica":
```markdown
## Extensión: Retroalimentación Masa-Vacío

El acoplamiento dinámico entre la masa inercial total (incluyendo la energía del vacío/tensión de brana) y el momento angular del Bulk genera una retroalimentación no lineal en ω₄D(R). Para la derivación completa, ver [`acoplamiento_masa_inercia_centrifuga.md`](acoplamiento_masa_inercia_centrifuga.md).
```

**Referenciar desde `01_marco_teorico.md`** (sección 2 Fundamentos Geométricos):

Agregar nota:
```markdown
**Contribución del vacío**: La energía del vacío (tensión de brana T₃) contribuye a la masa inercial total del universo, modificando la evolución de ω₄D(R). Ver [`acoplamiento_masa_inercia_centrifuga.md`](acoplamiento_masa_inercia_centrifuga.md) para el tratamiento completo.
```

#### 7.1.3 calculo_radio_tamano_universo.md

**Referenciar desde `01_marco_teorico.md`** (sección 2.1 Parametrización):

Agregar nota:
```markdown
**Valores numéricos**: Para el cálculo observacional de R₀ ≈ 10²⁶ m y el volumen de la 3-esfera V₃ᴅ = 2π²R₀³, ver [`calculo_radio_tamano_universo.md`](calculo_radio_tamano_universo.md).
```

**Referenciar desde `comparacion_curvas_expansion.md`** (introducción):

Agregar nota:
```markdown
**Escala cosmológica**: El radio hiperdimensional R₀ ≈ 10²⁶ m establece la escala de la 3-esfera. Ver [`calculo_radio_tamano_universo.md`](calculo_radio_tamano_universo.md) para la derivación desde parámetros observacionales.
```

### 7.2 Agregar referencias cruzadas DESDE docs de apoyo HACIA el hub

Verificar que cada doc de apoyo linkea a `conservacion_momento_inercia_geff.md` donde sea relevante:

- `formalismo_dbi_energia_oscura.md`: Ya menciona conservación de momento angular → agregar link explícito.
- `acoplamiento_masa_inercia_centrifuga.md`: Tema central es momento angular → debe linkear al hub múltiples veces.
- `calculo_radio_tamano_universo.md`: Calcula R₀ que entra en ω₄D ∝ 1/R² → linkear al hub.

### 7.3 Actualizar docs/AGENTS.md WHERE TO LOOK

Ya hecho en Fase 6.1 (agregar filas para los 3 docs de apoyo).

### Verificación Fase 7

```bash
# Cada doc de apoyo debe tener ≥2 links entrantes
grep -l "formalismo_dbi_energia_oscura" docs/*.md | wc -l  # Debe ser ≥2
grep -l "acoplamiento_masa_inercia" docs/*.md | wc -l      # Debe ser ≥2
grep -l "calculo_radio_tamano" docs/*.md | wc -l           # Debe ser ≥2

# Cada doc de apoyo debe linkear al hub
grep -c "conservacion_momento_inercia_geff" docs/formalismo_dbi_energia_oscura.md
grep -c "conservacion_momento_inercia_geff" docs/acoplamiento_masa_inercia_centrifuga.md
grep -c "conservacion_momento_inercia_geff" docs/calculo_radio_tamano_universo.md
```

---

## FASE 8: Actualización de README.md Principal

Editar `README.md` de raíz:

### 8.1 Actualizar sección "Estructura del Proyecto"

Reemplazar con:

```markdown
### Estructura del Proyecto

```
UniversoCentrífugo/
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias Python
│
├── docs/                              # Documentación científica (27 archivos)
│   ├── AGENTS.md                      # Índice de navegación
│   ├── 01_marco_teorico.md → 12_*.md  # Serie numerada (lectura secuencial)
│   ├── formulacion_matematica_*.md    # Formalismo especializado
│   ├── informe_*.md                   # Informes temáticos
│   ├── plan_simulacion_elastica.md    # Plan maestro de simulación
│   └── simulacion_256cubed/           # Subdirectorio técnico
│
├── notebooks/                         # Scripts Python de simulación y análisis
│   ├── AGENTS.md                      # Inventario de scripts
│   ├── simulacion_membrana_elastica.py # Motor FFT principal
│   ├── simulacion_*.py                # Motores de tests físicos
│   ├── calculate_*.py                 # Cálculos teóricos
│   └── setup_*.py                     # Setup y configuración
│
├── results/                           # Resultados de simulaciones
│   ├── membrana_elastica/{32,64,128,256}cubed/
│   ├── {curvas_expansion,estabilidad_gravedad,...}/
│   ├── simulation_256cubed/           # Output completo 256³
│   └── reports/                       # Reportes científicos
│
├── data/                              # Datos de entrada y configuración
│   ├── configs/                       # JSONs de configuración
│   ├── observational/                 # Catálogos galácticos (SPARC, Rotmod)
│   └── initial_conditions/            # Datos iniciales .npz
│
├── checkpoints/                       # Estados de simulación serializados
│
├── scientific_publication/            # Manuscrito formal
│   └── {01,02,04,05}_*/               # Secciones del paper
│
├── publication_strategy/              # Estrategia editorial
│   └── target_analysis/journal_selection_analysis.md
│
├── simulation_256cubed_data/          # Legacy bulk data (~1.7GB, BSSN)
│
├── downloads/                         # Papers y referencias
│   └── Modelos teóricos de un universo rotante.pdf
│
├── archive/                           # Material histórico/obsoleto
│   ├── bssn_paradigm/                 # Documentación BSSN abandonada
│   ├── audits/                        # Informes de auditoría
│   ├── plans_legacy/                  # Planes viejos
│   ├── scripts_legacy/                # Scripts obsoletos
│   └── empty_containers_snapshot/     # AGENTS.md de carpetas eliminadas
│
└── Entry Points de Raíz               # Scripts ejecutables principales
    ├── run_complete_simulation.py
    ├── run_256cubed_complete_pipeline.py
    └── [otros runners y herramientas]
```
```

### 8.2 Actualizar sección "Documentación Científica"

Agregar subsección "Documentación de Apoyo":

```markdown
### 📚 Documentación de Apoyo (Ex-Huérfanos Integrados)

| Archivo | Propósito | Relación con docs principales |
|---------|-----------|-------------------------------|
| [`formalismo_dbi_energia_oscura.md`](docs/formalismo_dbi_energia_oscura.md) | Acción DBI para w=-1 | Extiende `02_propuesta_investigacion.md` §3 |
| [`acoplamiento_masa_inercia_centrifuga.md`](docs/acoplamiento_masa_inercia_centrifuga.md) | Retroalimentación masa-vacío | Extiende `conservacion_momento_inercia_geff.md` |
| [`calculo_radio_tamano_universo.md`](docs/calculo_radio_tamano_universo.md) | Cálculo R₀ y volumen S³ | Apoya `01_marco_teorico.md` §2 |
```

### 8.3 Actualizar sección "Resultados y Estado Actual"

Modificar:

```markdown
### ✅ Logros Completados

1. **Marco teórico riguroso**: Formalismo matemático consistente (docs 01-03)
2. **Cambio de paradigma completado**: Transición BSSN → FFT espectral (junio 2026)
3. **Solver FFT validado**: Correlación >99.8% contra Schwarzschild en 256³
4. **Tests físicos implementados**: Precesión, lensing, materia oscura, expansión
5. **Reorganización integral**: Proyecto totalmente consistente (junio 2026)
```

### 8.4 Eliminar referencias a paradigmas muertos

Buscar y eliminar/marcar cualquier mención a:
- "BSSN" como sistema activo
- "128GB RAM" o "semanas de ejecución"
- Referencias a archivos que ya no existen

### Verificación Fase 8

```bash
# README no debe mencionar BSSN como activo
grep -i "BSSN" README.md | grep -v "abandonado\|obsoleto\|archivo" && echo "ERROR" || echo "OK"

# README debe mencionar docs de apoyo
grep "formalismo_dbi_energia_oscura" README.md && echo "OK: doc de apoyo mencionado"
```

---

## FASE 9: Actualización de .gitignore

Editar `.gitignore` y agregar:

```gitignore
# Artefactos pip (errores de sintaxis)
=*.*/

# Backups de editores y versiones anteriores
*.backup
*.original
*.bak
*~

# Python cache
__pycache__/
*.pyc
*.pyo

# Datos de simulación grandes (>100MB) fuera de ubicaciones autorizadas
/*.npz
!data/**/*.npz
!checkpoints/**/*.npz
!results/**/*.npz

# Visualizaciones generadas en raíz
/*.png
!docs/**/*.png
!results/**/*.png

# Archivos temporales
*.tmp
*.temp
*.log

# IDE y editors
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

### Verificación Fase 9

```bash
cat .gitignore | grep "=\\*"
cat .gitignore | grep "backup"
```

---

## FASE 10: Verificación Final de Consistencia

### Checklist de 15 puntos

```bash
#!/bin/bash
# Script de verificación final

echo "=== VERIFICACIÓN FINAL DE CONSISTENCIA ==="
echo ""

# 1. Raíz limpia
echo "1. Raíz limpia (solo entry points, READMEs, carpetas):"
ls -1 *.py *.md *.txt 2>/dev/null | wc -l
echo "   (Debe ser ~20-25 archivos)"

# 2. Sin basura
echo ""
echo "2. Sin archivos basura:"
ls =* 2>/dev/null && echo "   ERROR: hay archivos =X.Y.Z" || echo "   ✓ OK"
find . -name "*.backup" -o -name "*.original" 2>/dev/null | grep -v archive && echo "   ERROR: hay backups" || echo "   ✓ OK"

# 3. Carpetas muertas eliminadas
echo ""
echo "3. Carpetas muertas eliminadas:"
for dir in computational_implementation experimental_validation ideas_descabelladas test_validation_figures validation_figures output; do
  test -d "$dir" && echo "   ERROR: $dir existe" || echo "   ✓ $dir eliminada"
done

# 4. AGENTS.md consistentes
echo ""
echo "4. AGENTS.md existentes:"
find . -name "AGENTS.md" -not -path "./archive/*" | while read f; do
  echo "   - $f"
done

# 5. Docs de apoyo integrados
echo ""
echo "5. Docs de apoyo tienen links entrantes:"
for doc in formalismo_dbi_energia_oscura acoplamiento_masa_inercia_centrifuga calculo_radio_tamano_universo; do
  count=$(grep -l "$doc" docs/*.md 2>/dev/null | wc -l)
  echo "   $doc: $count referencias"
done

# 6. scientific_publication sin fantasmas
echo ""
echo "6. scientific_publication/AGENTS.md refleja realidad:"
grep "ESTADO REAL" scientific_publication/AGENTS.md >/dev/null && echo "   ✓ OK" || echo "   ERROR: no tiene ESTADO REAL"

# 7. notebooks/AGENTS.md existe
echo ""
echo "7. notebooks/AGENTS.md existe:"
test -f notebooks/AGENTS.md && echo "   ✓ OK" || echo "   ERROR: no existe"

# 8. data/ estructurado
echo ""
echo "8. data/ tiene subcarpetas correctas:"
ls data/*/ 2>/dev/null | head -5

# 9. results/reports/ tiene reportes
echo ""
echo "9. results/reports/ tiene reportes científicos:"
ls results/reports/*.txt 2>/dev/null | wc -l
echo "   (Debe ser 2)"

# 10. archive/ estructurado
echo ""
echo "10. archive/ tiene subcarpetas:"
ls -d archive/*/ 2>/dev/null

# 11. README.md actualizado
echo ""
echo "11. README.md menciona docs de apoyo:"
grep -q "formalismo_dbi_energia_oscura" README.md && echo "   ✓ OK" || echo "   ERROR: no menciona"

# 12. .gitignore previene basura
echo ""
echo "12. .gitignore tiene patrones anti-basura:"
grep -q "=\\*" .gitignore && echo "   ✓ OK (=*)" || echo "   ERROR: falta =*"
grep -q "\\.backup" .gitignore && echo "   ✓ OK (.backup)" || echo "   ERROR: falta .backup"

# 13. No hay referencias rotas en docs
echo ""
echo "13. Verificación de paths mencionados en docs (sample):"
grep -h "\[.*\](.*\.md)" docs/*.md | head -5

# 14. simulation_256cubed_data/ documentado
echo ""
echo "14. simulation_256cubed_data/ tiene README:"
test -f simulation_256cubed_data/README.md && echo "   ✓ OK" || echo "   ERROR: no tiene README"

# 15. git status limpio
echo ""
echo "15. git status (debe mostrar solo movimientos/ediciones):"
git status --short | wc -l
echo "   archivos modificados"

echo ""
echo "=== VERIFICACIÓN COMPLETADA ==="
```

Ejecutar:

```bash
chmod +x verificar_consistencia.sh  # Si lo guardás como script
./verificar_consistencia.sh
```

O ejecutar los comandos manualmente uno por uno.

---

## Resumen de Ejecución

| Fase | Estado | Tiempo real | Notas |
|------|--------|-------------|-------|
| 1 | ⏳ Pendiente | - | |
| 2 | ⏳ Pendiente | - | |
| 3 | ⏳ Pendiente | - | |
| 4 | ⏳ Pendiente | - | |
| 5 | ⏳ Pendiente | - | |
| 6 | ⏳ Pendiente | - | CRÍTICA |
| 7 | ⏳ Pendiente | - | |
| 8 | ⏳ Pendiente | - | |
| 9 | ⏳ Pendiente | - | |
| 10 | ⏳ Pendiente | - | |

**Total estimado**: 2.5 horas

---

## Próximos Pasos Inmediatos

1. Ejecutar Fase 1 (eliminación de basura)
2. Ejecutar Fase 2 (archivar BSSN)
3. Ejecutar Fase 3 (archivar complementario)
4. Continuar secuencialmente hasta Fase 10
5. Commit final: `git commit -m "Reorganización integral: consistencia total"`
