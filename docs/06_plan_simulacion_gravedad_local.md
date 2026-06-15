# Plan de Simulación Numérica: Gravedad Local Emergente por Membrana Elástica

*Versión: 2.0 - Fecha: 7 de junio de 2026 (Revisión Crítica y Alineación Elástica)*

---

## 1. Objetivo y Fundamentos Físicos

El objetivo de esta simulación es verificar cuantitativamente que la curvatura local espacio-temporal (gravedad) emerge de forma natural como la **deflexión elástica estática** ($h$) de nuestro universo tridimensional (modelado como una 3-esfera o brana flexible con radio variable $R(t)$) sometida a tensión superficial ($T_b$) al ser empujada en la cuarta dimensión por la fuerza centrífuga inercial en $\mathbb{R}^4$.

### El Modelo Físico
Al colocar una masa central $M$ en la brana, esta masa es arrastrada por la rotación isoclínica global del universo de velocidad angular $\omega_{4D}(t)$ (valor instantáneo local; cosmológicamente decae como $1/R(t)^2$), sufriendo una aceleración centrífuga radial hacia el exterior de la 3-esfera:

$$a_{cf} = \omega_{4D}(t)^2 R(t)$$

Esta aceleración centrífuga constante genera una fuerza de empuje normal estática en la brana que deforma su geometría. La deflexión resultante $h(\mathbf{x})$ se rige por la **ecuación elástica de Poisson de la membrana** con amortiguamiento cosmológico (provisto por la curvatura global $1/R(t)$):

$$\nabla^2 h(\mathbf{x}) - \lambda^2 h(\mathbf{x}) = \frac{\rho(\mathbf{x}) \omega_{4D}(t)^2 R(t)}{T_b(t)}$$

Donde:
*   $\lambda = \frac{1}{R(t)}$: Coeficiente de restitución elástica global.
*   $\rho(\mathbf{x})$: Densidad de masa 3D local.
*   $T_b$: Tensión superficial de la brana.

---

## 2. Metodología de Resolución Espectral (FFT)

Para garantizar estabilidad numérica y resolver la física de forma rápida, eficiente y libre de singularidades de coordenadas, utilizaremos el **Método de Elementos Espectrales por Transformada de Fourier (FFT)**.

### 2.1 Ecuaciones Discretas en el Espacio de Fourier
Aplicando la transformada de Fourier tridimensional $\mathcal{F}$ a ambos miembros, el operador diferencial Laplaciano se transforma en una multiplicación por la de la frecuencia espacial de la malla, $-k^2 = -(k_x^2 + k_y^2 + k_z^2)$:

$$-k^2 H(\mathbf{k}) - \lambda^2 H(\mathbf{k}) = \mathcal{F}\left\{ \frac{\rho(\mathbf{x}) \omega_{4D}(t)^2 R(t)}{T_b(t)} \right\}$$

Despejando la deflexión en el dominio espectral:

$$H(\mathbf{k}) = -\frac{\mathcal{F}\left\{ \frac{\rho(\mathbf{x}) \omega_{4D}(t)^2 R(t)}{T_b(t)} \right\}}{k^2 + \lambda^2}$$

La solución final para la deflexión en el espacio real se recupera aplicando la transformada de Fourier inversa ($\mathcal{F}^{-1}$):

$$h(\mathbf{x}) = \text{Re}\left( \mathcal{F}^{-1}\{ H(\mathbf{k}) \} \right)$$

---

## 3. Configuración del Pipeline de Simulación

Para validar el modelo físico, se define un pipeline automatizado integrado por tres módulos principales que se ejecutarán secuencialmente.

### 3.1 Fase 1: Datos Iniciales (Malla y Parámetros)
1.  **Definición de la Malla**: Mallas tridimensionales con resolución $N^3$ (de $32^3$ a $256^3$) en una caja cúbica de tamaño $L$.
2.  **Masa Central Suave**: Para evitar singularidades numéricas infinitesimales, la masa puntual se modela como una esfera gaussiana de densidad volumétrica suavizada:
    $$\rho(r) = \rho_0 e^{-r^2 / 2\sigma^2}$$
3.  **Parámetros Físicos de Entrada**:
    *   Radio del universo: $R = 50.0$ (límite de campo plano local) o $R = 5.0$ (amortiguamiento Yukawa fuerte).
    *   Velocidad angular: $\omega_{4D} = 1.0$.
    *   Masa total integrada: $M_{total} = 1.0$.

### 3.2 Fase 2: Reconstrucción de la Métrica Espacio-Temporal
Una vez obtenida la deflexión $h(\mathbf{x})$, se calculan numéricamente los componentes del tensor métrico inducido $g_{\mu\nu}$:
1.  **Métrica Temporal ($g_{00}$)**:
    $$g_{00}(\mathbf{x}) = -(1 + 2h(\mathbf{x}))$$
2.  **Métrica Espacial ($g_{rr}$)**:
    $$g_{rr}(\mathbf{x}) = 1 + (\nabla h(\mathbf{x}))^2$$
    El gradiente $\nabla h$ se calcula utilizando diferencias finitas centrales de segundo orden en la malla regular.

### 3.3 Fase 3: Análisis y Comparación con Schwarzschild
1.  **Mapeo Radial**: Se promedian los perfiles tridimensionales de la malla en capas esféricas radiales $r = \sqrt{x^2+y^2+z^2}$ para extraer el perfil unidimensional medio.
2.  **Métrica de Schwarzschild de Referencia**:
    $$g_{00}^{Schw}(r) = -\left(1 - \frac{r_s}{r}\right), \quad g_{rr}^{Schw}(r) = 1 + \frac{r_s^2}{4r^4}$$
    Donde la constante gravitatoria efectiva y el radio de Schwarzschild emergen de los coeficientes de tensión y rotación:
    $$G_{eff} = \frac{c^2 \omega_{4D}(t)^2 R(t)}{4\pi T_b(t)}, \quad r_s = \frac{2 G_{eff} M}{c^2}$$

*(Nota: En simulaciones estáticas de un solo timestep, $\omega_{4D}$, $R$ y $T_b$ se tratan como valores instantáneos constantes. Cosmológicamente, $\omega_{4D}(t) \propto 1/R(t)^2$ y $T_b(t) \propto 1/R(t)^3$, con cancelación exacta que produce $G_{eff}$ constante.)*
3.  **Métricas de Error**: Se calcula la correlación de Pearson y la norma L2 para validar la convergencia exacta con un éxito superior al 99%.
