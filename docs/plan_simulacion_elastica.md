# Plan de Simulación Numérica: Gravedad Emergente por Membrana Elástica

*Versión: 1.0 - Fecha: 7 de junio de 2026*
*Autor: Fede & Sisyphus*

Este documento establece la metodología matemática, las ecuaciones discretas de física elástica y el diseño de arquitectura de software para construir la nueva simulación computacional de la Conjetura del Universo Centrífugo. El objetivo es proporcionar una referencia completa y rigurosa para codificar el simulador en una fase posterior.

---

## 1. Fundamentos Físicos de la Simulación

La conjetura propone que la gravedad local no es una fuerza fundamental mediada por un espín-2 (gravitón), sino una **reacción elástica macroscópica** de la brana 3D ($S^3$) al deformarse en la cuarta dirección espacial ($w$) debido al empuje centrífugo de la inercia rotacional en $R^4$.

### 1.1 La Ecuación de Estado de Membrana
El equilibrio hidrostático-elástico de la brana se rige por una ecuación de deformación de tipo Poisson con amortiguamiento cosmológico. En el espacio continuo:

$$\nabla^2 h(\mathbf{x}) - \lambda^2 h(\mathbf{x}) = S(\mathbf{x})$$

Donde:
*   $h(\mathbf{x})$: Deflexión hiperdimensional en el eje $w$ (unidades de longitud).
*   $\lambda = \frac{1}{R(t)}$: Coeficiente de restitución elástica global, determinado por el radio de curvatura dinámico de la 3-esfera.
*   $S(\mathbf{x})$: Término fuente de empuje centrífugo inercial.

### 1.2 El Término Fuente de Empuje
Para una distribución de densidad de masa ordinaria $\rho(\mathbf{x})$ en la brana, la inercia centrífuga en ℝ⁴ empuja la masa hacia el exterior esférico con fuerza radial constante. El término fuente acoplado es:

$$S(\mathbf{x}) = \frac{\rho(\mathbf{x}) \omega_{4D}(t)^2 R(t)}{T_b(t)}$$

Donde:
*   $\omega_{4D}(t)$: Velocidad angular de la rotación isoclínica en ℝ⁴. En escalas cosmológicas, $\omega_{4D}(t) \propto 1/R(t)^2$ por conservación del momento angular (ver [`conservacion_momento_inercia_geff.md`](conservacion_momento_inercia_geff.md)). En simulaciones de un solo timestep (escala local), se trata como valor instantáneo constante.
*   $T_b(t)$: Tensión superficial de la brana (resistencia elástica intrínseca de nuestro espacio-tiempo). Cosmológicamente, $T_b(t) \propto 1/R(t)^3$ por dilución elástica del volumen de la brana.

---

## 2. Formulación Matemática Espectral (FFT)

Dado que la ecuación diferencial es lineal y posee simetría esférica local, el método más estable, rápido y libre de inestabilidades numéricas es el **Método Espectral en el Espacio de Fourier**.

### 2.1 Transformada de Fourier de la Ecuación
Al aplicar la Transformada de Fourier Tridimensional ($\mathcal{F}$) a ambos miembros de la ecuación elástica de Poisson:

$$\mathcal{F}\{\nabla^2 h\} - \lambda^2 \mathcal{F}\{h\} = \mathcal{F}\{S\}$$

Sabiendo que en el espacio de frecuencias el operador Laplaciano equivale a multiplicar por $-k^2$ (donde $k^2 = k_x^2 + k_y^2 + k_z^2$ es la magnitud del vector de onda al cuadrado):

$$-k^2 H(\mathbf{k}) - \lambda^2 H(\mathbf{k}) = S(\mathbf{k})$$

Donde $H(\mathbf{k}) = \mathcal{F}\{h\}$ y $S(\mathbf{k}) = \mathcal{F}\{S\}$. Despejando la deflexión en el espacio de Fourier:

$$H(\mathbf{k}) = -\frac{S(\mathbf{k})}{k^2 + \lambda^2}$$

### 2.2 Solución en el Espacio Real
La deflexión espacial se obtiene aplicando la Transformada Inversa de Fourier ($\mathcal{F}^{-1}$):

$$h(\mathbf{x}) = \mathcal{F}^{-1} \left\{ -\frac{\mathcal{F}\{S(\mathbf{x})\}}{k^2 + \lambda^2} \right\}$$

Este método tiene complejidad computacional de orden $\mathcal{O}(N^3 \log N)$, lo que permite resolver mallas de alta resolución ($128^3$ o $256^3$) en segundos en cualquier computadora de escritorio estándar.

---

## 3. Parametrización y Unidades de la Simulación

Para evitar el desbordamiento numérico por el uso de constantes extremadamente pequeñas (como $G = 6.674 \times 10^{-11}$ o constantes atómicas de la brana), utilizaremos **unidades geometrizadas** donde la velocidad de la luz $c = 1$.

### 3.1 Escala Fisiológica y Parámetros del Simulador
Definimos los parámetros físicos de control que el simulador recibirá como inputs:

*   `grid_size` ($N$): Resolución de la malla en cada dirección (ej., $N=64, 128$).
*   `box_size` ($L$): Tamaño físico de la caja de simulación local (en unidades arbitrarias, ej., $L=10.0$).
*   `omega_4D` ($\omega_{4D}$): Velocidad angular inercial. Valor instantáneo local; cosmológicamente $\omega_{4D}(t) \propto 1/R(t)^2$ (ver [`conservacion_momento_inercia_geff.md`](conservacion_momento_inercia_geff.md)).
*   `R` ($R$): Radio cosmológico de la brana (establece el amortiguamiento $\lambda = 1/R$).
*   `tension` ($T_b$): Tensión de la brana. Regulando $T_b$, controlamos de forma directa la constante gravitacional efectiva $G_{eff}$.
*   `sigma` ($\sigma$): Ancho de la distribución gaussiana de masa. Una masa puntual real genera infinitos numéricos en diferencias finitas. Para evitarlo, modelamos el cuerpo celeste como una esfera gaussiana suave:
    $$\rho(r) = \rho_0 e^{-r^2 / 2\sigma^2}$$

---

## 4. Reconstrucción de la Métrica y Geodésicas

Una vez que se obtiene el mapa 3D de la deflexión $h(\mathbf{x})$ en el espacio real, el simulador debe mapear esta deformación hiperdimensional a las componentes del tensor métrico observable $g_{\mu\nu}$.

### 4.1 Componentes Métricos Inducidos
1.  **Métrica Temporal ($g_{00}$)**:
    $$g_{00}(\mathbf{x}) = -(1 + 2h(\mathbf{x}))$$
    Este componente describe el pozo de potencial que gobierna la dilatación temporal y la atracción gravitacional clásica.
2.  **Métrica Espacial ($g_{rr}$)**:
    $$g_{rr}(\mathbf{x}) = 1 + (\nabla h(\mathbf{x}))^2$$
    Donde $\nabla h = \left( \frac{\partial h}{\partial x}, \frac{\partial h}{\partial y}, \frac{\partial h}{\partial z} \right)$ es el gradiente tridimensional obtenido mediante diferencias finitas centrales de la deflexión hiperdimensional.

### 4.2 Comparación Cuantitativa de Errores (Validation Protocol)
El simulador comparará los resultados numéricos en el plano ecuatorial con el potencial analítico de Schwarzschild de campo débil. Se calculará el error medio cuadrático (L2 norm) y el error relativo porcentual:

$$\text{Error } g_{00} = \left| \frac{g_{00}^{\text{numérico}}(r) - g_{00}^{\text{Schwarzschild}}(r)}{g_{00}^{\text{Schwarzschild}}(r)} \right| \times 100\%$$

---

## 5. Diseño del Software y Visualización

La arquitectura del script estará dividida en tres módulos internos:

### 5.1 Módulo del Solucionador (Solver)
*   **Input**: Grilla 3D de densidad de masa, vector de coordenadas, parámetros de la brana ($T_b, \omega_{4D}, R$). Nota: en simulaciones estáticas de un solo timestep, $\omega_{4D}$ se pasa como valor instantáneo local; para simulaciones cosmológicas dinámicas, debe calcularse como $\omega_{4D}(t) = \omega_{4D,0}(R_0/R(t))^2$.
*   **Proceso**: Cálculo espectral de Poisson mediante la API FFT de `scipy.fftpack`.
*   **Output**: Matriz 3D de la deflexión $h(\mathbf{x})$.

### 5.2 Módulo de Reconstrucción de Métrica
*   **Input**: Matriz de deflexión $h(\mathbf{x})$, paso de malla $dx$.
*   **Proceso**: Gradiente numérico multidimensional (`np.gradient`) para computar las componentes de la métrica $g_{00}$ y $g_{rr}$.
*   **Output**: Matrices 3D de la perturbación temporal y espacial.

### 5.3 Módulo de Visualización y Análisis (Plotting)
Para evaluar físicamente el éxito de la simulación, el script generará tres gráficos interactivos guardados de manera local:
1.  **Visualización 3D/2D del Pozo**: Mapa de color o superficie de deformación de la brana "hundida" en el eje $w$.
2.  **Perfil Radial de Gravedad**: Curvas comparativas de $g_{00}$ numérico contra Schwarzschild teórico.
3.  **Comportamiento de $g_{rr}$**: Curva del componente métrico espacial mostrando cómo la curvatura del espacio físico emerge únicamente del "estiramiento elástico" causado por la inercia en la cuarta dimensión.

---

## 6. Calibración Físico-Numérica y Factor de Escala (Brecha M2)

Para conectar los resultados adimensionales del simulador espectral con el universo real, se define un factor de calibración de escala lineal L_c. Este factor vincula el dominio de simulación numérico con las escalas cosmológicas observadas.

### 6.1 El Factor de Escala de Calibración (L_c)
Definimos el factor de escala lineal del simulador como:
L_c = 1.30 × 10²⁵ m (aproximadamente 421.3 Megapársecs)

Este factor permite mapear de forma exacta el radio adimensional de la simulación R_sim = 50.0 al radio físico de la 3-esfera cósmica actual R₀:
R₀ = L_c × R_sim = (1.30 × 10²⁵ m) × 50.0 ≈ 6.50 × 10²⁶ m

### 6.2 Significado Cosmológico y Curvatura Global
Este radio físico de la 3-esfera R₀ ≈ 6.50 × 10²⁶ m equivale a unos 68.7 mil millones de años luz de radio de curvatura. Este valor no es arbitrario; está calibrado directamente con los datos de curvatura global del satélite Planck (donde el parámetro de curvatura espacial es Ω_k = -0.044, lo que indica un universo cerrado de geometría S³).

El factor L_c asegura que la rigidez de la membrana y el acoplamiento elástico de la masa den una constante de gravedad efectiva local G_eff idéntica a la constante de Newton G, garantizando que el simulador numérico represente fielmente la física observable de nuestro universo.
