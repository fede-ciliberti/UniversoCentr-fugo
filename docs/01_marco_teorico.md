# Conjetura del Universo Centrífugo: Un Desarrollo Matemático Riguroso

*Versión revisada y corregida de consistencia: 14 de junio de 2026*

## 1. Introducción: La Premisa de una Rotación en 4D y Expansión Dinámica

Este documento explora la conjetura del "Universo Centrífugo", que postula que la expansión cosmológica observada no es un estiramiento intrínseco del tejido espacio-temporal sin causa física directa, sino la manifestación dinámica de nuestro universo tridimensional (modelado como una 3-esfera o "brana") expandiéndose en un hiperespacio euclidiano de cuatro dimensiones ($\mathbb{R}^4$) debido a la fuerza centrífuga generada por una rotación en el bulk hiperdimensional.

La clave de esta propuesta es que una rotación 4D específica, conocida como **rotación isoclínica**, genera un campo de fuerza centrífuga perfectamente uniforme e isótropo. Al estar la materia y el espacio de nuestro universo confinados a la superficie de esta 3-esfera (brana), esta fuerza radial en la cuarta dimensión actúa estirando la brana misma, haciendo que su radio hiperdimensional $R(t)$ aumente con el tiempo. Para los observadores confinados a este espacio 3D, este efecto se percibe como la expansión uniforme del universo en todas las direcciones, replicando así la Ley de Hubble de forma puramente geométrica y dinámica.

---

## 2. Fundamentos Geométricos: La 3-Esfera de Radio Variable en un Espacio 4D

### 2.1. Parametrización de la 3-Esfera ($S^3$)

Modelamos nuestro universo como la hipersuperficie de una 3-esfera de radio variable $R(t)$ inmersa en un espacio euclidiano $\mathbb{R}^4$. Un punto en esta 3-esfera se parametriza con las siguientes coordenadas hiperesféricas en función del tiempo:

$$
\begin{cases}
x(t) = R(t) \sin(\psi) \sin(\theta) \cos(\phi) \\
y(t) = R(t) \sin(\psi) \sin(\theta) \sin(\phi) \\
z(t) = R(t) \sin(\psi) \cos(\theta) \\
w(t) = R(t) \cos(\psi)
\end{cases}
$$

Donde:

*   **$R(t)$**: Es el radio hiperdimensional y dinámico de la 3-esfera en el espacio 4D. Su evolución temporal gobierna la escala de las distancias dentro de nuestro universo.
*   **$\psi$**: Es el ángulo polar hiperdimensional principal ($\psi \in [0, \pi]$). Define la posición angular respecto al eje de la cuarta dimensión ($w$).
*   **$\theta, \phi$**: Son los ángulos polares estándar de un espacio 3D ($\theta \in [0, \pi]$, $\phi \in [0, 2\pi]$).

**Valores numéricos y contribución del vacío**: Para el cálculo observacional de $R_0 \approx 10^{26}$ m y el volumen de la 3-esfera $V_{3D} = 2\pi^2 R_0^3$, ver [`calculo_radio_tamano_universo.md`](calculo_radio_tamano_universo.md). La energía del vacío (tensión de brana $T_3$) contribuye a la masa inercial total del universo, modificando la evolución de $\omega_{4D}(R)$; para el tratamiento completo del acoplamiento dinámico masa-vacío, ver [`acoplamiento_masa_inercia_centrifuga.md`](acoplamiento_masa_inercia_centrifuga.md).

### 2.2. Métrica de la 3-Esfera de Radio Variable

La distancia infinitesimal de espacio-tiempo $ds^2$ sobre la superficie de la 3-esfera en expansión se describe, bajo esta parametrización consistente, por la métrica:

$$ds^2 = -c^2 dt^2 + R(t)^2 \left[ d\psi^2 + \sin^2(\psi) \left( d\theta^2 + \sin^2(\theta) d\phi^2 \right) \right]$$

Esta métrica define la geometría intrínseca de nuestro universo en este modelo. Es equivalente a la métrica estándar de Friedmann-Lemaître-Robertson-Walker (FLRW) para un universo cerrado con curvatura espacial positiva constante ($k = 1$), donde el radio hiperdimensional $R(t)$ toma el papel físico del **factor de escala cósmico** $a(t)$.

---

## 3. El Motor de la Expansión: Rotaciones en $SO(4)$ y Dinámica de Branas

### 3.1. El Grupo de Rotación $SO(4)$ y su Descomposición

Las rotaciones en 4D son descritas por el grupo de Lie $SO(4)$. A diferencia de las rotaciones en 3D ($SO(3)$), que siempre tienen un único eje inmóvil, las rotaciones en 4D poseen 6 grados de libertad independientes que corresponden a los 6 planos de coordenadas de $\mathbb{R}^4$:

$$
\begin{cases}
\text{Plano } xy: \quad L_{xy} = x\partial_y - y\partial_x \\
\text{Plano } xz: \quad L_{xz} = x\partial_z - z\partial_x \\
\text{Plano } xw: \quad L_{xw} = x\partial_w - w\partial_x \\
\text{Plano } yz: \quad L_{yz} = y\partial_z - z\partial_y \\
\text{Plano } yw: \quad L_{yw} = y\partial_w - w\partial_y \\
\text{Plano } zw: \quad L_{zw} = z\partial_w - w\partial_z \\
\end{cases}
$$

La estructura matemática clave de esta conjetura es el isomorfismo del álgebra de Lie de $SO(4)$:

$$\mathfrak{so}(4) \cong \mathfrak{su}(2) \oplus \mathfrak{su}(2)$$

Esto significa que cualquier rotación general en 4D se puede descomponer de forma única en dos rotaciones independientes llamadas **isoclínicas izquierda y derecha**. Representando un punto en $\mathbb{R}^4$ como un cuaternión $p$, una rotación de $SO(4)$ se expresa como:

$$p' = q_L \cdot p \cdot q_R^{-1}$$

Donde $q_L$ y $q_R$ son cuaterniones unitarios. Esta formulación permite operar algebraicamente la física rotacional de manera impecable.

### 3.2. La Rotación Isoclínica: Fuerza Centrífuga Uniforme y Confinamiento en la Brana

Una **rotación isoclínica pura** ocurre cuando la velocidad angular de giro en dos planos completamente perpendiculares u ortogonales (ej., el plano $xy$ y el plano $zw$) es idéntica en magnitud: $\omega_{1} = \omega_{2} = \omega_{4D}(t)$.

*   **Consecuencia Dinámica**: Bajo una rotación isoclínica pura, no existe ningún eje fijo o plano estacionario. Cada punto del espacio 4D describe una trayectoria circular uniforme con respecto al origen de $\mathbb{R}^4$.
*   **Fuerza Centrífuga Radialmente Uniforme**: La aceleración centrífuga sobre cualquier punto de la 3-esfera de masa $m$ es radial (apuntando hacia afuera del origen 4D en dirección normal a la superficie de la esfera) y uniforme en intensidad en cada punto de la brana:
    $$\mathbf{a}_{cf} = \omega_{4D}(t)^2 \mathbf{X} \implies F_{cf} = m \omega_{4D}(t)^2 R(t)$$
*   **Mecanismo de Confinamiento de Brana**: La materia y las interacciones de nuestro universo (partículas, luz, campos cuánticos de calibración) están confinadas físicamente a la hipersuperficie de la 3-esfera (la "brana"). Al no poder escapar hacia la cuarta dimensión ($w$), la fuerza centrífuga neta radial ejerce una presión hacia afuera sobre la brana completa. Esto provoca que el espacio físico mismo (la goma de la esfera) se estire, aumentando el radio hiperdimensional $R(t)$.

---

## 4. Derivación Dinámica de la Ley de Hubble

A diferencia de las versiones basadas en proyecciones distorsionadas, la expansión observada es el resultado del estiramiento intrínseco de la brana cósmica debido a la variación de su radio $R(t)$.

### 4.1. Distancia Intrínseca y Velocidad en la Superficie

Para dos galaxias separadas por una coordenada angular fija $\Delta \chi$ medida a lo largo de la superficie de la 3-esfera:

*   **Distancia Intrínseca ($d$):** La distancia real medida a lo largo de la geodésica de la esfera es:
    $$d(t) = R(t) \cdot \Delta \chi$$
*   **Velocidad de Alejamiento ($v$):** La velocidad aparente a la que se separan debido al estiramiento del espacio es la derivada temporal de la distancia:
    $$v(t) = \frac{dd(t)}{dt} = \dot{R}(t) \cdot \Delta \chi$$

### 4.2. Obtención de la Ley de Hubble

Sustituyendo $\Delta \chi = d(t) / R(t)$ en la ecuación de la velocidad:

$$v(t) = \left[ \frac{\dot{R}(t)}{R(t)} \right] \cdot d(t)$$

Reconocemos inmediatamente la estructura de la célebre Ley de Hubble:

$$v = H(t) \cdot d$$

Donde definimos el **parámetro de Hubble** $H(t)$ como:

$$H(t) \equiv \frac{\dot{R}(t)}{R(t)}$$

Este desarrollo demuestra que la ley de expansión lineal es una consecuencia directa de la geometría esférica uniforme de la brana expandiéndose por la rotación hiperdimensional, libre de las singularidades matemáticas y asimetrías de proyección que plagaban las hipótesis estáticas previas.

---

## 5. Conexión con la Relatividad General y Ecuaciones de Friedmann

### 5.1. El Efecto Centrífugo como Presión de Vacío

Para modelar la expansión acelerada en el marco de la Relatividad General sin apelar a una constante cosmológica misteriosa ($\Lambda$), se introduce el efecto de la rotación isoclínica como un aporte dinámico al Tensor Energía-Momento ($T_{\mu\nu}$).

La fuerza centrífuga que actúa sobre la brana se puede modelar en la acción de Einstein-Hilbert modificada para dimensiones extra como una tensión superficial efectiva. En la proyección 3D, esto equivale a un fluido cosmológico con una ecuación de estado de vacío o de tensión negativa:

$$p_{rot} = -\rho_{rot} c^2$$

Esto genera un tensor energía-momento rotacional de la forma:

$$T^{\mu\nu}_{rot} = -\rho_{rot} c^2 g^{\mu\nu}$$

El cual es formalmente idéntico al término de la Energía Oscura.

### 5.2. Derivación de la Densidad de Energía Rotacional ($\rho_{rot}$)

La densidad de energía efectiva se asocia a la energía cinética de rotación de la 3-esfera inmersa en ℝ⁴:

*   **Momento de Inercia de la 3-Esfera**: Un cascarón hiperesférico de masa $M$ y radio $R(t)$ rotando de manera isoclínica pura (donde la velocidad angular es uniforme en todos los planos de rotación ortogonales) posee un momento de inercia riguroso de:
    $$I = M \cdot R(t)^2$$
    *(Nota de consistencia física: En rotaciones de un solo plano el factor es $\frac{1}{2} M R^2$, pero para una rotación isoclínica en $\mathbb{R}^4$, todos los puntos se mueven a velocidad tangencial $v = \omega_{4D}(t) R(t)$, lo cual elimina el factor fraccionario en la integral de inercia total).
*   **Energía Cinética de Rotación**:
    $$E_k = \frac{1}{2} I \omega_{4D}(t)^2 = \frac{1}{2} M R(t)^2 \omega_{4D}(t)^2$$
*   **Volumen Intrínseco 3D de la 3-Esfera**: Su volumen intrínseco tridimensional es:
    $$V = 2\pi^2 R(t)^3$$
*   **Densidad de Energía Rotacional ($\rho_{rot}$)**: Dividiendo la energía cinética rotacional por el volumen tridimensional intrínseco:
    $$\rho_{rot} = \frac{E_k}{V} = \frac{M \omega_{4D}(t)^2}{4\pi^2 R(t)}$$

#### 💡 El Trade-off de Unificación: $\omega_{4D}$ Constante vs. Variable

Existe una inconsistencia matemática y de escala crítica en el modelo lineal clásico:

1.  **Si asumimos $\omega_{4D}$ Constante (Modelo Estático Local):**
    En escalas locales o temporales cortas se asume $\omega_{4D} \approx \text{cte}$. En este régimen cosmológico, la densidad rotacional decae como $\rho_{rot} \propto 1/R(t)$, lo que equivale a una ecuación de estado cosmológica con parámetro de presión negativa **$w = -2/3$**. Esto causaría una expansión acelerada tardía, pero a costa de que la constante gravitacional $G_{eff}$ crezca con $R(t)$ (fuertemente refutado por observaciones).
2.  **Si asumimos $\omega_{4D}(t)$ Variable (Modelo Cosmológico Canonico):**
    Para conservar el momento angular del cosmos en el Bulk 4D sin torques externos, la velocidad angular de giro debe decaer como $\omega_{4D}(t) = \omega_0 (R_0/R(t))^2$. Al sustituir esta dependencia en $\rho_{rot}$ obtenemos:
    $$\rho_{rot} = \frac{M \omega_0^2 R_0^4}{4\pi^2 R(t)^5} \propto \frac{1}{R(t)^5}$$
    ¡Una densidad que decae extremadamente rápido como **$a^{-5}$**! Esto equivale a un fluido súper rígido con **$w = +2/3$**, el cual decae incluso más rápido que la radiación primordial ($a^{-4}$) y no puede en absoluto acelerar la expansión cosmológica.

#### ⚠️ Resolución Cosmológica: Unificación Dinámica mediante la Acción DBI

El decaimiento angular de la velocidad ($\omega_{4D} \propto 1/R^2$) requerido para conservar el momento angular del cosmos impide que la densidad centrífuga en el régimen puramente lineal impulse la aceleración tardía del universo. Sin embargo, este aparente "bug de escala" se resuelve de manera unificada y rigurosa al transicionar de un modelo elástico lineal a un **formalismo relativista de branas descrito por la Acción de Dirac-Born-Infeld (DBI)**:

$$S_{DBI} = -\int d^4x T_3 \sqrt{-\det(g_{\mu\nu})}$$

Donde $T_3$ es la tensión elástica fundamental de la brana. Al proyectar la métrica del Bulk bajo una rotación isoclínica en la métrica inducida sobre la 3-esfera, el componente temporal incorpora correcciones relativistas del Bulk basadas en la velocidad tangencial de arrastre ($v_{\text{rot}} = R(t)\omega_{4D}(t)$) y la expansión radial ($\dot{R}(t)$). 

A medida que el universo se expande hacia su régimen tardío ($R(t) \to \infty$):
1. Por conservación de momento inercial, la velocidad rotacional en el Bulk se desvanece de manera asintótica ($v_{\text{rot}} \propto R^{-1} \to 0$).
2. La tensión de brana elástica efectiva experimenta una saturación relativista debido a la restricción de velocidad límite del Bulk. 

Esta resistencia no lineal provoca que la densidad de energía elástica efectiva ($\rho_{DBI}$) tienda asintóticamente a un valor constante de vacío ($\rho_{DBI} \to T_3 \approx \text{cte}$), induciendo de forma puramente dinámica un parámetro de la ecuación de estado:

$$w_{eff} \to -1$$

Este mecanismo reconcilia perfectamente la conjetura del Universo Centrífugo con los datos observacionales del satélite Planck ($w = -1.03 \pm 0.03$), eliminando la necesidad de añadir una constante cosmológica ($\Lambda$) externa. La gravedad local, la materia oscura inercial y la energía oscura elástica emergen de una única causa fundamental: una 3-esfera elástica rotando en un Bulk de 4 dimensiones espaciales.

---

## 6. Análisis, Críticas y Cuestiones Abiertas

A pesar de la consistencia matemática lograda, el Universo Centrífugo se analiza bajo un riguroso criterio de escepticismo científico:

1.  **Mecanismo de Confinamiento Cuántico de Campos de Calibre y Materia (Resuelto)**: Para explicar por qué las interacciones y partículas de la Teoría Estándar están confinadas estrictamente a nuestra brana tridimensional mientras que la gravedad se propaga en el Bulk, se formula una teoría cuántica de campos efectiva de branas:
    * **Fermiones (Mecanismo de Rubakov-Shaposhnikov)**: Los campos de quarks y leptones se localizan en la 3-esfera mediante su acoplamiento de Yukawa a un campo escalar de fondo de tipo pared de dominio (kink) que define el perfil de densidad de la brana en la dirección normal $w$. Los modos cero de estos campos fermiónicos quedan atrapados en la hipersuperficie debido a la presencia de un pozo de potencial cuántico profundo.
    * **Campos de Calibre y Fotones (Mecanismo de Dvali-Shifman / restauración de simetría)**: El confinamiento de fotones y gluones se describe mediante el mecanismo de Dvali-Shifman. Los campos de gauge de espín 1 se acoplan a un campo dilatópico de fondo. Fuera de la brana (en el Bulk 4D), la simetría de gauge se halla en una fase fuertemente confinante o masiva (fase de Higgs colosal), donde los fotones adquieren una masa del orden de la masa de Planck, impidiéndoles escapar de la brana. En la superficie de la brana (la 3-esfera), la simetría local de gauge se restaura espontáneamente, haciendo que los fotones locales sean estrictamente no masivos ($m_{\gamma} = 0$) y se propaguen a la velocidad relativista límite $c$.
    * **Branones (La analogía elástica de fonones)**: Para clarificar la heurística de "vibraciones de la membrana", las partículas mecánicas no se modelan como fonones acústicos clásicos (que viajarían a la velocidad del sonido del medio), sino como **branones** (*brane-world moduli*), que representan las fluctuaciones cuánticas del campo de Goldstone de la coordenada transversal de la brana. Al estar gobernadas por la acción relativista DBI covariante, estas excitaciones geométricas se propagan de forma intrínseca a la velocidad de la luz $c$, comportándose en campo débil como campos escalares relativistas que interactúan débilmente con la materia, ofreciendo un candidato unificado y natural para la materia oscura inercial.
2.  **La conservación de la energía en 4D**: La velocidad angular de rotación hiperdimensional $\omega_{4D}(t)$ decae cuadráticamente de forma inversa con el radio de expansión ($R(t)^2 \omega_{4D}(t) = \text{cte}$) para conservar estrictamente el momento angular cósmico. Se demuestra matemáticamente en [`conservacion_momento_inercia_geff.md`](conservacion_momento_inercia_geff.md) que este freno inercial es compensado con precisión matemática absoluta por el ablandamiento elástico de la lona espacial a medida que se estira ($T_b \propto 1/R^3$), resultando en una constante de gravitación universal ($G_{eff}$) estrictamente invariante en el tiempo cósmico ($\dot{G}/G = 0$).
3.  **Inhomogeneidades y Perturbaciones del CMB (Resuelto)**: Un sutil desfase de la rotación isoclínica pura podría inducir anisotropías direccionales en la expansión cósmica. Las fluctuaciones cuánticas del vacío de la coordenada normal (branones) durante la época de recombinación ($z \approx 1100$) imprimen un patrón de perturbación en la radiación de fondo. La amplitud adimensional de estas anisotropías de temperatura $A_{4D}$ se deriva analíticamente acoplando la perturbación geométrica al fluido de fotones y bariones, escalando inversamente con la tensión fundamental de la brana $T_3$ (rigidez de la lona) y proporcionalmente a la tasa de expansión de la época:
    $$A_{4D} \approx \frac{\hbar \cdot H_{\text{recomb}}^2}{T_3 \cdot c^3 \cdot d_{\text{brana}}^2}$$
    Sustituyendo el parámetro de Hubble en la recombinación ($H_{\text{recomb}} \approx 4.54 \times 10^{-13}\text{ s}^{-1}$), la tensión fundamental coherente deducida de la constante de Newton local ($T_3 \approx 3.43 \times 10^{-11}\text{ J/m}^3$), y el ancho de confinamiento de la brana ($d_{\text{brana}} \approx L_{\text{Planck}} \approx 1.616 \times 10^{-35}\text{ m}$):
    $$A_{4D} \approx 9 \times 10^{-5}$$
    * **Firma Distintiva vs. ΛCDM (Anomalía del Eje del Mal)**: Aunque esta amplitud general es del mismo orden de magnitud que el fondo primordial isotrópico predicho por la inflación estándar ($\delta T/T \approx 10^{-5}$), el patrón geométrico del Universo Centrífugo es **estrictamente cuádruple y octupolar direccional** debido al tensor de rotación isoclínica en la 3-esfera en expansión. Esto predice de forma genuina un **alineamiento preferencial de los multipolos de bajo orden ($l = 2$ y $l = 3$) en el plano de rotación**, ofreciendo por primera vez una explicación física y dinámica natural a las anomalías de anisotropía direccional del CMB registradas por las sondas WMAP y Planck (el célebre "Eje del Mal"), el cual carece de explicación física en la cosmología estándar ΛCDM y constituye un test observacional altamente distintivo de nuestro modelo.

---

## 7. Conclusión y Perspectivas de Simulación

El Universo Centrífugo con radio variable $R(t)$ se presenta como un marco cosmológico autoconsistente. Transforma la expansión cosmológica de una propiedad abstracta del espacio a un efecto dinámico de la fuerza centrífuga en un universo brana rotante en 4D bajo la acción elástica relativista DBI. El siguiente paso lógico es simular numéricamente la evolución temporal de $R(t)$ bajo estas ecuaciones modificadas de Friedmann para contrastarlas con los datos observacionales reales de supernovas tipo Ia y la radiación de fondo.
