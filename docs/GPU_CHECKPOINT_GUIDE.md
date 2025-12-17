# Guía Completa: Sistema de Checkpoints y Aceleración GPU

## Tabla de Contenido

1. [Sistema de Checkpoints Robusto](#sistema-de-checkpoints-robusto)
2. [Aceleración GPU Multiplataforma](#aceleración-gpu-multiplataforma)
3. [Instalación en Windows](#instalación-en-windows)
4. [Configuración y Uso](#configuración-y-uso)
5. [Optimización de Rendimiento](#optimización-de-rendimiento)
6. [Benchmarking y Comparación](#benchmarking-y-comparación)
7. [Solución de Problemas](#solución-de-problemas)

---

## Sistema de Checkpoints Robusto

### Características Principales

El sistema de checkpoints implementado proporciona:

- **Guardado automático** cada N pasos o intervalos de tiempo
- **Recuperación inteligente** que detecta checkpoints existentes
- **Validación de integridad** mediante checksums SHA-256
- **Múltiples niveles** de checkpoints (frecuentes + periódicos)
- **Compresión** para optimizar espacio de almacenamiento
- **Metadatos completos** con información de estado y parámetros

### Arquitectura del Sistema

```
checkpoints/
├── checkpoint_metadata.json          # Metadatos de todos los checkpoints
├── checkpoint_frequent_step_00100_*.chk  # Checkpoints frecuentes
├── checkpoint_periodic_step_01000_*.chk  # Checkpoints periódicos
└── ...
```

### Configuración de Checkpoints

```python
checkpoint_config = {
    'checkpoint_dir': 'checkpoints',      # Directorio de almacenamiento
    'frequent_interval': 100,            # Cada 100 pasos
    'periodic_interval': 1000,           # Cada 1000 pasos
    'max_checkpoints': 10,                # Máximo a mantener
    'compression_level': 6                 # Nivel de compresión (1-9)
}
```

### Uso Programático

```python
from checkpoint_manager import CheckpointManager

# Inicializar gestor
checkpoint_manager = CheckpointManager(**checkpoint_config)

# Guardar checkpoint
state = simulator.get_simulation_state()
params = simulator.get_simulation_params()
checkpoint_file = checkpoint_manager.save_checkpoint(
    step=1000, 
    t=0.5, 
    simulation_state=state,
    simulation_params=params
)

# Cargar checkpoint
state, params = checkpoint_manager.load_checkpoint(
    checkpoint_file="auto"  # Carga el más reciente automáticamente
)

# Validar integridad
is_valid = checkpoint_manager.validate_checkpoint(checkpoint_file)
```

### Recuperación Automática

El simulador puede reanudar automáticamente desde el checkpoint más reciente:

```python
simulator.run_simulation(
    save_checkpoints=True,
    verbose=True,
    resume_from_checkpoint="auto"  # Detección automática
)
```

### Metadatos de Checkpoints

Cada checkpoint incluye:

- **Información temporal**: paso, tiempo de simulación, timestamp
- **Estado completo**: todas las variables BSSN
- **Parámetros**: configuración de la simulación
- **Checksum**: validación de integridad SHA-256
- **Estadísticas**: tamaño comprimido, tipo de checkpoint

---

## Aceleración GPU Multiplataforma

### Arquitectura GPU

El sistema soporta múltiples backends GPU:

1. **CuPy (NVIDIA CUDA)** - Recomendado para GPUs NVIDIA
2. **PyOpenCL** - Soporte genérico para AMD/Intel/NVIDIA
3. **CPU Fallback** - Ejecución en CPU multi-core si GPU no disponible

### Detección Automática

```python
from run_simulation_windows_gpu import GPUAccelerator

accelerator = GPUAccelerator()

if accelerator.gpu_available:
    print(f"GPU detectada: {accelerator.gpu_type}")
    print(f"Memoria: {accelerator.gpu_memory:.1f} GB")
    
    # Obtener módulo de arrays apropiado
    xp = accelerator.get_array_module()  # numpy o cupy
    
    # Transferir datos a GPU
    gpu_array = accelerator.to_gpu(cpu_array)
    
    # Transferir de vuelta a CPU
    cpu_array = accelerator.to_cpu(gpu_array)
```

### Optimizaciones GPU Implementadas

- **Transferencias eficientes** CPU-GPU
- **Kernel optimization** para cálculos BSSN
- **Memory management** para grandes volúmenes
- **Sincronización automática** de operaciones

### Configuración GPU

```python
simulator = EinsteinSimulatorGPU(
    data_file="simulation_initial_data.npz",
    max_cores=None,        # Usar todos los cores CPU
    use_gpu=True,          # Activar aceleración GPU
    checkpoint_config=checkpoint_config
)
```

---

## Instalación en Windows

### Requisitos del Sistema

- **Windows 10/11** (64 bits recomendado)
- **Python 3.8+** con pip
- **GPU NVIDIA** con CUDA Toolkit 11.x/12.x (opcional)
- **8 GB RAM** mínimo (16 GB recomendado)
- **2 GB espacio** en disco

### Instalación Automática

```bash
# Ejecutar instalador Windows
python computational_implementation/simulations/install_windows_gpu.py
```

El instalador realiza:

1. ✅ Verificación de requisitos del sistema
2. ✅ Instalación de dependencias básicas
3. ✅ Detección e instalación de soporte GPU
4. ✅ Creación de archivos de configuración
5. ✅ Generación de ejecutable portable (opcional)

### Instalación Manual

#### Paso 1: Instalar Python
Descargar desde https://python.org y marcar "Add Python to PATH"

#### Paso 2: Instalar dependencias básicas
```bash
pip install numpy scipy matplotlib numba tqdm h5py psutil
```

#### Paso 3: Instalar soporte GPU

**Para NVIDIA CUDA:**
```bash
# Instalar CUDA Toolkit desde https://developer.nvidia.com/cuda-downloads
pip install cupy-cuda11x  # o cupy-cuda12x
```

**Para otras GPUs:**
```bash
pip install pyopencl
```

#### Paso 4: Verificar instalación
```bash
python -c "import cupy; print('CuPy disponible')"  # NVIDIA
python -c "import pyopencl; print('PyOpenCL disponible')"  # Genérico
```

### Ejecutable Portable

El instalador puede crear un ejecutable standalone:

```bash
EinsteinSimulatorGPU.exe  # No requiere instalación de Python
```

---

## Configuración y Uso

### Configuración Básica

```python
# Archivo: config.json
{
    "simulation": {
        "dt": 0.001,
        "t_final": 1.0,
        "grid_size": [32, 32, 32]
    },
    "checkpoints": {
        "frequent_interval": 100,
        "periodic_interval": 1000,
        "max_checkpoints": 10,
        "compression_level": 6
    },
    "gpu": {
        "use_gpu": true,
        "memory_fraction": 0.8
    }
}
```

### Ejecución desde Línea de Comandos

```bash
# Simulación básica
python run_simulation_windows_gpu.py

# Reanudar desde checkpoint
python run_simulation_windows_gpu.py --resume auto

# Usar configuración específica
python run_simulation_windows_gpu.py --config config.json

# Forzar modo CPU
python run_simulation_windows_gpu.py --cpu-only
```

### Script por Lotes (Windows)

```batch
@echo off
echo Einstein Simulator GPU
echo.

REM Verificar datos iniciales
if not exist "simulation_initial_data.npz" (
    echo Error: No se encontraron datos iniciales
    echo Ejecute: python setup_numerical_simulation.py
    pause
    exit /b 1
)

REM Iniciar simulación
python run_simulation_windows_gpu.py --resume auto

echo.
echo Simulación completada
pause
```

### Monitoreo en Tiempo Real

El simulador proporciona información en tiempo real:

```
Paso    100/1000 | t=0.1000 | Progreso: 10.0% | ETA: 5.2min
  det(γ)=1.000000 | tr(K)=0.000000
  Checkpoint guardado: checkpoint_frequent_step_000100.chk
```

---

## Optimización de Rendimiento

### Configuración de Memoria GPU

```python
# Para GPUs con memoria limitada
simulator = EinsteinSimulatorGPU(
    data_file="simulation_initial_data.npz",
    use_gpu=True,
    gpu_memory_fraction=0.7  # Usar 70% de memoria GPU
)
```

### Optimización de Malla

- **Mallas pequeñas** (16³): Pruebas rápidas, bajo uso de memoria
- **Mallas medianas** (32³): Balance rendimiento/memoria
- **Mallas grandes** (64³+): Máximo rendimiento, requiere más memoria

### Paralelización CPU

```python
# Configurar número de cores CPU
import multiprocessing

simulator = EinsteinSimulatorGPU(
    data_file="simulation_initial_data.npz",
    max_cores=multiprocessing.cpu_count() - 1,  # Dejar un core libre
    use_gpu=False  # Solo CPU
)
```

### Optimización de Checkpoints

```python
# Para simulaciones largas
checkpoint_config = {
    'frequent_interval': 500,    # Menos frecuente
    'periodic_interval': 5000,    # Más espaciado
    'compression_level': 9,        # Máxima compresión
    'max_checkpoints': 5          # Menos checkpoints
}
```

---

## Benchmarking y Comparación

### Ejecutar Benchmarks

```bash
# Suite completa de benchmarks
python benchmark_gpu_cpu.py

# Resultados guardados en:
# - benchmark_results.json
# - benchmark_analysis.json
# - benchmark_plots.png
# - benchmark_report.md
```

### Métricas de Rendimiento

El benchmark mide:

- **Throughput**: puntos procesados por segundo
- **Uso de memoria**: RAM y VRAM consumida
- **Escalabilidad**: rendimiento vs número de cores
- **Speedup**: aceleración GPU vs CPU

### Resultados Esperados

| Configuración | Malla 32³ | Malla 64³ | Speedup |
|---------------|------------|------------|---------|
| CPU 1 core    | 50k pts/s  | 12k pts/s  | 1.0x    |
| CPU 4 cores   | 180k pts/s | 45k pts/s  | 3.6x    |
| CPU 8 cores   | 320k pts/s | 80k pts/s  | 6.4x    |
| GPU NVIDIA    | 2000k pts/s| 800k pts/s | 40x     |
| GPU AMD       | 500k pts/s | 200k pts/s | 10x     |

---

## Solución de Problemas

### Errores Comunes

#### 1. "CUDA out of memory"
```python
# Solución: Reducir resolución o fracción de memoria
simulator = EinsteinSimulatorGPU(
    grid_size=[16, 16, 16],  # Malla más pequeña
    gpu_memory_fraction=0.5     # Usar menos memoria
)
```

#### 2. "CuPy not found"
```bash
# Instalar CuPy apropiado
pip install cupy-cuda11x  # Para CUDA 11.x
pip install cupy-cuda12x  # Para CUDA 12.x
```

#### 3. "Checkpoint corrupted"
```python
# Validar y limpiar checkpoints
checkpoint_manager = CheckpointManager()
checkpoint_manager.cleanup_all_checkpoints()
```

#### 4. "Slow GPU performance"
```python
# Verificar sincronización
accelerator = GPUAccelerator()
accelerator.synchronize()  # Forzar sincronización
```

### Depuración

```python
# Habilitar logging detallado
import logging
logging.basicConfig(level=logging.DEBUG)

# Monitorear uso de recursos
import psutil
print(f"CPU: {psutil.cpu_percent()}%")
print(f"RAM: {psutil.virtual_memory().percent}%")
```

### Rendimiento Subóptimo

1. **Verificar drivers GPU**: Actualizar a última versión
2. **Monitorear temperatura**: Sobrecalentamiento reduce rendimiento
3. **Ajustar intervalos de checkpoints**: Demasiados frecuentes ralentizan
4. **Optimizar transferencias**: Minimizar CPU-GPU transfers

---

## Ejemplos Prácticos

### Simulación Corta (Prueba)
```python
# Configuración para prueba rápida
config = {
    'dt': 0.01,
    't_final': 0.1,
    'grid_size': [16, 16, 16]
}
checkpoint_config = {
    'frequent_interval': 10,
    'periodic_interval': 50
}
```

### Simulación Larga (Producción)
```python
# Configuración para simulación extendida
config = {
    'dt': 0.0001,
    't_final': 10.0,
    'grid_size': [64, 64, 64]
}
checkpoint_config = {
    'frequent_interval': 1000,
    'periodic_interval': 10000,
    'compression_level': 9
}
```

### Análisis de Resultados
```python
# Cargar resultados
results = np.load('simulation_results_gpu.npz')

# Analizar evolución temporal
time_evolution = results['time_evolution']
metric_evolution = results['metric_evolution']

# Visualizar métrica
import matplotlib.pyplot as plt
plt.plot(time_evolution, [m['det_gamma'] for m in metric_evolution])
plt.xlabel('Tiempo')
plt.ylabel('det(γ)')
plt.show()
```

---

## Referencias y Recursos

### Documentación Adicional
- [CuPy Documentation](https://docs.cupy.dev/)
- [PyOpenCL Documentation](https://documen.tician.de/pyopencl/)
- [Numba Documentation](https://numba.pydata.org/)

### Soporte Técnico
- **Logs**: Revisar salida de consola para errores detallados
- **Checkpoints**: Validar integridad con `checkpoint_manager.validate_checkpoint()`
- **Performance**: Usar `benchmark_gpu_cpu.py` para diagnóstico

### Actualizaciones
Mantener actualizados:
- **Drivers GPU**: Última versión estable
- **Python packages**: `pip install --upgrade numpy cupy`
- **CUDA Toolkit**: Versión compatible con CuPy