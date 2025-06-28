# Plan de Verificación: Ley de Hubble en Simulación Cosmológica

*Versión: 1.0 - Fecha: 28 de junio de 2025*

## 1. Objetivo Principal

Demostrar cuantitativamente que la expansión del espacio-tiempo observada en la simulación BSSN sigue la Ley de Hubble (`v = H₀d`), calculando la constante de Hubble `H₀` efectiva del universo simulado.

## 2. Fases del Plan

```mermaid
graph TD
    A[Fase 1: Preparación y Entendimiento de Datos] --> B[Fase 2: Cálculo de Distancia Propia];
    B --> C[Fase 3: Cálculo de Velocidad de Recesión];
    C --> D[Fase 4: Análisis y Verificación (Gráfico de Hubble)];
    D --> E[Fase 5: Implementación y Entregables];
```

---

### **Fase 1: Preparación y Entendimiento de Datos**

1.  **Identificar la Fuente de Datos:**
    *   El principal insumo son los resultados de la simulación de alta resolución (256³), que se encuentran en el archivo `output/simulation_256cubed/results/simulation_results.npz`.
    *   Este archivo debe contener la evolución temporal del **tensor de la métrica espacial** `γ_ij(t, x, y, z)`.

2.  **Análisis del Script Existente:**
    *   Revisar el script `analyze_simulation_results.py` para comprender cómo se cargan y estructuran los datos. Esto es crucial para saber cómo acceder a la métrica `γ_ij` en cada punto de la malla y en cada instante de tiempo.

3.  **Selección de Puntos de Muestra:**
    *   Para probar la ley de Hubble, no necesitamos todas las 16 millones de celdas. Seleccionaremos un conjunto estratégico de puntos:
        *   **Punto de Referencia (Observador):** El centro de la malla de simulación `(x=0, y=0, z=0)`.
        *   **Puntos de "Galaxias":** Varios puntos a lo largo de un eje (p. ej., el eje x) a diferentes distancias de coordenadas del centro. Por ejemplo: `(10, 0, 0)`, `(20, 0, 0)`, `(40, 0, 0)`, `(80, 0, 0)`, etc. Esto nos dará un rango de distancias para construir el gráfico.

---

### **Fase 2: Cálculo de Distancia Propia (`d`)**

Este es el paso más importante desde el punto de vista físico. La distancia entre dos "galaxias" no es la simple distancia euclidiana de las coordenadas, sino la distancia medida a lo largo del tejido del espacio-tiempo en expansión.

1.  **Concepto Físico:** La distancia propia `d(t)` entre dos puntos A y B en un tiempo `t` se calcula integrando el elemento de línea `dl` a lo largo del camino geodésico que los une:
    *   `dl² = γ_ij dx^i dx^j`
    *   `d(t) = ∫_A^B sqrt(γ_ij dx^i dx^j)`

2.  **Implementación Numérica:**
    *   Para cada par de puntos (el observador central y una "galaxia") y para **cada paso de tiempo** de la simulación:
    *   Se calculará la integral de la raíz cuadrada del componente relevante de la métrica (`sqrt(γ_xx)`) a lo largo del eje x.
    *   Esto se implementará usando una función de integración numérica robusta (ej. `scipy.integrate.quad`).
    *   El resultado será una serie temporal `d(t)` para cada "galaxia", mostrando cómo su distancia propia al observador aumenta con el tiempo.

---

### **Fase 3: Cálculo de Velocidad de Recesión (`v`)**

1.  **Concepto Físico:** La velocidad de recesión es simplemente la tasa de cambio de la distancia propia.
    *   `v(t) = d(d(t))/dt`

2.  **Implementación Numérica:**
    *   Usando la serie temporal `d(t)` calculada en la fase anterior, se calculará su derivada numérica.
    *   Se puede usar un método de diferencias finitas: `v(t_i) ≈ (d(t_{i+1}) - d(t_i)) / (t_{i+1} - t_i)`.
    *   El resultado será una serie temporal `v(t)` para cada "galaxia".

---

### **Fase 4: Análisis y Verificación (Gráfico de Hubble)**

Aquí es donde se comprueba la ley.

1.  **Construcción del Gráfico de Hubble:**
    *   Se elegirá un instante de tiempo específico (p. ej., el último paso de la simulación, `t_final`).
    *   Se creará un gráfico de dispersión (scatter plot) con:
        *   **Eje X:** La distancia propia `d(t_final)` de cada "galaxia".
        *   **Eje Y:** La velocidad de recesión `v(t_final)` de cada "galaxia".

2.  **Regresión Lineal y Cálculo de `H₀`:**
    *   Se realizará un ajuste lineal (regresión lineal) a los puntos del gráfico.
    *   **La pendiente de esta línea es la constante de Hubble de la simulación, `H₀`**.
    *   Se calculará el coeficiente de determinación (R²). Un valor de R² muy cercano a 1 indicará que los datos se ajustan perfectamente a una línea, validando la Ley de Hubble.

---

### **Fase 5: Implementación y Entregables**

1.  **Nuevo Script:**
    *   Se creará un nuevo script Python llamado `verify_hubble_law.py`. Este script contendrá toda la lógica descrita en las fases 2, 3 y 4. Estará bien documentado para explicar cada paso del cálculo.

2.  **Entregables:**
    *   **Código Fuente:** El script `verify_hubble_law.py`.
    *   **Visualización:** Un archivo de imagen `hubble_plot.png` que mostrará el gráfico de Hubble con los puntos de datos y la línea de regresión.
    *   **Informe de Resultados:** Un archivo Markdown `hubble_analysis_report.md` que resumirá:
        *   El valor calculado de `H₀` (con sus unidades).
        *   El valor de R² del ajuste.
        *   Una conclusión clara sobre si la simulación valida la Ley de Hubble.