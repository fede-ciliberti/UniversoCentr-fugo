# COMPUTATIONAL IMPLEMENTATION

**Dominio**: Simulaciones numéricas BSSN, GPU acceleration, demostraciones matemáticas.

## OVERVIEW

Módulo central de implementación computacional: simulaciones BSSN con soporte GPU (CuPy/PyOpenCL), sistema de checkpoints con validación SHA-256, y pruebas matemáticas de rotación 4D isoclínica.

## STRUCTURE

```
computational_implementation/
├── simulations/                 # 10 archivos Python - Orchestrator + GPU + Windows
│   ├── run_complete_simulation.py      # Entry point principal (244 líneas)
│   ├── run_simulation_windows_gpu.py   # Simulador GPU multiplataforma (646 líneas)
│   ├── run_numerical_simulation.py     # Core numérico (576 líneas)
│   ├── benchmark_gpu_cpu.py            # Suite benchmarking (587 líneas)
│   ├── checkpoint_manager.py           # Checkpoints con SHA-256 (386 líneas)
│   ├── install_windows_gpu.py          # Instalador Windows (587 líneas)
│   ├── setup_numerical_simulation.py   # Setup inicial (198 líneas)
│   ├── optimize_simulation_params.py   # Optimización parámetros (359 líneas)
│   └── install_simulation_deps.py      # Instalador deps (318 líneas)
├── analysis_tools/
│   └── test_performance.py             # Test de performance (140 líneas)
└── theoretical_proofs/
    └── kerr_to_4d_isoclinic.py         # Demostración Kerr → 4D (173 líneas)
```

## WHERE TO LOOK

| Tarea | Archivo | Notas |
|-------|---------|-------|
| Ejecutar simulación | `simulations/run_complete_simulation.py` | Orchestrator, referencia `notebooks/` inexistente |
| Simulación GPU | `simulations/run_simulation_windows_gpu.py` | CuPy + PyOpenCL, auto-detect |
| Core numérico | `simulations/run_numerical_simulation.py` | BSSN equations, 576 líneas |
| Checkpoints | `simulations/checkpoint_manager.py` | SHA-256 validation, auto-resume |
| Benchmark | `simulations/benchmark_gpu_cpu.py` | CPU vs GPU comparativa |
| Demostración matemática | `theoretical_proofs/kerr_to_4d_isoclinic.py` | Kerr metric → 4D isoclinic |
| Test performance | `analysis_tools/test_performance.py` | No pytest, script standalone |

## CONVENTIONS

- **Sin __init__.py**: Directorios NO son paquetes. Imports por path relativo.
- **Scripts auto-ejecutables**: Cada archivo corre independientemente con `python archivo.py`.
- **Nomenclatura científica**: Variables con notación matemática en comentarios.
- **Config hardcodeada**: `optimal_simulation_config.json` y `test_32_config.json` en root del proyecto.

## ANTI-PATTERNS

- **No crear `__init__.py`**: El proyecto deliberadamente NO usa paquetes Python.
- **No asumir `notebooks/` existe**: `run_complete_simulation.py` referencia directorio inexistente.
- **No modificar configs desde código**: Los JSON de config están en root, no en este directorio.
- **No commitear .npz**: Checkpoints generados pueden pesar cientos de MB.

## COMMANDS

```bash
# Simulación completa
python computational_implementation/simulations/run_complete_simulation.py

# GPU (recomendado)
python computational_implementation/simulations/run_simulation_windows_gpu.py

# Benchmark
python computational_implementation/simulations/benchmark_gpu_cpu.py

# Test
python computational_implementation/analysis_tools/test_performance.py
```
