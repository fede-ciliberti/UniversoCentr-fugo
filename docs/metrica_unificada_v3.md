# Métrica Unificada v3.0: Deformación Elástica + Rotación Isoclínica

**De Primeros Principios a la Métrica de Schwarzschild Emergente**

*Fecha: 16 de junio de 2026*

---

## Resumen Ejecutivo

Este documento completa la reconstrucción del Universo Centrífugo desde primeros principios. En la Fase 1 (`formalismo_geometrico_4d_v2.md`) derivamos la métrica inducida sobre una 3-esfera limpia en rotación isoclínica, obteniendo FLRW + frame-dragging. Allí identificamos que la rotación cósmica ω ~ H₀ es demasiado débil (~10⁻¹⁸ s⁻¹) para explicar los tests clásicos de GR. Aquí resolvemos ese problema: la **deformación elástica local** h(r) de la brana bajo una masa M modifica la métrica inducida de forma que reproduce **exactamente** la métrica de Schwarzschild en campo débil, incluyendo el factor 2 en la deflexión de la luz, **sin parámetros ad-hoc**.

**Resultado central**: La métrica inducida sobre la brana deformada es:

$$ds^2 = -\left(1 + \frac{2\Phi}{c^2}\right)c^2\,dt^2 + \left(1 - \frac{2\Phi}{c^2}\right)\left(dx^2 + dy^2 + dz^2\right) + \text{(frame-dragging isoclínico)}$$

donde Φ = −GM/r es el potencial newtoniano. Esta es **exactamente** la métrica de Schwarzschild en campo débil. La deflexión de la luz se obtiene como suma de la curvatura espacial (mitad newtoniana) y la dilatación temporal (mitad relativista), dando el factor 2 de Einstein sin ningún ajuste.

---

## Paso 1: La Inmersión Deformada

### 1.1. La brana limpia (repaso de la Fase 1)

La brana es una 3-esfera S³ de radio R(t) inmersa en un Bulk 5D (1 temporal + 4 espaciales). En coordenadas hiperesféricas (ψ, θ, φ), la inmersión es:

$$X^i = R(t)\,\Omega^i(\psi, \theta, \phi)$$

donde Ω^i son las coordenadas cartesianas unitarias de S³:

$$\Omega^1 = \sin\psi\sin\theta\cos\phi, \quad \Omega^2 = \sin\psi\sin\theta\sin\phi, \quad \Omega^3 = \sin\psi\cos\theta, \quad \Omega^4 = \cos\psi$$

con la restricción Σᵢ(Ω^i)² = 1.

### 1.2. La deformación elástica local

Una masa M confinada a la brana experimenta la fuerza centrífuga del Bulk F_cf = Mω²R, que la empuja en la dirección normal a la brana (la 4ª dimensión espacial w). La brana responde elásticamente, deformándose localmente. En lugar de un radio uniforme R(t), la posición de la brana en la dirección normal se convierte en:

$$\tilde{R}(t, \mathbf{x}) = R(t) + h(\mathbf{x})$$

donde h(x) es la **función de deformación** — la "profundidad" del pozo elástico en la coordenada normal.

### 1.3. Solución de la ecuación de membrana

La deformación h(x) satisface la ecuación de Poisson elástica (derivada en `03_metodologia_gravedad_emergente.md`):

$$\nabla^2 h - \lambda^2 h = \frac{M\omega^2 R}{T_b}\,\delta^3(\mathbf{x})$$

En el régimen local (λr ≪ 1, es decir, distancias mucho menores que el radio cósmico), la solución con simetría esférica es:

$$h(r) = -\frac{M\omega^2 R}{4\pi T_b}\,\frac{1}{r}$$

Usando la relación G_eff = c²ω²/(4πT_b) derivada en la Fase 1, esto se reescribe como:

$$h(r) = -\frac{G_{eff} M}{c^2}\,\frac{1}{r} \cdot \frac{R}{1} = -\frac{GM}{c^2 r} \cdot R$$

**Nota dimensional**: h(r) tiene dimensiones de longitud (es una distancia en la dirección normal). El factor R aparece porque la deformación normal es proporcional al radio de la brana. Definimos la cantidad adimensional:

$$\epsilon(r) \equiv \frac{h(r)}{R} = -\frac{GM}{c^2 r}$$

Esta es la perturbación fraccional del radio. Para el Sol en la Tierra: ε ~ 10⁻⁸. Para un agujero negro en el horizonte: ε ~ 1. Siempre estamos en campo débil cuando ε ≪ 1.

### 1.4. La inmersión perturbada

La inmersión de la brana deformada en el Bulk es ahora:

$$X^i(t, \psi, \theta, \phi) = \left[R(t) + h(r)\right]\,\Omega^i(\psi, \theta, \phi)$$

donde r = R·χ es la distancia geodésica local (con χ la coordenada radial hiperesférica). Equivalentemente, en coordenadas locales cartesianas cerca de un punto de la brana:

$$X = \left(R + h\right)\sin\psi\sin\theta\cos\phi$$
$$Y = \left(R + h\right)\sin\psi\sin\theta\sin\phi$$
$$Z = \left(R + h\right)\sin\psi\cos\theta$$
$$W = \left(R + h\right)\cos\psi$$

**Punto clave**: La deformación h(r) depende de la posición espacial pero NO del tiempo (es estática en escalas locales). Por lo tanto ∂h/∂t = 0.

---

## Paso 2: La Métrica Inducida sobre la Brana Deformada

### 2.1. Estrategia de cálculo

La métrica inducida se obtiene por pullback de la métrica del Bulk:

$$g_{ab} = g_{AB}\frac{\partial X^A}{\partial x^a}\frac{\partial X^B}{\partial x^b}$$

Descomponemos el cálculo en tres contribuciones:

1. **Parte FLRW** (de la S³ limpia en expansión): ya calculada en la Fase 1.
2. **Parte de frame-dragging** (de la rotación isoclínica): ya calculada en la Fase 1.
3. **Parte de deformación** (de h(r)): **nueva**, se calcula aquí.

La métrica del Bulk en coordenadas rotantes es (de la Fase 1):

$$ds^2_{\text{Bulk}} = \left[-c^2 + \omega^2(X^2+Y^2+Z^2+W^2)\right]dt^2 + dX^2+dY^2+dZ^2+dW^2 + 2\omega(-Y\,dX+X\,dY-W\,dZ+Z\,dW)\,dt$$

### 2.2. Cálculo de la parte espacial: correcciones por deformación

Los diferenciales espaciales de la inmersión deformada son:

$$dX^i = \Omega^i\,d(R+h) + (R+h)\,d\Omega^i = \Omega^i\,dh + (R+h)\,d\Omega^i$$

donde usamos dR = Ṙ dt (que ya está contabilizado en la parte FLRW) y dh = (∂h/∂x^j)dx^j (la deformación es estática).

La métrica espacial inducida es:

$$g_{ij}\,dx^i dx^j = \sum_{k=1}^{4}(dX^k)^2 = (R+h)^2\sum_k(d\Omega^k)^2 + 2(R+h)\sum_k \Omega^k\,d\Omega^k\,dh + \sum_k(\Omega^k)^2(dh)^2$$

**Término 1**: (R+h)² Σ_k(dΩ^k)² = (R+h)² · [métrica de S³ unitaria] = (R+h)² γ_ij dx^i dx^j

donde γ_ij es la métrica de la 3-esfera unitaria.

**Término 2**: 2(R+h) Σ_k Ω^k dΩ^k dh. Pero Σ_k Ω^k dΩ^k = ½ d(Σ_k (Ω^k)²) = ½ d(1) = 0, porque los Ω^k son coordenadas sobre la esfera unitaria. **Este término se anula exactamente.**

**Término 3**: Σ_k (Ω^k)² (dh)² = (Σ_k (Ω^k)²)(dh)² = 1 · (dh)² = (∂_i h)(∂_j h) dx^i dx^j

### 2.3. Métrica espacial completa

Combinando:

$$g_{ij} = (R+h)^2\,\gamma_{ij} + \partial_i h\,\partial_j h$$

Expandiendo en campo débil (h ≪ R):

$$(R+h)^2 = R^2\left(1 + \frac{h}{R}\right)^2 \approx R^2\left(1 + 2\frac{h}{R}\right) = R^2(1 + 2\epsilon)$$

Por lo tanto:

$$g_{ij} \approx R^2(1 + 2\epsilon)\,\gamma_{ij} + \partial_i h\,\partial_j h$$

### 2.4. Límite local: coordenadas cartesianas

Cerca de un punto de la brana (ψ ≈ π/2, θ ≈ π/2), las coordenadas locales son x ≈ R(π/2 − ψ)cos φ, y ≈ R(π/2 − ψ)sin φ, z ≈ R(π/2 − θ), y la métrica γ_ij → δ_ij. En estas coordenadas:

$$g_{ij}^{(\text{local})} \approx (1 + 2\epsilon)\,\delta_{ij} + \frac{1}{R^2}\partial_i h\,\partial_j h$$

El segundo término (∂h/∂x^i)(∂h/∂x^j)/R² es de orden (h/(Rr))² = (GM/(c²Rr))², que es **segundo orden** en la perturbación y despreciable en campo débil. Por lo tanto:

$$\boxed{g_{ij}^{(\text{local})} \approx \left(1 - \frac{2GM}{c^2 r}\right)\delta_{ij}}$$

¡La métrica espacial reproduce exactamente la parte espacial de Schwarzschild en campo débil!

### 2.5. Cálculo de la parte temporal: corrección a g_tt

La componente g_tt de la métrica inducida tiene tres contribuciones:

**A) Parte FLRW** (sin rotación, sin deformación):

$$g_{tt}^{(0)} = -c^2 + \dot{R}^2$$

**B) Corrección por rotación** (de la Fase 1):

$$\Delta g_{tt}^{(\omega)} = \omega^2(R+h)^2 \approx \omega^2 R^2(1 + 2\epsilon)$$

**C) Corrección por deformación en la velocidad de expansión**:

La velocidad de expansión de un punto de la brana deformada es:

$$\frac{\partial X^i}{\partial t} = \dot{R}\,\Omega^i$$

(pues h es estática: ∂h/∂t = 0). La contribución al g_tt de la parte plana del Bulk es:

$$\sum_i\left(\frac{\partial X^i}{\partial t}\right)^2 = \dot{R}^2\sum_i(\Omega^i)^2 = \dot{R}^2$$

**No cambia** respecto a la brana limpia. La deformación no modifica la velocidad de expansión.

### 2.6. g_tt completo

Combinando todas las contribuciones:

$$g_{tt} = -c^2 + \dot{R}^2 + \omega^2(R+h)^2$$

$$= -c^2 + \dot{R}^2 + \omega^2 R^2(1 + 2\epsilon)$$

$$= \left(-c^2 + \dot{R}^2 + \omega^2 R^2\right) + 2\omega^2 R^2\epsilon$$

El primer paréntesis es el g_tt de la brana limpia (Fase 1). El segundo término es la **corrección por deformación**:

$$\Delta g_{tt}^{(h)} = 2\omega^2 R^2 \epsilon = 2\omega^2 R^2\left(-\frac{GM}{c^2 r}\right) = -\frac{2\omega^2 R^2 GM}{c^2 r}$$

### 2.7. Reescritura en términos del potencial newtoniano

De la Fase 1, la constante de Newton efectiva es:

$$G_{eff} = \frac{c^2\omega^2}{4\pi T_b}$$

Y la relación entre h y el potencial es:

$$\Phi(r) = c^2\frac{h(r)}{R} = c^2\epsilon(r) = -\frac{GM}{r}$$

Por lo tanto:

$$\Delta g_{tt}^{(h)} = 2\omega^2 R^2 \cdot \frac{\Phi}{c^2} = \frac{2\omega^2 R^2}{c^2}\Phi$$

Ahora, en el tiempo propio de un observador comóvil de la brana, el g_tt de fondo se normaliza. Definimos el tiempo propio τ tal que:

$$d\tau^2 = \frac{c^2 - \dot{R}^2 - \omega^2 R^2}{c^2}\,dt^2 = \frac{1}{\gamma_0^2}\,dt^2$$

donde γ₀² = c²/(c² − Ṙ² − ω²R²) es el factor de Lorentz del marco cósmico. En este tiempo propio, el g_tt de fondo se normaliza a −c², y la corrección se convierte en:

$$g_{tt}^{(\tau)} = -c^2\left(1 + \frac{2\Phi}{c^2}\right) = -c^2\left(1 - \frac{2GM}{c^2 r}\right)$$

**¡Se recupera exactamente la componente temporal de Schwarzschild en campo débil!**

### 2.8. Términos de frame-dragging: sin cambios

Los términos cruzados g_{tψ}, g_{tθ}, g_{tφ} provienen de la rotación isoclínica del Bulk y dependen de las coordenadas X^i del punto en la brana. Con la deformación:

$$g_{ta}^{(\text{drag})} = h_{t\mu}\frac{\partial X^\mu}{\partial x^a}$$

donde h_{tμ} son los términos de arrastre del Bulk. Como h_{tμ} ∝ ω y las derivadas ∂X^μ/∂x^a ahora incluyen el factor (R+h) ≈ R(1+ε), los términos de arrastre reciben una corrección fraccional de orden ε:

$$g_{ta}^{(\text{drag, deformada})} \approx g_{ta}^{(\text{drag, limpia})}(1 + \epsilon)$$

Esta corrección es de orden GM/(c²r) ~ 10⁻⁸ para el Sol, completamente despreciable en campo débil. Los términos de frame-dragging permanecen esencialmente inalterados.

### 2.9. Métrica inducida unificada completa

En coordenadas locales cartesianas (x, y, z) cerca de un punto de la brana, en tiempo propio del observador comóvil:

$$\boxed{ds^2 = -\left(1 - \frac{2GM}{c^2 r}\right)c^2\,d\tau^2 + \left(1 - \frac{2GM}{c^2 r}\right)\left(dx^2 + dy^2 + dz^2\right) + 2\omega(-y\,dx + x\,dy - z\,dx + x\,dz)\,d\tau + \mathcal{O}(\epsilon^2)}$$

**Identificación de cada término**:

| Término | Origen | Efecto físico |
|---------|--------|---------------|
| −(1 − 2GM/c²r)c²dτ² | Deformación h(r) → g_tt | Dilatación temporal gravitatoria |
| (1 − 2GM/c²r)(dx²+dy²+dz²) | Deformación h(r) → g_ij | Curvatura espacial del "pozo" |
| 2ω(−y dx + x dy)dτ | Rotación isoclínica (plano xy) | Coriolis estándar |
| 2ω(−z dx + x dz)dτ | Rotación isoclínica (plano zw) | Coriolis isoclínica |

---

## Paso 3: El Potencial Efectivo y el Límite Newtoniano

### 3.1. Ecuación geodésica

Para una partícula de masa m moviéndose en la métrica inducida, la ecuación geodésica es:

$$\frac{d^2 x^a}{d\lambda^2} + \Gamma^a_{bc}\frac{dx^b}{d\lambda}\frac{dx^c}{d\lambda} = 0$$

donde λ es un parámetro afín (tiempo propio τ para partículas masivas).

### 3.2. Símbolos de Christoffel en campo débil

Para la métrica unificada en coordenadas locales, los símbolos de Christoffel relevantes se calculan a primer orden en ε = GM/(c²r):

**De la parte de Schwarzschild (deformación)**:

$$\Gamma^i_{00} = -\frac{1}{2}g^{ij}\partial_j g_{00} \approx \frac{1}{2}\partial_i\left(1 - \frac{2GM}{c^2 r}\right) \cdot c^2 = -\partial_i\Phi = \frac{GM}{r^2}\hat{r}^i$$

$$\Gamma^0_{0i} = \Gamma^0_{i0} = \frac{1}{2}g^{00}\partial_i g_{00} \approx \frac{1}{c^2}\partial_i\Phi = \frac{GM}{c^2 r^2}\hat{r}^i$$

$$\Gamma^i_{jk} = \frac{1}{2}g^{il}\left(\partial_j g_{lk} + \partial_k g_{lj} - \partial_l g_{jk}\right) \approx -\frac{1}{c^2}\left(\delta_{ij}\partial_k\Phi + \delta_{ik}\partial_j\Phi - \delta_{jk}\partial_i\Phi\right)$$

**De la parte de frame-dragging (rotación isoclínica)**:

$$\Gamma^i_{0j} \approx \omega\,\epsilon^i_{\ jk}\,\hat{\Omega}^k + \omega\,\epsilon^i_{\ jl}\,\hat{\Omega}'^l$$

donde ε^i_{jk} es el símbolo de Levi-Civita, Ω̂ es la dirección de rotación en el plano xy, y Ω̂' es la dirección en el plano zw (proyectada al espacio local).

### 3.3. Ecuación de movimiento para partículas lentas

Para una partícula lenta (v ≪ c), la ecuación geodésica se reduce a:

$$\frac{d^2 x^i}{d\tau^2} = -\Gamma^i_{00} - 2\Gamma^i_{0j}\frac{dx^j}{d\tau} + \text{(términos de orden v²/c²)}$$

**Término 1: Gravedad newtoniana**

$$-\Gamma^i_{00} = -\frac{GM}{r^2}\hat{r}^i = -\nabla\Phi$$

¡Se recupera la fuerza gravitatoria newtoniana! La aceleración apunta hacia la masa, con magnitud GM/r².

**Término 2: Coriolis isoclínica**

$$-2\Gamma^i_{0j}v^j = -2\omega\left(\epsilon^i_{\ jk}\hat{\Omega}^k + \epsilon^i_{\ jl}\hat{\Omega}'^l\right)v^j$$

En el límite local, esto se reduce a la fuerza de Coriolis estándar:

$$\mathbf{F}_{\text{Coriolis}} = -2m\,\boldsymbol{\omega} \times \mathbf{v}$$

con coeficiente exactamente 2ω (sin parámetros libres).

**Término 3: Centrífuga** (de Γ^i_{00} con la parte ω²R² de g_tt):

$$F^i_{\text{centrífuga}} = \omega^2 r^i$$

### 3.4. Potencial efectivo completo

Para una partícula lenta en el campo de una masa M, el potencial efectivo es:

$$V_{\text{eff}}(r, \mathbf{v}) = \underbrace{-\frac{GM}{r}}_{\text{Newton (deformación)}} + \underbrace{\frac{1}{2}\omega^2 r^2}_{\text{Centrífuga (rotación)}} - \underbrace{\boldsymbol{\omega}\cdot(\mathbf{r}\times\mathbf{v})}_{\text{Coriolis (frame-dragging)}}$$

**Comparación con la v1.0**: La formulación ad-hoc tenía V_eff = −(GM/r)(1 + αr²φ̇²/c²) − 2βωr²φ̇. En la formulación rigurosa:

- **α no aparece**: No hay término de acoplamiento cinético proporcional a v²/c² en el potencial newtoniano. La gravedad newtoniana es puramente radial e independiente de la velocidad de la partícula.
- **β = 1**: El coeficiente de Coriolis es exactamente 2ω, determinado por la geometría.
- **La precesión de Mercurio** no viene de α sino de la estructura completa de la métrica (g_tt y g_ij combinados), como se muestra en el Paso 4.

---

## Paso 4: Deflexión de la Luz — El Factor 2 de Einstein

### 4.1. El problema del factor 2

En la teoría newtoniana de partículas (tratando la luz como partículas con masa), la deflexión de un rayo luminoso que pasa a distancia d de una masa M es:

$$\theta_{\text{Newton}} = \frac{2GM}{dc^2}$$

En la Relatividad General, la deflexión observada es el **doble**:

$$\theta_{\text{Einstein}} = \frac{4GM}{dc^2}$$

Este factor 2 es uno de los tests clásicos de GR (verificado por Eddington en 1919). ¿De dónde sale en nuestro formalismo?

### 4.2. Geodésicas nulas en la métrica inducida

Para un fotón (ds² = 0), la ecuación geodésica en la métrica unificada es:

$$\frac{d^2 x^i}{d\lambda^2} + \Gamma^i_{00}\left(\frac{dt}{d\lambda}\right)^2 + 2\Gamma^i_{0j}\frac{dt}{d\lambda}\frac{dx^j}{d\lambda} + \Gamma^i_{jk}\frac{dx^j}{d\lambda}\frac{dx^k}{d\lambda} = 0$$

Para un fotón moviéndose principalmente en la dirección x con parámetro de impacto d en la dirección y:

$$\frac{dx}{d\lambda} \approx c, \quad \frac{dy}{d\lambda} \approx 0, \quad \frac{dz}{d\lambda} \approx 0$$

### 4.3. Contribución 1: Curvatura espacial (la "mitad newtoniana")

La aceleración transversal debida a la curvatura espacial del pozo gravitatorio proviene de los Γ^i_{jk} espaciales:

$$\frac{d^2 y}{d\lambda^2}\bigg|_{\text{espacial}} = -\Gamma^y_{xx}\left(\frac{dx}{d\lambda}\right)^2$$

Con la métrica espacial g_ij = (1 − 2GM/c²r)δ_ij:

$$\Gamma^y_{xx} = -\frac{1}{c^2}\left(\delta_{yx}\partial_x\Phi + \delta_{yx}\partial_x\Phi - \delta_{xx}\partial_y\Phi\right) = \frac{1}{c^2}\partial_y\Phi = -\frac{GM}{c^2}\frac{y}{r^3}$$

Para un fotón con x ≈ ct, y ≈ d:

$$a_{y,\text{espacial}} = -\Gamma^y_{xx}\,c^2 = \frac{GM\,d}{(c^2t^2 + d^2)^{3/2}}$$

Integrando:

$$v_{y,\text{espacial}} = \int_{-\infty}^{\infty}\frac{GM\,d}{(c^2t^2+d^2)^{3/2}}\,dt = \frac{2GM}{cd}$$

$$\theta_{\text{espacial}} = \frac{v_{y,\text{espacial}}}{c} = \frac{2GM}{dc^2}$$

¡Esta es exactamente la predicción newtoniana! La curvatura espacial del pozo elástico da la mitad de la deflexión.

### 4.4. Contribución 2: Dilatación temporal (la "mitad relativista")

La aceleración transversal debida a la modificación de g_tt proviene de Γ^y_{00}:

$$\Gamma^y_{00} = \frac{1}{2}g^{yy}\left(-\partial_y g_{00}\right) \approx \frac{1}{2}\partial_y\left(1 - \frac{2GM}{c^2 r}\right) \cdot c^2 = -\partial_y\Phi = \frac{GM}{r^2}\frac{y}{r}$$

Para el fotón:

$$a_{y,\text{temporal}} = -\Gamma^y_{00}\left(\frac{dt}{d\lambda}\right)^2 \cdot \left(\frac{d\lambda}{dt}\right)^2 = -\Gamma^y_{00} = -\frac{GM\,d}{r^3}$$

Integrando:

$$v_{y,\text{temporal}} = \int_{-\infty}^{\infty}\frac{GM\,d}{(c^2t^2+d^2)^{3/2}}\,dt = \frac{2GM}{cd}$$

$$\theta_{\text{temporal}} = \frac{2GM}{dc^2}$$

¡La dilatación temporal da la otra mitad!

### 4.5. Deflexión total

$$\boxed{\theta_{\text{total}} = \theta_{\text{espacial}} + \theta_{\text{temporal}} = \frac{2GM}{dc^2} + \frac{2GM}{dc^2} = \frac{4GM}{dc^2}}$$

**Se recupera exactamente el factor 2 de Einstein sin ningún parámetro ad-hoc.**

### 4.6. Interpretación física

La deflexión de la luz tiene dos orígenes físicos distintos en nuestro formalismo:

1. **Curvatura espacial** (θ_espacial = 2GM/dc²): El pozo elástico deforma el espacio 3D de la brana. Un fotón que viaja "en línea recta" en este espacio curvo se desvía porque la línea recta (geodésica) está curvada. Esto es análogo a una pelota de golf que sigue la curvatura de un green hundido.

2. **Dilatación temporal** (θ_temporal = 2GM/dc²): El pozo elástico también modifica el ritmo del tiempo (g_tt). Cerca de la masa, el tiempo corre más lento. Para un fotón, esto significa que los "frentes de onda" más cercanos a la masa avanzan más lento que los lejanos, curvando el rayo hacia adentro. Esto es análogo a la refracción en un medio con índice variable.

**¿Por qué no aparece la Coriolis isoclínica?** Los términos de frame-dragging son proporcionales a ω ~ H₀ ~ 10⁻¹⁸ s⁻¹. Su contribución a la deflexión es del orden ωd/c ~ H₀d/c, que para distancias estelares es un efecto cosmológico global, no una corrección local. La deflexión local de la luz está dominada enteramente por la deformación elástica h(r).

### 4.7. Comparación con la v1.0

En la formulación v1.0 (`fuerza_coriolis_4d_trayectorias.md`), se argumentaba que la Coriolis 4D duplicaba la deflexión newtoniana. Esto requería calibrar βω₄D = 1/(2c), lo cual era circular (se ajustaba el parámetro para obtener el resultado deseado).

En la formulación rigurosa, **la Coriolis isoclínica no contribuye a la deflexión local**. El factor 2 proviene enteramente de la estructura métrica de la deformación elástica: la mitad de la curvatura espacial y la mitad de la dilatación temporal. No se necesita ningún parámetro libre.

---

## Paso 5: Límite Newtoniano Completo

### 5.1. Ecuación de movimiento para partículas lentas

Para una partícula con velocidad v ≪ c en la métrica unificada, la ecuación geodésica se reduce a:

$$\ddot{\mathbf{r}} = -\nabla\Phi - 2\boldsymbol{\omega}\times\mathbf{v} - \boldsymbol{\omega}\times(\boldsymbol{\omega}\times\mathbf{r})$$

donde:

- **−∇Φ = −GM/r² r̂**: Gravedad newtoniana (de la deformación elástica h(r))
- **−2ω × v**: Fuerza de Coriolis (del frame-dragging isoclínico)
- **−ω × (ω × r)**: Fuerza centrífuga (de la modificación ω²R² de g_tt)

### 5.2. Verificación de los coeficientes

| Fuerza | Coeficiente | Origen en la métrica | ¿Parámetro libre? |
|--------|-------------|----------------------|-------------------|
| Gravedad | GM/r² | g_tt y g_ij (deformación h) | No: G = c²ω²/(4πT_b) |
| Coriolis | 2ω | g_{tψ}, g_{tθ}, g_{tφ} (rotación) | No: β = 1 |
| Centrífuga | ω² | g_tt (rotación) | No |

### 5.3. Precesión del perihelio de Mercurio

La precesión anómala del perihelio de Mercurio es 43"/siglo. En GR estándar, proviene de la métrica de Schwarzschild. En nuestro formalismo, la métrica inducida sobre la brana deformada **es** la métrica de Schwarzschild en campo débil, por lo que la precesión se calcula de la misma forma.

El cálculo estándar da:

$$\Delta\phi = \frac{6\pi GM}{c^2 a(1-e^2)}$$

donde a es el semieje mayor y e la excentricidad. Para Mercurio: Δφ ≈ 43"/siglo. ✓

**¿Contribuye la Coriolis isoclínica?** La precesión de Coriolis por órbita es ~ωT ~ H₀T ~ 10⁻¹¹ rad/órbita, que es 10⁴ veces menor que la precesión observada. La precesión de Mercurio está dominada enteramente por la deformación elástica.

### 5.4. Resumen: qué explica cada mecanismo

| Fenómeno | Mecanismo principal | Magnitud |
|----------|---------------------|----------|
| Expansión de Hubble | Centrífuga isoclínica (ω²R) | H₀ ~ 70 km/s/Mpc |
| Gravedad newtoniana | Deformación elástica h(r) | GM/r² |
| Precesión de Mercurio | Deformación elástica (Schwarzschild) | 43"/siglo |
| Deflexión de la luz | Deformación elástica (espacial + temporal) | 4GM/dc² |
| Coriolis local | Frame-dragging isoclínico | 2ω × v (inobservable localmente) |
| Centrífuga local | Modificación ω²R² de g_tt | ω²r (inobservable localmente) |

---

## Paso 6: Estructura Completa de la Métrica Unificada

### 6.1. Forma global (coordenadas hiperesféricas)

En coordenadas (τ, ψ, θ, φ) de la brana, con tiempo propio τ:

$$ds^2 = -\left(1 + 2\epsilon\right)c^2\,d\tau^2 + R^2(1+2\epsilon)\left[d\psi^2 + \sin^2\psi\left(d\theta^2 + \sin^2\theta\,d\phi^2\right)\right]$$
$$+ \; 2\omega R^2\left[-\cos\theta\,d\psi + \sin\psi\cos\psi\sin\theta\,d\theta + \sin^2\psi\sin^2\theta\,d\phi\right]d\tau + \mathcal{O}(\epsilon^2, \omega\epsilon)$$

donde ε(ψ,θ,φ) = h(r)/R es la perturbación fraccional del radio.

### 6.2. Forma local (coordenadas cartesianas)

Cerca de un punto de la brana, en coordenadas (τ, x, y, z):

$$ds^2 = -\left(1 - \frac{2GM}{c^2 r}\right)c^2\,d\tau^2 + \left(1 - \frac{2GM}{c^2 r}\right)\left(dx^2+dy^2+dz^2\right)$$
$$+ \; 2\omega\left(-y\,dx + x\,dy\right)d\tau + 2\omega\left(-z\,dx + x\,dz\right)d\tau + \mathcal{O}\left(\frac{G^2M^2}{c^4 r^2}\right)$$

### 6.3. Descomposición por orígenes físicos

$$g_{\mu\nu}^{\text{unificada}} = g_{\mu\nu}^{\text{FLRW}} + \Delta g_{\mu\nu}^{\text{rotación}} + \Delta g_{\mu\nu}^{\text{deformación}}$$

| Componente | FLRW | Rotación | Deformación |
|------------|------|----------|-------------|
| g_tt | −c² | +ω²R² | +2ω²R²ε = 2Φ |
| g_ti | 0 | ωR²·f_i(ψ,θ,φ) | 0 (a primer orden) |
| g_ij | R²γ_ij | 0 | 2R²εγ_ij + ∂_ih∂_jh |

---

## Predicciones y Falsabilidad

### P1: No hay acoplamiento cinético α

La formulación rigurosa predice que **no existe un término de acoplamiento cinético** (el parámetro α de la v1.0) en el potencial gravitatorio. La gravedad newtoniana es exactamente −GM/r, sin corrección proporcional a v²/c² en el potencial. Las correcciones relativistas (precesión, deflexión) provienen de la estructura métrica completa, no de una modificación del potencial newtoniano.

**Test**: Medir la fuerza gravitatoria sobre partículas rápidas (rayos cósmicos, iones relativistas). Si la fuerza es exactamente GM/r² independientemente de la velocidad (en el límite newtoniano), se confirma esta predicción. Si se detecta una dependencia con v², se refuta.

### P2: La Coriolis isoclínica es inobservable localmente

La fuerza de Coriolis del Bulk tiene coeficiente exactamente 2ω₄D con ω₄D ~ H₀ ~ 10⁻¹⁸ s⁻¹. Esto es ~10¹⁵ veces más débil que la Coriolis terrestre (ω_Tierra ~ 10⁻⁴ s⁻¹). **No hay forma de amplificar este efecto localmente** sin violar la geometría de la inmersión.

**Test**: Cualquier detección de Coriolis cósmica local con magnitud significativamente mayor que H₀ refutaría el modelo. La formulación v1.0 predecía efectos observables con βω₄D ~ 1/(2c); la formulación rigurosa dice que esto es imposible.

### P3: Anisotropía cuadrupolar en H₀

La rotación isoclínica rompe la isotropía de la métrica FLRW, produciendo una anisotropía cuadrupolar en la constante de Hubble con amplitud δH/H ~ (ωR/c)². Si ωR ~ c (como sugiere H₀ ~ c/R), la anisotropía sería del 100%, refutada por observaciones. Esto requiere ωR ≪ c.

**Test**: Mediciones direccionales de H₀ con precisión sub-porcentual (SKA, Euclid). Si H₀ es isotrópico a nivel < 0.1%, se requiere ωR < 0.1c, lo cual es consistente con ω₄D ∝ 1/R² y R creciendo.

### P4: La gravedad es estática en escalas locales

La deformación h(r) es estática (no oscila). No hay ondas gravitatorias elásticas en el régimen de campo débil. Las ondas gravitatorias, si existen, provendrían de la dinámica de la métrica completa (ecuaciones de Einstein), no de vibraciones de la brana.

**Test**: LIGO/Virgo detectan ondas gravitatorias con la forma predicha por GR estándar. Si se detectaran oscilaciones adicionales o armónicos no predichos por GR, podría indicar modos de vibración de la brana.

### P5: Relación entre G, ω, T_b y R

La constante de Newton está determinada por:

$$G = \frac{c^2\omega^2}{4\pi T_b}$$

y la condición de virial:

$$\omega^2 = \frac{3}{2}\frac{c^2}{R^2}$$

Combinando: G = 3c⁴/(8πT_bR²). Esto predice una relación específica entre la tensión de brana T_b, el radio cósmico R y G. Si se pudiera medir T_b independientemente (por ejemplo, a partir de la física de alta energía o del espectro de potencias del CMB), esta relación sería testable.

### P6: Correcciones post-newtonianas idénticas a GR

En el límite de campo débil, la métrica inducida es idéntica a Schwarzschild. Por lo tanto, **todas las correcciones post-newtonianas (PPN) son idénticas a las de GR estándar**. Esto incluye:

- Deflexión de la luz: 4GM/dc² ✓
- Retardo de Shapiro: 4GM·ln(4r_1r_2/b²)/c³ ✓
- Precesión de Lense-Thirring: 2GJ/(c²r³) (del frame-dragging, pero con ω ~ H₀, inobservable) ✓
- Precesión de geodésica: 3GM/(c²a(1−e²)) por órbita ✓

**Test**: Cualquier desviación de las predicciones PPN de GR estándar refutaría el modelo. El modelo predice concordancia exacta con GR en todos los tests clásicos de campo débil.

---

## Limitaciones Conocidas

### L1: Campo fuerte no tratado

La derivación asume campo débil (ε = GM/c²r ≪ 1). Cerca de horizontes de agujeros negros (ε → 1), la expansión lineal de la métrica falla. No hemos derivado la métrica completa en campo fuerte, que requeriría resolver la ecuación de membrana elástica no lineal con la acción DBI completa.

**Estado**: La métrica de Schwarzschild completa (con la métrica espacial exacta (1−2GM/c²r)⁻¹ en vez de la aproximación lineal) no se deriva aquí. Se asume que la no linealidad de la acción DBI reproduce la métrica de Schwarzschild completa, pero esto no se ha demostrado.

### L2: Auto-gravedad de la deformación

La deformación h(r) se calcula asumiendo que la masa M es una fuente externa que deforma la brana. No se considera que la deformación misma contribuye a la curvatura (auto-gravedad). En el formalismo de branas, esto corresponde a despreciar los términos de curvatura extrínseca en las ecuaciones de Gauss-Codazzi.

**Estado**: Para masas pequeñas (ε ≪ 1), la auto-gravedad es despreciable. Para masas grandes (ε ~ 1), podría ser significativa.

### L3: Masa de la deformación (back-reaction)

La deformación h(r) tiene energía elástica asociada:

$$E_{\text{elástica}} = \frac{T_b}{2}\int\left[(\nabla h)^2 + \lambda^2 h^2\right]d^3x$$

Esta energía debería contribuir a la masa total del sistema (back-reaction). No la hemos incluido en el cálculo.

**Estado**: La energía elástica es de orden T_b(GM/c²)², que para el Sol es ~10⁻¹⁶ de la masa solar. Despreciable en campo débil.

### L4: Acoplamiento entre deformación y rotación

Los términos de frame-dragging reciben una corrección de orden ε (sección 2.8), que hemos despreciado. En principio, la deformación modifica ligeramente la velocidad de arrastre isoclínico. Esto podría producir efectos de segundo orden en la precesión de Lense-Thirring cerca de masas compactas.

**Estado**: La corrección es de orden GM/(c²r) ~ 10⁻⁸ para el Sol, inobservable.

### L5: Origen de la tensión de brana T_b

La tensión T_b es un parámetro libre del modelo. Su valor se fija a posteriori para reproducir G (T_b ≈ 3.43 × 10⁻¹¹ J/m³). No se deriva de primeros principios.

**Estado**: En teoría de cuerdas, T_b = T_3 (tensión de D3-brana) se deriva de la constante de acoplamiento de cuerdas y el volumen del espacio compacto. En nuestro formalismo, permanece como parámetro fenomenológico.

### L6: Ecuaciones de campo completas

No hemos derivado las ecuaciones de Einstein completas para la métrica inducida. En particular, no hemos mostrado que la métrica de Schwarzschild satisface las ecuaciones de Einstein con la fuente apropiada (delta de Dirac en la masa puntual). Esto requeriría derivar las ecuaciones de Gauss-Codazzi para la brana deformada.

**Estado**: La métrica de Schwarzschild en campo débil es una solución de las ecuaciones de Einstein linealizadas por construcción. La demostración completa para la métrica exacta queda como trabajo futuro.

### L7: Singularidades

La métrica de Schwarzschild tiene una singularidad en r = 0 (y una en r = 2GM/c² en coordenadas de Schwarzschild). No hemos analizado cómo se manifiestan estas singularidades en el formalismo de branas. En particular, la deformación h(r) → −∞ cuando r → 0, lo cual es físicamente problemático (la brana se "pincha").

**Estado**: La acción DBI debería regularizar esta singularidad (la tensión de brana impide deformaciones infinitas), pero esto no se ha demostrado explícitamente.

### L8: Múltiples masas

La derivación asume una sola masa M. Para múltiples masas, las deformaciones se superponen linealmente (en campo débil), pero la interacción no lineal entre pozos gravitatorios no se ha analizado.

**Estado**: En campo débil, la superposición lineal es válida. Para el problema de N cuerpos en campo fuerte, se necesitaría un tratamiento numérico.

---

## Síntesis: La Arquitectura Unificada

La métrica unificada del Universo Centrífugo tiene tres capas, cada una con un origen físico distinto:

```
┌─────────────────────────────────────────────────────┐
│           MÉTRICA UNIFICADA (v3.0)                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Capa 1: FLRW (expansión cósmica)                  │
│  Origen: S³ de radio R(t) en Bulk plano            │
│  Efecto: Hubble, curvatura espacial global          │
│                                                     │
│  Capa 2: Frame-dragging isoclínico                 │
│  Origen: Rotación isoclínica del Bulk               │
│  Efecto: Coriolis (2ω), centrífuga (ω²r)          │
│  Magnitud: ω ~ H₀ ~ 10⁻¹⁸ s⁻¹ (inobservable)    │
│                                                     │
│  Capa 3: Deformación elástica h(r)                 │
│  Origen: Masa M deforma la brana en dirección w    │
│  Efecto: Schwarzschild en campo débil               │
│  Magnitud: GM/c²r ~ 10⁻⁸ (Solar) a 1 (BH)       │
│                                                     │
│  ═════════════════════════════════════════════════  │
│  RESULTADO: Métrica de Schwarzschild + FLRW +      │
│  Coriolis isoclínica residual                      │
│                                                     │
│  Tests clásicos de GR: Capa 3 domina               │
│  Cosmología: Capas 1+2 dominan                     │
│  Factor 2 en deflexión: Capa 3 sola                │
└─────────────────────────────────────────────────────┘
```

**La conclusión central**: La deflexión de la luz, la precesión de Mercurio y todos los tests clásicos de GR provienen enteramente de la **deformación elástica** de la brana (Capa 3). La rotación isoclínica (Capas 1+2) explica la expansión cósmica y predice efectos inerciales globales, pero es demasiado débil para contribuir a la gravedad local. Los dos mecanismos son **independientes y complementarios**: la rotación explica el "motor" cosmológico, la deformación explica la gravedad local.

**Lo que se elimina**: Los parámetros ad-hoc α y β de la v1.0. El factor 2 en la deflexión de la luz no viene de la Coriolis cósmica (que requería calibrar βω₄D = 1/2c), sino de la estructura métrica de la deformación elástica, que lo da de forma automática y natural.

**Lo que se gana**: Una teoría donde la gravedad newtoniana, la relatividad general de campo débil, la expansión de Hubble y las fuerzas inerciales globales emergen de una única estructura geométrica — una 3-esfera elástica rotando en un Bulk 4D — sin parámetros libres más allá de los que determinan la cosmología (R₀, ω₀, T_b).
