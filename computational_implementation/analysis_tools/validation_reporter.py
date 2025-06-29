#!/usr/bin/env python3
"""
Generador de informes técnicos para validación de regímenes físicos.
Módulo de la Tarea 2.1.2 - Validación de Regímenes Físicos

Este módulo genera el informe técnico completo requerido por la Tarea 2.1.2:
validacion_superposicion.md

Fecha: 29 de junio de 2025
Autor: Universo Centrífugo Research Team
"""

import numpy as np
from datetime import datetime
from pathlib import Path

class ValidationReporter:
    """
    Generador del informe técnico de validación de regímenes físicos.
    
    Produce el documento markdown completo que documenta los resultados
    de la validación del Principio de Superposición Cosmológico.
    """
    
    def __init__(self, output_dir="."):
        """
        Args:
            output_dir: Directorio donde guardar el informe generado
        """
        self.output_dir = Path(output_dir)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_report(self, validation_results, visualization_files):
        """
        Genera el informe técnico completo de validación.
        
        Args:
            validation_results: Resultados completos de la validación
            visualization_files: Archivos de visualización generados
            
        Returns:
            str: Ruta del archivo de informe generado
        """
        print("📋 Generando informe técnico de validación...")
        
        # Construir contenido del informe
        report_content = self._build_report_content(validation_results, visualization_files)
        
        # Escribir archivo
        report_file = self.output_dir / "validacion_superposicion.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Informe técnico generado: {report_file}")
        return str(report_file)
    
    def _build_report_content(self, results, viz_files):
        """Construye el contenido completo del informe."""
        
        # Extraer datos clave
        overall_success = results.get('overall_success', False)
        local_results = results.get('local_regime', {})
        global_results = results.get('global_regime', {})
        transition_results = results.get('transition_zone', {})
        decoupling_results = results.get('decoupling', {})
        params = results.get('parameters', {})
        
        # Construir informe sección por sección
        content = self._generate_header(overall_success)
        content += self._generate_executive_summary(results)
        content += self._generate_simulation_config(params)
        content += self._generate_local_validation_section(local_results, viz_files)
        content += self._generate_global_validation_section(global_results, viz_files)
        content += self._generate_transition_analysis_section(transition_results, viz_files)
        content += self._generate_decoupling_verification_section(decoupling_results)
        content += self._generate_conclusions_section(results)
        content += self._generate_appendices_section(viz_files)
        
        return content
    
    def _generate_header(self, overall_success):
        """Genera el encabezado del informe."""
        status_emoji = "🎉" if overall_success else "⚠️"
        status_text = "VALIDACIÓN EXITOSA" if overall_success else "VALIDACIÓN PARCIAL"
        
        return f"""# Informe de Validación de Regímenes Físicos
## Tarea 2.1.2: Validación del Principio de Superposición Cosmológico

**Fecha:** {self.timestamp}  
**Estado:** {status_emoji} {status_text}  
**Proyecto:** Universo Centrífugo - Plan de Investigación 2025  

---

"""
    
    def _generate_executive_summary(self, results):
        """Genera el resumen ejecutivo."""
        local_success = results['local_regime'].get('success', False)
        global_success = results['global_regime'].get('success', False)
        transition_success = results['transition_zone'].get('success', False)
        decoupling_success = results['decoupling'].get('success', False)
        overall_success = results.get('overall_success', False)
        
        successful_tests = sum([local_success, global_success, transition_success, decoupling_success])
        
        content = """## 1. Resumen Ejecutivo

### Objetivo
Validar que la simulación con el Principio de Superposición Cosmológico reproduce correctamente tanto el régimen cosmológico como el newtoniano simultáneamente, cumpliendo con los criterios establecidos en la Tarea 2.1.2.

### Metodología
Se implementó un análisis post-simulación que evalúa cuantitativamente:
- **Régimen Local**: Recuperación de la solución de Schwarzschild cerca de la masa
- **Régimen Global**: Preservación de la expansión de Hubble en el fondo cosmológico  
- **Zona de Transición**: Transición suave entre ambos regímenes
- **Desacoplamiento**: Ausencia de interferencias no físicas entre escalas

### Resultado Clave
"""
        
        if overall_success:
            content += f"""**🎉 VALIDACIÓN EXITOSA** - El Principio de Superposición Cosmológico es físicamente válido.

- **Tests exitosos**: {successful_tests}/4
- **Conclusión**: La implementación reproduce simultáneamente ambos regímenes sin inconsistencias físicas
- **Criterio de completitud**: ✅ CUMPLIDO - Métricas locales y globales correctas simultáneamente

"""
        else:
            content += f"""**⚠️ VALIDACIÓN PARCIAL** - Se requieren ajustes adicionales.

- **Tests exitosos**: {successful_tests}/4  
- **Conclusión**: La implementación muestra prometedores indicios pero requiere optimización
- **Criterio de completitud**: ⚠️ PARCIAL - Revisar componentes que no pasaron validación

"""
        
        # Añadir tabla de resultados por componente
        content += """### Tabla de Resultados por Componente

| Componente | Estado | Observaciones |
|------------|--------|---------------|
"""
        
        components = [
            ("Régimen Local (Schwarzschild)", local_success, 
             results['local_regime'].get('validation_summary', 'N/A')),
            ("Régimen Global (Cosmológico)", global_success,
             results['global_regime'].get('validation_summary', 'N/A')),
            ("Zona de Transición", transition_success,
             results['transition_zone'].get('validation_summary', 'N/A')),
            ("Desacoplamiento de Regímenes", decoupling_success,
             "Tests de interferencia entre escalas")
        ]
        
        for name, success, summary in components:
            status = "✅ VÁLIDO" if success else "❌ FALLIDO"
            content += f"| {name} | {status} | {summary} |\n"
        
        content += "\n---\n\n"
        
        return content
    
    def _generate_simulation_config(self, params):
        """Genera la sección de configuración de simulación."""
        content = """## 2. Configuración de la Simulación de Prueba

### Parámetros de Masa Local
"""
        
        mass = params.get('mass_local', 'N/A')
        position = params.get('position_local', 'N/A')
        smoothing = params.get('smoothing_radius', 'N/A')
        tol_local = params.get('tolerance_local', 'N/A')
        tol_global = params.get('tolerance_global', 'N/A')
        
        content += f"""- **Masa**: M = {mass} (unidades geométricas)
- **Posición**: {position}
- **Radio de suavizado**: σ = {smoothing:.6f}
- **Perfil de densidad**: Gaussiano suavizado

### Criterios de Validación
- **Tolerancia régimen local**: {tol_local*100:.1f}% (desviación máxima de masa efectiva)
- **Tolerancia régimen global**: {tol_global*100:.1f}% (desviación máxima de isotropía)
- **Criterio de suavidad**: Curvatura máxima < 0.1

### Arquitectura de Superposición
- **Implementación**: T_total = T_cosmológico + T_local
- **Base**: Herencia limpia de EinsteinSimulator
- **Estabilidad**: Métricas automáticas de validación integradas

---

"""
        return content
    
    def _generate_local_validation_section(self, local_results, viz_files):
        """Genera la sección de validación del régimen local."""
        content = """## 3. Validación del Régimen Local (r << R_sistema)

### Objetivo
Demostrar que cerca de la masa central, la métrica recupera aproximadamente la solución de Schwarzschild en el límite de campo débil.

### Metodología
- **Región de análisis**: 3σ < r < 0.1×L_box
- **Ajuste teórico**: g_μν ≈ η_μν + h_μν con h_μν ∝ M/r (aproximación linealizada)
- **Observables**: Componentes de la métrica γ_xx, γ_yy, γ_zz

"""
        
        if local_results.get('success', False):
            content += """### Resultados del Ajuste
"""
            
            # Extraer datos del ajuste
            fits = local_results.get('schwarzschild_fits', {})
            mass_measurements = local_results.get('mass_measurements', {})
            
            if mass_measurements:
                content += "#### Masas Efectivas Medidas\n\n"
                for component, mass_eff in mass_measurements.items():
                    fit_data = fits.get(component, {})
                    if fit_data.get('fit_success', False):
                        error_rms = fit_data['error_rms']
                        mass_dev = fit_data['mass_deviation']
                        status = "✅" if mass_dev < 0.01 else "⚠️"
                        content += f"- **{component}**: M_eff = {mass_eff:.4f}, "
                        content += f"RMS = {error_rms:.6f}, "
                        content += f"Desviación = {mass_dev*100:.2f}% {status}\n"
                
                content += "\n"
            
            summary = local_results.get('validation_summary', '')
            content += f"""### Evaluación
{summary}

#### Interpretación Física
La recuperación exitosa de la masa efectiva en múltiples componentes de la métrica confirma que:
1. **Principio de Equivalencia**: La superposición preserva la geometría local esperada
2. **Campo Débil**: La aproximación linealizada es válida en la región analizada  
3. **Consistencia**: No hay artefactos numéricos significativos en la zona de masa

"""
        else:
            error_msg = local_results.get('error', 'Error no especificado')
            content += f"""### ❌ Validación Fallida
**Error**: {error_msg}

#### Posibles Causas
- Resolución espacial insuficiente para la escala de masa
- Radio de suavizado inapropiado
- Interferencia de efectos de frontera
- Inestabilidades numéricas en la región central

"""
        
        # Añadir referencia a visualización
        if 'local' in viz_files:
            content += f"""### Visualización
Ver análisis gráfico detallado en: `{viz_files['local']}`

"""
        
        content += "---\n\n"
        return content
    
    def _generate_global_validation_section(self, global_results, viz_files):
        """Genera la sección de validación del régimen global."""
        content = """## 4. Validación del Régimen Cosmológico (r >> R_masa)

### Objetivo
Confirmar que la métrica en regiones lejanas preserva las propiedades cosmológicas esperadas (isotropía, expansión de Hubble) sin perturbaciones significativas por la masa local.

### Metodología
- **Región de análisis**: r > 0.5×L_box
- **Tests aplicados**: 
  - Isotropía: |γ_ii - γ_jj| << tolerancia
  - Ausencia de términos cruzados: |γ_ij| ≈ 0 (i≠j)
  - Evolución temporal: Análisis del factor de escala det(γ)

"""
        
        if global_results.get('success', False):
            content += """### Resultados de Isotropía
"""
            
            isotropy_data = global_results.get('isotropy', {})
            if isotropy_data:
                max_aniso = isotropy_data.get('max_anisotropy', 0)
                is_isotropic = isotropy_data.get('is_isotropic', False)
                
                content += f"""- **Anisotropía máxima**: {max_aniso:.6f}
- **Estado**: {'✅ Isotrópico' if is_isotropic else '❌ Anisótropo'}
- **Criterio**: Desviación < {global_results.get('tolerance', 0.05)*100}%

"""
            
            content += """### Resultados de Perturbaciones
"""
            
            perturbation_data = global_results.get('perturbations', {})
            if perturbation_data:
                max_pert = perturbation_data.get('max_perturbation', 0)
                is_unperturbed = perturbation_data.get('is_unperturbed', False)
                
                content += f"""- **Perturbación máxima**: {max_pert:.6f}
- **Estado**: {'✅ No perturbado' if is_unperturbed else '❌ Perturbado'}
- **Interpretación**: La masa local no contamina significativamente el régimen cosmológico

"""
            
            # Evolución temporal si está disponible
            temporal_data = global_results.get('temporal_evolution', {})
            if temporal_data.get('available', False):
                expansion_rate = temporal_data.get('expansion_rate', 0)
                expansion_detected = temporal_data.get('expansion_detected', False)
                
                content += f"""### Evolución Temporal
- **Tasa de expansión**: H ≈ {expansion_rate:.6f}
- **Expansión detectada**: {'✅ Sí' if expansion_detected else '⚠️ No'}
- **Interpretación**: {'Expansión cosmológica preservada' if expansion_detected else 'Sin evidencia clara de expansión (limitación temporal)'}

"""
            
            summary = global_results.get('validation_summary', '')
            content += f"""### Evaluación
{summary}

#### Interpretación Física
La preservación de isotropía y la ausencia de perturbaciones confirman que:
1. **Separación de escalas**: La masa local no interfiere con la dinámica cosmológica global
2. **Linealidad**: La superposición no introduce acoplamientos no físicos
3. **Principio cosmológico**: Se mantiene la homogeneidad e isotropía a gran escala

"""
        else:
            error_msg = global_results.get('error', 'Error no especificado')
            content += f"""### ❌ Validación Fallida
**Error**: {error_msg}

#### Posibles Causas
- Dominio computacional demasiado pequeño
- Efectos de frontera dominantes en región "global"
- Contaminación por la masa local (escalas mal separadas)

"""
        
        # Añadir referencia a visualización
        if 'global' in viz_files:
            content += f"""### Visualización
Ver análisis gráfico detallado en: `{viz_files['global']}`

"""
        
        content += "---\n\n"
        return content
    
    def _generate_transition_analysis_section(self, transition_results, viz_files):
        """Genera la sección de análisis de la zona de transición."""
        content = """## 5. Análisis de la Zona de Transición

### Objetivo
Caracterizar la suavidad de la transición entre los regímenes local y global, verificando la ausencia de discontinuidades o saltos abruptos en la métrica.

### Metodología
- **Región de análisis**: 0.1×L_box ≤ r ≤ 0.5×L_box
- **Análisis**: Derivadas numéricas del perfil radial γ_xx(r)
- **Criterio de suavidad**: Segunda derivada máxima < 0.1

"""
        
        if transition_results.get('success', False):
            smoothness_data = transition_results.get('smoothness', {})
            if smoothness_data:
                is_smooth = smoothness_data.get('is_smooth', False)
                max_curvature = smoothness_data.get('max_curvature', 0)
                mean_curvature = smoothness_data.get('mean_curvature', 0)
                
                content += f"""### Resultados del Análisis de Suavidad
- **Curvatura máxima**: {max_curvature:.6f}
- **Curvatura promedio**: {mean_curvature:.6f}
- **Estado**: {'✅ Transición suave' if is_smooth else '⚠️ Posibles discontinuidades'}

### Interpretación
"""
                
                if is_smooth:
                    content += """La transición suave confirma que:
1. **Continuidad física**: No hay saltos artificiales en la métrica
2. **Estabilidad numérica**: El esquema de superposición es robusto
3. **Validez del modelo**: La interpolación entre regímenes es físicamente realista

"""
                else:
                    content += """La detección de rugosidad sugiere:
1. **Limitación de resolución**: Puede requerirse mayor refinamiento de malla
2. **Efectos de discretización**: Artefactos numéricos en la zona de transición
3. **Revisión de parámetros**: El radio de suavizado podría necesitar ajuste

"""
            
            summary = transition_results.get('validation_summary', '')
            content += f"""### Evaluación
{summary}

"""
        else:
            error_msg = transition_results.get('error', 'Error no especificado')
            content += f"""### ❌ Análisis Fallido
**Error**: {error_msg}

#### Posibles Causas
- Datos insuficientes en la zona de transición
- Resolución radial inadecuada
- Problemas en el cálculo de perfiles

"""
        
        # Añadir referencia a visualización
        if 'transition' in viz_files:
            content += f"""### Visualización
Ver análisis gráfico detallado en: `{viz_files['transition']}`

"""
        
        content += "---\n\n"
        return content
    
    def _generate_decoupling_verification_section(self, decoupling_results):
        """Genera la sección de verificación de desacoplamiento."""
        content = """## 6. Verificación de Desacoplamiento

### Objetivo
Verificar que los regímenes local y global coexisten sin interferencias no físicas, confirmando la validez del Principio de Superposición lineal.

### Tests Aplicados
1. **Consistencia de masa local**: Las diferentes medidas de masa efectiva deben ser coherentes
2. **Independencia del régimen global**: La métrica global no debe estar fuertemente afectada por la masa local
3. **Separación de escalas**: Verificar que las escalas espaciales están suficientemente separadas

"""
        
        if decoupling_results.get('success', False):
            content += """### ✅ Resultados Positivos
Los tests de desacoplamiento fueron exitosos:

"""
            
            # Añadir detalles específicos si están disponibles
            if 'mass_consistency' in decoupling_results:
                mass_consistency = decoupling_results['mass_consistency']
                content += f"- **Consistencia de masa**: {mass_consistency*100:.2f}% de variación entre medidas\n"
            
            if 'scale_separation' in decoupling_results:
                scale_sep = decoupling_results['scale_separation']
                content += f"- **Separación de escalas**: {scale_sep:.1f}x entre escalas local y global\n"
            
            content += """
#### Interpretación Física
El éxito de los tests de desacoplamiento confirma que:
1. **Linealidad válida**: La superposición T_total = T_local + T_cosmológico es físicamente consistente
2. **No hay efectos espúreos**: Los regímenes no se interfieren de manera no física
3. **Escalas separadas**: La aproximación de regímenes independientes es válida

"""
        else:
            issues = decoupling_results.get('issues', [])
            content += f"""### ⚠️ Problemas Detectados
Se identificaron {len(issues)} problemas de desacoplamiento:

"""
            
            issue_descriptions = {
                'mass_inconsistency': 'Inconsistencia entre medidas de masa efectiva',
                'global_contamination': 'Régimen global afectado por masa local',
                'poor_scale_separation': 'Escalas insuficientemente separadas'
            }
            
            for issue in issues:
                description = issue_descriptions.get(issue, issue)
                content += f"- ❌ **{description}**\n"
            
            content += """
#### Recomendaciones
Para mejorar el desacoplamiento:
1. **Aumentar dominio computacional**: Mejor separación de escalas
2. **Optimizar radio de suavizado**: Reducir interferencias numéricas
3. **Revisar implementación**: Verificar la fidelidad de la superposición

"""
        
        content += "---\n\n"
        return content
    
    def _generate_conclusions_section(self, results):
        """Genera la sección de conclusiones."""
        overall_success = results.get('overall_success', False)
        
        content = """## 7. Conclusiones

### Evaluación de Criterios de Éxito
"""
        
        # Criterios específicos
        local_success = results['local_regime'].get('success', False)
        global_success = results['global_regime'].get('success', False)
        transition_success = results['transition_zone'].get('success', False)
        decoupling_success = results['decoupling'].get('success', False)
        
        criteria = [
            ("Cerca de la masa (r << R_sistema): Métrica ≈ Schwarzschild + correcciones menores", local_success),
            ("Lejos de la masa (r >> R_masa): Métrica ≈ expansión cosmológica pura", global_success),
            ("Zona de transición: Transición suave sin discontinuidades", transition_success),
            ("Ambos simultáneos: No hay conflicto entre regímenes en la misma simulación", decoupling_success)
        ]
        
        for criterion, success in criteria:
            status = "✅ CUMPLIDO" if success else "❌ NO CUMPLIDO"
            content += f"- {criterion}: **{status}**\n"
        
        successful_criteria = sum([success for _, success in criteria])
        
        content += f"""
**Criterios cumplidos**: {successful_criteria}/4

"""
        
        if overall_success:
            content += """### 🎉 Interpretación Física: El Principio de Superposición Cosmológico es Físicamente Viable

Los resultados demuestran que la implementación del Principio de Superposición Cosmológico:

1. **✅ Reproduce correctamente el régimen newtoniano** cerca de masas puntuales
2. **✅ Preserva la expansión cosmológica** en regiones lejanas  
3. **✅ Mantiene continuidad física** en la zona de transición
4. **✅ Opera sin interferencias no físicas** entre escalas

#### Implicaciones Científicas
- **Validación del modelo teórico**: El Universo Centrífugo puede explicar simultáneamente gravedad local y expansión global
- **Robustez numérica**: La implementación computacional es estable y confiable
- **Preparación para siguiente fase**: Base sólida para la Tarea 2.1.3 (Efectos de Acoplamiento)

### Limitaciones y Próximos Pasos
"""
        else:
            content += """### ⚠️ Interpretación: Validación Parcial - Se Requieren Ajustes

Los resultados muestran un avance significativo pero indican áreas de mejora:

#### Logros Alcanzados
"""
            
            if local_success:
                content += "- ✅ Régimen local correctamente implementado\n"
            if global_success:
                content += "- ✅ Régimen cosmológico preservado\n"
            if transition_success:
                content += "- ✅ Transición suave validada\n"
            if decoupling_success:
                content += "- ✅ Desacoplamiento verificado\n"
            
            content += """
#### Áreas de Mejora
"""
            
            if not local_success:
                content += "- ❌ Régimen local requiere optimización\n"
            if not global_success:
                content += "- ❌ Régimen cosmológico necesita refinamiento\n"
            if not transition_success:
                content += "- ❌ Zona de transición requiere análisis adicional\n"
            if not decoupling_success:
                content += "- ❌ Desacoplamiento necesita mejora\n"
            
            content += """
### Recomendaciones para Mejora
1. **Incrementar resolución espacial**: Malla más fina para mejor precisión
2. **Optimizar parámetros**: Ajustar masa y radio de suavizado
3. **Extender dominio temporal**: Simulaciones más largas para efectos dinámicos
4. **Refinar criterios**: Tolerancias más apropiadas para el sistema específico

### Próximos Pasos
"""
        
        content += """
#### Tarea 2.1.3: Efectos de Acoplamiento
- Implementar análisis de desviaciones del modelo lineal
- Estudiar superposición no-lineal opcional
- Buscar efectos de acoplamiento entre escalas

#### Optimizaciones Técnicas
- Paralelización avanzada para simulaciones de mayor resolución
- Implementación de esquemas adaptativos de refinamiento
- Desarrollo de criterios de convergencia más sofisticados

---

"""
        return content
    
    def _generate_appendices_section(self, viz_files):
        """Genera la sección de apéndices."""
        content = """## Apéndices

### A. Archivos de Visualización Generados
"""
        
        if viz_files:
            for viz_type, file_path in viz_files.items():
                content += f"- **{viz_type.capitalize()}**: `{file_path}`\n"
        else:
            content += "- Sin archivos de visualización generados\n"
        
        content += """
### B. Metodología de Análisis

#### Definición de Regiones
- **Región Local**: 3σ < r < 0.1×L_box (donde σ es el radio de suavizado)
- **Zona de Transición**: 0.1×L_box ≤ r ≤ 0.5×L_box  
- **Región Global**: r > 0.5×L_box

#### Métodos Numéricos
- **Perfiles radiales**: Promediado en bins logarítmicos
- **Ajustes teóricos**: Algoritmo de Levenberg-Marquardt
- **Análisis de suavidad**: Diferencias finitas de segundo orden

#### Criterios de Validación
- **Régimen local**: Desviación de masa efectiva < tolerancia_local
- **Régimen global**: Anisotropía máxima < tolerancia_global  
- **Transición**: Curvatura máxima < 0.1
- **Desacoplamiento**: Tests de consistencia y separación de escalas

### C. Referencias Técnicas
- **Formulación BSSN**: Baumgarte & Shapiro (1999)
- **Simulaciones Einstein**: Alcubierre (2008) 
- **Aproximación Post-Newtoniana**: Will (2014)
- **Cosmología Numérica**: Bentivegna & Bruni (2016)

---

**Fin del Informe**  
*Generado automáticamente por el sistema de validación de regímenes físicos*  
*Tarea 2.1.2 - Plan de Investigación Universo Centrífugo 2025*
"""
        
        return content