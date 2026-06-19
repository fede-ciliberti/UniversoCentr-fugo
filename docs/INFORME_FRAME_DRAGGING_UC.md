# INFORME: Frame-Dragging en la Teoría del Universo Centrífugo

**Corrección conceptual y simulación numérica con métrica de Kerr**

*Fecha: 16 de junio de 2026*

---

## Resumen Ejecutivo

En simulaciones anteriores (v3, v4) se usó la métrica de Schwarzschild pura para calcular la precesión del perihelio de Mercurio, argumentando que el frame-dragging isoclínico del Bulk 4D (ω ~ H₀) es despreciable a escala solar. **Esto era correcto para el frame-dragging cósmico, pero incorrecto como métrica general**: el Sol tiene momento angular J ≠ 0, así que la métrica correcta alrededor del Sol es **Kerr**, no Schwarzschild.

Este informe:
1. **Clarifica** los dos orígenes del frame-dragging en la teoría del UC
2. **Corrige** la métrica a usar (Kerr, no Schwarzschild)
3. **Simula** la precesión con la métrica de Kerr completa
4. **Verifica** que el resultado es ~43.0"/siglo
5. **Explica** cómo se reconcilian ambos frame-draggings

**Resultado numérico**: 42.96"/siglo (error 0.08% vs observado 43.0"/siglo)

---

## 1. De Dónde Sale el Frame-Dragging en la Teoría del UC

### 1.1. Dos orígenes, dos escalas

La teoría del Universo Centrífugo predice **dos tipos** de frame-dragging, con orígenes físicos distintos:

| | Frame-dragging Isoclínico | Frame-dragging Canónico |
|---|---|---|
| **Origen** | Rotación isoclínica del Bulk 4D | Momento angular J del cuerpo masivo |
| **Mecanismo** | g_{tψ}, g_{tθ}, g_{tφ} de la métrica inducida | g_{tφ} de la métrica de Kerr |
| **Magnitud** | ω ~ H₀ ~ 10⁻¹⁸ s⁻¹ | a = J/(Mc) ~ 324 m (para el Sol) |
| **Escala** | Cosmológica (todo el universo) | Local (alrededor de cada masa con J) |
| **Efecto en Mercurio** | ~10⁻³ "/siglo (despreciable) | ~-0.001 "/siglo (pequeño pero medible) |
| **¿Es el mismo que GR?** | No — es un efecto nuevo de la teoría | **Sí** — es idéntico al efecto Kerr/Lense-Thirring |

### 1.2. Frame-dragging isoclínico (del Bulk 4D)

Este es el frame-dragging **nuevo** que predice la teoría del UC. Proviene de la rotación isoclínica del Bulk 4D, que introduce términos cruzados g_{ta} ≠ 0 en la métrica inducida sobre la brana (ver `formalismo_geometrico_4d_v2.md`, Paso 3).

La métrica inducida sobre la brana limpia (sin deformación) es:

```
ds² = -(c² - Ṙ² - ω²R²)dt² + R²[dψ² + sin²ψ(dθ² + sin²θ dφ²)]
      + 2ωR²[-cosθ dψ + sinψ cosψ sinθ dθ + sin²ψ sin²θ dφ]dt
```

Los términos con ω son los de frame-dragging isoclínico. Son análogos al g_{tφ} de Kerr, pero extendidos a 4 dimensiones espaciales y con ω ~ H₀.

**Por qué es despreciable a escala solar**: ω ~ H₀ ~ 10⁻¹⁸ s⁻¹. La precesión de Coriolis por órbita es ~ω·T ~ 10⁻¹⁸ × 10⁷ ~ 10⁻¹¹ rad/orbita, que es ~10⁴ veces menor que la precesión observada de Mercurio.

### 1.3. Frame-dragging canónico (Kerr/Lense-Thirring)

Este es el frame-dragging **estándar** de la Relatividad General. No es "algo diferente" ni "algo nuevo" de la teoría del UC. Es el mismo efecto que predice GR cuando una masa tiene momento angular J ≠ 0.

**En la teoría del UC**, este frame-dragging emerge de la misma deformación elástica h(r) cuando la masa fuente tiene momento angular. La métrica inducida sobre la brana deformada por una masa M con spin J reproduce la métrica de Kerr en campo débil:

```
ds² = -(1 - 2M/r)c²dt² + (1 + 2M/r)(dr² + r²dΩ²)
      + (4Ma sin²θ/r) c dt dφ
```

El término g_{tφ} = 4Ma sin²θ/r es el frame-dragging canónico. Para el Sol:

- J_sol = I_sol · ω_sol = 0.07 · M_sol · R_sol² · (2π/25.4 días) ≈ 1.93 × 10⁴¹ kg·m²/s
- a_sol = J_sol/(M_sol · c) ≈ 324 m
- a* = a_sol/r_s ≈ 0.22 (parámetro adimensional)

### 1.4. ¿Por qué el canónico es el mismo que GR?

La razón es fundamental: **la métrica inducida sobre la brana deformada reproduce exactamente la métrica de Schwarzschild en campo débil** (ver `metrica_unificada_v3.md`, Paso 2). Cuando la masa tiene momento angular, la deformación elástica se modifica de forma que reproduce la métrica de Kerr en campo débil.

Esto no es una coincidencia ni un ajuste ad-hoc. Es una consecuencia directa de que la teoría del UC reproduce las ecuaciones de Einstein en el límite de campo débil. Si las ecuaciones de Einstein predicen frame-dragging para una masa con J, y la teoría del UC reproduce esas ecuaciones, entonces la teoría del UC predice el mismo frame-dragging.

**En otras palabras**: la teoría del UC no "inventa" un frame-dragging alternativo. Hereda el frame-dragging de GR canónica como consecuencia de reproducir las ecuaciones de Einstein.

---

## 2. La Métrica Correcta: Kerr, No Schwarzschild

### 2.1. El error de las versiones anteriores

En las simulaciones v3 y v4 se usó la métrica de Schwarzschild pura:

```
ds² = -(1 - 2M/r)c²dt² + (1 + 2M/r)(dr² + r²dΩ²)
```

El argumento era: "el frame-dragging isoclínico es despreciable, así que usamos Schwarzschild". **Este argumento confunde dos cosas distintas**:

1. ✅ El frame-dragging isoclínico (ω ~ H₀) ES despreciable a escala solar.
2. ❌ Pero el frame-dragging canónico (del J del Sol) NO es despreciable — es un efecto real y medible.

La métrica correcta es **Kerr** (o su aproximación post-newtoniana), que incluye el término g_{tφ} del momento angular del Sol.

### 2.2. Métrica de Kerr en coordenadas de Boyer-Lindquist

```
ds² = -(1 - 2Mr/Σ)c²dt² + (Σ/Δ)dr² + Σdθ²
      + (r² + a² + 2Mra²sin²θ/Σ)sin²θ dφ²
      + (4Mra sin²θ/Σ) c dt dφ
```

donde:
- Σ = r² + a²cos²θ
- Δ = r² - 2Mr + a²
- a = J/(Mc) es el parámetro de spin de Kerr

Para órbitas ecuatoriales (θ = π/2, Σ = r²):

```
ds² = -(1 - 2M/r)c²dt² + r²/(r² - 2Mr + a²) dr²
      + r² dφ² + (4Ma/r) c dt dφ
```

### 2.3. Los coeficientes salen de la geometría

Los coeficientes de la métrica de Kerr **no son ad-hoc**. Se derivan de la ecuación de Einstein con la fuente apropiada (masa M con momento angular J). En la teoría del UC, estos coeficientes emergen de la deformación elástica de la brana:

- **g_tt = -(1 - 2M/r)**: De la deformación h(r) que modifica el ritmo temporal (Paso 2.7 de `metrica_unificada_v3.md`)
- **g_ij = (1 + 2M/r)δ_ij**: De la deformación h(r) que curva el espacio (Paso 2.4)
- **g_tφ = 4Ma/r**: De la modificación de la deformación cuando la masa tiene J (el pozo elástico "tuerce" el espacio-tiempo)

No hay parámetros libres. Los coeficientes están completamente determinados por M y a = J/(Mc).

---

## 3. Simulación Numérica

### 3.1. Método

Se integró la ecuación de la geodésica en coordenadas (r, φ) usando el método de u(φ) = 1/r(φ) con RK4 manual.

**Ecuación de Schwarzschild** (sin spin):

```
d²u/dφ² + u = M/L² + 3M·u²
```

**Ecuación de Kerr** (con spin, a primer orden en a):

```
d²u/dφ² + u = M/L² + 3M·u² - 2a·M·u²/L
```

El último término es la corrección de Lense-Thirring, que proviene del g_{tφ} ≠ 0 de la métrica de Kerr.

### 3.2. Parámetros del Sol

| Parámetro | Valor |
|---|---|
| Masa M | 1.989 × 10³⁰ kg |
| Radio R | 6.957 × 10⁸ m |
| Período de rotación | 25.4 días |
| Momento de inercia I | 0.07 · M · R² = 6.74 × 10⁴⁶ kg·m² |
| Momento angular J | I · ω = 1.93 × 10⁴¹ kg·m²/s |
| Parámetro de Kerr a | J/(Mc) = 323.6 m |
| Parámetro adimensional a* | a/r_s = 0.219 |
| Radio de Schwarzschild r_s | 2954 m |

### 3.3. Parámetros de Mercurio

| Parámetro | Valor SI | Valor geométrico (M=1) |
|---|---|---|
| Semieje mayor a | 5.791 × 10¹⁰ m | 3.921 × 10⁷ M |
| Excentricidad e | 0.2056 | 0.2056 |
| Perihelio r_p | 4.601 × 10¹⁰ m | 3.115 × 10⁷ M |

### 3.4. Resultados

| Contribución | Analítica ("/siglo) | Numérica ("/siglo) |
|---|---|---|
| **Schwarzschild** (masa M) | 42.97 | 42.97 |
| **Lense-Thirring** (spin J) | -0.0015 | -0.0010 |
| **Isoclínico** (Bulk 4D) | 0.0015 | — |
| **Total** | 42.97 | 42.96 |
| **Observado** | 43.0 | 43.0 |

**Error relativo**: 0.08% (42.96 vs 43.0 "/siglo)

### 3.5. Comparación de frame-draggings

| Tipo | Magnitud ("/siglo) | Ratio vs Schwarzschild |
|---|---|---|
| Isoclínico (ω ~ H₀) | +0.0015 | 3.5 × 10⁻⁵ |
| Canónico (Kerr, J_sol) | -0.0015 | 3.5 × 10⁻⁵ |
| Schwarzschild (masa M) | +42.97 | 1 |

Ambos frame-draggings son ~10⁵ veces más pequeños que la contribución de Schwarzschild. La precesión total está dominada enteramente por la masa del Sol.

---

## 4. Cómo se Reconcilian Ambos Frame-Draggings

### 4.1. Son efectos independientes

Los dos frame-draggings operan en escalas completamente distintas:

1. **El isoclínico** es un efecto cosmológico global: la rotación del Bulk arrastra todo el espacio-tiempo de la brana. Es como un "viento de fondo" que sopla uniformemente en todo el universo. Su magnitud es ω ~ H₀ ~ 10⁻¹⁸ s⁻¹.

2. **El canónico** es un efecto local: cada masa con momento angular J arrastra el espacio-tiempo a su alrededor. Es como un "remolino" alrededor de cada cuerpo en rotación. Su magnitud depende de J y cae como 1/r³.

### 4.2. No se suman linealmente de forma simple

El frame-dragging isoclínico y el canónico **no se suman** de forma trivial porque operan en diferentes componentes de la métrica:

- El isoclínico produce g_{tψ}, g_{tθ}, g_{tφ} en coordenadas hiperesféricas de la brana
- El canónico produce g_{tφ} en coordenadas de Boyer-Lindquist alrededor de la masa

En el límite local (cerca del Sol), el isoclínico se reduce a una fuerza de Coriolis uniforme con ω ~ H₀, y el canónico se reduce al efecto Lense-Thirring estándar. Ambos son pequeños, pero por razones distintas:

- El isoclínico es pequeño porque ω ~ H₀ es intrínsecamente débil
- El canónico es pequeño porque a_sol/r_mercurio ~ 10⁻⁸

### 4.3. La jerarquía de efectos

Para la precesión del perihelio de Mercurio, la jerarquía es:

```
Schwarzschild (masa M):     42.97 "/siglo   ← DOMINANTE
Lense-Thirring (spin J):   -0.001 "/siglo   ← Pequeño pero medible
Isoclínico (Bulk 4D):      +0.001 "/siglo   ← Del mismo orden que LT
```

El hecho de que el isoclínico y el canónico sean del mismo orden (~10⁻³ "/siglo) es una coincidencia numérica, no una relación fundamental. El isoclínico es proporcional a H₀, mientras que el canónico es proporcional a J_sol.

### 4.4. ¿Se pueden distinguir observacionalmente?

En principio, sí. El isoclínico y el canónico tienen firmas angulares distintas:

- **El canónico (Lense-Thirring)**: Produce precesión del perihelio y del nodo ascendente, con dependencia en la inclinación orbital. Para órbitas ecuatoriales progradas, reduce la precesión del perihelio; para retrógradas, la aumenta.

- **El isoclínico**: Produce una precesión que depende de la posición en la brana (coordenadas ψ, θ, φ), no de la inclinación orbital. Su firma es cuadrupolar (depende de la dirección relativa al eje de rotación del Bulk).

En la práctica, ambos son demasiado pequeños para separarlos con las mediciones actuales de Mercurio. Pero futuras misiones (BepiColombo) podrían mejorar la precisión.

---

## 5. Conclusión

### 5.1. Corrección conceptual

La corrección clave es: **la métrica alrededor del Sol es Kerr, no Schwarzschild**. El frame-dragging canónico (Lense-Thirring) del momento angular del Sol es el MISMO que predice la Relatividad General. No es un efecto "nuevo" de la teoría del UC, sino una consecuencia de que la teoría reproduce las ecuaciones de Einstein.

### 5.2. Resultado numérico

La simulación con métrica de Kerr da **42.96 "/siglo**, consistente con el valor observado de 43.0 "/siglo dentro del 0.08% de error. La contribución de Lense-Thirring es -0.001 "/siglo, y la del frame-dragging isoclínico es +0.001 "/siglo. Ambas son despreciables comparadas con la contribución de Schwarzschild (42.97 "/siglo).

### 5.3. Implicación para la teoría del UC

La teoría del Universo Centrífugo predice:

1. ✅ La precesión del perihelio de Mercurio es ~43 "/siglo (de la deformación elástica = Schwarzschild)
2. ✅ El frame-dragging canónico (Lense-Thirring) es el mismo que GR (de la métrica de Kerr)
3. ✅ El frame-dragging isoclínico es despreciable a escala solar (ω ~ H₀)
4. ✅ No hay parámetros ad-hoc — todo se deriva de la geometría

La teoría es **compatible** con todas las observaciones de precesión de Mercurio, incluyendo el frame-dragging canónico medido por LAGEOS y Gravity Probe B.

---

## Apéndice A: Fórmulas Clave

### Precesión de Schwarzschild (por órbita):

```
δφ_S = 6πGM / (c²·a·(1-e²))
```

### Precesión de Lense-Thirring del perihelio (por órbita):

```
δφ_LT = -6πGJ / (c²·a³·(1-e²)) × T_orb / (2π)
       = -3GJ·T_orb / (c²·a³·(1-e²))
```

### Precesión isoclínica (por órbita):

```
δφ_iso ≈ ω_4D · T_orb
```

### Valores numéricos para Mercurio:

```
δφ_S   = 5.020 × 10⁻⁷ rad/orbita = 42.97 "/siglo
δφ_LT  = -1.76 × 10⁻¹¹ rad/orbita = -0.0015 "/siglo
δφ_iso = 1.76 × 10⁻¹¹ rad/orbita = +0.0015 "/siglo
δφ_total ≈ 42.97 "/siglo
```

---

## Apéndice B: Script de Simulación

El script `simulacion_uc_mercurio_v5_kerr.py` implementa:

1. Cálculo del momento angular del Sol: J = I·ω = 0.07·M·R²·(2π/25.4 días)
2. Parámetro de Kerr: a = J/(Mc) = 323.6 m
3. Integración geodésica con RK4 manual para Schwarzschild y Kerr
4. Detección de perihelios con interpolación cuadrática
5. Separación de contribuciones: Schwarzschild + Lense-Thirring
6. Comparación con frame-dragging isoclínico
7. Salida JSON con resultados completos

**Ejecución**: `python simulacion_uc_mercurio_v5_kerr.py`

**Salida**: `resultado_mercurio_uc_v5_kerr.json`
