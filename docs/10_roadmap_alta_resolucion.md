# Roadmap Científico: Cosmología de Membranas Elásticas y Publicación

*Versión: 2.0 - Fecha: 7 de junio de 2026 (Refundación Elástica y Pruebas Multigrid)*
*Autor: Fede & Sisyphus — Universo Centrífugo Research Team*

---

## 1. Visión General del Próximo Hito de Investigación

Con la convalidación cuantitativa superior al **99.8%** de la gravedad emergente de Schwarzschild lograda en segundos mediante el solucionador espectral FFT, el proyecto del Universo Centrífugo ha completado su validación local de campo débil. 

El siguiente hito estratégico es escalar este modelo espectral desde una sola masa puntual aislada hacia **sistemas multi-cuerpo, distribuciones de masa galácticas completas y simulaciones cosmológicas de estructura a gran escala** para explicar la Materia Oscura y la Energía Oscura bajo el marco elástico de la 3-esfera, allanando el camino para publicaciones en revistas de alto impacto como *Physical Review D* y *JCAP*.

---

## 2. Roadmap de Desarrollo de Simulaciones Elásticas Multigrid

La rapidez matemática del solucionador espectral FFT permite simular sistemas infinitamente más complejos sin necesidad de recursos HPC masivos de supercómputo.

```
Masa Puntual Aislada (Schwarzschild 256³) [COMPLETO]
       │
       ▼
Sistemas Binarios de Membrana (Dos Masas en Órbita) [Q3 2026]
       │
       ▼
Distribuciones Galácticas y Curvas de Rotación (Materia Oscura) [Q4 2026]
       │
       ▼
Simulación Cosmológica de Estructura a Gran Escala S³ [Q1 2027]
```

### 2.1. Hitos Técnicos y de Software

#### Hito 1: Sistemas Binarios y Emisión de Ondas de Membrana (Q3 2026)
*   **Física**: Simular dos cuerpos en órbita mutua deformando la brana. Evaluar cómo el movimiento de los pozos de potencial elásticos genera "arrugas" (ondas elásticas de membrana) que se propagan en la brana, simulando ondas gravitacionales.
*   **Software**: Desarrollo de un resolvedor temporal acoplado que actualice las trayectorias de las masas (geodésicas en $g_{\mu\nu}$) y resuelva el campo elástico de forma interactiva.

#### Hito 2: Simulación Galáctica Esférica y Curvas de Rotación (Q4 2026)
*   **Física**: Cargar perfiles de densidad reales de galaxias espirales (como el perfil de Navarro-Frenk-White) y resolver la deflexión de Yukawa resultante en mallas de alta densidad para comprobar cómo el término $e^{-r/R}$ acopla la inercia centrífuga y elimina la necesidad de materia oscura exótica.
*   **Visualización**: Generar mapas interactivos de tensión elástica y perfiles de velocidad rotacional galáctica.

---

## 3. Plan de Publicación Científica de Alto Impacto

### 3.1. Artículos Proyectados en la Secuencia Editorial

#### 📄 Paper 1: "Emergent Local Schwarzschild Gravity from 4D Rotational Dynamics of an Elastic 3-Brane"
*   **Objetivo**: Presentar el marco matemático del universo elástico $S^3$ en rotación isoclínica y la convalidación numérica espectral (>99.8% de ajuste con Schwarzschild).
*   **Revistas Objetivo**: *Physical Review D* (PRD), *Classical and Quantum Gravity* (CQG).
*   **Estado**: Borrador técnico completo; listo para empaquetado en LaTeX en `scientific_publication/`.

#### 📄 Paper 2: "Galactic Rotation Curves and Yukawa Shielding in Centrifugal Elastic Branes"
*   **Objetivo**: Explicar las curvas de rotación galácticas como la firma geométrica elástica de Yukawa del universo curvado, eliminando la materia oscura física.
*   **Revistas Objetivo**: *Journal of Cosmology and Astroparticle Physics* (JCAP), *Astrophysical Journal* (ApJ).

---

## 4. Cronograma de Trabajo y Entregables

| Período | Tareas de Desarrollo y Teoría | Entregable Científico |
|---|---|---|
| **Mes 1 (Julio 2026)** | Refactorizar el solver espectral FFT en la carpeta `scientific_publication/` y unificar el manuscrito LaTeX. | Borrador final del primer paper en formato APS (Physical Review). |
| **Mes 2-3 (Agosto 2026)** | Implementar la simulación binaria de membrana y estudiar la propagación de ondas de curvatura. | Script de simulación de ondas elásticas y reporte técnico. |
| **Mes 4-5 (Octubre 2026)** | Modelado de curvas de rotación galácticas con potencial elástico Yukawa. | Segundo Borrador listo para envío a revisión por pares (Peer Review). |
| **Mes 6 (Diciembre 2026)** | Envío formal de los trabajos a *Physical Review D* y JCAP. | Publicación de pre-prints en el repositorio abierto arXiv. |
