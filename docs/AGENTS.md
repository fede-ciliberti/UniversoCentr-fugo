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
├── ── FASE 4: ALTA RESOLUCIÓN Y COSMOLOGÍA ──
├── 10_roadmap_alta_resolucion.md                # Roadmap hacia simulaciones 512³ y 1024³
├── 11_plan_estrategico_256cubed_completo.md     # Plan estratégico completo para cubo 256³
├── 12_validacion_plan_256cubed_completado.md    # Validación completada del plan 256³
│
├── ── FORMULACIÓN MATEMÁTICA ESPECIALIZADA ──
├── formulacion_matematica_rotacion_4d.md        # Formalismo SO(4), rotación isoclínica, tensor energía-momento
├── ecuaciones_movimiento_rotacion_4d.md         # Ecuaciones de movimiento 3D: acoplamiento cinético α, Coriolis β
├── conservacion_momento_inercia_geff.md         # Estabilidad de G_eff por conservación de momento angular en Bulk
├── comparacion_curvas_expansion.md              # Ecuación de Friedmann emergente vs ΛCDM
├── fuerza_coriolis_4d_trayectorias.md           # Trazado de rayos, lensing y desvío de luz por Coriolis 4D
│
├── ── INFORMES TEMÁTICOS ──
├── informe_precesion_perihelio.md               # Simulación de precesión orbital (Mercurio) con parámetros magnificados
├── informe_materia_oscura_elastica.md           # Curvas de rotación galáctica planas sin materia oscura
├── plan_simulacion_elastica.md                  # Plan maestro de simulación elástica de membrana
│
└── ── SUBDIRECTORIO DE SIMULACIÓN ──
    └── simulacion_256cubed/                     # Especificaciones y troubleshooting de simulación 256³
        ├── README_256cubed.md                   #README del subdirectorio 256³
        ├── SPECS_256cubed.md                    # Especificaciones técnicas hardware/software
        ├── TROUBLESHOOTING_256cubed.md          # Resolución de problemas comunes
        └── TROUBLESHOOTING_PARALLELIZATION.md   # Problemas específicos de paralelización
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
| **Formalismo SO(4)** | `formulacion_matematica_rotacion_4d.md` | Matemática |
| **Ecuaciones movimiento** | `ecuaciones_movimiento_rotacion_4d.md` | Dinámica |
| **Estabilidad de G_eff** | `conservacion_momento_inercia_geff.md` | Conservación |
| **Cosmología comparada** | `comparacion_curvas_expansion.md` | Cosmología |
| **Lensing / desvío luz** | `fuerza_coriolis_4d_trayectorias.md` | Óptica gravitacional |
| **Precesión perihelio** | `informe_precesion_perihelio.md` | Test solar |
| **Materia oscura elástica** | `informe_materia_oscura_elastica.md` | Astrofísica galáctica |
| **Plan simulación maestra** | `plan_simulacion_elastica.md` | Plan maestro |
| **Simulación 256³** | `simulacion_256cubed/` | Subdirectorio técnico |

## CONVENTIONS

- **Numeración secuencial**: Archivos `01_` a `12_` siguen orden lógico y cronológico de lectura.
- **Documentos temáticos sin numeración**: Los archivos especializados (formulación, informes) se identifican por nombre descriptivo.
- **Markdown puro**: Todos los documentos están en formato Markdown con ecuaciones LaTeX ($...$ y $$...$$).
- **Documentación viva**: Estos archivos evolucionan con la investigación y las auditorías adversariales.
- **Última actualización estructural**: Junio 2026 (post-auditoría adversarial integral).

## ANTI-PATTERNS

- **No confundir con `scientific_publication/`**: `docs/` contiene material auxiliar y de trabajo, no el manuscrito formal para publicación.
- **No confundir con `notebooks/`**: El código de simulación vive en `notebooks/`, no en `docs/`.
- **Parámetros magnificados**: Los informes de simulación (precesión, materia oscura) usan parámetros amplificados didácticamente; siempre buscar la sección de calibración física real antes de interpretar resultados como datos astronómicos.
