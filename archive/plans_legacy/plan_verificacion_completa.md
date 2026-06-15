# 🔬 PLAN DE VERIFICACIÓN COMPLETA

## Conjetura del Universo Centrífugo - Validación Rigurosa

**Objetivo**: Verificar sistemáticamente cada componente de la conjetura y su implementación numérica mediante sub-tareas específicas y medibles.

---

## 📋 FASE 1: AUDITORÍA DE FUNDAMENTOS TEÓRICOS

### 1.1 Verificación Matemática Base

**Sub-tareas:**

- [ ] **1.1.1** Verificar algebra de rotaciones 4D (SO(4) → SU(2)×SU(2))
- [ ] **1.1.2** Validar métrica de 3-esfera en coordenadas estereográficas
- [ ] **1.1.3** Confirmar tensor energía-momento para rotación isoclínica
- [ ] **1.1.4** Verificar proyección 4D→3D de efectos gravitacionales

**Criterios de éxito:**

- Cálculos verificados independientemente con WolframAlpha
- Consistencia dimensional en todas las ecuaciones
- Límites físicos correctos (v→0, ω→0)

### 1.2 Validación de Predicciones

**Sub-tareas:**

- [ ] **1.2.1** Derivar H₀ = f(ω₄D, R₄D) analíticamente
- [ ] **1.2.2** Calcular densidad de energía rotacional vs observada
- [ ] **1.2.3** Verificar que ρ_rot ≈ 0.27 ρ_crítica para materia oscura
- [ ] **1.2.4** Comprobar escalas de tiempo cosmológicas

**Criterios de éxito:**

- Valores numéricos consistentes con observaciones (H₀ ≈ 70 km/s/Mpc)
- Órdenes de magnitud correctos para materia oscura
- Predicciones falsables específicas

---

## 🔧 FASE 2: AUDITORÍA DE IMPLEMENTACIÓN NUMÉRICA

### 2.1 Verificación de Cálculos Fundamentales

**Sub-tareas:**

- [ ] **2.1.1** Auditar `calculate_4_velocity.py` paso a paso
- [ ] **2.1.2** Verificar `calculate_stress_energy_tensor.py` contra analítico
- [ ] **2.1.3** Validar `calculate_projected_tensor.py` con casos test
- [ ] **2.1.4** Comprobar `calculate_time_averaged_tensor.py` numéricamente

**Criterios de éxito:**

- Cada cálculo reproducible manualmente
- Casos test simples dan resultados esperados
- Conservación de cantidades relevantes

### 2.2 Validación del Motor de Simulación

**Sub-tareas:**

- [ ] **2.2.1** Verificar implementación BSSN contra literatura
- [ ] **2.2.2** Test de convergencia: 16³ → 32³ → 64³ → 128³
- [ ] **2.2.3** Verificar condiciones de frontera y estabilidad
- [ ] **2.2.4** Comprobar conservación de energía-momento

**Criterios de éxito:**

- Soluciones convergen con refinamiento de malla
- Estabilidad numérica sin divergencias
- Violaciones de conservación < 1e-12

### 2.3 Diagnóstico del Problema de Velocidad

**Sub-tareas:**

- [ ] **2.3.1** Profile de rendimiento detallado (tiempo por operación)
- [ ] **2.3.2** Contar operaciones FLOPs reales vs esperadas
- [ ] **2.3.3** Verificar que loops de evolución temporal se ejecuten
- [ ] **2.3.4** Auditar paralelización Numba

**Criterios de éxito:**

- Tiempo de ejecución consistente con estimación teórica
- Verificación de que todos los pasos se ejecutan
- Carga computacional distribuida correctamente

---

## 🎯 FASE 3: VALIDACIÓN FÍSICA ESPECÍFICA

### 3.1 Tests de Casos Límite

**Sub-tareas:**

- [ ] **3.1.1** ω₄D = 0 → universo estático (sin evolución)
- [ ] **3.1.2** R₄D → ∞ → efectos lineales en ω₄D
- [ ] **3.1.3** Límite newtoniano: recuperar potencial Φ = GM/r
- [ ] **3.1.4** Límite cosmológico: recuperar ecuación de Friedmann

**Criterios de éxito:**

- Límites teóricos correctamente reproducidos
- Transiciones suaves entre regímenes
- Concordancia con física conocida

### 3.2 Verificación de Signatures Observacionales

**Sub-tareas:**

- [ ] **3.2.1** Detectar dependencia radial tipo 1/r en métrica
- [ ] **3.2.2** Verificar anisotropía direccional (efectos 4D)
- [ ] **3.2.3** Comprobar evolución temporal consistente
- [ ] **3.2.4** Medir "expansión" vs contracción local

**Criterios de éxito:**

- Patrones espaciales consistentes con rotación 4D
- Evolución temporal monotónica y estable
- Signos de efectos direccionales (no isotrópicos)

---

## 🔍 FASE 4: TESTS DE IMPLEMENTACIONES CRUZADAS

### 4.1 Comparación Entre Versiones

**Sub-tareas:**

- [ ] **4.1.1** 32³ original vs 64³ manual vs 256³ optimizada
- [ ] **4.1.2** Script simple vs implementación completa BSSN
- [ ] **4.1.3** Diferentes esquemas de diferencias finitas
- [ ] **4.1.4** Múltiples condiciones iniciales

**Criterios de éxito:**

- Resultados cualitativamente consistentes
- Convergencia hacia mismo límite
- Dependencias sistemáticas explicables

### 4.2 Validación Independiente

**Sub-tareas:**

- [ ] **4.2.1** Implementación completamente nueva desde cero
- [ ] **4.2.2** Uso de diferentes librerías numéricas
- [ ] **4.2.3** Verificación con software comercial (si disponible)
- [ ] **4.2.4** Comparación con simulaciones estándar (Schwarzschild)

**Criterios de éxito:**

- Resultados reproducibles independientemente
- Consistencia entre diferentes implementaciones
- Acuerdo con casos test conocidos

---

## 📊 FASE 5: ANÁLISIS DE SENSIBILIDAD Y ROBUSTEZ

### 5.1 Dependencia Paramétrica

**Sub-tareas:**

- [ ] **5.1.1** Mapear resultados vs (ω₄D, R₄D) sistemáticamente
- [ ] **5.1.2** Verificar escalamiento teórico vs numérico
- [ ] **5.1.3** Identificar rangos de parámetros válidos
- [ ] **5.1.4** Test de estabilidad ante perturbaciones

**Criterios de éxito:**

- Dependencias paramétricas predichas teóricamente
- Rangos de validez claramente definidos
- Robustez ante variaciones pequeñas

### 5.2 Convergencia y Precisión

**Sub-tareas:**

- [ ] **5.2.1** Análisis de convergencia espacial: Δx → 0
- [ ] **5.2.2** Análisis de convergencia temporal: Δt → 0
- [ ] **5.2.3** Estimación de errores numéricos
- [ ] **5.2.4** Verificación orden de precisión del esquema

**Criterios de éxito:**

- Convergencia de orden esperado (2do orden típicamente)
- Errores numéricos controlados y cuantificados
- Resultados estables bajo refinamiento

---

## 🎯 FASE 6: INTEGRATION TESTS COMPREHENSIVOS

### 6.1 Simulación de Referencia Completa

**Sub-tareas:**

- [ ] **6.1.1** Simulación 128³ con tiempo extendido (t=5.0)
- [ ] **6.1.2** Múltiples checkpoints y análisis intermedio
- [ ] **6.1.3** Comparación exhaustiva con predicciones teóricas
- [ ] **6.1.4** Análisis estadístico de resultados

**Criterios de éxito:**

- Simulación estable por tiempo cosmológicamente relevante
- Evolución consistente con predicciones
- Significancia estadística de efectos observados

### 6.2 Validación Final de la Conjetura

**Sub-tareas:**

- [ ] **6.2.1** Confirmar H₀ efectiva vs observacional
- [ ] **6.2.2** Verificar densidad de energía vs materia oscura
- [ ] **6.2.3** Demostrar efectos de curvatura espacio-temporal
- [ ] **6.2.4** Generar predicciones observacionales específicas

**Criterios de éxito:**

- Concordancia cuantitativa con observaciones cosmológicas
- Predicciones falsables para futuros experimentos
- Evidencia convincente de validez de la conjetura

---

## 📝 CRITERIOS DE EVALUACIÓN GLOBAL

### Niveles de Confianza

- **🔴 Crítico**: Fallo invalida completamente la conjetura
- **🟡 Importante**: Fallo requiere revisión mayor de teoría/implementación
- **🟢 Deseable**: Fallo indica necesidad de refinamiento

### Métricas de Éxito

1. **Consistencia Teórica**: ≥95% de tests fundamentales pasan
2. **Implementación Numérica**: ≥90% de verificaciones técnicas correctas  
3. **Validación Física**: ≥85% de predicciones confirmadas
4. **Robustez**: ≥80% de tests de sensibilidad estables

### Timeline Sugerido

- **Fases 1-2**: 2-3 días (fundamentos críticos)
- **Fases 3-4**: 3-4 días (validación física)
- **Fases 5-6**: 4-5 días (análisis exhaustivo)

---

## 🚀 PRÓXIMO PASO INMEDIATO

**Acción recomendada**: Comenzar con **Fase 2.3** (Diagnóstico del problema de velocidad) ya que:

1. Es la anomalía más evidente (6 segundos para 64³)
2. Su resolución afecta interpretación de todos los demás resultados
3. Es técnicamente verificable de inmediato
4. No requiere revisión teórica compleja

**Output esperado**: Script de diagnóstico que confirme o refute si la simulación realmente ejecutó 187 pasos temporales completos en 64³ puntos.
