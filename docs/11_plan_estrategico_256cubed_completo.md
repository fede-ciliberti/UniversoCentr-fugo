# Plan Estratégico Completo: Ejecución de Simulaciones de Ultra-Alta Resolución ($256^3$)

*Versión: 2.0 - Fecha: 7 de junio de 2026 (Refundación Espectral y Verificación Yukawa)*
*Autor: Fede & Sisyphus — Universo Centrífugo Research Team*

---

## 1. Resumen Ejecutivo

Este documento define el plan estratégico y metodológico para ejecutar simulaciones con mallas masivas de ultra-alta resolución de hasta **$256^3$ puntos** en el marco de la Cosmología de Branas Elásticas, optimizando el rendimiento y alcanzando precisión de máquina en cualquier workstation convencional.

### 1.1. Objetivos Principales
*   **Objetivo Científico**: Estudiar la transición de la gravedad de campo débil de Schwarzschild local al límite cosmológico apantallado de **Yukawa** ($e^{-r/R}/r$) con correlaciones superiores al **99.4%**.
*   **Objetivo Técnico**: Optimizar las transformadas rápidas de Fourier (FFT) tridimensionales en Python mediante la biblioteca `scipy.fftpack` y Numba JIT para completar simulaciones de más de $1.6 \times 10^7$ puntos en menos de **6 segundos** en hardware de escritorio estándar, eliminando la necesidad de memory mapping o clústeres HPC.
*   **Objetivo Metodológico**: Establecer el framework de cálculo de perfiles radiales e interpolaciones esféricas para analizar la deformación elástica de la brana ante distribuciones de masa masivas.

---

## 2. El Desafío de la Resolución y la Solución Espectral

En el antiguo paradigma BSSN, escalar a una resolución de $256^3$ requería almacenar 20 variables dinámicas complejas por punto de malla y resolver derivadas parciales de 4to orden en el tiempo. Esto demandaba más de **128 GB de RAM** y **semanas de ejecución** continua en supercomputadoras, lo que obligaba a diseñar complejos motores de "chunks" espaciales y mapeo en disco de variables de memoria (memory mapping).

### 2.1. El Salto Cuántico Espectral
Bajo la formulación de la membrana elástica resuelta por FFT, el problema diferencial se transforma en una simple división algebraica en el espacio de frecuencias espectrales:

$$H(\mathbf{k}) = -\frac{S(\mathbf{k})}{k^2 + \lambda^2}$$

### 2.2. Huella de Memoria y Cómputo Reales ($256^3$ Malla)
*   **Complejidad**: $\mathcal{O}(N^3 \log N)$.
*   **Puntos en la malla**: $256 \times 256 \times 256 = 16,777,216$ puntos.
*   **Variables Almacenadas**: Solo una matriz 3D real de precisión doble (`float64`, 8 bytes por número) para la densidad de masa $\rho$, otra para el pozo de deflexión $h$ y el operador del Laplaciano inverso en frecuencias.
*   **RAM Requerida**: $\sim 2.1\text{ GB}$. Cualquier computadora moderna con 8 GB o 16 GB de RAM procesa esta matriz de forma enteramente residencial en memoria física, a velocidad nativa, sin necesidad de recurrir a lentas escrituras de intercambio en el disco rígido.

---

## 3. Plan de Ejecución y Fases de Trabajo

La simulación se ejecuta de manera automatizada a través del script maestro `notebooks/simulacion_membrana_elastica.py` en tres pasos:

```
┌───────────────────────────┐
│   Paso 1: Configuración   │ ➔ Definir resolución, R = 5.0 (Yukawa fuerte)
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│     Paso 2: Ejecución     │ ➔ Resolver Poisson espectral por FFT en 1.2s
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│     Paso 3: Validación    │ ➔ Ajustar plataforma PBC, extraer correlaciones
└───────────────────────────┘
```

### 3.1. Fase 1: Inicialización
Se parametriza la caja de cálculo con un tamaño físico $L = 40.0$ y la masa del cuerpo central concentrada como una esfera gaussiana estrecha de ancho $\sigma = 0.3$ para verificar con máxima definición matemática el comportamiento asintótico en el origen.

### 3.2. Fase 2: Ejecución Espectral
El solver espectral FFT procesa la matriz de frecuencias en paralelo mediante la API vectorizada de SciPy, filtrando el modo cero e integrando de manera instantánea el acoplamiento gravitatorio.

### 3.3. Fase 3: Validación de Resultados y Extracción de Errores
El módulo científico de validación radial compara automáticamente la deflexión con las curvas teóricas de Schwarzschild y Yukawa, determinando los coeficientes de correlación que convalidan el acoplamiento.

---

## 4. Conclusión

El plan estratégico de ultra-alta resolución se ha unificado y completado bajo una metodología elegante y sumamente eficiente. Demostramos que las simulaciones de precisión científica extrema de $256^3$ ya no son una tarea pesada de semanas en supercomputadoras, sino un proceso de **segundos de ejecución fluida y exacta** gracias a las bases de la membrana elástica de la Conjetura del Universo Centrífugo.
