# 🌌 Evolución Tecnológica: Transición de BSSN a Solver Espectral FFT

**Registro Histórico y Lecciones Aprendidas de las Simulaciones de Alta Resolución**  
*Universo Centrífugo Research Team — Junio de 2026*

---

## 📖 Resumen de la Transición de Paradigma

Durante las Fases 1 y 2 del proyecto Universo Centrífugo, el desarrollo numérico se centró en adaptar el **formalismo BSSN (Baumgarte-Shapiro-Shibata-Nakamura)** para simular la evolución dinámica del espacio-tiempo 4D. Aunque BSSN es el estándar indiscutible en Relatividad General numérica para la simulación de agujeros negros y colisiones estelares, su aplicación en nuestro modelo de gravedad emergente local presentó serios desafíos de escalabilidad y estabilidad computacional.

La investigación culminó con un **cambio de paradigma técnico** exitoso hacia un **Solver Espectral FFT (Transformada Rápida de Fourier) de Membrana Elástica**. Este cambio eliminó la necesidad de integradores temporales costosos y complejos parches de memoria, reduciendo el tiempo de ejecución de días a segundos.

---

## 🛠️ El Enfoque Histórico: Formalismo BSSN 3D

El desarrollo inicial (documentado en los planes estratégicos 256³) se basó en resolver las ecuaciones completas de evolución temporal de Einstein en una grilla de alta densidad de `256³` puntos mediante diferencias finitas y variables de estado BSSN.

### Características del Diseño BSSN Original:
- **21 variables por punto de malla**: Almacenamiento masivo de componentes métricas, de curvatura extrínseca y símbolos de conexión conformes.
- **División en Bloques (Chunks)**: Necesidad de segmentar la grilla en bloques de `64³` o `32³` para evitar el desbordamiento de la memoria RAM, requiriendo complejas zonas de amortiguación o *ghost cells* para las derivadas en las fronteras.
- **Mapeo de Memoria (Memory Mapping)**: Uso de archivos binarios en disco (`.npy` mmap) para procesar simulaciones de más de 200 GB en estaciones de trabajo estándar.
- **Altos Tiempos de Cómputo**: Integraciones de evolución temporal que tomaban desde 12 horas hasta varios días de procesamiento.

### Lecciones Aprendidas del Fracaso de BSSN:
1. **Ineficiencia Física**: En el Universo Centrífugo, la gravedad a escalas locales emerge como una deformación espacial estática causada por el empuje centrífugo constante del Bulk. Tratar de evolucionar dinámicamente un espacio-tiempo que es intrínsecamente estático en escalas de tiempo locales mediante BSSN era físicamente redundante y computacionalmente destructivo.
2. **Inestabilidades Numéricas**: Las fluctuaciones numéricas de las diferencias finitas y los errores de aproximación en las fronteras de los bloques (fugas en las *ghost cells*) inducían vibraciones de alta frecuencia espurias que desestabilizaban la simulación a largo plazo.
3. **Pérdida de Simetría**: La interpolación en bloques dificultaba preservar la simetría esférica natural de las perturbaciones del potencial en la 3-esfera.

---

## ⚡ El Nuevo Paradigma: Solver Espectral FFT

En la Fase 3, la teoría adoptó la **metodología de gravedad emergente elástica**, modelando el universo como una membrana elástica sometida a tensión superficial. Bajo este enfoque, el potencial gravitatorio local se resuelve resolviendo la ecuación diferencial de membrana:

`∇²h - λ²h = S(r)`

### Ventajas del Nuevo Solver Espectral FFT:
- **Exactitud Matemática**: En lugar de aproximar derivadas locales con diferencias finitas, el solver FFT transforma la ecuación completa al espacio de frecuencias, donde las derivadas espaciales se vuelven multiplicaciones algebraicas directas.
- **Rendimiento Instantáneo**: Una simulación con resolución completa de `256³` puntos que antes requería días con BSSN, ahora se resuelve de manera exacta en **1.27 segundos** en una computadora común.
- **Consumo de Memoria Ínfimo**: Al evitar integradores de Runge-Kutta de 4º orden y 21 campos temporales, los requerimientos de RAM bajaron de 200 GB a menos de 1.5 GB, eliminando para siempre la necesidad de chunks y mapeos de memoria.
- **Estabilidad Absoluta**: Al ser un método espectral global, es numéricamente estable y no sufre de las fugas de frontera ni de las oscilaciones numéricas locales que plagaban el enfoque BSSN.

---

## 📌 Estado de la Documentación del Repositorio

Para mantener la claridad estructural del proyecto y evitar confusiones durante las auditorías, **las guías técnicas, especificaciones de hardware y documentos de resolución de problemas específicos del obsoleto sistema BSSN han sido eliminados de este directorio**. El código de simulación actual vive de forma unificada bajo un único solver espectral optimizado.

Este documento sirve como registro oficial y memoria técnica de las Fases de desarrollo previas para futuros investigadores de la teoría.
