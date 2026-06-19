# Revisión de Literatura: Universos Rotantes y Equivalentes Formales

**Proyecto**: Universo Centrífugo — Opción B: Cirugía Mayor  
**Fecha**: 16 de junio de 2026  
**Propósito**: Determinar si la idea de una 3-esfera rotando en un Bulk 4D tiene precedentes rigurosos en la literatura, y si esos precedentes son viables o tienen problemas fatales.

---

## 1. Teorías Formales Existentes

### 1.1 Universo de Gödel (1949) y Extensiones

**Referencia original**: Gödel, K. (1949). *An Example of a New Type of Cosmological Solutions of Einstein's Field Equations*. Rev. Mod. Phys. 21, 447.

**Qué es**: Una solución exacta de las ecuaciones de Einstein que describe un universo homogéneo con rotación global (vorticidad). La métrica original es estacionaria (no expande) y contiene **curvas temporales cerradas (CTCs)**, es decir, permite viajes en el tiempo.

**Problema fatal**: Las CTCs violan la causalidad. Einstein mismo lo consideró problemático.

**Extensiones causales (Gödel-type con expansión)**:
- **Obukhov (1992, 2000)** y **Korotkii & Obukhov (1998)**: Desarrollaron una clase de métricas de tipo Gödel que **expanden y rotan simultáneamente**, y demostraron que para ciertos valores de parámetros (condición k > 0), **no existen CTCs**. La métrica es:

  ds² = dt² + 2√σ eᵐˣ dt dy - (e²ᵐˣ - k)dy² - dx² - dz²

  donde m, σ, k > 0 son constantes. La condición k > 0 garantiza ausencia de CTCs.

- **Rebouças & Tiomno (1983)**: Demostraron que la condición m² = 4Ω² produce la primera solución exacta de tipo Gödel **completamente causal** con homogeneidad espacio-temporal.

**Veredicto para UC**: La métrica de Gödel-type con expansión es el equivalente formal más cercano a la idea de un universo rotante. **Es viable sin CTCs** si se satisface k > 0. Sin embargo, es una métrica 3+1D — no involucra embebimiento en un Bulk 4D.

### 1.2 Cosmologías de Bianchi (Tipos V, VII_h, IX)

**Referencia clave**: Saadeh, D., et al. (2016). *How Isotropic is the Universe?* Phys. Rev. Lett. 117, 131302.

**Qué son**: Las métricas de Bianchi son las soluciones homogéneas pero anisotrópicas de las ecuaciones de Einstein. Los tipos V, VII₀, VII_h y IX permiten rotación (vorticidad). El tipo VII_h es el más general y contiene al tipo V y VII₀ como límites.

**Restricciones observacionales severas**:
- **Planck 2015** (Saadeh et al.): Límite sobre vorticidad (ω/H)₀ < 7.6 × 10⁻¹⁰ (95% CL) usando solo temperatura CMB.
- **Saadeh et al. 2016** (con polarización): Límite mejorado (ω/H)₀ < 5.2 × 10⁻¹¹ (95% CL) — un orden de magnitud más estricto.
- Esto significa que la rotación global del universo, si existe, es **extremadamente pequeña**: ω₀ < 5.2 × 10⁻¹¹ × H₀ ≈ 10⁻²⁸ s⁻¹.

**Veredicto para UC**: Este es el **obstáculo observacional más serio**. Cualquier teoría con rotación global debe predecir ω₀ < 10⁻²⁸ s⁻¹, lo cual es 8 órdenes de magnitud menor que el ω₄D ≈ 10⁻²⁰ s⁻¹ que el modelo UC postula. El modelo UC necesita explicar por qué la rotación observable es tan pequeña a pesar de que la rotación hiperdimensional es mucho mayor.

### 1.3 Teoría Einstein-Cartan y Torsión Cosmológica

**Referencias clave**:
- Hehl, F.W., et al. (1976). *General relativity with spin and torsion*. Rev. Mod. Phys. 48, 393.
- Popławski, N. (2010). *Cosmology with torsion*. arXiv:1007.1919.
- Kranas, et al. (2019). *Friedmann-like universes with torsion*.
- Ivanov (2016). *Einstein-Cartan gravity with torsion field serving as origin for cosmological constant or dark energy density*. ApJ 829, 47.

**Qué es**: La teoría Einstein-Cartan (EC) extiende la relatividad general permitiendo que la conexión afín tenga torsión (parte antisimétrica). La torsión está acoplada al espín de la materia. En el contexto cosmológico, la torsión modifica las ecuaciones de Friedmann:

H² = (8πG/3)ρ - k/a² - 4φ² - 4Hφ

donde φ(t) es el campo de torsión. La torsión puede:
1. Actuar como **energía oscura efectiva** (w = -1), explicando la aceleración cósmica sin Λ.
2. Generar un **Big Bounce** (evitar la singularidad inicial).
3. Mimetizar **curvatura espacial** o **constante cosmológica** según la orientación del vector de torsión.

**Conexión con UC**: La torsión de Einstein-Cartan es **exactamente el equivalente formal** del "efecto Coriolis 4D" que el modelo UC postula ad-hoc. En EC, la torsión emerge naturalmente de la geometría (conexión no-simétrica), no se postula. Las ecuaciones de Friedmann modificadas por torsión son formalmente idénticas a lo que UC intenta derivar.

**Veredicto para UC**: La teoría Einstein-Cartan **ya hace lo que UC quiere hacer**, pero de forma rigurosa. La torsión cosmológica produce términos adicionales en Friedmann que pueden explicar energía oscura y materia oscura. La diferencia clave es que EC no necesita un Bulk 4D — la torsión es intrínseca al espacio-tiempo 4D.

### 1.4 Modelos de Branas en Rotación

**Estado**: **No existe en la literatura mainstream** un modelo de brana 3D rotando en un Bulk 4D plano que produzca una métrica FLRW con términos extra.

Los modelos de branas (Randall-Sundrum, DGP, etc.) típicamente:
- Tienen Bulk 5D (no 4D).
- La dinámica viene de gravedad que "filtra" al Bulk, no de rotación.
- No consideran rotación isoclínica de la brana.

**La rotación isoclínica de S³ en ℝ⁴** es una construcción matemática bien definida (conocida desde Clifford en el siglo XIX), pero **no ha sido usada como base de un modelo cosmológico formal** en la literatura revisada por pares.

---

## 2. Críticas y Resultados Conocidos

### 2.1 Curvas Temporales Cerradas (CTCs)

| Modelo | ¿Tiene CTCs? | Condición para evitarlas |
|--------|-------------|--------------------------|
| Gödel original (1949) | **Sí** | No hay condición — siempre tiene CTCs |
| Gödel-type con expansión (Obukhov 2000) | **No** | Si k > 0 (parámetro métrico) |
| Bianchi VII_h con vorticidad | **No** | No produce CTCs por construcción |
| UC (rotación isoclínica S³) | **No confirmado** | Depende de la métrica inducida — no se ha demostrado formalmente |

**Nota crítica**: La rotación isoclínica en S³ es matemáticamente diferente de la rotación de Gödel. En la rotación isoclínica, **todos los puntos de S³ se mueven con la misma velocidad angular** respecto al centro 4D, lo cual es una propiedad de simetría que no existe en 3D. Esto podría evitar CTCs por construcción, pero **requiere demostración formal**.

### 2.2 Restricciones del CMB

La restricción más fuerte viene de Planck con polarización:

**(ω/H)₀ < 5.2 × 10⁻¹¹** (Saadeh et al. 2016, 95% CL)

Esto es devastador para modelos con rotación global observable. Sin embargo:

1. **Los modelos de tipo Gödel con expansión (Obukhov/Korotkii)** son compatibles con CMB isotrópico porque la rotación **no produce anisotropía en la temperatura del CMB** — solo efectos de segundo orden (polarización, parallax). Obukhov demostró formalmente que la vorticidad pura no viola la isotropía del CMB.

2. **El modelo UC** postula que la rotación es en el Bulk 4D, no directamente observable como vorticidad 3D. La pregunta clave es: ¿la proyección de la rotación isoclínica produce vorticidad observable en 3D? Si la rotación isoclínica preserva la isotropía (como argumenta el modelo), entonces las restricciones del CMB no aplican directamente.

**Veredicto**: Las restricciones del CMB son compatibles con UC **solo si** la rotación isoclínica no produce vorticidad observable en 3D. Esto necesita demostración formal.

### 2.3 Frame-Dragging y Efecto Coriolis

En relatividad general, la rotación produce **frame-dragging** (arrastre de marcos inerciales), cuantificado por el tensor de vorticidad ω_μν. En los modelos de Gödel-type:

ω = (m/2R)√(σ/(k+σ))

En Einstein-Cartan, el "efecto Coriolis" emerge naturalmente de la torsión — es **derivado de la geometría**, no postulado.

**En UC**: El "efecto Coriolis 4D" está **postulado** como consecuencia de la rotación isoclínica, pero no se ha derivado formalmente de una métrica inducida. El RECONSTRUCTION_PLAN.md reconoce esto explícitamente: Track 1 pide "demostrar que la conexión inducida contiene términos que mapean a Coriolis".

---

## 3. Mapeo al Universo Centrífugo

### 3.1 ¿Cómo se llama en la literatura lo que UC intenta hacer?

La idea central de UC — un universo con rotación global que produce expansión y efectos tipo energía oscura — tiene **dos equivalentes formales** en la literatura:

| Concepto UC | Equivalente formal en la literatura |
|-------------|-------------------------------------|
| Rotación isoclínica de S³ en ℝ⁴ | **No tiene equivalente directo** — es una construcción original |
| Efecto Coriolis 4D → expansión 3D | **Torsión cosmológica** (Einstein-Cartan) |
| Brana S³ rotando en Bulk 4D | **Métrica de Gödel-type con expansión** (Obukhov/Korotkii) |
| Tensor energía-momento rotacional | **Tensor de espín-fluido** (Weyssenhoff) en EC |
| Expansión como proyección de rotación | **Vorticidad cósmica** (Bianchi VII_h) |

### 3.2 Diferencias clave entre UC y los modelos existentes

| Aspecto | UC (ad-hoc) | Gödel-type con expansión | Einstein-Cartan |
|---------|-------------|--------------------------|-----------------|
| **Dimensión del Bulk** | 4D (ℝ⁴) | 3+1D (intrínseco) | 3+1D (intrínseco) |
| **Origen de la rotación** | Postulada (ω₄D) | Postulada (Ω) | Derivada del espín de fermiones |
| **Mecanismo de expansión** | Proyección geométrica | Término métrico explícito | Término de torsión en Friedmann |
| **CTCs** | No demostrado | Evitables (k > 0) | No aplicable (no hay rotación global) |
| **CMB** | Compatible si isoclínica preserva isotropía | Compatible (Obukhov 2000) | Compatible (torsión no produce anisotropía de T) |
| **Predicción de eje** | Sí (eje preferencial) | Sí (dirección z) | No (torsión es escalar en FLRW) |
| **Formalismo** | Ad-hoc (mecánico) | Riguroso (métrica exacta) | Riguroso (conexión con torsión) |

### 3.3 ¿Qué necesita UC para ser riguroso?

1. **Métrica inducida**: Derivar explícitamente la métrica 3+1D inducida en la brana S³ por la rotación isoclínica en ℝ⁴. Esto es lo que el RECONSTRUCTION_PLAN.md pide en Track 1.

2. **Demostración de ausencia de CTCs**: Probar formalmente que la métrica inducida no contiene curvas temporales cerradas.

3. **Conexión con torsión**: Mostrar que los términos extra en la métrica inducida son equivalentes a los términos de torsión de Einstein-Cartan. Si esto se logra, UC se convierte en una **realización geométrica** de la torsión cosmológica, lo cual es una contribución legítima.

4. **Compatibilidad con CMB**: Demostrar que la rotación isoclínica no produce vorticidad observable en 3D, o calcular la vorticidad residual y verificar que cumple (ω/H)₀ < 5.2 × 10⁻¹¹.

---

## 4. Veredicto Final

### ¿Es la idea de un universo FLRW rotante geométricamente válida?

**Sí, con condiciones.** La idea de un universo con rotación global que expande es geométricamente válida y tiene precedentes rigurosos:

1. **Las métricas de Gödel-type con expansión** (Obukhov, Korotkii, Rebouças-Tiomno) son soluciones exactas de las ecuaciones de Einstein que describen universos rotantes y expandentes, sin CTCs, y compatibles con la isotropía del CMB.

2. **La teoría Einstein-Cartan** proporciona un marco formal donde la torsión (equivalente a "efecto Coriolis") emerge naturalmente de la geometría y modifica las ecuaciones de Friedmann, pudiendo explicar energía oscura y materia oscura.

3. **Los modelos de Bianchi VII_h** con vorticidad son la clase más general de universos homogéneos anisotrópicos con rotación, y están fuertemente constreñidos por datos del CMB.

### ¿Es la idea de UC (S³ rotando isoclínicamente en ℝ⁴) nueva?

**Parcialmente nueva.** La rotación global del universo es una idea antigua (Gödel 1949). La torsión cosmológica es una idea establecida (Einstein-Cartan, Hehl 1976). Lo que es **nuevo** en UC es:

- **El mecanismo específico**: Rotación isoclínica de S³ embebida en ℝ⁴ como origen de la expansión y efectos de energía oscura.
- **La conexión entre embebimiento y torsión**: Si se puede demostrar que la métrica inducida por la rotación isoclínica produce términos equivalentes a la torsión de Einstein-Cartan, UC sería una **realización geométrica concreta** de la torsión cosmológica.

### ¿Qué modificaciones necesita UC?

1. **Obligatorio**: Derivar la métrica inducida formalmente (Track 1 del RECONSTRUCTION_PLAN.md). Sin esto, el modelo permanece ad-hoc.

2. **Obligatorio**: Demostrar ausencia de CTCs en la métrica inducida.

3. **Recomendado**: Establecer la equivalencia formal entre los términos de la métrica inducida y los términos de torsión de Einstein-Cartan. Esto convertiría UC de una analogía mecánica en una **realización geométrica** de la torsión cosmológica — una contribución legítima y publicable.

4. **Recomendado**: Calcular la vorticidad residual observable en 3D y verificar compatibilidad con las restricciones de Planck (ω/H < 5.2 × 10⁻¹¹).

### ¿Es un red herring?

**No.** La idea no es un red herring. Es una **variante geométrica legítima** de ideas establecidas (rotación cósmica, torsión cosmológica) con un mecanismo específico nuevo (rotación isoclínica de S³). Sin embargo, **en su forma actual es ad-hoc** y necesita el trabajo formal del Track 1 para ser rigurosa. La literatura existente proporciona el marco teórico necesario para hacer este trabajo.

---

## 5. Papers y Autores Clave

| Referencia | Año | Relevancia |
|-----------|-----|-----------|
| Gödel, K. *Rev. Mod. Phys.* 21, 447 | 1949 | Solución original del universo rotante |
| Obukhov, Yu.N. *Gen. Rel. Grav.* 24, 121 | 1992 | Métricas Gödel-type causales con expansión |
| Korotkii, V.G. & Obukhov, Yu.N. *Gen. Rel. Grav.* 24, 121 | 1992 | Extensión con expansión, sin CTCs |
| Rebouças, M.J. & Tiomno, J. *Phys. Rev. D* 28, 1251 | 1983 | Primera solución Gödel-type causal exacta |
| Hehl, F.W., et al. *Rev. Mod. Phys.* 48, 393 | 1976 | Revisión completa de Einstein-Cartan |
| Popławski, N. *arXiv:1007.1919* | 2010 | Big Bounce y universo cerrado desde espín y torsión |
| Kranas, et al. *Friedmann-like universes with torsion* | 2019 | Friedmann modificadas por torsión, compatible con datos |
| Saadeh, D., et al. *Phys. Rev. Lett.* 117, 131302 | 2016 | Restricción más fuerte sobre vorticidad cósmica |
| Barrow, et al. *Friedmann-like universes with torsion* | 2018 | Torsión puede mimetizar curvatura, Λ, o energía oscura |
| Ivanov, A. *ApJ* 829, 47 | 2016 | Torsión como origen de constante cosmológica/energía oscura |
| Svozilová, et al. *arXiv:2506.00860* | 2025 | Restricciones cosmográficas sobre universo Gödel-type |
| Campista, et al. *arXiv:2508.00759* | 2025 | ¿Puede la rotación cósmica resolver la tensión de Hubble? |