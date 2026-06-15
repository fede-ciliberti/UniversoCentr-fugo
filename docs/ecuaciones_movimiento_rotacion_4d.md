# 🔬 FORMULACIÓN MATEMÁTICA: ECUACIONES DE MOVIMIENTO EN BRANAS ROTATORIAS
## Acoplamiento Inercial de la Velocidad 3D con la Fuerza Centrífuga 4D
### Autor: Fede & Sisyphus — Universo Centrífugo Research Team (Junio 11, 2026)

---

## 📖 INTRODUCCIÓN DIDÁCTICA

Para entender cómo se mueven las cosas en nuestro universo bajo la conjetura del Universo Centrífugo, primero tenemos que entender qué pasa cuando combinamos el movimiento local con un movimiento de rotación global.

### ¿Qué es el Acoplamiento Inercial?
Imaginate que estás parado arriba de una calesita gigante que gira. Si te quedás quieto, sentís una fuerza constante que te empuja hacia afuera (la **fuerza centrífuga**). Pero si empezás a correr en la dirección en la que gira la calesita, tu velocidad total respecto al suelo firme aumenta. Al ir más rápido, ¡el empuje hacia afuera se vuelve más fuerte! Esto es el acoplamiento inercial: **tu movimiento local modifica las fuerzas ficticias que experimentás**.

### Las fuerzas en juego en 4D:
Cuando un objeto se mueve dentro de nuestra "brana" (nuestro universo tridimensional, que a su vez gira en un espacio hiperdimensional 4D o *Bulk*), su movimiento local interacciona con la gran rotación cósmica. Esto genera dos efectos físicos fundamentales:
1.  **Fuerza de Coriolis Hiperdimensional:** Es una fuerza de arrastre que aparece debido a que el objeto cambia su distancia respecto a los planos de rotación 4D. Actúa de forma perpendicular a la velocidad, desviando suavemente las órbitas.
2.  **Modificación Cinética de la Gravedad:** Al moverte por la brana, tu velocidad se acopla a la velocidad angular global $\omega_{4D}$, haciendo que deformes la membrana elástica un poquito más. Esto equivale a decir que tu "masa inercial" y la atracción gravitatoria efectiva aumentan con la velocidad, replicando mecánicamente los efectos que la Relatividad Especial de Einstein atribuye al aumento de masa relativista.

---

## 📐 1. DERIVACIÓN DEL LAGRANGIANO PROYECTADO

Consideremos una partícula de prueba de masa $m = 1$ en el Bulk de cuatro dimensiones espaciales $\mathbb{R}^4$, donde las coordenadas cartesianas son $\mathbf{X} = (x, y, z, w)$. 

El Bulk rota de forma global con velocidad angular $\omega_{4D}(t)$ mediante una rotación isoclínica (doble rotación en planos perpendiculares). Cosmológicamente, $\omega_{4D}(t) \propto 1/R(t)^2$ por conservación del momento angular (ver [`conservacion_momento_inercia_geff.md`](conservacion_momento_inercia_geff.md)), pero en escalas de tiempo locales (órbitas, precesión) es efectivamente constante y se denota simplemente como $\omega_{4D}$. Sin perder generalidad, centramos nuestro análisis en el plano ecuatorial de la brana 3-esférica deformable, donde la posición hiperdimensional de la brana está descrita por su altura de deflexión elástica $w(\mathbf{x}) = R + h(\mathbf{x})$, siendo $R$ el radio cosmológico y $h(\mathbf{x})$ la deformación local causada por una masa central $M$.

### 1.1. Métrica del Bulk en Rotación
Si pasamos a un sistema de referencia que rota junto con el Bulk a velocidad angular $\omega_{4D}$, la métrica del espacio-tiempo plano en rotación adquiere componentes cruzadas de tipo "arrastre" (Coriolis). La acción para una partícula libre de masa unitaria viene dada por la integral del Lagrangiano $L$:

$$L = T - V$$

Donde la energía cinética en coordenadas locales de la brana se ve modificada por la velocidad de arrastre del Bulk. En coordenadas esféricas de la brana $(r, \theta, \phi)$, el acoplamiento directo de la velocidad angular local con el giro cósmico se manifiesta en la dirección angular principal $\phi$.

La velocidad de rotación en el Bulk a una distancia radial $r$ es $v_{rot} = \omega_{4D} R_{rot}(r)$. Al movernos con una velocidad local en la dirección $\phi$ dada por $v_{\phi} = r \dot{\phi} \sin\theta$, la velocidad neta respecto al Bulk inmóvil es:

$$v_{neto} = \omega_{4D} R_{rot}(r) + v_{\phi}$$

Dado que la aceleración centrífuga es proporcional al cuadrado de la velocidad neta, la fuerza centrífuga efectiva $a_{c}$ que actúa sobre la partícula de prueba es:

$$a_{c} = \frac{v_{neto}^2}{R} = \frac{\left(\omega_{4D} R_{rot}(r) + r \dot{\phi} \sin\theta\right)^2}{R}$$

Expandiendo esta expresión, encontramos tres componentes físicas transparentes:

$$a_{c} = \underbrace{\frac{\omega_{4D}^2 R_{rot}^2}{R}}_{\text{Gravedad base (Reposó)}} + \underbrace{\frac{2 \omega_{4D} R_{rot} r \dot{\phi} \sin\theta}{R}}_{\text{Efecto Coriolis Hiperdimensional}} + \underbrace{\frac{r^2 \dot{\phi}^2 \sin^2\theta}{R}}_{\text{Corrección Centrífuga Cinética}}$$

---

## ⚗️ 2. ECUACIONES DE MOVIMIENTO EN EL PLANO ORBITAL ($\theta = \pi/2$)

Restringiendo el movimiento al plano ecuatorial de la órbita de un planeta (como Mercurio), donde $\theta = \pi/2$ y $\dot{\theta} = 0$, el Lagrangiano efectivo por unidad de masa de la partícula de prueba bajo el potencial gravitatorio emergente de la membrana es:

$$L = \frac{1}{2} \left( \dot{r}^2 + r^2 \dot{\phi}^2 \right) - V_{eff}(r, \dot{\phi})$$

Donde el potencial efectivo $V_{eff}$ incorpora tanto el pozo de gravedad base (que aproximamos localmente por el potencial Newtoniano $V_N(r) = -G M/r$) como las correcciones por acoplamiento centrífugo derivadas en la sección anterior:

$$V_{eff}(r, \dot{\phi}) = -\frac{G M}{r} \left( 1 + \alpha \frac{r^2 \dot{\phi}^2}{c^2} \right) - 2 \beta \omega_{4D} r^2 \dot{\phi}$$

Donde:
*   $\alpha$: Parámetro adimensional que calibra el acoplamiento de la energía cinética de la órbita con la deformación elástica de la brana.
*   $\beta$: Parámetro adimensional que calibra el arrastre de Coriolis hiperdimensional debido a la rotación cósmica.
*   $c$: Velocidad de la luz (utilizada como escala de normalización de velocidad).

### 2.1. Ecuaciones de Euler-Lagrange
Aplicando las ecuaciones de movimiento $\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}}\right) - \frac{\partial L}{\partial q} = 0$:

#### Para la coordenada angular $\phi$:
Dado que el Lagrangiano no depende explícitamente de $\phi$, la variable conjugada (el momento angular modificado $J$) es una constante del movimiento:

$$J = \frac{\partial L}{\partial \dot{\phi}} = r^2 \dot{\phi} - \frac{\partial V_{eff}}{\partial \dot{\phi}} = r^2 \dot{\phi} \left( 1 + 2 \alpha \frac{G M}{r c^2} \right) + 2 \beta \omega_{4D} r^2$$

A bajas velocidades y con arrastre débil, podemos aproximar la velocidad angular de la órbita como:

$$\dot{\phi} \approx \frac{J - 2 \beta \omega_{4D} r^2}{r^2 \left( 1 + 2 \alpha \frac{G M}{r c^2} \right)}$$

Esto muestra que **el momento angular ya no es una constante Newtoniana simple**: la rotación global del Bulk $\omega_{4D}$ induce un arrastre constante (el término con $\beta$) que obliga a la órbita a precesar.

#### Para la coordenada radial $r$:
La ecuación radial resultante es:

$$\ddot{r} = r \dot{\phi}^2 - \frac{\partial V_{eff}}{\partial r}$$

Sustituyendo el potencial efectivo modificado, obtenemos:

$$\ddot{r} = r \dot{\phi}^2 - \frac{G M}{r^2} - \alpha \frac{G M \dot{\phi}^2}{c^2} + 4 \beta \omega_{4D} r \dot{\phi}$$

Donde:
*   $r \dot{\phi}^2$: Aceleración centrífuga estándar de la órbita 3D.
*   $-\frac{G M}{r^2}$: Fuerza gravitatoria Newtoniana clásica (emergente de la deflexión estática).
*   $-\alpha \frac{G M \dot{\phi}^2}{c^2}$: **Fuerza gravitatoria correctiva de tipo relativista**. Atrae con más fuerza a los cuerpos que se mueven rápido.
*   $4 \beta \omega_{4D} r \dot{\phi}$: **Fuerza de Coriolis hiperdimensional**. Depende de la dirección del giro orbital; si el planeta orbita a favor del giro cósmico experimenta un empuje diferente que si gira en contra.

---

## 🪐 3. MECANISMO DE PRECESIÓN DEL PERIHELIO

En la Relatividad General de Einstein, la precesión del perihelio de Mercurio se explica mediante un término correctivo en el potencial radial de la forma $-G M L^2 / (c^2 r^3)$, lo que causa un desvío acumulativo de:

$$\Delta \phi_{\text{Einstein}} \approx \frac{6 \pi G M}{a (1-e^2) c^2} \text{ radianes por órbita}$$

En nuestra formulación del **Universo Centrífugo**, la precesión emerge de manera natural por dos canales físicos combinados:

1.  **La Corrección Cinética (Término $\alpha$):** Al alterar la fuerza radial de forma proporcional a $\dot{\phi}^2 \propto 1/r^4$, introduce una perturbación de rango ultra-corto en el origen del pozo, imitando de forma exacta el término de Schwarzschild de Einstein.
2.  **El Arrastre Cósmico (Término $\beta$):** El acoplamiento lineal con $\omega_{4D}$ actúa como un campo magnético constante que tuerce la órbita continuamente, generando una precesión constante independiente de la masa del sol central.

Esta formulación dual es sumamente potente, porque permite explicar tanto la precesión relativista de Mercurio (dominada por $\alpha$ cerca del Sol) como anomalías de rotación a gran escala en galaxias (dominadas por $\beta$ en el límite débil cósmico).

---

## 🏆 CRITERIOS DE VALIDACIÓN NUMÉRICA

Para verificar si estas ecuaciones reproducen la precesión observada de Mercurio (aproximadamente **43 segundos de arco por siglo**), diseñaremos una simulación numérica en el siguiente paso con las siguientes metas cuantitativas:

*   **Conservación de Energía**: Las ecuaciones modificadas deben ser numéricamente estables, conservando la energía del sistema integrado (con derivas relativas menores al $10^{-6}$ por órbita).
*   **Aislamiento de la Precesión**: Debemos medir el ángulo del perihelio (punto más cercano al Sol) en cada órbita y demostrar que avanza de manera constante y lineal en el tiempo.
*   **Calibración de Parámetros**: Encontrar la combinación física de $\alpha$ y $\beta$ que mapea con precisión el desvío relativista clásico.
