# Formalismo Geométrico Riguroso v2.0: Reconstrucción desde Primeros Principios

**Opción B: Cirugía Mayor — Sin parámetros ad-hoc**

*Fecha: 16 de junio de 2026*

---

## Resumen Ejecutivo

Este documento reconstruye la teoría de Coriolis 4D desde un formalismo geométrico riguroso, eliminando los parámetros adimensionales ad-hoc (α, β, A₄D) de la formulación v1.0. Se deriva todo index-algebraicamente desde la métrica del Bulk y la inmersión de la brana, sin ajuste libre alguno.

**Resultado central**: La métrica inducida sobre la brana NO es la métrica FLRW estándar. Es una métrica FLRW modificada por términos de arrastre (frame-dragging) provenientes de la rotación isoclínica. Estos términos son análogos al g_{tφ} de la métrica de Kerr y producen naturalmente fuerzas de Coriolis y centrífuga a través de la conexión de Levi-Civita — **sin necesidad de torsión ni de parámetros libres**.

**Advertencia honesta**: La magnitud cosmológica de ω₄D es demasiado pequeña (~H₀) para explicar los tests clásicos de GR (precesión de Mercurio, deflexión de la luz). Estos efectos requieren un mecanismo adicional — la deformación elástica local h(r) de la brana — que no se deriva del formalismo de inmersión pura aquí presentado.

---

## Paso 1: Métrica del Bulk en Coordenadas Rotantes

### 1.1. Espacio-tiempo del Bulk

El Bulk es un espacio-tiempo plano de 5 dimensiones (1 temporal + 4 espaciales) con signatura (−, +, +, +, +). En coordenadas inerciales (t, x, y, z, w), la métrica es:

$$ds^2_{\text{Bulk}} = -c^2 dt^2 + dx^2 + dy^2 + dz^2 + dw^2$$

### 1.2. Rotación isoclínica

Una rotación isoclínica izquierda pura en SO(4) gira simultáneamente en dos planos ortogonales — el plano xy y el plano zw — con la misma velocidad angular ω₄D(t). La transformación de coordenadas del marco rotante (X, Y, Z, W) al marco inercial (x, y, z, w) es:

$$x = X\cos(\omega t) - Y\sin(\omega t)$$
$$y = X\sin(\omega t) + Y\cos(\omega t)$$
$$z = Z\cos(\omega t) - W\sin(\omega t)$$
$$w = Z\sin(\omega t) + W\cos(\omega t)$$

donde escribimos ω ≡ ω₄D(t) para aligerar la notación. El parámetro ω₄D es función del tiempo cósmico por conservación del momento angular: ω₄D(t) = L/(MR²) ∝ 1/R(t)².

### 1.3. Cálculo explícito de la métrica rotante

Calculamos los diferenciales:

$$dx = \cos(\omega t)\,dX - \sin(\omega t)\,dY - \omega\left[X\sin(\omega t) + Y\cos(\omega t)\right]dt$$

$$dy = \sin(\omega t)\,dX + \cos(\omega t)\,dY + \omega\left[X\cos(\omega t) - Y\sin(\omega t)\right]dt$$

$$dz = \cos(\omega t)\,dZ - \sin(\omega t)\,dW - \omega\left[Z\sin(\omega t) + W\cos(\omega t)\right]dt$$

$$dw = \sin(\omega t)\,dZ + \cos(\omega t)\,dW + \omega\left[Z\cos(\omega t) - W\sin(\omega t)\right]dt$$

**Cálculo de dx² + dy²**: Expandimos y usamos cos²(ωt) + sin²(ωt) = 1. Los términos cruzados dX·dY se cancelan exactamente. Los términos cruzados con dt se simplifican usando identidades trigonométricas:

- **Término dX·dt**: El coeficiente es −2ωY (los términos en X·sin·cos se cancelan)
- **Término dY·dt**: El coeficiente es +2ωX
- **Término dt²**: ω²(X² + Y²)

Resultado:

$$dx^2 + dy^2 = dX^2 + dY^2 + \omega^2(X^2 + Y^2)\,dt^2 - 2\omega Y\,dX\,dt + 2\omega X\,dY\,dt$$

**Cálculo de dz² + dw²**: Por la misma estructura (rotación idéntica en el plano zw):

$$dz^2 + dw^2 = dZ^2 + dW^2 + \omega^2(Z^2 + W^2)\,dt^2 - 2\omega W\,dZ\,dt + 2\omega Z\,dW\,dt$$

### 1.4. Métrica del Bulk en coordenadas rotantes

Sumando todos los términos:

$$\boxed{ds^2_{\text{Bulk}} = \left[-c^2 + \omega^2(X^2 + Y^2 + Z^2 + W^2)\right]dt^2 + dX^2 + dY^2 + dZ^2 + dW^2 + 2\omega\left(-Y\,dX + X\,dY - W\,dZ + Z\,dW\right)dt}$$

**Componentes métricas explícitas**:

| Componente | Valor |
|---|---|
| g_{tt} | −c² + ω²(X² + Y² + Z² + W²) |
| g_{tX} = g_{Xt} | −ωY |
| g_{tY} = g_{Yt} | +ωX |
| g_{tZ} = g_{Zt} | −ωW |
| g_{tW} = g_{Wt} | +ωZ |
| g_{XX} = g_{YY} = g_{ZZ} = g_{WW} | 1 |
| Todo otro g_{ij} | 0 |

**Interpretación física**:

- El término ω²ρ²dt² (con ρ² = X² + Y² + Z² + W²) es la **contribución centrífuga** a g_{tt}: modifica el "ritmo del tiempo" para observadores en rotación.
- Los términos cruzados g_{tμ} son los **términos de arrastre** (Coriolis): representan el frame-dragging isoclínico, análogos al g_{tφ} de Kerr pero extendidos a 4 dimensiones espaciales.
- La parte espacial g_{ij} = δ_{ij} permanece plana — la rotación no curva el espacio, solo introduce arrastre temporal.

Los términos de arrastre se pueden escribir como la 2-forma de momento angular isoclínica:

$$2\omega\,dt \cdot \left(\underbrace{X\,dY - Y\,dX}_{L_{xy}} + \underbrace{Z\,dW - W\,dZ}_{L_{zw}}\right)$$

donde L_{xy} y L_{zw} son las 2-formas de momento angular en los planos xy y zw respectivamente.

---

## Paso 2: Inmersión de la Brana

### 2.1. Parametrización de la 3-esfera

La brana es una 3-esfera S³ de radio dinámico R(t), inmersa en el Bulk. Usamos coordenadas hiperesféricas (ψ, θ, φ) con ψ ∈ [0, π], θ ∈ [0, π], φ ∈ [0, 2π]:

$$X = R(t)\sin\psi\sin\theta\cos\phi$$
$$Y = R(t)\sin\psi\sin\theta\sin\phi$$
$$Z = R(t)\sin\psi\cos\theta$$
$$W = R(t)\cos\psi$$

**Verificación**: X² + Y² + Z² + W² = R(t)²(sin²ψ sin²θ cos²φ + sin²ψ sin²θ sin²φ + sin²ψ cos²θ + cos²ψ) = R(t)²(sin²ψ + cos²ψ) = R(t)² ✓

### 2.2. Vectores tangentes

Las derivadas parciales de la inmersión definen la base tangente de la brana:

**Derivadas respecto al tiempo** (expansión de la brana):

$$\frac{\partial X}{\partial t} = \dot{R}\sin\psi\sin\theta\cos\phi, \quad \frac{\partial Y}{\partial t} = \dot{R}\sin\psi\sin\theta\sin\phi$$
$$\frac{\partial Z}{\partial t} = \dot{R}\sin\psi\cos\theta, \quad \frac{\partial W}{\partial t} = \dot{R}\cos\psi$$

**Derivadas respecto a ψ** (latitud hiperesférica):

$$\frac{\partial X}{\partial\psi} = R\cos\psi\sin\theta\cos\phi, \quad \frac{\partial Y}{\partial\psi} = R\cos\psi\sin\theta\sin\phi$$
$$\frac{\partial Z}{\partial\psi} = R\cos\psi\cos\theta, \quad \frac{\partial W}{\partial\psi} = -R\sin\psi$$

**Derivadas respecto a θ** (colatitud estándar):

$$\frac{\partial X}{\partial\theta} = R\sin\psi\cos\theta\cos\phi, \quad \frac{\partial Y}{\partial\theta} = R\sin\psi\cos\theta\sin\phi$$
$$\frac{\partial Z}{\partial\theta} = -R\sin\psi\sin\theta, \quad \frac{\partial W}{\partial\theta} = 0$$

**Derivadas respecto a φ** (azimut):

$$\frac{\partial X}{\partial\phi} = -R\sin\psi\sin\theta\sin\phi, \quad \frac{\partial Y}{\partial\phi} = R\sin\psi\sin\theta\cos\phi$$
$$\frac{\partial Z}{\partial\phi} = 0, \quad \frac{\partial W}{\partial\phi} = 0$$

---

## Paso 3: Métrica Inducida (Primera Forma Fundamental)

### 3.1. Método de cálculo

La métrica inducida se obtiene por pullback de la métrica del Bulk:

$$g_{ab} = g_{\mu\nu}\frac{\partial X^\mu}{\partial x^a}\frac{\partial X^\nu}{\partial x^b}$$

donde x^a = (t, ψ, θ, φ) son coordenadas de la brana y X^μ = (t, X, Y, Z, W) son coordenadas del Bulk.

Descomponemos: g_{μν} = η_{μν} + h_{μν}, donde η_{μν} = diag(−c², 1, 1, 1, 1) es la métrica de Minkowski plana y h_{μν} son las correcciones por rotación.

### 3.2. Parte estándar (sin rotación): métrica FLRW

La parte η_{μν} da la métrica inducida estándar de una 3-esfera en expansión:

**g_{tt}^(0)**: La velocidad de expansión es uniforme:

$$\left(\frac{\partial X}{\partial t}\right)^2 + \left(\frac{\partial Y}{\partial t}\right)^2 + \left(\frac{\partial Z}{\partial t}\right)^2 + \left(\frac{\partial W}{\partial t}\right)^2 = \dot{R}^2$$

(por la identidad sin²ψ sin²θ + sin²ψ cos²θ + cos²ψ = 1)

Por lo tanto: g_{tt}^{(0)} = −c² + Ṙ²

**g_{tψ}^(0)**: Verificamos ortogonalidad:

$$g_{t\psi}^{(0)} = \sum_i \frac{\partial X^i}{\partial t}\frac{\partial X^i}{\partial\psi} = \dot{R}R\cos\psi\sin\psi\left[\sin^2\theta\cos^2\phi + \sin^2\theta\sin^2\phi + \cos^2\theta\right] - \dot{R}R\cos\psi\sin\psi = 0$$

Similarmente: g_{tθ}^{(0)} = 0 y g_{tφ}^{(0)} = 0 ✓

**Parte espacial**: La métrica estándar de S³:

$$g_{\psi\psi}^{(0)} = R^2, \quad g_{\theta\theta}^{(0)} = R^2\sin^2\psi, \quad g_{\phi\phi}^{(0)} = R^2\sin^2\psi\sin^2\theta$$

con todos los términos cruzados espaciales nulos.

**Resultado sin rotación**:

$$ds^2_{(0)} = -(c^2 - \dot{R}^2)\,dt^2 + R^2\left[d\psi^2 + \sin^2\psi\left(d\theta^2 + \sin^2\theta\,d\phi^2\right)\right]$$

**Nota sobre el tiempo propio**: El tiempo coordenado t del Bulk NO es el tiempo propio τ de la brana. Para un observador comóvil (dψ = dθ = dφ = 0):

$$d\tau = \sqrt{1 - \frac{\dot{R}^2}{c^2}}\,dt$$

Reparametrizando con τ, se recupera la métrica FLRW estándar para universo cerrado (k = +1):

$$ds^2_{(0)} = -c^2\,d\tau^2 + R^2(\tau)\left[d\psi^2 + \sin^2\psi\left(d\theta^2 + \sin^2\theta\,d\phi^2\right)\right]$$

### 3.3. Correcciones por rotación: términos de arrastre

Las correcciones Δg_{ab} = h_{μν}(∂X^μ/∂x^a)(∂X^ν/∂x^b) se calculan componente por componente.

**Δg_{tt}**: Los términos cruzados h_{ti} · (∂X^i/∂t) se cancelan parejamente:

$$-2\omega Y\frac{\partial X}{\partial t} + 2\omega X\frac{\partial Y}{\partial t} = -2\omega\dot{R}R\sin^2\psi\sin^2\theta\sin\phi\cos\phi + 2\omega\dot{R}R\sin^2\psi\sin^2\theta\cos\phi\sin\phi = 0$$

$$-2\omega W\frac{\partial Z}{\partial t} + 2\omega Z\frac{\partial W}{\partial t} = -2\omega\dot{R}R\sin\psi\cos\psi\cos\theta + 2\omega\dot{R}R\sin\psi\cos\psi\cos\theta = 0$$

Por lo tanto: Δg_{tt} = ω²R² (solo el término diagonal sobrevive)

**Resultado**: g_{tt} = −(c² − Ṙ² − ω²R²)

**Δg_{tψ}**: Calculamos h_{ti}(∂X^i/∂ψ):

$$\Delta g_{t\psi} = (-\omega Y)(R\cos\psi\sin\theta\cos\phi) + (\omega X)(R\cos\psi\sin\theta\sin\phi) + (-\omega W)(R\cos\psi\cos\theta) + (\omega Z)(-R\sin\psi)$$

Los primeros dos términos se cancelan (son iguales y opuestos). Los últimos dos:

$$-\omega R^2\cos^2\psi\cos\theta - \omega R^2\sin^2\psi\cos\theta = -\omega R^2\cos\theta$$

**Δg_{tθ}**: Similarmente:

$$\Delta g_{t\theta} = (-\omega Y)(R\sin\psi\cos\theta\cos\phi) + (\omega X)(R\sin\psi\cos\theta\sin\phi) + (-\omega W)(-R\sin\psi\sin\theta) + (\omega Z)(0)$$

Los primeros dos términos se cancelan. El tercero da:

$$\Delta g_{t\theta} = \omega R^2\sin\psi\cos\psi\sin\theta$$

**Δg_{tφ}**:

$$\Delta g_{t\phi} = (-\omega Y)(-R\sin\psi\sin\theta\sin\phi) + (\omega X)(R\sin\psi\sin\theta\cos\phi) + 0 + 0$$

$$= \omega R^2\sin^2\psi\sin^2\theta\left(\sin^2\phi + \cos^2\phi\right) = \omega R^2\sin^2\psi\sin^2\theta$$

**Componentes espaciales**: Δg_{ψψ} = Δg_{θθ} = Δg_{φφ} = Δg_{ψθ} = Δg_{ψφ} = Δg_{θφ} = 0 (pues h_{ij} = 0 y ∂t/∂x^a = 0 para a ≠ t).

### 3.4. Métrica inducida completa

$$\boxed{ds^2_{\text{brana}} = -\left(c^2 - \dot{R}^2 - \omega^2 R^2\right)dt^2 + R^2\left[d\psi^2 + \sin^2\psi\left(d\theta^2 + \sin^2\theta\,d\phi^2\right)\right] + 2\omega R^2\left[-\cos\theta\,d\psi + \sin\psi\cos\psi\sin\theta\,d\theta + \sin^2\psi\sin^2\theta\,d\phi\right]dt}$$

**Tabla de componentes**:

| Componente | Valor |
|---|---|
| g_{tt} | −(c² − Ṙ² − ω²R²) |
| g_{tψ} | −ωR² cos θ |
| g_{tθ} | +ωR² sin ψ cos ψ sin θ |
| g_{tφ} | +ωR² sin²ψ sin²θ |
| g_{ψψ} | R² |
| g_{θθ} | R² sin²ψ |
| g_{φφ} | R² sin²ψ sin²θ |
| g_{ψθ} = g_{ψφ} = g_{θφ} | 0 |

### 3.5. Análisis del resultado

**¿Es FLRW?** NO. La métrica FLRW para universo cerrado tiene g_{ta} = 0 para todo a espacial. Nuestra métrica tiene tres términos de arrastre no nulos. Es una métrica tipo **FLRW + frame-dragging**, análoga a cómo la métrica de Kerr extiende a Schwarzschild con un término g_{tφ}.

**¿Preserva la isotropía?** Los términos de arrastre dependen de (ψ, θ, φ), rompiendo la isotropía. Esto es **físicamente correcto**: una rotación global define una dirección preferente. La isoclínica garantiza que la *magnitud* de la velocidad de arrastre es uniforme (v = ωR para todo punto), pero la *dirección* de esa velocidad varía con la posición, produciendo arrastre diferencial.

**Condición de temporalidad**: La brana es temporal si Ṙ² + ω²R² < c². Esto requiere que la velocidad total (expansión + rotación) sea sublumínica.

**Límite ω → 0**: Se recupera la métrica FLRW estándar. ✓

**Límite local** (r ≪ R): Cerca de un punto de la brana, los términos de arrastre se reducen a la forma estándar de un marco rotante en espacio plano, como se muestra en el Paso 5.

---

## Paso 4: Conexión y Análisis de Torsión

### 4.1. Conexión de Levi-Civita de la métrica inducida

Los símbolos de Christoffel de la métrica inducida se calculan mediante:

$$\Gamma^\mu_{\alpha\beta} = \frac{1}{2}g^{\mu\nu}\left(\partial_\alpha g_{\nu\beta} + \partial_\beta g_{\nu\alpha} - \partial_\nu g_{\alpha\beta}\right)$$

Dado que la métrica tiene términos g_{ta} ≠ 0, los símbolos de Christoffel contendrán:

- **Términos ∝ ω²**: Contribuciones centrífugas (de ∂g_{tt}/∂x^a, que contiene ω²R²)
- **Términos ∝ ω**: Contribuciones de Coriolis (de ∂g_{ta}/∂x^b)
- **Términos independientes de ω**: Geodésicas FLRW estándar (curvatura espacial + expansión)

### 4.2. Mapeo a fuerzas inerciales clásicas

Para identificar las fuerzas, analizamos la ecuación geodésica:

$$\frac{d^2 x^a}{d\tau^2} + \Gamma^a_{bc}\frac{dx^b}{d\tau}\frac{dx^c}{d\tau} = 0$$

Los términos relevantes son:

**Fuerza centrífuga** (de Γ^a_{tt}):

$$\Gamma^a_{tt} \sim g^{ab}\left(\partial_t g_{tb} - \frac{1}{2}\partial_b g_{tt}\right)$$

El término ∂_b g_{tt} = ∂_b(ω²R²) da la fuerza centrífuga clásica:

$$F^a_{\text{centrífuga}} \propto \omega^2 R\,\hat{n}^a$$

donde n̂^a es la dirección radial en la brana. Esta fuerza apunta "hacia afuera" del centro de rotación y es responsable de la expansión cósmica.

**Fuerza de Coriolis** (de Γ^a_{tb}):

$$\Gamma^a_{tb} \sim g^{ac}\left(\partial_t g_{cb} + \partial_b g_{tc} - \partial_c g_{tb}\right)$$

En el límite local (coordenadas cartesianas cerca de un punto de la brana), esto se reduce a:

$$F^i_{\text{Coriolis}} = -2\omega\,\epsilon^{ijk}\,\Omega_j\,v_k$$

donde Ω_j es el vector de rotación del Bulk y v_k es la velocidad de la partícula en la brana. Esta es la **fuerza de Coriolis estándar** de un marco rotante.

**Gravedad newtoniana** (de la curvatura espacial):

Los Γ^a_{bc} puramente espaciales de la métrica de la 3-esfera dan la conexión de la S³, que en el límite de campo débil produce la gravedad newtoniana estándar más correcciones de curvatura de orden r²/R².

### 4.3. ¿Es torsión o conexión de Levi-Civita?

**Respuesta definitiva: NO es torsión.** Los términos de Coriolis y centrífuga surgen enteramente de la **conexión de Levi-Civita** de la métrica inducida. Son consecuencia de los términos g_{ta} ≠ 0 en la métrica, no de una conexión no métrica.

En geometría diferencial, un marco rotante en espacio plano produce exactamente estos términos en los símbolos de Christoffel — es el mismo mecanismo que produce las fuerzas ficticias en un tiovivo en la mecánica newtoniana. No se necesita Einstein-Cartan ni torsión alguna.

**La torsión T^a_{bc} = Γ^a_{bc} − Γ^a_{cb}** de la conexión de Levi-Civita es **idénticamente cero** por construcción (la conexión es simétrica). Para obtener torsión, habría que postular una conexión no métrica adicional, lo cual no está justificado por el formalismo de inmersión.

### 4.4. Sobre la curvatura extrínseca

La brana como subvariedad del Bulk tiene curvatura extrínseca (segunda forma fundamental) K_{ab}, que describe cómo se curva "hacia afuera" en el Bulk. La ecuación de Gauss relaciona:

$$R^{\text{brana}}_{abcd} = R^{\text{Bulk}}_{abcd} + K_{ac}K_{bd} - K_{ad}K_{bc}$$

Como el Bulk es plano (R^{\text{Bulk}} = 0), la curvatura intrínseca de la brana proviene enteramente de la curvatura extrínseca:

$$R^{\text{brana}}_{abcd} = K_{ac}K_{bd} - K_{ad}K_{bc}$$

Para la 3-esfera de radio R, la curvatura extrínseca es K_{ab} = (1/R)g_{ab}, lo que da curvatura intrínseca constante R_{abcd} = (1/R²)(g_{ac}g_{bd} − g_{ad}g_{bc}). Esta es la curvatura que, en el límite local, produce la gravedad newtoniana.

---

## Paso 5: Ecuaciones de Movimiento

### 5.1. Ecuación geodésica en la brana

Para una partícula confinada a la brana, la ecuación de movimiento es la geodésica de la métrica inducida:

$$\frac{d^2 x^a}{d\tau^2} + \Gamma^a_{bc}\frac{dx^b}{d\tau}\frac{dx^c}{d\tau} = 0$$

### 5.2. Límite local: coordenadas cartesianas cerca de un punto

Para conectar con la física local (sistema solar, galaxias), tomamos el límite cerca de un punto de la brana. Cerca de ψ = π/2, θ = π/2 (el "ecuador" donde W = 0), definimos coordenadas locales:

$$x \approx R\left(\frac{\pi}{2} - \psi\right)\cos\phi, \quad y \approx R\left(\frac{\pi}{2} - \psi\right)\sin\phi, \quad z \approx R\left(\frac{\pi}{2} - \theta\right)$$

En este límite, la métrica se reduce a:

$$ds^2 \approx -\left(c^2 - \dot{R}^2 - \omega^2 R^2\right)dt^2 + dx^2 + dy^2 + dz^2 + 2\omega\left(-y\,dx + x\,dy\right)dt + 2\omega\left(-z\,dx + x\,dz\right)dt$$

**Nota**: El segundo grupo de términos cruzados (−z dx + x dz) proviene de la rotación en el plano zw, que en coordenadas locales se manifiesta como un arrastre entre la dirección z local y la dirección x. Esto es una consecuencia de la isoclínica: la rotación en zw se "proyecta" al espacio local.

### 5.3. Ecuaciones de movimiento en el límite local

La ecuación geodésica en estas coordenadas produce:

$$\ddot{x} = 2\omega\dot{y} + 2\omega\dot{z} + \omega^2 x + \text{(curvatura espacial)}$$
$$\ddot{y} = -2\omega\dot{x} + \omega^2 y + \text{(curvatura espacial)}$$
$$\ddot{z} = -2\omega\dot{x} + \omega^2 z + \text{(curvatura espacial)}$$

Identificamos:

| Término | Fuerza | Origen geométrico |
|---|---|---|
| 2ωẏ, −2ωẋ, 2ωż | **Coriolis** | g_{tψ}, g_{tθ}, g_{tφ} (arrastre isoclínico) |
| ω²x, ω²y, ω²z | **Centrífuga** | ∂g_{tt}/∂x^a (modificación de g_{tt}) |
| Curvatura espacial | **Gravedad** | Γ^a_{bc} espaciales (curvatura de S³) |

**No hay parámetros libres α o β**: Los coeficientes están completamente determinados por ω y R. La fuerza de Coriolis tiene coeficiente exactamente 2ω (el factor 2 es estándar de la mecánica de marcos rotantes), y la centrífuga tiene coeficiente exactamente ω².

### 5.4. ¿Se recuperan las ecuaciones de la v1.0?

La formulación v1.0 proponía:

$$V_{\text{eff}}(r, \dot\phi) = -\frac{GM}{r}\left(1 + \alpha\frac{r^2\dot\phi^2}{c^2}\right) - 2\beta\omega_{4D}\,r^2\dot\phi$$

con α y β parámetros adimensionales libres.

**Del formalismo riguroso se obtiene**:

1. **El término de Coriolis** tiene coeficiente 2ω (no 2βω). Es decir, **β = 1** está determinado por la geometría, no es libre.

2. **El término de acoplamiento cinético** (el análogo de α) no surge de la métrica inducida de la S³ en rotación. La métrica inducida produce Coriolis y centrífuga estándar, pero no un término proporcional a ṽ²/c² que modifique la fuerza gravitatoria.

3. **La precesión de Mercurio** no se explica por la rotación cósmica. Estimemos la magnitud:

$$\omega_{4D} \sim H_0 \sim 10^{-18}\,\text{s}^{-1}$$

La precesión de Coriolis por órbita es:

$$\Delta\phi_{\text{Coriolis}} \sim \omega \cdot T_{\text{órbita}} \sim 10^{-18} \times 10^7 \sim 10^{-11}\,\text{rad/orbita}$$

Esto es **10⁴ veces más pequeño** que la precesión observada de Mercurio (~10⁻⁷ rad/orbita). La rotación cósmica es irrelevante para la dinámica local.

4. **La deflexión de la luz**: El argumento v1.0 de que la Coriolis 4D duplica la deflexión newtoniana requiere calibrar βω₄D = 1/(2c), lo cual es circular (se ajusta el parámetro para obtener el resultado deseado). Del formalismo riguroso, la Coriolis con ω ~ H₀ produce una deflexión de orden ωR/c ~ H₀R/c ~ 1, que es un efecto cosmológico global, no una corrección local a la deflexión de luz estelar.

### 5.5. ¿De dónde viene entonces la gravedad local?

La gravedad newtoniana (y sus correcciones relativistas) no proviene de la métrica inducida de la S³ limpia, sino de la **deformación elástica local** h(r) de la brana — la deflexión en la coordenada normal al Bulk causada por masas puntuales. Esta deformación modifica la métrica inducida localmente:

$$g_{00} \approx -\left(1 + \frac{2\Phi(r)}{c^2}\right), \quad \Phi(r) = c^2 h(r) \approx -\frac{GM}{r}$$

Este es un mecanismo **separado** del frame-dragging isoclínico. La deformación h(r) es una perturbación de la inmersión, no un término inherente a la métrica del Bulk rotante.

**Implicación**: Para derivar la precesión de Mercurio y la deflexión de la luz desde primeros principios, se necesita combinar:
1. La métrica inducida de la S³ en rotación (este documento)
2. La perturbación de la inmersión por deformación elástica h(r) (formulación existente)
3. La interacción entre ambas (trabajo futuro)

---

## Paso 6: Hermeneutica — Predicciones, Inconsistencias y Falsabilidad

### 6.1. Predicciones del formalismo riguroso

1. **Anisotropía direccional cosmológica**: La métrica inducida tiene términos de arrastre que dependen de (ψ, θ, φ). Esto predice una **anisotropía cuadrupolar** en la expansión de Hubble, con amplitud:

$$\frac{\delta H}{H} \sim \frac{\omega^2 R^2}{c^2} \sim \frac{v_{\text{rot}}^2}{c^2}$$

Si ωR ~ H₀R ~ c (lo cual es consistente con H₀ ~ c/R), entonces δH/H ~ 1, lo cual es **refutado observacionalmente** (Hubble es isotrópico a nivel ~1%). Esto requiere ωR ≪ c, es decir, la velocidad de rotación es mucho menor que c.

2. **Frame-dragging solar system**: La fuerza de Coriolis del Bulk produce una precesión de Lense-Thirring-like en órbitas locales, con magnitud ∝ ω₄D. Si ω₄D ~ H₀ ~ 10⁻¹⁸ s⁻¹, el efecto es inobservable con tecnología actual.

3. **Corrección centrífuga a g_{tt}**: El término ω²R² en g_{tt} modifica el ritmo del tiempo cósmico. Para observadores comóviles, el tiempo propio es:

$$d\tau = \sqrt{1 - \frac{\dot{R}^2 + \omega^2 R^2}{c^2}}\,dt$$

Esto predice que la "edad del universo" en tiempo propio difiere del tiempo coordenado del Bulk. Si ωR es comparable a Ṙ, la corrección es del mismo orden que la de la expansión.

4. **No se necesitan α, β ni A₄D**: Todos los efectos inerciales están determinados por ω₄D y R(t), que son cantidades físicas con valores fijados por la cosmología.

### 6.2. Inconsistencias internas

1. **Ruptura de isotropía**: La isoclínica garantiza velocidad uniforme, pero la métrica inducida NO es isotrópica. Los términos g_{tψ}, g_{tθ} dependen de la posición angular. Esto viola el Principio Cosmológico en su forma fuerte. **Mitigación**: En el límite ωR ≪ c, los términos de arrastre son perturbaciones pequeñas y la métrica es "casi FLRW".

2. **Precesión de Mercurio no explicada**: La rotación cósmica es ~10⁴ veces demasiado débil para explicar la precesión observada. El mecanismo α de la v1.0 no surge de la métrica inducida. **Estado**: Se necesita la deformación elástica h(r) como mecanismo adicional.

3. **Deflexión de la luz no explicada**: El argumento de "Coriolis duplica Newton" de la v1.0 requiere calibración ad-hoc (βω₄D = 1/2c). Del formalismo riguroso, la Coriolis con ω ~ H₀ no produce este efecto. **Estado**: Se necesita derivar la deflexión desde la métrica perturbada por h(r), no desde la Coriolis cósmica.

4. **Doble cuenta de la centrífuga**: La fuerza centrífuga aparece tanto en g_{tt} (como ω²R²) como en la ecuación de movimiento (como ω²r). Esto es consistente — son la misma fuerza vista desde diferentes perspectivas — pero hay que tener cuidado de no contarla dos veces al combinar con la deformación elástica.

5. **Condición de temporalidad**: Se requiere Ṙ² + ω²R² < c². Si ωR ~ c (como sugeriría H₀ ~ c/R), la brana sería luminica o casi luminica, lo cual es problemático. Esto sugiere que ωR ≪ c en la época actual, consistente con ω₄D ∝ 1/R² y R creciendo.

### 6.3. Predicciones falsables originales

1. **Anisotropía cuadrupolar en H₀**: Si la rotación isoclínica es real, debe existir una anisotropía cuádruple en la constante de Hubble con amplitud δH/H ~ (ωR/c)². Los datos actuales limitan esto a < 1%, lo que implica ωR < 0.1c. **Test**: Mediciones de H₀ direccional con precisión sub-porcentual (SKA, Euclid).

2. **Precesión de Lense-Thirring 4D**: La Coriolis isoclínica produce una precesión de ejes orbitales proporcional a ω₄D, con una firma angular distinta de la Lense-Thirring estándar (porque involucra dos planos de rotación, no uno). **Test**: Medir precesión de LAGEOS con precisión ~10⁻¹⁸ s⁻¹ (actualmente ~10⁻¹⁵ s⁻¹, 3 órdenes de magnitud lejos).

3. **Correlación CMB-estructura**: La dirección preferente de la rotación isoclínica debería correlacionar el eje del mal del CMB con alineamientos de estructura a gran escala. **Test**: Análisis cruzado Planck + catálogos de galaxias (SDSS, DESI).

### 6.4. ¿Qué podría refutar esta teoría?

1. **H₀ perfectamente isotrópico** a nivel < 0.1% → refuta la predicción de anisotropía cuádruple.
2. **Detección de materia oscura partícula** con las propiedades exactas predichas por ΛCDM → elimina la motivación principal.
3. **Falta de correlación CMB-estructura** en la dirección predicha → refuta la predicción de eje preferente.
4. **Precesión de Mercurio explicada completamente por GR estándar** sin necesidad de dimensiones extra → elimina la necesidad del mecanismo de deformación de brana.

### 6.5. Síntesis honesta

El formalismo geométrico riguroso confirma que:

- ✅ La inmersión de S³ en un Bulk 4D rotante isoclínicamente produce una métrica con frame-dragging natural.
- ✅ Los términos de arrastre generan fuerzas de Coriolis y centrífuga sin parámetros libres.
- ✅ La expansión de Hubble emerge de la dinámica de R(t).
- ✅ No se necesita torsión (Einstein-Cartan) — todo proviene de la conexión de Levi-Civita.

Pero también revela que:

- ❌ La métrica inducida NO es FLRW pura — tiene anisotropía direccional.
- ❌ La rotación cósmica es demasiado débil (~H₀) para explicar tests locales de GR.
- ❌ Los parámetros α y β de la v1.0 no surgen del formalismo de inmersión; α no tiene justificación geométrica y β = 1 está fijo por la geometría.
- ❌ La deflexión de la luz "factor 2 de Einstein" no se explica por Coriolis cósmica sin calibración ad-hoc.

**El camino a seguir**: Combinar este formalismo de inmersión con la deformación elástica h(r) para obtener una métrica inducida perturbada que incluya tanto el frame-dragging global como los pozos gravitatorios locales. Solo esa métrica combinada puede pretender reproducir los tests clásicos de GR.
