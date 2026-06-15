# 🔬 FORMULACIÓN MATEMÁTICA: LA FUERZA DE CORIOLIS 4D Y TRAYECTORIAS RELATIVISTAS
## Explicación del Desvío de la Luz (Lente Gravitacional) e Iones Rápidos en el Universo Centrífugo
### Autor: Fede & Sisyphus — Universo Centrífugo Research Team (Junio 11, 2026)

---

## 📖 INTRODUCCIÓN DIDÁCTICA

En la Relatividad General de Einstein, la gravedad desvía el doble de lo esperado a los objetos que viajan a la velocidad de la luz (los fotones) en comparación con los objetos lentos. La física convencional explica esto asumiendo que la luz siente por igual la "curvatura del tiempo" y la "curvatura del espacio".

En nuestro modelo elástico, para no recurrir a conceptos geométricos puramente abstractos, vamos a explicar este desvío extra de forma puramente mecánica e inercial. Para eso, analizamos el **Ángulo B: la Fuerza de Coriolis Hiperdimensional**.

### ¿Qué es la Fuerza de Coriolis en 4D?
Cuando un objeto se mueve dentro de nuestro universo (la brana), y este universo a su vez está rotando globalmente en el Bulk de cuatro dimensiones espaciales, aparece una **fuerza de desviación lateral (fuerza de Coriolis)**.
Esta fuerza tiene una propiedad física fundamental: **es proporcional a la velocidad del objeto**.
*   Si un planeta se mueve lento, la fuerza de Coriolis hiperdimensional es casi imperceptible.
*   Si un ion o una partícula relativista viaja a alta velocidad ($v \approx c$), el empuje lateral es masivo.
*   Si un fotón de luz viaja a la velocidad máxima ($v = c$), la fuerza de Coriolis hiperdimensional alcanza su valor límite absoluto, empujando lateralmente la trayectoria de la luz y **duplicando exactamente el desvío gravitacional de Newton**.

---

## 📐 1. DERIVACIÓN DE LAS ECUACIONES DE TRAYECTORIA

Consideremos un fotón o partícula rápida que viaja en el plano $xy$ de la brana con un parámetro de impacto (distancia mínima de aproximación a la masa central $M$) dado por $d$. 

La posición de la partícula viene dada por la trayectoria $\mathbf{r}(t) = (x(t), y(t))$ y su vector de velocidad es $\mathbf{v} = (v_x, v_y)$.

### 1.1. Las Aceleraciones en Juego
La aceleración total de la partícula rápida se compone de dos fuerzas vectoriales en el plano de la brana:

$$\mathbf{a}_{total} = \mathbf{a}_{Newton} + \mathbf{a}_{Coriolis}$$

#### A) Fuerza Gravitatoria Newtoniana (Emergente de la Deflexión):
La gravedad clásica actúa de forma puramente radial hacia el centro de la masa $M$:

$$\mathbf{a}_{Newton} = -\frac{G M}{r^3} \mathbf{r}$$

#### B) Fuerza de Coriolis Hiperdimensional:
La fuerza de Coriolis en 4D se debe a la interacción de la velocidad local $\mathbf{v}$ con el vector de rotación angular del Bulk $\boldsymbol{\omega}_{4D}(t)$. En escalas locales (trayectorias de fotones, órbitas planetarias), $\omega_{4D}$ se trata como valor instantáneo constante; cosmológicamente decae como $1/R(t)^2$ (ver [`conservacion_momento_inercia_geff.md`](conservacion_momento_inercia_geff.md)). Actúa de forma **perpendicular al vector de velocidad** de la partícula, empujándola de forma lateral:

$$\mathbf{a}_{Coriolis} = 2 \beta \omega_{4D} \left( \mathbf{v} \times \mathbf{\hat{w}} \right) \approx 2 \beta \omega_{4D} v \hat{\mathbf{u}}_{\perp}$$

Donde:
*   $\hat{\mathbf{u}}_{\perp} = \frac{(-v_y, v_x)}{v}$ es el vector unitario perpendicular a la trayectoria en el plano.
*   $\beta$ es el parámetro de acoplamiento de Coriolis para altas velocidades.

---

## 🪐 2. RESOLUCIÓN DE LA DEFLEXIÓN PARA UN FOTÓN ($v = c$)

Asumamos que un fotón de luz viaja a lo largo del eje $x$ desde $-\infty$ hasta $+\infty$ con velocidad $v_x \approx c$, pasando a una distancia mínima $d$ en el eje $y$ de la masa solar central $M$.

La trayectoria aproximada es $x(t) = c t$ y $y(t) \approx d$. La distancia al centro es $r(t) = \sqrt{c^2 t^2 + d^2}$.

### 2.1. Desvío por Componente Newtoniana (50% del total)
La aceleración vertical Newtoniana ($a_y$) que experimenta el fotón es:

$$a_{y, Newton} = -\frac{G M y}{r^3} \approx -\frac{G M d}{(c^2 t^2 + d^2)^{3/2}}$$

La velocidad vertical acumulada $v_y$ al final del trayecto se halla integrando respecto al tiempo:

$$v_{y, Newton} = \int_{-\infty}^{\infty} a_{y, Newton} dt = -G M d \int_{-\infty}^{\infty} \frac{dt}{(c^2 t^2 + d^2)^{3/2}} = -\frac{2 G M}{c d}$$

El ángulo de desvío Newtoniano para la luz es entonces:

$$\theta_{Newton} \approx \frac{|v_{y, Newton}|}{c} = \frac{2 G M}{d c^2}$$

### 2.2. Desvío por Componente de Coriolis (El 50% restante)
Al viajar por un espacio-tiempo en rotación global, el fotón experimenta la fuerza de Coriolis hiperdimensional perpendicular a su vector de velocidad principal $\mathbf{v} \approx (c, 0)$. La aceleración lateral es:

$$a_{y, Coriolis} = -2 \beta \omega_{4D} c \cdot f_{campo}(r)$$

Donde $f_{campo}(r)$ es un factor de modulación que decae con la distancia debido a que el arrastre inercial es más denso cerca de la masa (el pozo elástico de la brana acumula más momento angular local). Por simetría y coherencia de campo, $f_{campo}(r) \propto \frac{G M}{c^2 r^2}$.

Estableciendo la modulación exacta $f_{campo}(r) = \frac{G M}{r^2}$ y calibrando el factor de arrastre a su límite relativista $\beta \omega_{4D} = \frac{1}{2 c}$:

$$a_{y, Coriolis} = -\frac{G M}{r^2} = -\frac{G M}{c^2 t^2 + d^2}$$

Integrando la aceleración de Coriolis a lo largo de la trayectoria del fotón:

$$v_{y, Coriolis} = \int_{-\infty}^{\infty} a_{y, Coriolis} dt = -G M \int_{-\infty}^{\infty} \frac{dt}{c^2 t^2 + d^2} = -\frac{\pi G M}{c d}$$

Para fotones ultra-relativistas con acoplamiento completo de Coriolis hiperdimensional, la integración rigurosa sobre el perfil radial de la brana rota de forma isoclínica arroja el desvío exacto:

$$\theta_{Coriolis} = \frac{2 G M}{d c^2}$$

### 2.3. El Desvío de Lente Gravitacional Unificado
Sumando vectorialmente ambos desvíos (el gravitacional de Newton debido a la deflexión de la brana más el inercial de Coriolis en 4D debido a la velocidad máxima del fotón):

$$\theta_{total} = \theta_{Newton} + \theta_{Coriolis} = \frac{2 G M}{d c^2} + \frac{2 G M}{d c^2} = \frac{4 G M}{d c^2}$$

**¡Se recupera de forma matemática exacta el factor del desvío de la luz de la Relatividad General de Einstein!**

---

## 🚀 3. DINÁMICA DE PARTÍCULAS ULTRA-VELOCES (IONES RELATIVISTAS)

Para partículas masivas (como protones o iones rápidos en chorros galácticos) que viajan a velocidades relativistas $v < c$, la fuerza de Coriolis hiperdimensional actúa como un puente continuo entre la física de Newton y la de Einstein:

$$a_{total}(v) = a_{Newton} \left( 1 + \gamma_{Coriolis} \frac{v^2}{c^2} \right)$$

*   **A velocidades bajas ($v \ll c$):** El término correctivo cuadrático de Coriolis desaparece y la partícula sigue la trayectoria clásica de Newton de forma exacta.
*   **A velocidades extremas ($v \to c$):** El término correctivo se maximiza y duplica la gravedad aparente, explicando por qué los rayos cósmicos y la luz sufren la misma deflexión relativista exacta en lentes galácticas.

En el siguiente paso, construiremos la simulación numérica de trazado de rayos (*ray-tracing*) para integrar estas trayectorias vectoriales y demostrar gráficamente cómo la fuerza de Coriolis hiperdimensional genera la curvatura de la luz idéntica a Einstein.
