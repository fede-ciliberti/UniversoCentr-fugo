# DOCS

**Dominio**: Documentación científica, formulación teórica, planes de simulación e informes de resultados del proyecto Universo Centrífugo.

## OVERVIEW

Documentación completa del proyecto: marco teórico fundamental, formulación matemática de rotación isoclínica en 4D, metodologías de verificación de gravedad emergente, informes de simulación numérica FFT de membrana elástica, análisis de precesión orbital, materia oscura elástica, estabilidad de $G_{eff}$, cosmología comparada y trazado de rayos por Coriolis 4D.

## STRUCTURE

```
docs/
├── AGENTS.md                                    # Este archivo (guía de navegación)
│
├── ── DOCUMENTACIÓN BASE (Lectura secuencial) ──
├── 01_marco_teorico.md                          # Marco teórico general: brana S³ en ℝ⁴, Friedmann modificadas
├── 02_propuesta_investigacion.md                # Propuesta formal, hipótesis y criterios de falsabilidad
├── 03_metodologia_gravedad_emergente.md         # Derivación de gravedad newtoniana desde elasticidad de brana
├── 04_metodologia_verificacion_gravedad.md      # Plan de verificación numérica del potencial gravitatorio
├── 05_informe_simulacion_numerica.md            # Primer informe del solver FFT espectral de membrana
│
├── ── FASE 2-3: SIMULACIÓN DE GRAVEDAD LOCAL ──
├── 06_plan_simulacion_gravedad_local.md         # Plan detallado de simulación estática local
├── 07_fase2_ejecucion_simulacion_completada.md  # Informe de ejecución: solver FFT validado hasta 256³
├── 08_fase3_analisis_resultados_completada.md   # Análisis de perfiles radiales vs Schwarzschild
├── 09_informe_ejecutivo_gravedad_local.md       # Resumen ejecutivo de resultados de gravedad local
│
├── ── FASE 4: ALTA RESOLUCIÓN Y SISTEMAS DINÁMICOS ──
├── 10_roadmap_alta_resolucion.md                # Roadmap hacia simulaciones 512³ y 1024³
├── 11_plan_estrategico_256cubed_completo.md     # Plan estratégico completo para cubo 256³
├── 12_validacion_plan_256cubed_completado.md    # Validación completada del plan 256³
├── 13_diseno_motor_fft_phase_shift.md           # Diseño de motor FFT para propagación de ondas dinámicas
├── 14_analisis_curvas_rotacion_sparc.md         # Curvas galácticas SPARC reales y aceleración inercial
├── 15_escalabilidad_alta_resolucion_512.md      # Análisis de paralelización y escalado 512³ y 1024³
├── 16_simulacion_ondas_gravitacionales_binarias.md # Simulación de binarias y firma de ondas de brana con LISA
│
├── ── FASE 5: VALIDACIÓN OBSERVACIONAL (CMB) ──
├── 17_analisis_eje_del_mal_cmb.md               # Alineación del cuadrupolo y octupolo en la rotación 4D
├── 18_algoritmo_correccion_coriolis_cmb.md      # De-biasing en bucle cerrado de Coriolis en CMB
├── 19_analisis_cmb_crudo_curado.md              # De-biasing pixel a pixel y simetría hemisférica sintética
├── 20_analisis_planck_real_crudo.md             # Validación empírica con datos reales del satélite Planck (ESA)
├── 21_formalismo_aberracion_coordenadas_cmb.md  # Formalismo teórico de aberración y Rodrigues en 4D
├── 22_analisis_planck_real_aberracion.md         # Validación final por pixel-shifting en Planck real
│
├── ── REFORMULACIONES TEÓRICAS MAYORES (CÚSPIDE MATEMÁTICA V2/V3) ──
├── formalismo_geometrico_4d_v2.md               # Reformulación de la geometría de rotación isoclínica v2
├── metrica_unificada_v3.md                       # Métrica unificada v3 y formalismo tensorial avanzado (el más completo)
│
├── ── FORMULACIÓN MATEMÁTICA ESPECIALIZADA ──
├── formulacion_matematica_rotacion_4d.md        # Formalismo SO(4), rotación isoclínica, tensor energía-momento
├── ecuaciones_movimiento_rotacion_4d.md         # Ecuaciones de movimiento 3D: acoplamiento cinético α, Coriolis β
├── conservacion_momento_inercia_geff.md         # Estabilidad de G_eff por conservación de momento angular en Bulk
├── comparacion_curvas_expansion.md              # Ecuación de Friedmann emergente vs ΛCDM y firma de anisotropía de H₀
├── fuerza_coriolis_4d_trayectorias.md           # Trazado de rayos, lensing y desvío de luz por Coriolis 4D
│
├── ── INFORMES TEMÁTICOS Y COMPLEMENTARIOS ──
├── informe_precesion_perihelio.md               # Simulación de precesión orbital (Mercurio) con parámetros magnificados
├── informe_materia_oscura_elastica.md           # Curvas de rotación galáctica planas sin materia oscura
├── plan_simulacion_elastica.md                  # Plan maestro de simulación elástica de membrana y factor L_c
├── INFORME_FRAME_DRAGGING_UC.md                 # Análisis del efecto Lense-Thirring / frame-dragging hiperdimensional
├── INFORME_RECONSTRUCCION_4D.md                 # Métodos para la reconstrucción del espacio 4D desde observables 3D
├── revision_literatura_universos_rotantes.md    # Revisión histórica de modelos cosmológicos rotantes clásicos (Gödel, etc.)
│
├── ── DOCUMENTACIÓN DE APOYO (ex-huérfanos integrados, junio 2026) ──
├── formalismo_dbi_energia_oscura.md             # Extensión DBI para energía oscura (w=-1 dinámico)
├── acoplamiento_masa_inercia_centrifuga.md      # Retroalimentación masa-vacío en momento angular
├── calculo_radio_tamano_universo.md             # Cálculo observacional de R₀ y volumen S³
├── informe_resolucion_auditoria.md              # Cierre oficial y resolución detallada de los 18 hallazgos adversariales
│
└── ── SUBDIRECTORIO DE SIMULACIÓN ──
    └── simulacion_256cubed/
        └── README_256cubed.md                   # Transición BSSN → FFT (único archivo real)
```

## WHERE TO LOOK

| Tema | Archivo | Tipo |
|------|---------|------|
| **Marco teórico base** | `01_marco_teorico.md` | Fundamentos |
| **Propuesta e hipótesis** | `02_propuesta_investigacion.md` | Proposal |
| **Gravedad emergente** | `03_metodologia_gravedad_emergente.md` | Metodología |
| **Verificación numérica** | `04_metodologia_verificacion_gravedad.md` | Metodología |
| **Primer informe FFT** | `05_informe_simulacion_numerica.md` | Informe |
| **Plan gravedad local** | `06_plan_simulacion_gravedad_local.md` | Plan |
| **Ejecución Fase 2** | `07_fase2_ejecucion_simulacion_completada.md` | Informe |
| **Análisis Fase 3** | `08_fase3_analisis_resultados_completada.md` | Informe |
| **Resumen ejecutivo** | `09_informe_ejecutivo_gravedad_local.md` | Executive summary |
| **Roadmap alta resolución** | `10_roadmap_alta_resolucion.md` | Planificación |
| **Plan estratégico 256³** | `11_plan_estrategico_256cubed_completo.md` | Planificación |
| **Validación 256³** | `12_validacion_plan_256cubed_completado.md` | Validación |
| **Motor FFT Desfase** | `13_diseno_motor_fft_phase_shift.md` | Diseño de software |
| **Curvas SPARC Reales** | `14_analisis_curvas_rotacion_sparc.md` | Verificación Astrofísica |
| **Escalado de Memoria** | `15_escalabilidad_alta_resolucion_512.md` | Análisis Técnico |
| **Ondas Binarias y LISA** | `16_simulacion_ondas_gravitacionales_binarias.md` | Óptica Gravitacional / LISA |
| **Alineación Eje del Mal** | `17_analisis_eje_del_mal_cmb.md` | Informe CMB |
| **Algoritmo de-biasing** | `18_algoritmo_correccion_coriolis_cmb.md` | Algoritmo |
| **Curación CMB Sintético** | `19_analisis_cmb_crudo_curado.md` | Validación CMB |
| **Validación Planck Real** | `20_analisis_planck_real_crudo.md` | Validación Real |
| **Teoría de Rodrigues** | `21_formalismo_aberracion_coordenadas_cmb.md` | Formalismo CMB |
| **Pixel-Shift Real** | `22_analisis_planck_real_aberracion.md` | Validation Real |
| **Geometría Isoclínica v2** | `formalismo_geometrico_4d_v2.md` | Geometría Superior |
| **Métrica Unificada v3** | `metrica_unificada_v3.md` | Tensor Einstein Completo |
| **Formalismo SO(4)** | `formulacion_matematica_rotacion_4d.md` | Matemática |
| **Ecuaciones movimiento** | `ecuaciones_movimiento_rotacion_4d.md` | Dinámica |
| **Estabilidad de G_eff** | `conservacion_momento_inercia_geff.md` | Conservación |
| **Cosmología comparada** | `comparacion_curvas_expansion.md` | Cosmología |
| **Lensing / desvío luz** | `fuerza_coriolis_4d_trayectorias.md` | Óptica gravitacional |
| **Precesión perihelio** | `informe_precesion_perihelio.md` | Test solar |
| **Materia oscura elástica** | `informe_materia_oscura_elastica.md` | Astrofísica galáctica |
| **Plan simulación maestra** | `plan_simulacion_elastica.md` | Plan maestro |
| **Efecto Frame-Dragging** | `INFORME_FRAME_DRAGGING_UC.md` | Relatividad General UC |
| **Reconstrucción 4D** | `INFORME_RECONSTRUCCION_4D.md` | Cosmografía |
| **Universos Rotantes** | `revision_literatura_universos_rotantes.md` | Revisión histórica |
| **Energía oscura DBI** | `formalismo_dbi_energia_oscura.md` | Extensión teórica |
| **Acoplamiento masa-vacío** | `acoplamiento_masa_inercia_centrifuga.md` | Extensión teórica |
| **Radio del universo** | `calculo_radio_tamano_universo.md` | Cálculo observacional |
| **Cierre de Auditoría** | `informe_resolucion_auditoria.md` | Registro de Calidad |
| **Simulación 256³** | `simulacion_256cubed/` | Subdirectorio técnico |

## CONVENTIONS

- **Numeración secuencial**: Archivos `01_` a `12_` siguen orden lógico y cronológico de lectura.
- **Documentos temáticos sin numeración**: Los archivos especializados (formulación, informes) se identifican por nombre descriptivo.
- **Markdown puro**: Todos los documentos están en formato Markdown con ecuaciones LaTeX ($...$ y $$...$$).
- **Documentación viva**: Estos archivos evolucionan con la investigación y las auditorías adversariales.
- **Última actualización estructural**: Junio 2026 (reorganización integral + integración de docs de apoyo).

## NOTA HISTÓRICA (Junio 2026)

El archivo `informe_resolucion_auditoria.md` fue movido a `archive/audits/` durante la reorganización integral de junio 2026. Era un documento meta (respuesta a auditoría adversarial de 4ta vuelta) que no alimentaba la investigación activa. Se conserva como registro histórico del proceso de validación científica.

Los documentos `formalismo_dbi_energia_oscura.md`, `acoplamiento_masa_inercia_centrifuga.md` y `calculo_radio_tamano_universo.md` eran previamente "huérfanos" (sin referencias cruzadas). En junio 2026 se integraron como **documentación de apoyo** con links bidireccionales desde/hacia los docs principales.

## ANTI-PATTERNS

- **No confundir con `scientific_publication/`**: `docs/` contiene material auxiliar y de trabajo, no el manuscrito formal para publicación.
- **No confundir con `notebooks/`**: El código de simulación vive en `notebooks/`, no en `docs/`.
- **Parámetros magnificados**: Los informes de simulación (precesión, materia oscura) usan parámetros amplificados didácticamente; siempre buscar la sección de calibración física real antes de interpretar resultados como datos astronómicos.
