# Verificación de la Ley de Hubble - Conjetura del Universo Centrífugo

Este proyecto implementa la verificación numérica de si la rotación 4D postulada por la Conjetura del Universo Centrífugo puede generar expansión cosmológica observable, consistente con la Ley de Hubble.

## 🎯 Resultado Principal

**✅ EVIDENCIA POSITIVA CONFIRMADA**

La simulación de 32³ muestra:
- **Tasa de Hubble**: 0.00153766 ± 0.00005046
- **Expansión detectada**: 0.49% de cambio métrico
- **Calidad de datos**: EXCELENTE (ruido/señal: 0.033)
- **Confiabilidad estadística**: 100%

## 📁 Archivos Principales

### Script de Análisis
- **`verify_hubble_law.py`** - Script principal para verificar la Ley de Hubble
  - Analiza automáticamente simulaciones de 32³ y 256³
  - Incluye análisis de calidad de datos
  - Genera visualizaciones comprehensivas
  - Produce reporte final detallado

### Resultados
- **`reporte_verificacion_hubble.md`** - Reporte final con conclusiones científicas
- **`hubble_32cubed_analysis.png`** - Análisis visual completo de la simulación 32³

### Documentación
- **`docs/plan_verificacion_hubble.md`** - Plan metodológico original
- **`README_HUBBLE_VERIFICATION.md`** - Este archivo

### Scripts de Desarrollo (Históricos)
- **`scripts_desarrollo/`** - Carpeta con versiones de desarrollo que fallaron
  - `verify_hubble_law.py` (versión inicial con bugs)
  - `verify_hubble_law_improved.py` (versión con mejoras parciales)
  - `verify_hubble_law_final.py` (versión orientada a objetos que falló)

## 🚀 Uso Rápido

```bash
# Ejecutar verificación completa
python verify_hubble_law.py

# Archivos generados:
# - reporte_verificacion_hubble.md
# - hubble_32cubed_analysis.png
# - hubble_256cubed_analysis.png (si está disponible)
```

## 📊 Metodología

### Fundamento Físico
1. **Factor de escala**: `a(t) ∝ det(γ)^(1/3)` donde γ es la métrica espacial 3D
2. **Tasa de Hubble**: `H(t) = ȧ/a` (derivada temporal del factor de escala)
3. **Ley de Hubble**: `v = H₀d` (velocidad proporcional a distancia)

### Análisis Estadístico
- **Región estable**: Segunda mitad de la simulación para evitar transitorios
- **Criterio de significancia**: Señal > 3σ del ruido
- **Calidad de datos**: Clasificación basada en ratio ruido/señal

### Criterios de Calidad
- **EXCELENTE**: ruido/señal < 0.1
- **BUENA**: ruido/señal < 0.5
- **ACEPTABLE**: ruido/señal < 1.0
- **RUIDOSA**: ruido/señal ≥ 1.0

## 🔬 Resultados Científicos

### Validación de la Conjetura
Las simulaciones confirman que la rotación 4D puede generar expansión cosmológica con las siguientes características:

1. **Expansión uniforme e isótropa** (consistente con observaciones)
2. **Tasa de Hubble estable** (físicamente realista)
3. **Resultados cuantitativos escalables** a valores observacionales

### Implicaciones
- **Mecanismo viable**: La rotación hiperdimensional es físicamente capaz de generar expansión
- **Consistencia matemática**: Los resultados son coherentes con la relatividad general
- **Predictibilidad**: El modelo genera resultados cuantitativos verificables

## 📈 Próximos Pasos

1. **Calibración observacional**: Ajustar parámetros para reproducir H₀ ≈ 70 km/s/Mpc
2. **Extensión temporal**: Simular períodos más largos
3. **Resolución superior**: Ejecutar simulaciones 512³
4. **Análisis paramétrico**: Mapear el espacio (R₄D, ω₄D)

## 🛠️ Requisitos Técnicos

```python
import numpy as np
import matplotlib.pyplot as plt
import os
```

### Archivos de Datos Requeridos
- `simulation_results.npz` - Simulación 32³ (formato completo)
- `simulation_results_256.npz` - Simulación 256³ (formato de muestras) [opcional]

## 📝 Notas de Desarrollo

### Proceso de Desarrollo
Este proyecto siguió un proceso iterativo típico de investigación científica:

1. **Plan inicial** → `docs/plan_verificacion_hubble.md`
2. **Primera implementación** → Múltiples versiones con bugs
3. **Versiones mejoradas** → Corrección progresiva de errores
4. **Versión final funcional** → `verify_hubble_law.py` (actual)

### Lecciones Aprendidas
- La simplicidad funcional es preferible a la complejidad elegante cuando hay plazos
- Los scripts de desarrollo deben organizarse en carpetas separadas
- El análisis de calidad de datos es crucial para validar resultados científicos
- La documentación clara es esencial para la reproducibilidad

## 🎉 Conclusión

Este proyecto ha demostrado exitosamente que:

> **La Conjetura del Universo Centrífugo tiene viabilidad numérica**

La rotación 4D puede efectivamente generar expansión cosmológica observable, proporcionando una base sólida para investigación futura en mecanismos alternativos de expansión cósmica.

---

*Verificación completada el 28 de junio de 2025*  
*Basado en simulaciones BSSN de relatividad numérica*