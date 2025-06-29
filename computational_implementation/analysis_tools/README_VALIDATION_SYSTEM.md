# Sistema de Validación de Regímenes Físicos
## Tarea 2.1.2: Validación del Principio de Superposición Cosmológico

### Descripción

Este sistema implementa la validación física completa del **Principio de Superposición Cosmológico** desarrollado en la Tarea 2.1.1. Su objetivo es demostrar cuantitativamente que la simulación reproduce correctamente tanto el régimen cosmológico como el newtoniano simultáneamente.

### Arquitectura Modular

El sistema está dividido en módulos especializados para facilitar mantenimiento y escalabilidad:

#### 1. `validate_physical_regimes.py` (Coordinador Principal)
- **Función**: Orquesta todo el proceso de validación
- **Características**:
  - Carga datos de simulación
  - Coordina validadores especializados
  - Genera informe técnico final
  - Evalúa éxito general

#### 2. `regime_validators.py` (Validadores Especializados)
- **`LocalRegimeValidator`**: Valida recuperación de Schwarzschild
- **`GlobalRegimeValidator`**: Valida preservación cosmológica
- **`TransitionAnalyzer`**: Analiza suavidad de transición

#### 3. `validation_visualizer.py` (Generador de Visualizaciones)
- **Función**: Crea gráficas comprehensivas de resultados
- **Salidas**:
  - Vista general del perfil radial
  - Validación de régimen local
  - Validación de régimen global
  - Análisis de transición
  - Resumen ejecutivo

#### 4. `validation_reporter.py` (Generador de Informes)
- **Función**: Produce el informe técnico completo
- **Salida**: `validacion_superposicion.md` (entregable de la Tarea 2.1.2)

#### 5. `test_validation_system.py` (Sistema de Pruebas)
- **Función**: Verifica funcionamiento del sistema
- **Pruebas**: Importaciones, inicialización, estructuras de datos

### Instalación y Configuración

#### Prerrequisitos
```bash
# Dependencias Python requeridas
pip install numpy scipy matplotlib
```

#### Verificación del Sistema
```bash
cd computational_implementation/analysis_tools
python test_validation_system.py
```

**Salida esperada**: Todas las pruebas deben pasar antes del uso.

### Uso Básico

#### 1. Ejecutar Simulación Previa
```bash
cd computational_implementation/simulations
python run_local_gravity_simulation.py --mass 1.0 --max-cores 4
```

**Archivos generados requeridos**:
- `simulation_results.npz`
- `local_gravity_simulation_results.npz`
- `simulation_initial_data.npz`

#### 2. Ejecutar Validación Completa

**Desde línea de comandos**:
```bash
cd computational_implementation/analysis_tools
python validate_physical_regimes.py
```

**Desde código Python**:
```python
from validate_physical_regimes import PhysicalRegimeValidator

# Configurar tolerancias
validator = PhysicalRegimeValidator(
    tolerance_local=0.01,    # 1% para régimen local
    tolerance_global=0.05    # 5% para régimen global
)

# Ejecutar validación completa
results = validator.run_complete_validation()

# Verificar resultados
if results['overall_success']:
    print("🎉 Validación exitosa!")
    print(f"Informe: {results['report_file']}")
else:
    print("⚠️ Validación parcial - revisar componentes")
```

### Criterios de Validación

#### Régimen Local (Schwarzschild)
- **Región**: 3σ < r < 0.1×L_box
- **Test**: Ajuste de componentes métricos a forma g_μν ≈ η_μν + 2M/r
- **Criterio de éxito**: Desviación de masa efectiva < tolerancia_local

#### Régimen Global (Cosmológico)
- **Región**: r > 0.5×L_box
- **Tests**:
  - Isotropía: |γ_ii - γ_jj| < tolerancia_global
  - Ausencia de perturbaciones: Términos cruzados ≈ 0
- **Criterio de éxito**: Ambos tests pasan

#### Zona de Transición
- **Región**: 0.1×L_box ≤ r ≤ 0.5×L_box
- **Test**: Análisis de suavidad via segunda derivada
- **Criterio de éxito**: Curvatura máxima < 0.1

#### Desacoplamiento
- **Tests**:
  - Consistencia de masa local entre componentes
  - Independencia del régimen global
  - Separación adecuada de escalas

### Archivos de Salida

#### Informe Principal
- **`validacion_superposicion.md`**: Informe técnico completo (entregable Tarea 2.1.2)

#### Visualizaciones (`validation_figures/`)
- **`radial_overview.png`**: Vista general del perfil radial con regiones
- **`local_regime_validation.png`**: Análisis detallado del régimen local
- **`global_regime_validation.png`**: Análisis del régimen cosmológico
- **`transition_analysis.png`**: Análisis de la zona de transición
- **`validation_summary.png`**: Resumen ejecutivo visual

### Interpretación de Resultados

#### Validación Exitosa (overall_success = True)
- ✅ **Criterio de completitud cumplido**
- ✅ **Métricas locales y globales correctas simultáneamente**
- ✅ **Principio de Superposición Cosmológico físicamente válido**

#### Validación Parcial (overall_success = False)
- ⚠️ **Al menos 1 de 4 tests falló**
- 🔧 **Requiere ajustes en parámetros o implementación**
- 📊 **Revisar secciones específicas del informe**

### Parámetros Configurables

| Parámetro | Descripción | Valor por Defecto |
|-----------|-------------|-------------------|
| `tolerance_local` | Tolerancia para régimen local | 0.01 (1%) |
| `tolerance_global` | Tolerancia para régimen global | 0.05 (5%) |
| `output_dir` | Directorio de visualizaciones | "validation_figures" |

### Troubleshooting

#### Error: "No se encontraron archivos de resultados"
**Solución**: Ejecutar primero la simulación con masa local
```bash
cd ../simulations
python run_local_gravity_simulation.py
```

#### Error: "Insufficient data in local/global region"
**Causas posibles**:
- Dominio computacional muy pequeño
- Radio de suavizado inapropiado
- Resolución insuficiente

**Soluciones**:
```bash
# Aumentar resolución
python run_local_gravity_simulation.py --grid-size 64

# Ajustar radio de suavizado
python run_local_gravity_simulation.py --smoothing 0.1
```

#### Warning: "Validation parcial"
**Acción**: Revisar el informe generado para identificar componentes específicos que requieren optimización.

### Extensiones Futuras

#### Tarea 2.1.3: Efectos de Acoplamiento
- Análisis de desviaciones del modelo lineal
- Implementación de superposición no-lineal
- Búsqueda de efectos de acoplamiento entre escalas

#### Mejoras Técnicas
- Validación automática de convergencia
- Tests estadísticos más sofisticados
- Análisis de sensibilidad a parámetros

### Referencias Técnicas

- **Formulación BSSN**: Baumgarte & Shapiro (1999)
- **Simulaciones Einstein**: Alcubierre (2008)
- **Aproximación Post-Newtoniana**: Will (2014)
- **Cosmología Numérica**: Bentivegna & Bruni (2016)

---

**Implementación**: Tarea 2.1.2 del Plan de Investigación 2025  
**Estado**: ✅ Sistema completo y funcional  
**Próximo hito**: Validación física del Principio de Superposición Cosmológico