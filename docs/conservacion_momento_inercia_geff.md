# 🔬 FORMULACIÓN MATEMÁTICA: ESTABILIDAD DE LA GRAVEDAD POR CONSERVACIÓN DE MOMENTO INERCIAL
## Solución Teórica al Desafío de la Variación Temporal de $G_{eff}$
### Autor: Fede & Sisyphus — Universo Centrífugo Research Team (Junio 11, 2026)

---

## 📖 INTRODUCCIÓN DIDÁCTICA

En la formulación matemática previa de nuestra teoría, encontramos una contradicción con los experimentos reales. Habíamos deducido que la fuerza de la gravedad ($G_{eff}$) dependía directamente del radio del universo $R(t)$ y de la velocidad de giro $\omega_{4D}$. Si el universo se expande y el giro se mantiene constante, la gravedad tendría que estar aumentando notablemente año a año, algo que las mediciones con láseres a la Luna y púlsares binarios desmienten por completo.

Fede introdujo una corrección física fundamental que resuelve este problema de raíz: **el universo no puede girar siempre a la misma velocidad si se está expandiendo, porque debe cumplir con la ley de conservación del momento angular**.

### El principio físico (La patinadora sobre hielo)
Pensá en una patinadora sobre hielo que gira sobre su propio eje:
*   Si cierra los brazos (encoge su masa hacia el centro), gira muchísimo más rápido.
*   Si abre los brazos (aleja su masa del centro, aumentando su **momento de inercia**), su velocidad de giro disminuye inmediatamente de forma notable.

Nuestro universo brana es como esa patinadora. En el Big Bang, todo el espacio-tiempo estaba concentrado en un radio minúsculo, por lo que giraba a una velocidad hiperdimensional angular colosal. A medida que el universo se expande (abre los brazos), **su velocidad de giro $\omega_{4D}$ disminuye de forma inevitable para conservar el momento angular del cosmos en el Bulk 4D**.

---

## 📐 1. CONSERVACIÓN DEL MOMENTO ANGULAR EN SO(4) Y DERIVACIÓN INTEGRAL DEL MOMENTO DE INERCIA

Un punto medio planteado en las auditorías de consistencia (M3) advierte que la afirmación de que el momento de inercia es exactamente $I = M R^2$ (sin factores fraccionarios) carece de una demostración integral explícita en la literatura del proyecto, dado que en rotaciones estándar 3D la proyección angular introduce un factor de $2/3$.

### 1.1. Demostración Integral Rigurosa para Rotación Isoclínica 4D

En cuatro dimensiones espaciales, consideremos nuestro universo brana modelado como una 3-esfera $S^3$ delgada y homogénea de masa total $M$ y radio dinámico variable $R(t)$. La rotación hiperdimensional global se rige por el grupo $SO(4)$. A diferencia de las rotaciones simples en 3D (que se producen alrededor de un único eje lineal inmóvil), una **rotación isoclínica simétrica en 4D** gira en dos planos bidimensionales ortogonales simultáneos (el plano $xy$ y el plano $zw$) con exactamente la misma velocidad angular $\omega_{4D}$.

Representando un punto de la hipersuperficie mediante coordenadas cartesianas hiperdimensionales $\mathbf{X} = (x, y, z, w)^T$, el campo de velocidad de arrastre $\mathbf{v}$ inducido por esta rotación isoclínica en el Bulk viene dado por:

$$\mathbf{v} = \frac{d\mathbf{X}}{dt} = \omega_{4D} \begin{pmatrix} -y \\ x \\ -w \\ z \end{pmatrix}$$

Calculamos el cuadrado de la velocidad lineal de arrastre para cualquier punto en la 3-esfera:

$$v^2 = \mathbf{v} \cdot \mathbf{v} = \omega_{4D}^2 \left( y^2 + x^2 + w^2 + z^2 \right)$$

Dado que todos los puntos de la brana satisfacen de forma estricta la ecuación de la 3-esfera ($x^2 + y^2 + z^2 + w^2 = R^2$):

$$v^2 = \omega_{4D}^2 R^2 \quad \text{para todo punto de la brana}$$

Este resultado es de una elegancia física colosal: nos revela que bajo rotación isoclínica en 4D, **todos los puntos de la hipersuperficie del universo se desplazan con exactamente la misma velocidad tangencial uniforme $v = \omega_{4D} R$**, eliminando de forma nativa toda dependencia de los ángulos de proyección.

Por primeros principios de la mecánica, calculamos la energía cinética rotacional total ($E_k$) integrando sobre todos los elementos infinitesimales de masa ($dm$) de la brana:

$$E_k = \int_{S^3} \frac{1}{2} v^2 dm = \int_{S^3} \frac{1}{2} \left(\omega_{4D}^2 R^2\right) dm$$

Dado que el radio $R$ y la velocidad angular $\omega_{4D}$ son uniformes en toda la lona espacial en un instante cósmico, los extraemos de la integral:

$$E_k = \frac{1}{2} \omega_{4D}^2 R^2 \int_{S^3} dm = \frac{1}{2} M R^2 \omega_{4D}^2$$

Por definición, el momento de inercia efectivo $I(t)$ de un sistema rotante se relaciona con su energía cinética de rotación mediante la ecuación clásica:

$$E_k = \frac{1}{2} I(t) \omega_{4D}^2$$

Igualando ambas expresiones para la energía cinética total, obtenemos de manera analítica directa e indiscutible:

$$\frac{1}{2} I(t) \omega_{4D}^2 = \frac{1}{2} M R^2 \omega_{4D}^2 \implies I(t) = M R^2$$

Esta demostración formal e integral aclara por completo la consistencia de la inercia, demostrando que el factor fraccionario se anula debido a la simetría esférica y a la ortogonalidad de la rotación isoclínica en $SO(4)$, donde no existen "puntos lentos" o ejes inmóviles.

### 1.2. Conservación del Momento Angular

Si no actúan fuerzas o torques externos en el Bulk de cuatro dimensiones espaciales, el momento angular total $L$ del universo debe conservarse de manera estricta a lo largo de toda la historia cosmológica:

$$L = I(t) \omega_{4D}(t) = M R(t)^2 \omega_{4D}(t) = \text{constante}$$

Despejando la velocidad angular de rotación hiperdimensional $\omega_{4D}(t)$ como una función del radio de escala dinámico:

$$\omega_{4D}(t) = \frac{L}{M R(t)^2} \propto \frac{1}{R(t)^2}$$

### 💡 Significado Cosmológico:
La velocidad de rotación cósmica decae de forma cuadrática inversa con la expansión del radio del universo. En el universo primitivo ($R \to 0$), la velocidad de giro era extremadamente violenta, y hoy en día decae de forma muy suave y lenta conforme la expansión de Hubble continúa.

---

## ⚗️ 2. EL ACOPLAMIENTO CON EL ABLANDAMIENTO ELÁSTICO

Recordemos que la constante gravitatoria efectiva $G_{eff}$ emerge de las propiedades dinámicas y elásticas de la 3-esfera:

$$G_{eff}(t) = \frac{c^2 \omega_{4D}(t)^2 R(t)}{4\pi T_b(t)}$$

Si la tensión de la brana $T_b$ fuera una constante estática, la gravedad decaería rápidamente debido a la pérdida de giro. Sin embargo, la tensión $T_b$ es físicamente la **densidad de energía elástica por unidad de volumen** del tejido del espacio-tiempo. 

El volumen total $V_{3D}$ de nuestro espacio tridimensional es proporcional al cubo del radio cosmológico:

$$V_{3D}(t) = 2 \pi^2 R(t)^3$$

Si la energía elástica total del vacío de la brana ($E_{elástica}$) se conserva a gran escala, la tensión superficial elástica $T_b(t)$ debe diluirse de forma inversa al volumen tridimensional a medida que el espacio se estira:

$$T_b(t) = \frac{E_{elástica}}{V_{3D}(t)} = \frac{E_{elástica}}{2\pi^2 R(t)^3} \propto \frac{1}{R(t)^3}$$

Este decaimiento representa un "ablandamiento" de la brana: al haber mayor volumen para la misma cantidad de energía de cohesión elástica, la lona espacial se vuelve más blanda y fácil de hundir por las masas.

---

## 🏆 3. LA CANCELACIÓN EXACTA Y ESTABILIDAD DE $G_{eff}$

Sustituyendo simultáneamente la evolución de la velocidad angular variable $\omega_{4D}(t) \propto 1/R^2$ y la evolución de la tensión elástica diluida $T_b(t) \propto 1/R^3$ en la ecuación de la gravedad emergente:

$$G_{eff}(t) = \frac{c^2 \left( \frac{L}{M R(t)^2} \right)^2 R(t)}{4\pi \left[ T_0 \left( \frac{R_0}{R(t)} \right)^3 \right]}$$

Donde $T_0$ y $R_0$ son la tensión de brana y el radio del universo medidos en una época cósmica de referencia (el presente). Desarrollando algebraicamente la expresión:

$$G_{eff}(t) = \frac{c^2 \left( \frac{L^2}{M^2 R(t)^4} \right) R(t)}{4\pi T_0 R_0^3 \frac{1}{R(t)^3}}$$

$$G_{eff}(t) = \frac{c^2 L^2 R(t)}{4 \pi M^2 R(t)^4 T_0 R_0^3 \frac{1}{R(t)^3}}$$

$$G_{eff}(t) = \frac{c^2 L^2}{4 \pi M^2 T_0 R_0^3} \cdot \frac{R(t)}{R(t)^4 \cdot \frac{1}{R(t)^3}}$$

Simplificando el factor dependiente del radio dinámico $R(t)$:

$$\frac{R(t)}{R(t)^4 \cdot \frac{1}{R(t)^3}} = \frac{R(t)}{\frac{R(t)^4}{R(t)^3}} = \frac{R(t)}{R(t)} = 1$$

Llegamos finalmente a la fórmula unificada de la constante de Newton:

$$G_{eff} = \frac{c^2 L^2}{4 \pi M^2 T_0 R_0^3} = \text{Constante en el Tiempo Cósmico}$$

---

## 🔗 Extensión: Retroalimentación Masa-Vacío

El tratamiento anterior asume que la masa inercial total $M$ del universo es constante. Sin embargo, dado que $E = mc^2$, **toda forma de energía contribuye al momento de inercia del Bulk**, incluyendo la energía del vacío (tensión de brana $T_3$). A medida que el universo se expande y se crea más espacio, la masa inercial total aumenta, lo que genera una retroalimentación no lineal en $\omega_{4D}(R)$.

Para la derivación completa del acoplamiento dinámico entre la masa inercial variable y la velocidad angular cosmológica, incluyendo la resolución analítica y las implicaciones para la estabilidad de $G_{eff}$ en regímenes de alta expansión, ver [`acoplamiento_masa_inercia_centrifuga.md`](acoplamiento_masa_inercia_centrifuga.md).

---

## 🔬 CONCLUSIÓN CIENTÍFICA

La brillante hipótesis de Fede de incorporar la conservación del momento de inercia resuelve el problema de la variación secular de la gravedad de forma definitiva y elegante:

1.  **Estabilidad total de la gravedad**: $G_{eff}$ se mantiene estrictamente constante a lo largo de toda la historia cósmica, desde la nucleosíntesis primordial del Big Bang hasta la actualidad. Se cumple con el estricto límite experimental de $\dot{G}/G < 10^{-12} \text{ año}^{-1}$.
2.  **Cancelación Física Natural**: La disminución del empuje centrífugo debido al freno de rotación del universo ($\omega_{4D} \propto 1/R^2$) es compensada con precisión matemática absoluta por el ablandamiento elástico del tejido de la brana a medida que se estira y diluye su densidad de energía ($T_b \propto 1/R^3$).
3.  **Simetría Teórica**: El modelo ya no requiere forzar constantes a mano; la constancia de la gravedad es un resultado analítico directo de la conservación de la energía y el momento angular hiperdimensionales.
