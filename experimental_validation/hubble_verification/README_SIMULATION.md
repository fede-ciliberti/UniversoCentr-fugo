# 🚀 Simulación Numérica de Einstein - Universo Centrífugo

Sistema completo de simulación numérica para verificar la conjetura del Universo Centrífugo mediante la resolución de las ecuaciones de Einstein.

## 📋 Resumen del Sistema

Este sistema implementa la **Aproximación 3: Simulación Numérica** del plan de verificación, resolviendo las ecuaciones de Einstein con el tensor energía-momento derivado de la rotación 4D usando un formalismo BSSN optimizado para CPU multi-core.

### 🎯 Objetivo
Demostrar que la métrica del espacio-tiempo generada por una partícula rotando en 4D es equivalente (o aproximadamente igual) a la métrica de Schwarzschild de la Relatividad General.

## 🛠️ Componentes del Sistema

### Scripts Principales:
1. **`run_complete_simulation.py`** - Script maestro que ejecuta todo el proceso
2. **`notebooks/install_simulation_deps.py`** - Instalador de dependencias optimizado
3. **`notebooks/optimize_simulation_params.py`** - Optimizador automático según tu hardware
4. **`notebooks/setup_numerical_simulation.py`** - Generador de datos iniciales
5. **`notebooks/run_numerical_simulation.py`** - Motor de simulación principal

### Scripts de Análisis:
- **`notebooks/test_performance.py`** - Test de rendimiento del sistema
- **Análisis automático** de resultados incluido

## 🚀 Uso Rápido

### Opción 1: Ejecución Automática (Recomendado)
```bash
# Ejecutar todo el proceso automáticamente
python run_complete_simulation.py
```

### Opción 2: Ejecución Paso a Paso
```bash
# 1. Instalar dependencias
python notebooks/install_simulation_deps.py

# 2. Test de rendimiento
python notebooks/test_performance.py

# 3. Optimizar parámetros
python notebooks/optimize_simulation_params.py

# 4. Generar datos iniciales
python notebooks/setup_numerical_simulation.py

# 5. Ejecutar simulación optimizada
python run_optimized_simulation.py
```

## ⚙️ Configuración Avanzada

### Parámetros Personalizados
```bash
# Simulación con límite de tiempo
python run_complete_simulation.py --time-limit 2.0

# Omitir instalación (si ya está hecho)
python run_complete_simulation.py --skip-install

# Omitir optimización (usar valores por defecto)
python run_complete_simulation.py --skip-optimize
```

### Configuración Manual
Edita `optimal_simulation_config.json` para personalizar:
- Resolución de la malla (`grid_size`)
- Paso temporal (`dt`)
- Tiempo total (`t_final`)
- Parámetros físicos (`R_param`, `omega_4d_param`)

## 📊 Interpretación de Resultados

### Archivos de Salida:
- **`simulation_results.npz`** - Datos completos de la simulación
- **`simulation_analysis.png`** - Gráficos de análisis automático
- **`checkpoint_*.npz`** - Puntos de control durante la simulación

### Indicadores de Éxito:
1. **Curvatura Detectada**: `std(γ_xx) > 1e-6`
2. **Estabilidad Numérica**: Sin valores `inf` o `NaN`
3. **Evolución Temporal**: Cambios graduales en la métrica

### Comparación con Schwarzschild:
La simulación exitosa debe mostrar:
- Curvatura radial que decae como `1/r`
- Preservación del determinante de la métrica
- Simetría esférica aproximada

## 🔧 Optimizaciones Implementadas

### Paralelización:
- **Multi-core**: Uso automático de todos los CPUs
- **Numba JIT**: Compilación just-in-time para loops críticos
- **Vectorización**: Operaciones optimizadas con NumPy

### Gestión de Memoria:
- **Análisis automático**: Recomendación de resolución según RAM
- **Checkpoints**: Guardado periódico para evitar pérdida de datos
- **Compresión**: Archivos de salida comprimidos

### Estabilidad Numérica:
- **Condiciones CFL**: Paso temporal automático para estabilidad
- **Disipación artificial**: Supresión de inestabilidades de alta frecuencia
- **Condiciones de frontera**: Ondas salientes en los bordes

## 📈 Rendimiento Esperado

### Sistemas Recomendados:
- **Mínimo**: 4 cores, 8 GB RAM → Resolución 16³, ~5 min
- **Recomendado**: 8 cores, 16 GB RAM → Resolución 32³, ~15 min  
- **Óptimo**: 16+ cores, 32+ GB RAM → Resolución 128³+, ~2 horas

### Métricas de Rendimiento:
El sistema mostrará en tiempo real:
- Puntos procesados por segundo
- Progreso y tiempo estimado restante
- Uso de memoria y CPU
- Indicadores de estabilidad

## 🔍 Troubleshooting

### Problemas Comunes:

#### Error: "Numba no disponible"
```bash
pip install numba
```

#### Error: "Memoria insuficiente"
- Reduce `grid_size` en la configuración
- Cierra otras aplicaciones
- Ejecuta: `python notebooks/optimize_simulation_params.py`

#### Error: "Inestabilidad numérica"
- Reduce `dt` (paso temporal)
- Incrementa `dissipation`
- Verifica condiciones iniciales

#### Simulación muy lenta
- Verifica que Numba esté instalado
- Reduce resolución para pruebas
- Ejecuta test de rendimiento: `python notebooks/test_performance.py`

## 📚 Base Teórica

### Formalismo BSSN:
La simulación usa una versión simplificada del formalismo BSSN (Baumgarte-Shapiro-Shibata-Nakamura), estándar en relatividad numérica.

### Variables Evolutivas:
- **γᵢⱼ**: Métrica espacial 3D
- **Kᵢⱼ**: Curvatura extrínseca
- **α**: Función de lapse
- **βⁱ**: Vector de shift

### Ecuaciones de Einstein Simplificadas:
```
∂γᵢⱼ/∂t = -2αKᵢⱼ + ∇ᵢβⱼ + ∇ⱼβᵢ
∂Kᵢⱼ/∂t = -∇ᵢ∇ⱼα + α(Rᵢⱼ - 8πTᵢⱼ) + ...
```

## 🤝 Contribución

### Mejoras Posibles:
- Implementación de AMR (Adaptive Mesh Refinement)
- Soporte para GPU computing
- Visualización 3D interactiva
- Análisis de ondas gravitacionales

### Estructura del Código:
```
notebooks/
├── setup_numerical_simulation.py     # Datos iniciales
├── run_numerical_simulation.py       # Motor principal
├── install_simulation_deps.py        # Instalador
├── optimize_simulation_params.py     # Optimizador
└── test_performance.py              # Benchmarks

run_complete_simulation.py           # Script maestro
```

## 📄 Licencia

Este proyecto forma parte de la investigación del "Universo Centrífugo" y está disponible para uso académico y científico.

## 🆘 Soporte

Para problemas o preguntas:
1. Revisa este README
2. Ejecuta `python notebooks/test_performance.py`
3. Verifica logs de error en la salida
4. Consulta los archivos de documentación en `docs/`

---

**¡Que comience la simulación! 🚀**