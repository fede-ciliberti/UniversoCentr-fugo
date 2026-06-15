# EXPERIMENTAL VALIDATION

**Dominio**: Verificación empírica de predicciones teóricas del Universo Centrífugo.

## OVERVIEW

Validación experimental de la teoría: verificación de Ley de Hubble desde simulaciones, análisis de convergencia numérica O(Δx⁴), y archivo de resultados reproducibles.

## STRUCTURE

```
experimental_validation/
├── hubble_verification/
│   ├── verify_hubble_law_final.py      # Verificación principal (509 líneas)
│   ├── verify_hubble_law.py            # Versión anterior (173 líneas) - NO USAR
│   └── run_hubble_verification_batch.py # Batch runs (73 líneas)
├── convergence_analysis/                # Convergencia numérica
└── results_archive/
    ├── analysis_results/                # Resultados procesados
    └── simulation_outputs/              # Output crudo de simulaciones
```

## WHERE TO LOOK

| Tarea | Archivo | Notas |
|-------|---------|-------|
| Verificar Ley de Hubble | `hubble_verification/verify_hubble_law_final.py` | **USAR SIEMPRE esta versión** |
| Batch verification | `hubble_verification/run_hubble_verification_batch.py` | Múltiples corridas |
| Convergencia | `convergence_analysis/` | Análisis O(Δx⁴) |
| Resultados | `results_archive/` | Datos históricos |

## CONVENTIONS

- **Versión _final**: Siempre usar `verify_hubble_law_final.py`, nunca `verify_hubble_law.py`.
- **Dependencia de datos**: Requiere `.npz` en root del proyecto (`simulation_results.npz`).
- **Múltiples formatos .npz**: El script maneja `metric_invariants` y `metric_evolution`.
- **Sin pytest**: Scripts standalone, ejecutar con `python`.

## ANTI-PATTERNS

- **NO usar `verify_hubble_law.py`**: Versión obsoleta, usar `_final`.
- **NO ejecutar sin datos**: Scripts esperan `.npz` generados por simulaciones previas.
- **NO asumir formato único**: `.npz` pueden tener estructuras internas distintas.
- **NO commitear resultados**: `results_archive/` contiene datos de simulación grandes.

## COMMANDS

```bash
# Verificación principal
python experimental_validation/hubble_verification/verify_hubble_law_final.py

# Batch de verificaciones
python experimental_validation/hubble_verification/run_hubble_verification_batch.py
```

## DEPENDENCIAS

1. Correr simulación primero: `run_complete_simulation.py` o `run_simulation_windows_gpu.py`
2. Verificar que `simulation_results.npz` existe en root
3. Ejecutar script de verificación
