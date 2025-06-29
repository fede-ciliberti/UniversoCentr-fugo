#!/usr/bin/env python3
"""
Generador de visualizaciones para validación de regímenes físicos.
Módulo de la Tarea 2.1.2 - Validación de Regímenes Físicos

Este módulo crea todas las visualizaciones necesarias para el informe
de validación del Principio de Superposición Cosmológico.

Fecha: 29 de junio de 2025
Autor: Universo Centrífugo Research Team
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path

class ValidationVisualizer:
    """
    Generador de visualizaciones para la validación de regímenes físicos.
    
    Crea gráficas comprehensivas que documentan la validación del
    Principio de Superposición Cosmológico.
    """
    
    def __init__(self, output_dir="validation_figures"):
        """
        Args:
            output_dir: Directorio donde guardar las figuras generadas
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Configurar estilo de matplotlib
        plt.style.use('default')
        plt.rcParams.update({
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.labelsize': 10,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'legend.fontsize': 9,
            'figure.titlesize': 14
        })
    
    def create_all_visualizations(self, validation_results, common_data):
        """
        Crea todas las visualizaciones necesarias para la validación.
        
        Args:
            validation_results: Resultados completos de la validación
            common_data: Datos comunes de la simulación
            
        Returns:
            dict: Rutas de archivos de visualización generados
        """
        print("📊 Generando visualizaciones de validación...")
        
        visualization_files = {}
        
        # 1. Vista general del perfil radial
        fig_overview = self.create_radial_overview(validation_results, common_data)
        overview_file = self.output_dir / "radial_overview.png"
        fig_overview.savefig(overview_file, dpi=300, bbox_inches='tight')
        visualization_files['overview'] = str(overview_file)
        plt.close(fig_overview)
        
        # 2. Validación del régimen local
        if validation_results['local_regime'].get('success', False):
            fig_local = self.create_local_validation_plots(validation_results['local_regime'])
            local_file = self.output_dir / "local_regime_validation.png"
            fig_local.savefig(local_file, dpi=300, bbox_inches='tight')
            visualization_files['local'] = str(local_file)
            plt.close(fig_local)
        
        # 3. Validación del régimen global
        if validation_results['global_regime'].get('success', False):
            fig_global = self.create_global_validation_plots(validation_results['global_regime'])
            global_file = self.output_dir / "global_regime_validation.png"
            fig_global.savefig(global_file, dpi=300, bbox_inches='tight')
            visualization_files['global'] = str(global_file)
            plt.close(fig_global)
        
        # 4. Análisis de transición
        if validation_results['transition_zone'].get('success', False):
            fig_transition = self.create_transition_analysis_plots(validation_results['transition_zone'])
            transition_file = self.output_dir / "transition_analysis.png"
            fig_transition.savefig(transition_file, dpi=300, bbox_inches='tight')
            visualization_files['transition'] = str(transition_file)
            plt.close(fig_transition)
        
        # 5. Resumen ejecutivo
        fig_summary = self.create_executive_summary(validation_results)
        summary_file = self.output_dir / "validation_summary.png"
        fig_summary.savefig(summary_file, dpi=300, bbox_inches='tight')
        visualization_files['summary'] = str(summary_file)
        plt.close(fig_summary)
        
        print(f"✅ Visualizaciones guardadas en: {self.output_dir}")
        
        return visualization_files
    
    def create_radial_overview(self, validation_results, common_data):
        """Crea vista general del perfil radial con regiones marcadas."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Obtener datos del perfil radial de transición
        transition_results = validation_results.get('transition_zone', {})
        
        if transition_results.get('success', False):
            radial_data = transition_results['radial_profile']
            r_centers = radial_data['r_centers']
            gamma_profile = radial_data['gamma_profile']
            
            # Plotear perfil principal
            ax.semilogx(r_centers, gamma_profile, 'b-', linewidth=2, 
                       label='γ_xx simulado', alpha=0.8)
            
            # Línea de referencia (métrica plana)
            ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.5, 
                      label='Métrica plana (γ = 1)')
            
            # Marcar regiones de análisis
            regions_info = common_data['regions_info']
            sigma = regions_info['sigma']
            r_local_max = regions_info['r_local_max']
            r_global_min = regions_info['r_global_min']
            
            ax.axvspan(3*sigma, r_local_max, alpha=0.2, color='red', 
                      label='Región Local (Schwarzschild)')
            ax.axvspan(r_local_max, r_global_min, alpha=0.2, color='orange',
                      label='Zona de Transición')
            ax.axvspan(r_global_min, np.max(r_centers), alpha=0.2, color='blue',
                      label='Región Global (Cosmológica)')
            
            # Añadir predicción teórica de Schwarzschild en región local
            if validation_results['local_regime'].get('success', False):
                local_data = validation_results['local_regime']
                if 'schwarzschild_fits' in local_data:
                    fits = local_data['schwarzschild_fits']
                    if 'g_xx' in fits and fits['g_xx'].get('fit_success', False):
                        M_eff = fits['g_xx']['M_eff']
                        r_theory = np.linspace(3*sigma, r_local_max, 50)
                        gamma_theory = 1.0 + 2*M_eff/r_theory
                        ax.semilogx(r_theory, gamma_theory, 'r--', linewidth=2,
                                   alpha=0.7, label=f'Schwarzschild teórico (M={M_eff:.3f})')
            
            ax.set_xlabel('Radio')
            ax.set_ylabel('γ_xx')
            ax.set_title('Perfil Radial Completo: Validación de Regímenes Físicos\n' +
                        'Tarea 2.1.2 - Principio de Superposición Cosmológico')
            ax.legend(loc='best')
            ax.grid(True, alpha=0.3)
            
        else:
            ax.text(0.5, 0.5, 'Datos de perfil radial no disponibles', 
                   ha='center', va='center', transform=ax.transAxes,
                   fontsize=14, bbox=dict(boxstyle='round', facecolor='wheat'))
            ax.set_title('Error: Perfil Radial No Disponible')
        
        return fig
    
    def create_local_validation_plots(self, local_results):
        """Crea gráficas de validación del régimen local."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Validación del Régimen Local (Schwarzschild)', fontsize=16)
        
        r_centers = local_results.get('r_centers', [])
        metric_profiles = local_results.get('metric_profiles', {})
        fits = local_results.get('schwarzschild_fits', {})
        
        components = ['g_xx', 'g_yy', 'g_zz']
        colors = ['blue', 'green', 'red']
        
        for i, (component, color) in enumerate(zip(components, colors)):
            if i >= 3:  # Solo plotear 3 componentes
                break
                
            row, col = i // 2, i % 2
            ax = axes[row, col]
            
            if component in metric_profiles and component in fits:
                profile_data = metric_profiles[component]
                fit_data = fits[component]
                
                if fit_data.get('fit_success', False):
                    # Datos de simulación
                    ax.plot(r_centers, profile_data, 'o', color=color, 
                           markersize=6, label='Simulación', alpha=0.8)
                    
                    # Ajuste teórico
                    theory_profile = fit_data['profile_theory']
                    ax.plot(r_centers, theory_profile, '-', color='black',
                           linewidth=2, label='Schwarzschild teórico')
                    
                    # Información del ajuste
                    M_eff = fit_data['M_eff']
                    error_rms = fit_data['error_rms']
                    mass_dev = fit_data['mass_deviation']
                    
                    info_text = f'M_eff = {M_eff:.4f}\nRMS = {error_rms:.6f}\nDesv = {mass_dev*100:.1f}%'
                    ax.text(0.05, 0.95, info_text, transform=ax.transAxes,
                           verticalalignment='top', fontsize=9,
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
                    
                    success_marker = "✅" if mass_dev < 0.01 else "⚠️"
                    ax.set_title(f'{component.replace("_", "")} {success_marker}')
                    
                else:
                    ax.text(0.5, 0.5, f'Ajuste fallido\n{fit_data.get("error", "")}',
                           ha='center', va='center', transform=ax.transAxes,
                           bbox=dict(boxstyle='round', facecolor='salmon', alpha=0.8))
                    ax.set_title(f'{component.replace("_", "")} ❌')
            else:
                ax.text(0.5, 0.5, 'Datos no disponibles',
                       ha='center', va='center', transform=ax.transAxes)
                ax.set_title(f'{component.replace("_", "")} ❓')
            
            ax.set_xlabel('Radio')
            ax.set_ylabel(f'{component.replace("_", "")}')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        # Resumen en el cuarto panel
        ax_summary = axes[1, 1]
        summary_text = local_results.get('validation_summary', 'No disponible')
        ax_summary.text(0.5, 0.5, f'Resumen de Validación Local:\n\n{summary_text}',
                       ha='center', va='center', transform=ax_summary.transAxes,
                       fontsize=12, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        ax_summary.set_title('Resumen de Validación')
        ax_summary.axis('off')
        
        plt.tight_layout()
        return fig
    
    def create_global_validation_plots(self, global_results):
        """Crea gráficas de validación del régimen global."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Validación del Régimen Global (Cosmológico)', fontsize=16)
        
        # 1. Análisis de isotropía
        ax1 = axes[0, 0]
        isotropy_data = global_results.get('isotropy', {})
        
        if isotropy_data:
            components = ['γ_xx - γ_yy', 'γ_yy - γ_zz', 'γ_xx - γ_zz']
            iso_components = isotropy_data.get('isotropy_components', {})
            values = [iso_components.get('xx_yy', 0), 
                     iso_components.get('yy_zz', 0),
                     iso_components.get('xx_zz', 0)]
            
            bars = ax1.bar(components, values, color=['red', 'green', 'blue'], alpha=0.7)
            ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
            ax1.set_ylabel('Desviación de isotropía')
            ax1.set_title('Análisis de Isotropía')
            ax1.tick_params(axis='x', rotation=45)
            
            max_aniso = isotropy_data.get('max_anisotropy', 0)
            is_isotropic = isotropy_data.get('is_isotropic', False)
            status = "✅ Isotrópico" if is_isotropic else "⚠️ Anisótropo"
            
            ax1.text(0.5, 0.95, f'{status}\nMáx: {max_aniso:.6f}',
                    transform=ax1.transAxes, ha='center', va='top',
                    bbox=dict(boxstyle='round', facecolor='lightgreen' if is_isotropic else 'yellow'))
        
        # 2. Análisis de perturbaciones
        ax2 = axes[0, 1]
        perturbation_data = global_results.get('perturbations', {})
        
        if perturbation_data:
            diag_devs = perturbation_data.get('diagonal_deviations', [])
            off_diag_mags = perturbation_data.get('off_diagonal_magnitudes', [])
            
            categories = ['γ_xx-1', 'γ_yy-1', 'γ_zz-1', 'γ_xy', 'γ_xz', 'γ_yz']
            values = diag_devs + off_diag_mags
            
            bars = ax2.bar(categories, values, 
                          color=['red', 'green', 'blue', 'orange', 'purple', 'brown'], 
                          alpha=0.7)
            ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
            ax2.set_ylabel('Magnitud de perturbación')
            ax2.set_title('Análisis de Perturbaciones')
            ax2.tick_params(axis='x', rotation=45)
            
            max_pert = perturbation_data.get('max_perturbation', 0)
            is_unperturbed = perturbation_data.get('is_unperturbed', False)
            status = "✅ No perturbado" if is_unperturbed else "⚠️ Perturbado"
            
            ax2.text(0.5, 0.95, f'{status}\nMáx: {max_pert:.6f}',
                    transform=ax2.transAxes, ha='center', va='top',
                    bbox=dict(boxstyle='round', facecolor='lightgreen' if is_unperturbed else 'yellow'))
        
        # 3. Evolución temporal (si disponible)
        ax3 = axes[1, 0]
        temporal_data = global_results.get('temporal_evolution', {})
        
        if temporal_data.get('available', False):
            times = temporal_data['times']
            det_evolution = temporal_data['det_evolution']
            
            ax3.plot(times, det_evolution, 'b-', linewidth=2, label='det(γ)')
            ax3.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='Sin expansión')
            ax3.set_xlabel('Tiempo')
            ax3.set_ylabel('det(γ)')
            ax3.set_title('Evolución Temporal del Factor de Escala')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            expansion_rate = temporal_data.get('expansion_rate', 0)
            expansion_detected = temporal_data.get('expansion_detected', False)
            status = "✅ Expansión detectada" if expansion_detected else "⚠️ Sin expansión clara"
            
            ax3.text(0.05, 0.95, f'{status}\nH ≈ {expansion_rate:.6f}',
                    transform=ax3.transAxes, va='top',
                    bbox=dict(boxstyle='round', facecolor='lightgreen' if expansion_detected else 'yellow'))
        else:
            ax3.text(0.5, 0.5, 'Datos temporales\nno disponibles',
                    ha='center', va='center', transform=ax3.transAxes,
                    bbox=dict(boxstyle='round', facecolor='lightgray'))
            ax3.set_title('Evolución Temporal - N/A')
        
        # 4. Resumen global
        ax4 = axes[1, 1]
        summary_text = global_results.get('validation_summary', 'No disponible')
        success = global_results.get('success', False)
        
        ax4.text(0.5, 0.5, f'Resumen de Validación Global:\n\n{summary_text}',
                ha='center', va='center', transform=ax4.transAxes,
                fontsize=12, 
                bbox=dict(boxstyle='round', 
                         facecolor='lightgreen' if success else 'yellow', 
                         alpha=0.8))
        ax4.set_title('Resumen de Validación')
        ax4.axis('off')
        
        plt.tight_layout()
        return fig
    
    def create_transition_analysis_plots(self, transition_results):
        """Crea gráficas de análisis de la zona de transición."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Análisis de la Zona de Transición', fontsize=16)
        
        radial_data = transition_results.get('radial_profile', {})
        smoothness_data = transition_results.get('smoothness', {})
        
        if radial_data.get('success', False):
            r_centers = radial_data['r_centers']
            gamma_profile = radial_data['gamma_profile']
            gamma_stds = radial_data['gamma_stds']
            
            # 1. Perfil completo
            ax1 = axes[0, 0]
            ax1.semilogx(r_centers, gamma_profile, 'b-', linewidth=2, label='γ_xx')
            ax1.fill_between(r_centers, 
                           gamma_profile - gamma_stds,
                           gamma_profile + gamma_stds,
                           alpha=0.3, color='blue', label='±1σ')
            ax1.axhline(y=1.0, color='k', linestyle='--', alpha=0.5, label='Métrica plana')
            ax1.set_xlabel('Radio (log)')
            ax1.set_ylabel('γ_xx')
            ax1.set_title('Perfil Radial Completo')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 2. Primera derivada
            ax2 = axes[0, 1]
            if len(r_centers) > 1:
                dr = np.diff(r_centers)
                dgamma_dr = np.diff(gamma_profile) / dr
                r_mid = 0.5 * (r_centers[1:] + r_centers[:-1])
                
                ax2.semilogx(r_mid, dgamma_dr, 'g-', linewidth=2, label='dγ/dr')
                ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
                ax2.set_xlabel('Radio (log)')
                ax2.set_ylabel('dγ/dr')
                ax2.set_title('Primera Derivada')
                ax2.legend()
                ax2.grid(True, alpha=0.3)
            
            # 3. Segunda derivada (curvatura)
            ax3 = axes[1, 0]
            if len(r_centers) > 2:
                d2gamma_dr2 = np.diff(dgamma_dr) / dr[:-1]
                r_mid2 = 0.5 * (r_mid[1:] + r_mid[:-1])
                
                ax3.semilogx(r_mid2, d2gamma_dr2, 'r-', linewidth=2, label='d²γ/dr²')
                ax3.axhline(y=0, color='k', linestyle='--', alpha=0.5)
                
                if smoothness_data:
                    threshold = smoothness_data.get('smoothness_threshold', 0.1)
                    ax3.axhline(y=threshold, color='orange', linestyle=':', 
                               label=f'Umbral suavidad ({threshold})')
                    ax3.axhline(y=-threshold, color='orange', linestyle=':')
                
                ax3.set_xlabel('Radio (log)')
                ax3.set_ylabel('d²γ/dr²')
                ax3.set_title('Segunda Derivada (Curvatura)')
                ax3.legend()
                ax3.grid(True, alpha=0.3)
        
        # 4. Resumen de suavidad
        ax4 = axes[1, 1]
        
        if smoothness_data:
            is_smooth = smoothness_data.get('is_smooth', False)
            max_curvature = smoothness_data.get('max_curvature', 0)
            mean_curvature = smoothness_data.get('mean_curvature', 0)
            
            status = "✅ SUAVE" if is_smooth else "⚠️ RUGOSA"
            
            summary_text = f'Estado de Transición:\n\n{status}\n\n'
            summary_text += f'Curvatura máxima: {max_curvature:.6f}\n'
            summary_text += f'Curvatura promedio: {mean_curvature:.6f}'
            
            ax4.text(0.5, 0.5, summary_text,
                    ha='center', va='center', transform=ax4.transAxes,
                    fontsize=12,
                    bbox=dict(boxstyle='round',
                             facecolor='lightgreen' if is_smooth else 'yellow',
                             alpha=0.8))
        else:
            ax4.text(0.5, 0.5, 'Análisis de suavidad\nno disponible',
                    ha='center', va='center', transform=ax4.transAxes,
                    bbox=dict(boxstyle='round', facecolor='lightgray'))
        
        ax4.set_title('Resumen de Suavidad')
        ax4.axis('off')
        
        plt.tight_layout()
        return fig
    
    def create_executive_summary(self, validation_results):
        """Crea un resumen ejecutivo visual de todos los resultados."""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Resumen Ejecutivo: Validación del Principio de Superposición Cosmológico\n' +
                    'Tarea 2.1.2 - Validación de Regímenes Físicos', fontsize=16)
        
        # Extraer resultados de éxito
        local_success = validation_results['local_regime'].get('success', False)
        global_success = validation_results['global_regime'].get('success', False)
        transition_success = validation_results['transition_zone'].get('success', False)
        decoupling_success = validation_results['decoupling'].get('success', False)
        overall_success = validation_results.get('overall_success', False)
        
        # 1. Dashboard de éxito
        ax1 = axes[0, 0]
        tests = ['Régimen Local', 'Régimen Global', 'Transición', 'Desacoplamiento']
        results = [local_success, global_success, transition_success, decoupling_success]
        colors = ['green' if success else 'red' for success in results]
        
        bars = ax1.barh(tests, [1]*4, color=colors, alpha=0.7)
        
        # Añadir checkmarks y X's
        for i, (test, success) in enumerate(zip(tests, results)):
            symbol = "✅" if success else "❌"
            ax1.text(0.5, i, symbol, ha='center', va='center', fontsize=20)
        
        ax1.set_xlim(0, 1)
        ax1.set_title('Estado de Validación por Régimen')
        ax1.set_xlabel('Tests de Validación')
        
        # Remover ticks del eje x
        ax1.set_xticks([])
        
        # 2. Métricas cuantitativas
        ax2 = axes[0, 1]
        
        # Extraer métricas clave
        metrics_text = "MÉTRICAS CLAVE DE VALIDACIÓN:\n\n"
        
        if local_success:
            local_summary = validation_results['local_regime'].get('validation_summary', '')
            metrics_text += f"• Régimen Local: {local_summary}\n\n"
        
        if global_success:
            global_summary = validation_results['global_regime'].get('validation_summary', '')
            metrics_text += f"• Régimen Global: {global_summary}\n\n"
        
        if transition_success:
            transition_summary = validation_results['transition_zone'].get('validation_summary', '')
            metrics_text += f"• Transición: {transition_summary}\n\n"
        
        # Resultado final
        final_status = "🎉 VALIDACIÓN EXITOSA" if overall_success else "⚠️ VALIDACIÓN PARCIAL"
        metrics_text += f"\n{final_status}"
        
        ax2.text(0.05, 0.95, metrics_text, transform=ax2.transAxes,
                verticalalignment='top', fontsize=10,
                bbox=dict(boxstyle='round', 
                         facecolor='lightgreen' if overall_success else 'yellow',
                         alpha=0.8))
        ax2.set_title('Métricas de Validación')
        ax2.axis('off')
        
        # 3. Parámetros de simulación
        ax3 = axes[1, 0]
        params = validation_results.get('parameters', {})
        
        params_text = "PARÁMETROS DE SIMULACIÓN:\n\n"
        params_text += f"• Masa local: M = {params.get('mass_local', 'N/A')}\n"
        params_text += f"• Radio suavizado: σ = {params.get('smoothing_radius', 'N/A'):.4f}\n"
        params_text += f"• Tolerancia local: {params.get('tolerance_local', 'N/A')*100:.1f}%\n"
        params_text += f"• Tolerancia global: {params.get('tolerance_global', 'N/A')*100:.1f}%\n"
        
        ax3.text(0.05, 0.95, params_text, transform=ax3.transAxes,
                verticalalignment='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        ax3.set_title('Configuración de Simulación')
        ax3.axis('off')
        
        # 4. Conclusiones y próximos pasos
        ax4 = axes[1, 1]
        
        conclusions_text = "CONCLUSIONES:\n\n"
        
        successful_tests = sum([local_success, global_success, transition_success, decoupling_success])
        conclusions_text += f"• Tests exitosos: {successful_tests}/4\n\n"
        
        if overall_success:
            conclusions_text += "✅ El Principio de Superposición\n"
            conclusions_text += "   Cosmológico es FÍSICAMENTE\n"
            conclusions_text += "   VÁLIDO según los criterios\n"
            conclusions_text += "   establecidos.\n\n"
            conclusions_text += "📋 PRÓXIMOS PASOS:\n"
            conclusions_text += "• Implementar Tarea 2.1.3\n"
            conclusions_text += "• Análisis de efectos de\n"
            conclusions_text += "  acoplamiento no lineal\n"
        else:
            conclusions_text += "⚠️ Validación parcial obtenida.\n\n"
            conclusions_text += "🔧 RECOMENDACIONES:\n"
            if not local_success:
                conclusions_text += "• Revisar régimen local\n"
            if not global_success:
                conclusions_text += "• Revisar régimen global\n"
            if not transition_success:
                conclusions_text += "• Analizar zona de transición\n"
            conclusions_text += "• Ajustar parámetros de simulación\n"
        
        ax4.text(0.05, 0.95, conclusions_text, transform=ax4.transAxes,
                verticalalignment='top', fontsize=10,
                bbox=dict(boxstyle='round',
                         facecolor='lightgreen' if overall_success else 'lightyellow',
                         alpha=0.8))
        ax4.set_title('Conclusiones y Próximos Pasos')
        ax4.axis('off')
        
        plt.tight_layout()
        return fig