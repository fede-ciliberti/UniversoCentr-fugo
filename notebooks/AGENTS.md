# NOTEBOOKS

**Dominio**: Scripts Python de simulación, cálculo teórico y análisis.

## ⚠️ NOTA IMPORTANTE

A pesar del nombre, este directorio contiene **scripts Python (.py)**, no Jupyter Notebooks. Se ejecutan con `python script.py`.

El nombre "notebooks" es histórico y se mantiene por compatibilidad, pero el contenido son scripts modulares organizados por función.

## STRUCTURE

```
notebooks/
│
├── AGENTS.md                                  # Este archivo (inventario)
│
├── ── MOTORES FÍSICOS (simulaciones principales) ──
├── simulacion_membrana_elastica.py            # Motor FFT de membrana elástica 3D
├── simulacion_orbita_precesion.py             # Simulación de órbita y precesión (Mercurio)
├── simulacion_desvio_luz_coriolis.py          # Desvío de luz por Coriolis 4D (lensing)
├── simulacion_evolucion_temporal_geff.py      # Evolución temporal de G_eff
├── analisis_materia_oscura.py                 # Curvas de rotación galáctica sin materia oscura
├── comparacion_curvas_expansion.py            # Friedmann emergente vs ΛCDM
│
├── ── CÁLCULOS TEÓRICOS ──
├── calculate_4velocity_field.py               # Campo de 4-velocidad en rotación isoclínica
├── calculate_strain_tensor.py                 # Tensor de deformación de brana
├── calculate_3d_projection.py                 # Proyección 4D→3D
├── calculate_volume_average.py                # Promedio en volumen de la 3-esfera
├── solve_linearized_equations.py              # Ecuaciones de Einstein linealizadas
├── demo_basic_calculation.py                  # Demo de cálculo básico
├── verify_hubble_relation.py                  # Verificación relación de Hubble
│
├── ── SETUP / INSTALACIÓN ──
├── setup_numerical_simulation.py              # Setup parametrización numérica
├── setup_local_gravity_sources.py             # Setup fuentes de gravedad local
├── setup_256cubed_optimized_simulation.py     # Setup simulación 256³ optimizada
├── install_simulation_deps.py                 # Instalador de dependencias
│
├── ── ANÁLISIS / MONITOREO ──
├── analyze_256cubed_results.py                # Análisis resultados 256³
├── analyze_local_gravity_results.py           # Análisis gravedad local
├── monitor_local_gravity_simulation.py        # Monitor de simulación gravedad local
├── check_simulation_status.py                 # Check de status de simulación
├── optimize_simulation_params.py              # Optimización de parámetros
├── test_performance.py                        # Test de performance
│
└── ── PIPELINES / RUNNERS ──
    ├── run_local_gravity_simulation.py        # Runner gravedad local
    ├── run_numerical_simulation.py            # Motor numérico (BSSN-like)
    └── run_256cubed_chunked_evolution.py      # Evolución 256³ por chunks
```

## MOTORES PRINCIPALES

### simulacion_membrana_elastica.py (Motor FFT)

**Rol**: Resolver ecuación de Poisson elástica ∇²h - λ²h = S(r) mediante FFT espectral.

**Uso**:
```bash
python notebooks/simulacion_membrana_elastica.py
```

**Output**: Genera archivos `.npy` en `results/membrana_elastica/{32,64,128,256}cubed/`.

**Validación**: Correlación >99.8% contra perfil de Schwarzschild en 256³. Ver:
- `docs/05_informe_simulacion_numerica.md`
- `docs/12_validacion_plan_256cubed_completado.md`

### Otros motores físicos

Cada motor corresponde a un test/predicción de la teoría:

| Script | Test/Predicción | Doc asociado | Output en results/ |
|--------|----------------|--------------|-------------------|
| `simulacion_orbita_precesion.py` | Precesión perihelio Mercurio | `docs/informe_precesion_perihelio.md` | `orbita_precesion/` |
| `simulacion_desvio_luz_coriolis.py` | Lensing gravitacional | `docs/fuerza_coriolis_4d_trayectorias.md` | `desvio_luz_coriolis/` |
| `analisis_materia_oscura.py` | Curvas rotación galáctica | `docs/informe_materia_oscura_elastica.md` | `materia_oscura_elastica/` |
| `comparacion_curvas_expansion.py` | Expansión cosmológica R(t) | `docs/comparacion_curvas_expansion.md` | `curvas_expansion/` |
| `simulacion_evolucion_temporal_geff.py` | Estabilidad de G_eff | `docs/conservacion_momento_inercia_geff.md` | `estabilidad_gravedad/` |

## CÁLCULOS TEÓRICOS

Scripts de verificación analítica independiente de los resultados numéricos:

| Script | Propósito | Relación con docs/ |
|--------|-----------|-------------------|
| `calculate_4velocity_field.py` | Campo de 4-velocidad U^α en rotación isoclínica | `docs/formulacion_matematica_rotacion_4d.md` |
| `calculate_strain_tensor.py` | Tensor de deformación ε_ij de la brana | `docs/03_metodologia_gravedad_emergente.md` |
| `calculate_3d_projection.py` | Proyección 4D→3D del tensor T^μν | `docs/formulacion_matematica_rotacion_4d.md` |
| `calculate_volume_average.py` | Promedio volumétrico en la 3-esfera | `docs/calculo_radio_tamano_universo.md` |
| `solve_linearized_equations.py` | Ecuaciones de Einstein linealizadas | `docs/04_metodologia_verificacion_gravedad.md` |
| `verify_hubble_relation.py` | Verificación H₀ = f(ω₄D, R₄D) | `docs/comparacion_curvas_expansion.md` |

## SETUP Y CONFIGURACIÓN

| Script | Función | Cuándo usar |
|--------|---------|-------------|
| `setup_numerical_simulation.py` | Genera condiciones iniciales | Antes de correr simulación nueva |
| `setup_local_gravity_sources.py` | Configura fuentes de masa para gravedad local | Para simulaciones de campo débil |
| `setup_256cubed_optimized_simulation.py` | Setup específico para 256³ | Para simulaciones de alta resolución |
| `install_simulation_deps.py` | Instala dependencias Python | Primera vez o al cambiar entorno |

## ANÁLISIS Y MONITOREO

| Script | Función | Output |
|--------|---------|--------|
| `analyze_256cubed_results.py` | Análisis estadístico de resultados 256³ | Reportes en `results/reports/` |
| `analyze_local_gravity_results.py` | Análisis de perfiles radiales | Figuras en `results/local_gravity_*/` |
| `monitor_local_gravity_simulation.py` | Monitoreo en tiempo real de ejecución | Logs en stdout |
| `check_simulation_status.py` | Verifica estado de simulaciones en curso | Status report |
| `optimize_simulation_params.py` | Ajusta parámetros según hardware | Configs en `data/configs/` |
| `test_performance.py` | Benchmarks CPU/GPU | Reporte de performance |

## CONVENCIONES

- **Sin __init__.py**: Los directorios NO son paquetes Python. Imports por path relativo cuando es necesario.
- **Scripts auto-ejecutables**: Cada archivo corre independientemente con `python script.py`.
- **Nomenclatura científica**: Variables con notación matemática en comentarios (omega_4D, R_0, T_b, etc.).
- **Outputs en results/**: Todos los datos generados van a `results/`, nunca en `notebooks/`.
- **Configs en data/configs/**: Parámetros de simulación en JSON, no hardcodeados.
- **Datos iniciales en data/initial_conditions/**: Archivos .npz de entrada.

## ANTI-PATTERNS

- ❌ No crear `__init__.py` ni convertir en paquete Python.
- ❌ No generar datos en `notebooks/` (siempre en `results/`).
- ❌ No commitear `.npz` grandes (>10MB) — ya están en `.gitignore`.
- ❌ No renombrar motores principales sin actualizar referencias en `docs/`.
- ❌ No hardcodear parámetros de simulación (usar configs en `data/configs/`).
- ❌ No mezclar scripts de setup con scripts de análisis en el mismo archivo.

## RELACIÓN CON OTRAS CARPETAS

| notebooks/ | Otras carpetas | Relación |
|---|---|---|
| Motores físicos (`simulacion_*.py`) | `docs/informe_*.md` | Cada motor tiene un doc asociado que describe la física y valida resultados |
| Setup (`setup_*.py`) | `data/configs/*.json` | Lee configuraciones de `data/configs/` |
| Outputs (generados) | `results/` | Todos los .npy, .png, reportes van aquí |
| Datos iniciales | `data/initial_conditions/` | Lee .npz de entrada |
| Entry points de raíz | `notebooks/` | Scripts de raíz llaman a funciones de notebooks/ |

## ÚLTIMA ACTUALIZACIÓN

Junio 2026 — Reorganización integral. Inventario completo de scripts creado.
