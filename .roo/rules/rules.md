---
description: "Reglas para mantener el README.md como el foco central del proyecto."
globs: ["README.md"]
alwaysApply: true
---

# Protocolo: README.md como Foco del Proyecto ("Ojo de Sauron")

## 1. Principio Rector
El `README.md` debe ser un reflejo fiel y actualizado del estado, prioridades y resultados más recientes del proyecto. Actúa como el punto de entrada principal y debe orientar a cualquier observador sobre en qué se está trabajando activamente.

## 2. Disparadores para la Actualización (Triggers)
Cualquier modo de IA (`code`, `debug`, `architect`) debe considerar una actualización del `README.md` como parte de su tarea si la acción a realizar implica:

- **Cambios en la Estructura del Proyecto:** Creación, eliminación o consolidación significativa de archivos o directorios.
- **Finalización de un Hito Clave:** Cuando un resultado importante es alcanzado (ej. una validación experimental, una simulación completada).
- **Modificación de la Metodología:** Si el enfoque para resolver un problema cambia.
- **Nuevos Resultados o Conclusiones:** Al generar nuevos datos o insights que impactan el estado del proyecto.

## 3. Proceso de Actualización
- **Responsabilidad:** El modo que ejecuta la tarea es responsable de identificar la necesidad de actualizar el `README.md`.
- **Integración en el DoD:** La actualización del `README.md` debe ser añadida como un ítem en el "Definition of Done" de la tarea delegada.
- **Contenido a Actualizar:** Las secciones más susceptibles de cambio son:
    - "Resultados Principales"
    - "Estado Actual del Proyecto" (Logros, En Desarrollo, Próximos Hitos)
    - "Uso Rápido" (comandos para ejecutar nuevos scripts)
    - "Última actualización"
