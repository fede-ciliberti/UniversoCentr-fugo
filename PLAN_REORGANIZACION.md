# Plan de Reorganización Integral — Universo Centrífugo

**Fecha**: 15 de junio de 2026
**Autor**: Sisyphus (a pedido de Fede)
**Objetivo**: Dejar el proyecto totalmente consistente — documentación, código, datos y metadata alineados sin fantasmas ni duplicaciones.

---

## Principios Rectores

1. **No romper lo que funciona**: Los scripts en `notebooks/` corren y generan resultados reales. No se renombran ni reestructuran internamente.
2. **Documentación huérfana = documentación de apoyo**: Se mantiene en `docs/`, se integra en el índice con referencias cruzadas desde los docs principales.
3. **Archivo > Eliminación**: Lo obsoleto va a `archive/` antes de borrarse. Solo se eliminan artefactos basura (=X.Y.Z) y __pycache__.
4. **Un AGENTS.md = Una realidad**: Cada AGENTS.md debe describir EXACTAMENTE lo que hay en disco. Sin listas de archivos inexistentes.
5. **Raíz limpia**: La raíz del proyecto solo contiene entry points, README, configs del repo, y carpetas de primer nivel organizadas.

---

## Estructura Final Objetivo

```
UniversoCentrífugo/
│
├── README.md                              # Entrada principal (ACTUALIZAR)
├── requirements.txt                       # Dependencias Python
│
├── docs/                                  # Documentación científica VIVA
│   ├── AGENTS.md                          # Índice (ACTUALIZAR con huérfanos integrados)
│   │
│   │  ── SERIE NUMERADA (lectura secuencial) ──
│   ├── 01_marco_teorico.md
│   ├── 02_propuesta_investigacion.md
│   ├── 03_metodologia_gravedad_emergente.md
│   ├── 04_metodologia_verificacion_gravedad.md
│   ├── 05_informe_simulacion_numerica.md
│   ├── 06_plan_simulacion_gravedad_local.md
│   ├── 07_fase2_ejecucion_simulacion_completada.md
│   ├── 08_fase3_analisis_resultados_completada.md
│   ├── 09_informe_ejecutivo_gravedad_local.md
│   ├── 10_roadmap_alta_resolucion.md
│   ├── 11_plan_estrategico_256cubed_completo.md
│   ├── 12_validacion_plan_256cubed_completado.md
│   │
│   │  ── FORMULACIÓN MATEMÁTICA ──
│   ├── formulacion_matematica_rotacion_4d.md
│   ├── ecuaciones_movimiento_rotacion_4d.md
│   ├── conservacion_momento_inercia_geff.md    ← HUB central
│   ├── comparacion_curvas_expansion.md
│   ├── fuerza_coriolis_4d_trayectorias.md
│   │
│   │  ── DOCUMENTACIÓN DE APOYO (ex-huérfanos, integrados) ──
│   ├── formalismo_dbi_energia_oscura.md        ← Extensión: energía oscura DBI
│   ├── acoplamiento_masa_inercia_centrifuga.md ← Extensión: retroaliment masa-vacío
│   ├── calculo_radio_tamano_universo.md        ← Apoyo: cálculo observacional R₀
│   │
│   │  ── INFORMES TEMÁTICOS ──
│   ├── informe_precesion_perihelio.md
│   ├── informe_materia_oscura_elastica.md
│   ├── plan_simulacion_elastica.md
│   │
│   │  ── SUBDIRECTORIO TÉCNICO ──
│   └── simulacion_256cubed/
│       └── README_256cubed.md              ← Único archivo real
│
├── notebooks/                             # Código Python activo (SIN RENOMBRAR)
│   ├── AGENTS.md                          # CREAR — inventario real de scripts
│   │
│   │  ── Motores físicos ──
│   ├── simulacion_membrana_elastica.py
│   ├── simulacion_orbita_precesion.py
│   ├── simulacion_desvio_luz_coriolis.py
│   ├── simulacion_evolucion_temporal_geff.py
│   ├── analisis_materia_oscura.py
│   ├── comparacion_curvas_expansion.py
│   │
│   │  ── Cálculos teóricos ──
│   ├── calculate_4velocity_field.py
│   ├── calculate_strain_tensor.py
│   ├── calculate_3d_projection.py
│   ├── calculate_volume_average.py
│   ├── solve_linearized_equations.py
│   ├── demo_basic_calculation.py
│   ├── verify_hubble_relation.py
│   │
│   │  ── Setup / Instalación ──
│   ├── setup_numerical_simulation.py
│   ├── setup_local_gravity_sources.py
│   ├── setup_256cubed_optimized_simulation.py
│   ├── install_simulation_deps.py
│   │
│   │  ── Análisis / Monitoreo ──
│   ├── analyze_256cubed_results.py
│   ├── analyze_local_gravity_results.py
│   ├── monitor_local_gravity_simulation.py
│   ├── check_simulation_status.py
│   ├── optimize_simulation_params.py
│   ├── test_performance.py
│   │
│   │  ── Pipelines / Runners ──
│   ├── run_local_gravity_simulation.py
│   ├── run_numerical_simulation.py
│   └── run_256cubed_chunked_evolution.py
│
├── results/                               # Todos los resultados de simulaciones
│   ├── membrana_elastica/{32,64,128,256}cubed/
│   ├── curvas_expansion/
│   ├── estabilidad_gravedad/
│   ├── desvio_luz_coriolis/
│   ├── materia_oscura_elastica/
│   ├── orbita_precesion/
│   ├── local_gravity_32cubed/
│   ├── simulation_256cubed/               ← MOVER desde output/simulation_256cubed/
│   │   ├── results/
│   │   ├── checkpoints/
│   │   ├── data/
│   │   └── visualizations/
│   └── reports/                           ← CONSOLIDAR reportes científicos
│       ├── scientific_analysis_report_32cubed.txt
│       └── scientific_analysis_report_256cubed.txt
│
├── data/                                  ← NUEVO: datos de entrada y configuración
│   ├── configs/                           ← MOVER JSONs de raíz
│   │   ├── simulation_256cubed_config.json
│   │   ├── optimal_simulation_config.json
│   │   ├── config_64cubed.json
│   │   ├── manual_64cubed_config.json
│   │   ├── parallelization_config_optimized.json
│   │   └── parallel_optimization_config.json
│   ├── observational/                     ← MOVER datos descargados
│   │   ├── SPARC_Lelli2016c.mrt.txt
│   │   ├── Rotmod_LTG.zip
│   │   └── Rotmod_LTG/                   ← 175 archivos .dat
│   └── initial_conditions/                ← MOVER .npz de raíz
│       ├── simulation_initial_data.npz
│       └── simulation_results_gpu.npz
│
├── checkpoints/                           # Ya existe, mantener
│   ├── checkpoint_frequent_step_*.chk
│   ├── checkpoint_periodic_step_*.chk
│   ├── checkpoint_metadata.json
│   ├── checkpoint_step_000000.npz         ← MOVER desde raíz
│   ├── checkpoint_step_000010.npz         ← MOVER desde raíz
│   └── checkpoint_step_000020.npz         ← MOVER desde raíz
│
├── simulation_256cubed_data/              # Legacy bulk data (1.7GB) — ARCHIVAR
│                                            Eventualmente mover a archive/ si no se usa
│
├── scientific_publication/                # Manuscrito formal
│   ├── AGENTS.md                          # ACTUALIZAR — reflejar estructura real
│   ├── README.md                          # ACTUALIZAR — eliminar refs a docs inexistentes
│   ├── 01_theoretical_foundations/core_hypothesis.md
│   ├── 02_mathematical_development/4d_rotation_dynamics.md
│   ├── 04_observational_predictions/cosmological_parameters.md
│   └── 05_experimental_verification/{desi,falsifiability}.md
│
├── publication_strategy/                  # Estrategia editorial
│   ├── AGENTS.md                          # ACTUALIZAR — marcar stubs como TODO
│   └── target_analysis/journal_selection_analysis.md
│
├── downloads/                             # Descargas originales (mantener)
│   ├── Modelos teóricos de un universo rotante.pdf
│   ├── Rotmod_LTG.zip                     ← Copia, puede eliminarse si data/observational/ tiene la misma
│   ├── Rotmod_LTG/                        ← Puede eliminarse si se mueve a data/observational/
│   └── SPARC_Lelli2016c.mrt.txt           ← Puede eliminarse si se mueve a data/observational/
│
├── archive/                               ← NUEVO: material histórico/obsoleto
│   ├── bssn_paradigm/                     # Documentación del paradigma BSSN abandonado
│   │   ├── plan_verificacion_algoritmo_completo.md
│   │   ├── RESUMEN_EJECUTIVO_256CUBED.md
│   │   ├── README_SIMULATION.md
│   │   └── plan_reorganizacion_cientifica_completo.md
│   ├── audits/                            # Informes de auditoría completados
│   │   └── informe_resolucion_auditoria.md
│   ├── plans_legacy/                      # Planes generales viejos
│   │   └── plan_verificacion_completa.md  # Existe duplicado en publication_strategy/
│   ├── scripts_legacy/                    # Scripts duplicados/obsoletos de raíz
│   │   ├── run_256cubed_complete_pipeline.py.original
│   │   ├── [scripts de raíz que ya tienen versión canónica en notebooks/]
│   │   ├── *.backup files
│   │   └── fix_parallelization_*.py       # Fixes de paralelización ya resueltos
│   └── empty_containers_snapshot/         # Snapshot de qué existía antes de eliminar
│       ├── computational_implementation/  # (solo AGENTS.md fantasma)
│       ├── experimental_validation/       # (solo AGENTS.md fantasma + carpetas vacías)
│       ├── ideas_descabelladas/           # (solo AGENTS.md fantasma)
│       ├── test_validation_figures/       # (vacío)
│       └── validation_figures/            # (vacío)
│
├── Entry Points de Raíz (MANTENER):      # Scripts ejecutables principales
│   ├── run_complete_simulation.py
│   ├── run_complete_local_gravity_pipeline.py
│   ├── run_256cubed_complete_pipeline.py
│   ├── run_256cubed_optimized.py
│   ├── run_256cubed_optimized_parallel.py
│   ├── run_optimized_simulation.py
│   ├── setup_256cubed_optimized_parallel.py
│   ├── setup_64cubed_simulation.py
│   ├── create_manual_64cubed_simulation.py
│   ├── analyze_simulation_results.py
│   ├── comparacion_algoritmos.py
│   ├── diagnostico_velocidad_simulacion.py
│   ├── estimate_simulation_scaling.py
│   ├── explain_physical_parameters.py
│   ├── monitor_checkpoints.py
│   └── test_parallelization.py
│
├── .github/                               # Config GitHub (mantener)
├── .vscode/                               # Config VS Code (mantener)
├── .roo/                                  # Config Roo (mantener)
├── .omo/                                  # Config OpenCode (mantener)
└── .gitignore                             # ACTUALIZAR
```

---

## Fases de Ejecución

### FASE 1: Eliminación de Basura Inmediata
**Riesgo**: Nulo | **Tiempo estimado**: 5 min | **Dependencias**: Ninguna

| Acción | Archivos |
|--------|----------|
| Eliminar artefactos pip | `=0.56.0`, `=1.21.0`, `=1.7.0`, `=3.5.0` |
| Eliminar backups sin valor | `notebooks/run_256cubed_chunked_evolution.py.backup`<br>`notebooks/run_256cubed_chunked_evolution.py.original`<br>`notebooks/setup_256cubed_optimized_simulation.py.backup`<br>`notebooks/setup_256cubed_optimized_simulation.py.original`<br>`run_256cubed_complete_pipeline.py.original` |
| Limpiar __pycache__ | `computational_implementation/simulations/__pycache__/`<br>`notebooks/__pycache__/` |

**Criterio de éxito**: `ls` de raíz no muestra archivos `=X.Y.Z` ni `.backup`/`.original`.

---

### FASE 2: Archivado de Línea BSSN Obsoleta
**Riesgo**: Bajo | **Tiempo estimado**: 10 min | **Dependencias**: Fase 1

Crear `archive/bssn_paradigm/` y mover:

| Archivo origen | Motivo |
|---|---|
| `plan_verificacion_algoritmo_completo.md` | Describe simulación BSSN 256³ abandonada |
| `RESUMEN_EJECUTIVO_256CUBED.md` | Arquitectura BSSN con chunks/memory mapping (obsoleto) |
| `README_SIMULATION.md` | Sistema BSSN completo (reemplazado por FFT) |
| `plan_reorganizacion_cientifica_completo.md` | Plan de junio 2025 parcialmente ejecutado, histórico |

Agregar `archive/bssn_paradigm/README.md` explicando:
> Estos documentos pertenecen al paradigma BSSN (Baumgarte-Shapiro-Shibata-Nakamura) que fue el enfoque inicial de simulación numérica del proyecto. En junio 2026, se abandonó este enfoque en favor del solver espectral FFT de membrana elástica. Se conservan como registro histórico de la evolución metodológica.

**Criterio de éxito**: Los 4 archivos ya no están en la raíz. `archive/bssn_paradigm/` existe con README explicativo.

---

### FASE 3: Archivado de Material Complementario Obsoleto
**Riesgo**: Bajo | **Tiempo estimado**: 10 min | **Dependencias**: Fase 2

#### 3a. Auditoría y planes legacy → `archive/audits/` y `archive/plans_legacy/`

| Archivo origen | Destino | Motivo |
|---|---|---|
| `docs/informe_resolucion_auditoria.md` | `archive/audits/` | Doc meta completado, no alimenta investigación activa |
| `plan_verificacion_completa.md` (raíz) | `archive/plans_legacy/` | Plan general viejo. Existe duplicado en `publication_strategy/submission_strategy/` |

#### 3b. Scripts legacy de raíz → `archive/scripts_legacy/`

Evaluar cada script de raíz contra su contraparte en `notebooks/`:

| Script raíz | ¿Tiene equivalente en notebooks/? | Acción |
|---|---|---|
| `fix_parallelization_bottlenecks.py` | No directamente | Archivar (fix ya aplicado) |
| `fix_parallelization_improved.py` | No directamente | Archivar (fix ya aplicado) |

Los demás scripts de raíz son entry points legítimos o herramientas únicas — se mantienen.

#### 3c. Bulk data legacy → evaluar

| Directorio | Tamaño | Decisión |
|---|---|---|
| `simulation_256cubed_data/` | ~1.7 GB | Mover a `archive/legacy_data/` si no se referencia desde código activo. Si algún script lo lee, documentar la dependencia. |

**Criterio de éxito**: `archive/` contiene subcarpetas `audits/`, `plans_legacy/`, `scripts_legacy/` con contenido organizado.

---

### FASE 4: Limpieza de Carpetas Muertas
**Riesgo**: Medio | **Tiempo estimado**: 10 min | **Dependencias**: Fase 3

Antes de eliminar, guardar snapshot de AGENTS.md de cada carpeta muerta en `archive/empty_containers_snapshot/`:

| Carpeta a eliminar | Contenido actual | Acción |
|---|---|---|
| `computational_implementation/` | AGENTS.md fantasma + __pycache__ | Guardar AGENTS.md → eliminar carpeta |
| `experimental_validation/` | AGENTS.md fantasma + subcarpetas vacías | Guardar AGENTS.md → eliminar carpeta |
| `ideas_descabelladas/` | AGENTS.md fantasma | Guardar AGENTS.md → eliminar carpeta |
| `test_validation_figures/` | Vacío | Eliminar directamente |
| `validation_figures/` | Vacío | Eliminar directamente |
| `scientific_publication/appendices/` | Vacío | Eliminar directamente |
| `output/` | Solo `simulation_256cubed/` | Mover contenido a `results/simulation_256cubed/` → eliminar carpeta |

**Criterio de éxito**: Las 7 carpetas ya no existen. Sus AGENTS.md están preservados en `archive/empty_containers_snapshot/`.

---

### FASE 5: Consolidación de Datos y Configuración
**Riesgo**: Bajo | **Tiempo estimado**: 15 min | **Dependencias**: Fase 4

#### 5a. Crear `data/` con subcarpetas

```bash
mkdir -p data/configs data/observational data/initial_conditions
```

#### 5b. Mover configs JSON de raíz → `data/configs/`

| Archivo | Nota |
|---|---|
| `config_64cubed.json` | |
| `manual_64cubed_config.json` | |
| `optimal_simulation_config.json` | |
| `parallelization_config_optimized.json` | |
| `parallel_optimization_config.json` | |
| `simulation_256cubed_config.json` | |

**IMPORTANTE**: Verificar si algún script de raíz o notebooks/ referencia estos paths. Si sí, actualizar las referencias o crear symlinks.

#### 5c. Mover datos observacionales de `downloads/` → `data/observational/`

| Archivo | Nota |
|---|---|
| `downloads/SPARC_Lelli2016c.mrt.txt` | Mover |
| `downloads/Rotmod_LTG/` | Mover (175 archivos .dat) |
| `downloads/Rotmod_LTG.zip` | Mover (compreso original) |

Mantener `downloads/Modelos teóricos de un universo rotante.pdf` en `downloads/` (es un paper de referencia, no dato).

#### 5d. Mover datos binarios sueltos de raíz

| Archivo | Destino |
|---|---|
| `simulation_initial_data.npz` | `data/initial_conditions/` |
| `simulation_results_gpu.npz` | `data/initial_conditions/` |
| `hubble_analysis_simulation_results_gpu.png` | `results/` |
| `checkpoint_step_000000.npz` | `checkpoints/` |
| `checkpoint_step_000010.npz` | `checkpoints/` |
| `checkpoint_step_000020.npz` | `checkpoints/` |

#### 5e. Consolidar outputs en `results/`

| Origen | Destino |
|---|---|
| `output/simulation_256cubed/` | `results/simulation_256cubed/` |
| `results/local_gravity_32cubed/scientific_analysis_report_32cubed.txt` | `results/reports/` |
| `output/simulation_256cubed/results/scientific_analysis_report_256cubed.txt` | `results/reports/` |

Eliminar carpeta `output/` vacía después.

**Criterio de éxito**: Raíz no tiene archivos .json, .npz, .png sueltos. Todo dato vive en `data/`, `results/` o `checkpoints/`.

---

### FASE 6: Actualización de AGENTS.md
**Riesgo**: Medio (documentación crítica) | **Tiempo estimado**: 30 min | **Dependencias**: Fases 1-5

Este es el paso más importante para consistencia. Cada AGENTS.md debe reflejar la realidad post-reorganización.

#### 6a. `docs/AGENTS.md` — Actualizar sección STRUCTURE

Cambios requeridos:
- Agregar sección "DOCUMENTACIÓN DE APOYO" con los 3 ex-huérfanos:
  - `formalismo_dbi_energia_oscura.md` — Extensión DBI para energía oscura
  - `acoplamiento_masa_inercia_centrifuga.md` — Retroalimentación masa-vacío
  - `calculo_radio_tamano_universo.md` — Cálculo observacional de R₀
- Corregir `simulacion_256cubed/`: solo lista `README_256cubed.md` (eliminar SPECS, TROUBLESHOOTING)
- Agregar nota sobre `informe_resolucion_auditoria.md` movido a `archive/audits/`

#### 6b. `scientific_publication/AGENTS.md` — Reflejar estructura real

La estructura real es:
```
scientific_publication/
├── AGENTS.md
├── README.md
├── 01_theoretical_foundations/core_hypothesis.md
├── 02_mathematical_development/4d_rotation_dynamics.md
├── 04_observational_predictions/cosmological_parameters.md
└── 05_experimental_verification/{desi_2024_validation.md, falsifiability_criteria.md}
```

Eliminar todas las referencias a archivos/carpetas inexistentes:
- Sección 03 (nunca creada)
- Sección 06 (nunca creada)
- appendices/ (eliminada)
- Archivos adicionales mencionados en cada sección que no existen

Marcar estado real:
| Sección | Estado real |
|---|---|
| 01_theoretical_foundations | 1 archivo (core_hypothesis.md) |
| 02_mathematical_development | 1 archivo (4d_rotation_dynamics.md) |
| 03_numerical_validation | NO EXISTE |
| 04_observational_predictions | 1 archivo (cosmological_parameters.md) |
| 05_experimental_verification | 2 archivos ✅ |
| 06_implications_and_conclusions | NO EXISTE |
| appendices | ELIMINADO |

#### 6c. `scientific_publication/README.md` — Eliminar referencias fantasma

Eliminar o marcar como "[NO EXISTE]" las referencias a:
- `../docs/conjetura_refundada.md`
- `../docs/desarrollo_matematico_detallado_v2.md`
- `../docs/predicciones_observacionales_4d.md`
- Todos los archivos listados en secciones que no existen

#### 6d. `publication_strategy/AGENTS.md` — Marcar stubs

Indicar claramente que la mayoría de los archivos son placeholders TODO:
```
## ESTADO REAL
Solo `target_analysis/journal_selection_analysis.md` (19KB) tiene contenido desarrollado.
Los restantes 15 archivos son stubs pendientes de completar.
```

#### 6e. `notebooks/AGENTS.md` — CREAR (nuevo)

Crear un AGENTS.md que documente la realidad:
```markdown
# NOTEBOOKS

**Dominio**: Scripts Python de simulación, cálculo teórico y análisis.

## NOTA
A pesar del nombre, este directorio contiene scripts Python (.py), no Jupyter Notebooks.
Se ejecutan con `python script.py`.

## STRUCTURE
[Lista real de los ~24 archivos .py con descripción de una línea]
```

#### 6f. Eliminar AGENTS.md de carpetas que fueron eliminadas

Ya no existirán:
- `computational_implementation/AGENTS.md` (guardado en archive)
- `experimental_validation/AGENTS.md` (guardado en archive)
- `ideas_descabelladas/AGENTS.md` (guardado en archive)

**Criterio de éxito**: Cada AGENTS.md existente describe exactamente los archivos que hay en su directorio. Ningún archivo listado es inexistente.

---

### FASE 7: Integración de Documentación de Apoyo
**Riesgo**: Nulo (solo agregar texto) | **Tiempo estimado**: 20 min | **Dependencias**: Fase 6a

Los 3 docs ex-huérfanos se quedan en `docs/` pero necesitan conexión con la red documental.

#### 7a. Agregar referencias cruzadas DESDE los docs principales HACIA los docs de apoyo

| Doc de apoyo | Referenciar desde | Tipo de referencia |
|---|---|---|
| `formalismo_dbi_energia_oscura.md` | `02_propuesta_investigacion.md` §3 (predicciones energía oscura)<br>`comparacion_curvas_expansion.md` (extensión DBI de Friedmann emergente) | Nota al pie o sección "Ver también" |
| `acoplamiento_masa_inercia_centrifuga.md` | `conservacion_momento_inercia_geff.md` (extensión dinámica del momento angular)<br>`01_marco_teorico.md` (contribución del vacío a la masa inercial) | Nota al pie o sección "Extensión" |
| `calculo_radio_tamano_universo.md` | `01_marco_teorico.md` §2 (radio de la 3-esfera)<br>`comparacion_curvas_expansion.md` (valores numéricos de R₀) | Referencia contextual |

#### 7b. Agregar referencias cruzadas DESDE los docs de apoyo HACIA el hub

Cada doc de apoyo debe linkear a `conservacion_momento_inercia_geff.md` donde sea relevante (ya lo hacen algunos, verificar todos).

#### 7c. Actualizar `docs/AGENTS.md` WHERE TO LOOK

Agregar fila por cada doc de apoyo en la tabla de búsqueda:

| Tema | Archivo | Tipo |
|------|---------|------|
| **Energía oscura DBI** | `formalismo_dbi_energia_oscura.md` | Extensión teórica |
| **Acoplamiento masa-vacío** | `acoplamiento_masa_inercia_centrifuga.md` | Extensión teórica |
| **Radio del universo** | `calculo_radio_tamano_universo.md` | Cálculo observacional |

**Criterio de éxito**: Cada doc de apoyo tiene al menos 2 links entrantes desde docs principales y al menos 1 link saliente hacia el hub o docs relacionados.

---

### FASE 8: Actualización de README.md Principal
**Riesgo**: Nulo | **Tiempo estimado**: 15 min | **Dependencias**: Fases 1-7

El `README.md` de raíz necesita:

1. **Actualizar estructura del proyecto** (sección "Estructura del Proyecto"):
   - Reflejar carpetas nuevas (`data/`, `archive/`)
   - Eliminar carpetas muertas (`computational_implementation/`, `experimental_validation/`)
   - Actualizar conteo de archivos

2. **Actualizar paths de scripts**: Si se movieron configs a `data/configs/`, actualizar ejemplos de uso.

3. **Actualizar tabla de documentación**:
   - Agregar sección "Documentación de Apoyo" con los 3 docs nuevos
   - Actualizar enlace a `informe_resolucion_auditoria.md` → `archive/audits/`

4. **Actualizar "Estado Actual"**:
   - Mencionar que el cambio BSSN→FFT está completado
   - Actualizar próximos hitos si corresponde

5. **Eliminar referencias a paradigmas muertos**:
   - Cualquier mención a BSSN como sistema activo
   - Referencias a archivos que ya no existen

**Criterio de éxito**: Un lector nuevo puede navegar el proyecto usando solo el README sin encontrar paths rotos.

---

### FASE 9: Actualización de .gitignore
**Riesgo**: Nulo | **Tiempo estimado**: 5 min | **Dependencias**: Fase 5

Agregar patrones para evitar que vuelva la basura:

```gitignore
# Artefactos pip
=*.*/

# Backups de editores
*.backup
*.original
*.bak

# Python cache
__pycache__/
*.pyc

# Datos de simulación grandes (>100MB)
*.npz
!data/**/*.npz
!checkpoints/**/*.npz

# Visualizaciones generadas
*.png
!docs/**/*.png
```

**Criterio de éxito**: `git status` no muestra archivos basura tras regenerar __pycache__ o ejecutar scripts.

---

### FASE 10: Verificación Final de Consistencia
**Riesgo**: Nulo | **Tiempo estimado**: 20 min | **Dependencias**: Fases 1-9

Checklist de verificación:

- [ ] `ls` de raíz: solo entry points .py, READMEs, requirements.txt, carpetas de primer nivel
- [ ] No existen archivos `=X.Y.Z`, `.backup`, `.original` en todo el proyecto
- [ ] Cada AGENTS.md existente describe exactamente su directorio (verificar uno por uno)
- [ ] No hay referencias a archivos inexistentes en ningún .md (grep de paths mencionados vs filesystem)
- [ ] `docs/AGENTS.md` incluye los 3 docs de apoyo con descripción y ubicación
- [ ] Los 3 docs de apoyo tienen ≥2 links entrantes desde docs principales
- [ ] `scientific_publication/README.md` no menciona archivos inexistentes
- [ ] Todos los .json de config están en `data/configs/`
- [ ] Todos los .npz de datos están en `data/` o `checkpoints/`
- [ ] `results/reports/` tiene los 2 reportes científicos
- [ ] `archive/bssn_paradigm/` tiene README explicativo
- [ ] No existen carpetas: `computational_implementation/`, `experimental_validation/`, `ideas_descabelladas/`, `test_validation_figures/`, `validation_figures/`, `output/`
- [ ] `README.md` principal refleja la estructura actual
- [ ] `.gitignore` previene regeneración de basura
- [ ] `git diff --stat` muestra solo movimientos y ediciones, nada roto

---

## Resumen de Movimientos

| Categoría | Cantidad de archivos | Acción |
|---|:-:|---|
| Eliminar (basura) | 9 | `rm` directo |
| Mover a `archive/` | ~8 | `mv` + crear README |
| Mover a `data/` | ~12 | `mv` a subcarpetas |
| Mover a `results/` | ~5 | `mv` + consolidar |
| Mover a `checkpoints/` | 3 | `mv` |
| Eliminar carpetas muertas | 7 | Guardar AGENTS.md → `rm -r` |
| Crear nuevos | ~5 | AGENTS.md, READMEs, carpetas |
| Editar docs existentes | ~10 | AGENTS.md, READMEs, links cruzados |

**Total aproximado**: ~60 acciones Individuales, agrupadas en 10 fases secuenciales.

---

## Orden de Ejecución Recomendado

```
FASE 1 (5 min)   → Basura inmediata
     ↓
FASE 2 (10 min)  → Archivar BSSN
     ↓
FASE 3 (10 min)  → Archivar complementario
     ↓
FASE 4 (10 min)  → Eliminar carpetas muertas
     ↓
FASE 5 (15 min)  → Consolidar datos
     ↓
FASE 6 (30 min)  → Actualizar AGENTS.md [CRÍTICO]
     ↓
FASE 7 (20 min)  → Integrar docs de apoyo
     ↓
FASE 8 (15 min)  → Actualizar README principal
     ↓
FASE 9 (5 min)   → Actualizar .gitignore
     ↓
FASE 10 (20 min) → Verificación final
```

**Tiempo total estimado**: ~2.5 horas de trabajo concentrado.

---

## Decisiones Pendientes de Fede

Antes de ejecutar, confirmar:

1. **¿`simulation_256cubed_data/` (1.7GB) va a `archive/` o se elimina?**
   - Si algún script activo lo lee, no se puede archivar sin actualizar el path.
   - Verificar con grep si algún .py referencia esa ruta.

2. **¿Los entry points de raíz se mantienen donde están o se mueven a una carpeta `runners/`?**
   - Opción A (conservadora): Mantener en raíz. Son la "interfaz" del proyecto.
   - Opción B (limpia): Mover a `runners/` o `scripts/`. Requiere actualizar paths en docs.

3. **¿`downloads/` se fusiona con `data/observational/` o se mantienen separados?**
   - El PDF "Modelos teóricos..." es un paper de referencia, no un dato observacional.
   - Propuesta: mover datos a `data/observational/`, mantener PDF en `downloads/` o mover a `references/`.

4. **¿`publication_strategy/` se limpia de stubs o se mantienen como TODOs?**
   - Opción A: Eliminar los 15 stubs vacíos, dejar solo `journal_selection_analysis.md`.
   - Opción B: Mantenerlos como marcadores de posición con contenido TODO explícito.

5. **¿Las secciones faltantes de `scientific_publication/` (03, 06, appendices) se crean como placeholders oficiales o se eliminan del esquema?**
   - Si hay plan de completarlas: crear carpetas con README placeholder.
   - Si no hay plan: eliminar del AGENTS.md y README para que la estructura documentada sea real.
