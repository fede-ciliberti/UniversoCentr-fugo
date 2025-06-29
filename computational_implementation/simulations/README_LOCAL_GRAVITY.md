# Tarea 2.1.1: Simulación con Superposición de Gravedad Local

## Descripción

Este módulo implementa el **Principio de Superposición Cosmológico** para validar la consistencia entre efectos locales y globales en el modelo del Universo Centrífugo. La implementación extiende la simulación cosmológica base para incluir una masa puntual local y verificar que el sistema puede reproducir simultáneamente:

1. **Expansión cosmológica isótropa** a gran escala
2. **Gravedad newtoniana** cerca de masas puntuales  
3. **Ambos regímenes simultáneamente** sin inconsistencias numéricas

## Archivos Principales

### `run_local_gravity_simulation.py`
**Script principal** que implementa la simulación con superposición de tensores.

- **Clase `LocalGravitySimulation`**: Hereda de `EinsteinSimulator` y añade funcionalidad de masa local
- **Superposición lineal**: `T_total = T_cosmológico + T_local`
- **Masa suavizada**: Usa perfil Gaussiano para estabilidad numérica
- **Validación automática**: Métricas de estabilidad y conservación integradas

### `test_local_gravity_simulation.py`
**Suite de pruebas** para validar la implementación antes de ejecutar simulaciones completas.

- Verificación de herencia y inicialización
- Validación del cálculo del tensor local
- Prueba de superposición de tensores
- Verificación de conservación de masa
- Test de estabilidad numérica básica

## Uso Básico

### 1. Ejecutar Pruebas de Validación

```bash
cd computational_implementation/simulations
python test_local_gravity_simulation.py
```

**Salida esperada**: Todas las pruebas deben pasar antes de ejecutar simulaciones completas.

### 2. Ejecutar Simulación Completa

```bash
# Configuración básica (masa unitaria en el centro)
python run_local_gravity_simulation.py

# Configuración personalizada
python run_local_gravity_simulation.py \
    --mass 2.0 \
    --pos-x 0.5 \
    --pos-y 0.0 \
    --pos-z 0.0 \
    --smoothing 0.1 \
    --max-cores 4
```

### 3. Parámetros de Línea de Comandos

| Parámetro | Descripción | Valor por Defecto |
|-----------|-------------|-------------------|
| `--mass` | Masa local en unidades geométricas | 1.0 |
| `--pos-x/y/z` | Posición del centro de masa | Centro automático |
| `--smoothing` | Radio de suavizado Gaussiano | Automático (5% malla) |
| `--no-time-mod` | Desactivar modulación temporal | Activada |
| `--max-cores` | Número máximo de cores | Todos disponibles |
| `--data-file` | Archivo de datos iniciales | `simulation_initial_data.npz` |

## Algoritmo de Superposición

### 1. Inicialización
```python
# Cargar simulación cosmológica base
simulator = LocalGravitySimulation(data_file, max_cores, local_mass_params)

# Pre-calcular tensor de masa local (invariante en tiempo)
T_local = calculate_gaussian_mass_tensor(M, position, sigma)
```

### 2. Bucle de Evolución Temporal
```python
for each timestep t:
    # Obtener tensor cosmológico
    T_cosmological = compute_cosmological_tensor(t)
    
    # Aplicar superposición lineal
    T_total = T_cosmological + T_local
    
    # Evolucionar métrica usando T_total
    evolve_spacetime_metric(T_total)
    
    # Validar estabilidad numérica
    validate_stability_metrics()
```

### 3. Modelo de Masa Local

**Perfil de densidad Gaussiano**:
```
ρ(r) = M / (σ√2π)³ × exp(-r² / 2σ²)
```

**Tensor de energía-impulso local**:
- `T_local^00 = ρ(r)` (densidad de energía)
- `T_local^ij = 0` (masa en reposo, sin presión)

## Métricas de Validación

### Estabilidad Numérica
- **Componente máximo del tensor**: `max(|T_μν|) < 10¹⁰`
- **Valores finitos**: Sin `NaN` o infinitos
- **Conservación de masa local**: Variación < 5%

### Conservación Física
- **Divergencia del tensor**: `∇μ T^μν ≈ 0` (dentro de precisión numérica)
- **Energía total del sistema**: Monitoreo de estabilidad

### Recuperación de Regímenes
- **Región local**: Verificar potencial `~ 1/r` cerca de la masa
- **Región cosmológica**: Mantener isotropía lejos de la masa

## Archivos de Salida

### `simulation_results.npz`
Resultados estándar de la simulación Einstein (desde clase base):
- Evolución temporal de la métrica
- Estados finales de todos los componentes métricos
- Parámetros de simulación

### `local_gravity_simulation_results.npz`
Resultados específicos de superposición:
- Parámetros de masa local utilizados
- Tensor `T_local` pre-calculado
- Métricas de estabilidad por paso temporal
- Verificación final de conservación

### `debug_local_gravity_*.npz`
Datos de depuración (solo en caso de error):
- Estado completo del sistema al momento del fallo
- Métricas de diagnóstico extendidas

## Interpretación de Resultados

### Éxito de la Validación
El Principio de Superposición se considera **validado** si:

1. ✅ **Simulación estable**: Sin divergencias numéricas
2. ✅ **Masa conservada**: `|M_final - M_inicial|/M_inicial < 5%`
3. ✅ **Tensor estable**: Variación de componentes < 10%
4. ✅ **Conservación física**: RMS de divergencia razonable

### Análisis Post-Simulación
```python
# Cargar resultados
import numpy as np
results = np.load('local_gravity_simulation_results.npz', allow_pickle=True)

# Extraer métricas temporales
metrics = results['superposition_metrics']
times = [m['time'] for m in metrics]
max_components = [m['max_tensor_component'] for m in metrics]

# Análisis de estabilidad
import matplotlib.pyplot as plt
plt.plot(times, max_components)
plt.xlabel('Tiempo')
plt.ylabel('Componente Máximo del Tensor')
plt.title('Estabilidad de la Superposición')
plt.show()
```

## Troubleshooting

### Error: "No se encontró simulation_initial_data.npz"
**Solución**: Ejecutar primero la configuración de datos iniciales:
```bash
python setup_numerical_simulation.py
```

### Error: "Tensor contiene NaN o infinitos"
**Causas posibles**:
- Radio de suavizado demasiado pequeño
- Masa demasiado grande para la resolución
- Paso temporal demasiado grande

**Soluciones**:
```bash
# Aumentar radio de suavizado
python run_local_gravity_simulation.py --smoothing 0.2

# Reducir masa
python run_local_gravity_simulation.py --mass 0.1
```

### Advertencia: "Error en conservación de masa"
**Causa**: Resolución insuficiente para el radio de suavizado elegido
**Solución**: Aumentar resolución de la malla o aumentar radio de suavizado

## Extensiones Futuras

### Tarea 2.1.2: Validación de Regímenes
- Implementar tests automáticos de recuperación newtoniana
- Medir potencial gravitacional efectivo
- Verificar isotropía cosmológica en regiones lejanas

### Tarea 2.1.3: Efectos de Acoplamiento
- Estudiar desviaciones del modelo lineal
- Implementar superposición no-lineal opcional
- Buscar efectos de acoplamiento entre escalas

## Referencias Técnicas

- **Formalismo BSSN**: Baumgarte & Shapiro (1999)
- **Simulaciones Einstein**: Alcubierre (2008)
- **Métodos numéricos**: Choptuik (1993)

---

**Implementación**: Tarea 2.1.1 del Plan de Investigación 2025  
**Estado**: ✅ Lista para validación  
**Próximo hito**: Demostración de recuperación dual de regímenes