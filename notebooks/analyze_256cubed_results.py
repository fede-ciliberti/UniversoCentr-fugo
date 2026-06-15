#!/usr/bin/env python3
"""
Analizador de resultados para simulación 256³ optimizada.
Herramientas de análisis post-simulación y validación científica.

Funcionalidades:
1. Análisis de convergencia espacial
2. Comparación con solución de Schwarzschild
3. Validación de isotropía
4. Análisis de estabilidad temporal
5. Generación de visualizaciones publication-ready
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import argparse
import json
from scipy.interpolate import griddata
from scipy.optimize import curve_fit
import warnings

warnings.filterwarnings('ignore')

class Schwarzschild256Analyzer:
    """
    Analizador especializado para resultados de simulación 256³.
    """
    
    def __init__(self, results_dir="output/simulation_256cubed/results"):
        """
        Inicializa el analizador.
        
        Args:
            results_dir: Directorio con resultados de la simulación
        """
        self.results_dir = Path(results_dir)
        self.figures_dir = self.results_dir / "analysis_figures"
        self.figures_dir.mkdir(exist_ok=True)
        
        # Parámetros de la simulación (se cargan desde resultados)
        self.grid_size = None
        self.sample_resolution = None
        self.dt = None
        self.final_time = None
        
        # Datos cargados
        self.gamma_xx = None
        self.gamma_yy = None
        self.gamma_zz = None
        self.time_evolution = None
        self.metric_invariants = None
        
        print("🔬 Analizador de Resultados 256³ Inicializado")
        print(f"   Directorio de resultados: {self.results_dir}")
        print(f"   Directorio de figuras: {self.figures_dir}")
    
    def load_simulation_results(self, results_file=None):
        """Carga los resultados de la simulación."""
        if results_file is None:
            # Buscar el archivo de resultados más reciente
            pattern = "simulation_256cubed_results_*.npz"
            results_files = list(self.results_dir.glob(pattern))
            
            if not results_files:
                raise FileNotFoundError(f"No se encontraron archivos de resultados en {self.results_dir}")
            
            results_file = max(results_files, key=lambda x: x.stat().st_mtime)
        
        print(f"📁 Cargando resultados desde: {results_file}")
        
        data = np.load(results_file, allow_pickle=True)
        
        # Cargar metadatos
        self.grid_size = int(data['grid_size'])
        self.sample_resolution = int(data['sample_resolution'])
        self.dt = float(data['dt'])
        self.final_time = float(data['final_time'])
        
        # Cargar datos métricos
        self.gamma_xx = data['final_gamma_xx_sample']
        self.gamma_yy = data['final_gamma_yy_sample']
        self.gamma_zz = data['final_gamma_zz_sample']
        
        # Cargar evolución temporal
        self.time_evolution = data['time_evolution']
        
        # Manejar metric_invariants que puede venir en diferentes formatos
        try:
            self.metric_invariants = data['metric_invariants'].item()  # Si es array con objeto
        except ValueError:
            # Si ya es una lista directamente
            self.metric_invariants = data['metric_invariants'].tolist() if hasattr(data['metric_invariants'], 'tolist') else data['metric_invariants']
        
        print(f"✓ Resultados cargados:")
        print(f"   Grid original: {self.grid_size}³")
        print(f"   Resolución de muestra: {self.sample_resolution}³")
        print(f"   Tiempo final: {self.final_time:.3f}")
        print(f"   Pasos temporales: {len(self.time_evolution)}")
        
        return True
    
    def create_coordinate_system(self):
        """Crea el sistema de coordenadas para análisis."""
        # Dominio espacial (asumiendo [-10, 10] como en simulaciones previas)
        domain_size = 20.0
        
        # Coordenadas de la muestra
        x_coords = np.linspace(-domain_size/2, domain_size/2, self.sample_resolution)
        y_coords = np.linspace(-domain_size/2, domain_size/2, self.sample_resolution)
        z_coords = np.linspace(-domain_size/2, domain_size/2, self.sample_resolution)
        
        self.X, self.Y, self.Z = np.meshgrid(x_coords, y_coords, z_coords, indexing='ij')
        
        # Coordenadas radiales desde el centro
        self.R = np.sqrt(self.X**2 + self.Y**2 + self.Z**2)
        
        print(f"✓ Sistema de coordenadas creado:")
        print(f"   Dominio: [{-domain_size/2:.1f}, {domain_size/2:.1f}]³")
        print(f"   Resolución efectiva: {domain_size/self.sample_resolution:.4f}")
    
    def generate_schwarzschild_reference(self, mass=0.5, G=1.0):
        """
        Genera la métrica de Schwarzschild teórica para comparación.
        
        Args:
            mass: Masa de la partícula central
            G: Constante gravitacional
        """
        print(f"🌌 Generando referencia de Schwarzschild (M={mass}, G={G})...")
        
        # Evitar singularidad en el origen
        R_safe = np.maximum(self.R, 0.1)
        
        # Métrica de Schwarzschild en coordenadas isotrópicas
        # g_rr = g_θθ = g_φφ = (1 + GM/2r)⁴
        
        schwarzschild_radius = G * mass
        factor = 1 + schwarzschild_radius / (2 * R_safe)
        
        self.g_schwarzschild_rr = factor**4
        self.g_schwarzschild_tt = -((1 - schwarzschild_radius/(2*R_safe)) / 
                                   (1 + schwarzschild_radius/(2*R_safe)))**2
        
        print(f"✓ Referencia de Schwarzschild generada")
        print(f"   Radio de Schwarzschild: {schwarzschild_radius}")
        print(f"   Rango radial: [{np.min(R_safe):.3f}, {np.max(R_safe):.3f}]")
    
    def analyze_convergence_to_schwarzschild(self):
        """Analiza la convergencia hacia la métrica de Schwarzschild."""
        print("📊 Analizando convergencia hacia Schwarzschild...")
        
        # Análisis radial: extraer perfil a lo largo del eje x
        center_idx = self.sample_resolution // 2
        
        # Perfiles radiales de la simulación
        r_profile = self.X[center_idx:, center_idx, center_idx]
        gamma_xx_profile = self.gamma_xx[center_idx:, center_idx, center_idx]
        gamma_yy_profile = self.gamma_yy[center_idx:, center_idx, center_idx]
        gamma_zz_profile = self.gamma_zz[center_idx:, center_idx, center_idx]
        
        # Perfiles teóricos de Schwarzschild
        schwarzschild_profile = self.g_schwarzschild_rr[center_idx:, center_idx, center_idx]
        
        # Calcular errores
        error_xx = np.abs(gamma_xx_profile - schwarzschild_profile) / schwarzschild_profile * 100
        error_yy = np.abs(gamma_yy_profile - schwarzschild_profile) / schwarzschild_profile * 100
        error_zz = np.abs(gamma_zz_profile - schwarzschild_profile) / schwarzschild_profile * 100
        
        # Filtrar región válida (evitar muy cerca del centro y bordes)
        valid_mask = (r_profile > 1.0) & (r_profile < 8.0)
        
        if np.sum(valid_mask) == 0:
            print("⚠️  No hay puntos válidos para análisis")
            return None
        
        r_valid = r_profile[valid_mask]
        error_xx_valid = error_xx[valid_mask]
        error_yy_valid = error_yy[valid_mask]
        error_zz_valid = error_zz[valid_mask]
        
        # Métricas de error
        rms_error_xx = np.sqrt(np.mean(error_xx_valid**2))
        rms_error_yy = np.sqrt(np.mean(error_yy_valid**2))
        rms_error_zz = np.sqrt(np.mean(error_zz_valid**2))
        
        max_error_xx = np.max(error_xx_valid)
        max_error_yy = np.max(error_yy_valid)
        max_error_zz = np.max(error_zz_valid)
        
        # Test de isotropía
        isotropy_error_xy = np.abs(gamma_xx_profile - gamma_yy_profile)[valid_mask]
        isotropy_error_xz = np.abs(gamma_xx_profile - gamma_zz_profile)[valid_mask]
        isotropy_error_yz = np.abs(gamma_yy_profile - gamma_zz_profile)[valid_mask]
        
        max_isotropy_error = np.max([np.max(isotropy_error_xy),
                                    np.max(isotropy_error_xz),
                                    np.max(isotropy_error_yz)])
        
        results = {
            'rms_errors': {
                'gamma_xx': rms_error_xx,
                'gamma_yy': rms_error_yy,
                'gamma_zz': rms_error_zz
            },
            'max_errors': {
                'gamma_xx': max_error_xx,
                'gamma_yy': max_error_yy,
                'gamma_zz': max_error_zz
            },
            'isotropy': {
                'max_error_percent': max_isotropy_error / np.mean(gamma_xx_profile[valid_mask]) * 100
            },
            'profiles': {
                'r': r_valid,
                'gamma_xx': gamma_xx_profile[valid_mask],
                'gamma_yy': gamma_yy_profile[valid_mask],
                'gamma_zz': gamma_zz_profile[valid_mask],
                'schwarzschild': schwarzschild_profile[valid_mask],
                'errors_xx': error_xx_valid,
                'errors_yy': error_yy_valid,
                'errors_zz': error_zz_valid
            }
        }
        
        print(f"✓ Análisis de convergencia completado:")
        print(f"   Error RMS γ_xx: {rms_error_xx:.2f}%")
        print(f"   Error RMS γ_yy: {rms_error_yy:.2f}%")
        print(f"   Error RMS γ_zz: {rms_error_zz:.2f}%")
        print(f"   Error máximo de isotropía: {results['isotropy']['max_error_percent']:.3f}%")
        
        return results
    
    def analyze_temporal_stability(self):
        """Analiza la estabilidad temporal de la simulación."""
        print("⏱️  Analizando estabilidad temporal...")
        
        if not self.metric_invariants:
            print("⚠️  No hay datos de evolución temporal")
            return None
        
        # Extraer series temporales
        times = np.array(self.time_evolution)
        det_gammas = np.array([inv['det_gamma_mean'] for inv in self.metric_invariants])
        trace_Ks = np.array([inv['trace_K_mean'] for inv in self.metric_invariants])
        
        # Análisis de tendencias
        if len(times) > 10:
            # Ajuste lineal para detectar deriva
            det_gamma_trend = np.polyfit(times, det_gammas, 1)
            trace_K_trend = np.polyfit(times, trace_Ks, 1)
            
            # Variabilidad (desviación estándar)
            det_gamma_std = np.std(det_gammas)
            trace_K_std = np.std(trace_Ks)
            
            # Estabilidad (cambio relativo)
            det_gamma_stability = np.abs(det_gammas[-1] - det_gammas[0]) / det_gammas[0]
            trace_K_stability = np.abs(trace_Ks[-1] - trace_Ks[0]) / (np.abs(trace_Ks[0]) + 1e-10)
            
            stability_results = {
                'times': times,
                'det_gamma': {
                    'values': det_gammas,
                    'trend_slope': det_gamma_trend[0],
                    'std': det_gamma_std,
                    'relative_change': det_gamma_stability
                },
                'trace_K': {
                    'values': trace_Ks,
                    'trend_slope': trace_K_trend[0],
                    'std': trace_K_std,
                    'relative_change': trace_K_stability
                }
            }
            
            print(f"✓ Análisis temporal completado:")
            print(f"   det(γ) - cambio relativo: {det_gamma_stability:.4f}")
            print(f"   det(γ) - tendencia: {det_gamma_trend[0]:.6f}/tiempo")
            print(f"   tr(K) - cambio relativo: {trace_K_stability:.4f}")
            
            return stability_results
        
        else:
            print("⚠️  Insuficientes datos temporales para análisis")
            return None
    
    def create_publication_quality_plots(self, convergence_results, stability_results):
        """Crea gráficos de calidad de publicación."""
        print("📈 Generando gráficos de calidad de publicación...")
        
        # Configurar estilo
        plt.style.use('default')
        plt.rcParams.update({
            'font.size': 12,
            'font.family': 'serif',
            'axes.linewidth': 1.5,
            'xtick.major.width': 1.5,
            'ytick.major.width': 1.5,
            'xtick.minor.width': 1.0,
            'ytick.minor.width': 1.0,
            'legend.frameon': True,
            'legend.fancybox': True,
            'legend.shadow': True
        })
        
        # Figura 1: Comparación con Schwarzschild
        fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))
        fig1.suptitle('Simulación 256³: Comparación con Métrica de Schwarzschild', 
                     fontsize=16, fontweight='bold')
        
        if convergence_results:
            profiles = convergence_results['profiles']
            
            # Perfil radial
            ax1.plot(profiles['r'], profiles['schwarzschild'], 'k-', linewidth=3, 
                    label='Schwarzschild (teórico)', alpha=0.8)
            ax1.plot(profiles['r'], profiles['gamma_xx'], 'r--', linewidth=2,
                    label=r'$\gamma_{xx}$ (simulación)')
            ax1.plot(profiles['r'], profiles['gamma_yy'], 'g--', linewidth=2,
                    label=r'$\gamma_{yy}$ (simulación)')
            ax1.plot(profiles['r'], profiles['gamma_zz'], 'b--', linewidth=2,
                    label=r'$\gamma_{zz}$ (simulación)')
            
            ax1.set_xlabel('Radio (unidades geométricas)')
            ax1.set_ylabel('Componente métrica')
            ax1.set_title('Perfiles Radiales de la Métrica')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.set_xlim(1.0, 8.0)
            
            # Error relativo
            ax2.semilogy(profiles['r'], profiles['errors_xx'], 'r-', linewidth=2,
                        label=r'Error $\gamma_{xx}$')
            ax2.semilogy(profiles['r'], profiles['errors_yy'], 'g-', linewidth=2,
                        label=r'Error $\gamma_{yy}$')
            ax2.semilogy(profiles['r'], profiles['errors_zz'], 'b-', linewidth=2,
                        label=r'Error $\gamma_{zz}$')
            
            ax2.set_xlabel('Radio (unidades geométricas)')
            ax2.set_ylabel('Error Relativo (%)')
            ax2.set_title('Error Relativo vs Schwarzschild')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_xlim(1.0, 8.0)
            
            # Mapa 2D de contornos
            center_slice = self.sample_resolution // 2
            gamma_xx_slice = self.gamma_xx[:, :, center_slice]
            
            extent = [-10, 10, -10, 10]  # Asumiendo dominio [-10, 10]
            im = ax3.imshow(gamma_xx_slice, extent=extent, cmap='RdBu_r',
                           vmin=0.95, vmax=1.05, origin='lower')
            ax3.set_xlabel('x (unidades geométricas)')
            ax3.set_ylabel('y (unidades geométricas)')
            ax3.set_title(r'$\gamma_{xx}$ en plano z=0')
            
            # Añadir contornos
            X_2d = np.linspace(-10, 10, self.sample_resolution)
            Y_2d = np.linspace(-10, 10, self.sample_resolution)
            X_mesh, Y_mesh = np.meshgrid(X_2d, Y_2d)
            contours = ax3.contour(X_mesh, Y_mesh, gamma_xx_slice.T, 
                                  levels=np.linspace(0.96, 1.04, 9),
                                  colors='black', alpha=0.6, linewidths=0.8)
            ax3.clabel(contours, inline=True, fontsize=8)
            
            plt.colorbar(im, ax=ax3, label=r'$\gamma_{xx}$')
        
        # Test de isotropía
        if convergence_results:
            iso_error = convergence_results['isotropy']['max_error_percent']
            
            ax4.text(0.5, 0.7, f'Análisis de Isotropía', transform=ax4.transAxes,
                    fontsize=14, fontweight='bold', ha='center')
            ax4.text(0.5, 0.5, f'Error máximo: {iso_error:.3f}%', transform=ax4.transAxes,
                    fontsize=12, ha='center')
            
            # Criterio de validación
            if iso_error < 0.1:
                status = "✓ APROBADO"
                color = 'green'
            else:
                status = "✗ NO CUMPLIDO"
                color = 'red'
            
            ax4.text(0.5, 0.3, f'Criterio < 0.1%: {status}', transform=ax4.transAxes,
                    fontsize=12, ha='center', color=color, fontweight='bold')
            
            ax4.set_xlim(0, 1)
            ax4.set_ylim(0, 1)
            ax4.axis('off')
        
        plt.tight_layout()
        figure1_path = self.figures_dir / "256cubed_schwarzschild_comparison.png"
        plt.savefig(figure1_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Figura 2: Estabilidad temporal
        if stability_results:
            fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
            fig2.suptitle('Simulación 256³: Análisis de Estabilidad Temporal',
                         fontsize=16, fontweight='bold')
            
            times = stability_results['times']
            det_gammas = stability_results['det_gamma']['values']
            trace_Ks = stability_results['trace_K']['values']
            
            # Evolución de det(γ)
            ax1.plot(times, det_gammas, 'b-', linewidth=2, marker='o', markersize=4)
            ax1.set_xlabel('Tiempo (unidades geométricas)')
            ax1.set_ylabel(r'$\det(\gamma)$')
            ax1.set_title('Evolución del Determinante de la Métrica')
            ax1.grid(True, alpha=0.3)
            
            # Añadir tendencia
            trend = stability_results['det_gamma']['trend_slope']
            trend_line = det_gammas[0] + trend * (times - times[0])
            ax1.plot(times, trend_line, 'r--', alpha=0.7, 
                    label=f'Tendencia: {trend:.6f}/tiempo')
            ax1.legend()
            
            # Evolución de tr(K)
            ax2.plot(times, trace_Ks, 'g-', linewidth=2, marker='s', markersize=4)
            ax2.set_xlabel('Tiempo (unidades geométricas)')
            ax2.set_ylabel(r'$\text{tr}(K)$')
            ax2.set_title('Evolución de la Traza de la Curvatura Extrínseca')
            ax2.grid(True, alpha=0.3)
            
            # Añadir tendencia
            trend_K = stability_results['trace_K']['trend_slope']
            trend_line_K = trace_Ks[0] + trend_K * (times - times[0])
            ax2.plot(times, trend_line_K, 'r--', alpha=0.7,
                    label=f'Tendencia: {trend_K:.6f}/tiempo')
            ax2.legend()
            
            plt.tight_layout()
            figure2_path = self.figures_dir / "256cubed_temporal_stability.png"
            plt.savefig(figure2_path, dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"✓ Gráficos guardados:")
        print(f"   {figure1_path}")
        if stability_results:
            print(f"   {figure2_path}")
        
        return [figure1_path, figure2_path] if stability_results else [figure1_path]
    
    def generate_scientific_report(self, convergence_results, stability_results):
        """Genera un reporte científico completo."""
        print("📋 Generando reporte científico...")
        
        report_file = self.results_dir / "scientific_analysis_report_256cubed.txt"
        
        with open(report_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("REPORTE CIENTÍFICO: SIMULACIÓN EINSTEIN 256³\n")
            f.write("Análisis de Convergencia hacia Métrica de Schwarzschild\n")
            f.write("=" * 80 + "\n\n")
            
            # Resumen ejecutivo
            f.write("RESUMEN EJECUTIVO\n")
            f.write("-" * 20 + "\n\n")
            
            if convergence_results:
                rms_avg = np.mean([convergence_results['rms_errors']['gamma_xx'],
                                 convergence_results['rms_errors']['gamma_yy'],
                                 convergence_results['rms_errors']['gamma_zz']])
                
                iso_error = convergence_results['isotropy']['max_error_percent']
                
                f.write(f"Resolución simulada: {self.grid_size}³ = {self.grid_size**3:,} puntos\n")
                f.write(f"Tiempo final: {self.final_time:.3f} unidades geométricas\n")
                f.write(f"Error RMS promedio: {rms_avg:.2f}%\n")
                f.write(f"Error de isotropía: {iso_error:.3f}%\n\n")
                
                # Criterios de validación
                f.write("CRITERIOS DE VALIDACIÓN\n")
                f.write("-" * 25 + "\n\n")
                
                criterios = [
                    ("Error RMS < 1%", rms_avg < 1.0, f"{rms_avg:.2f}%"),
                    ("Isotropía < 0.1%", iso_error < 0.1, f"{iso_error:.3f}%"),
                ]
                
                for criterio, cumplido, valor in criterios:
                    status = "✓ CUMPLIDO" if cumplido else "✗ NO CUMPLIDO"
                    f.write(f"{criterio}: {status} ({valor})\n")
                
                f.write(f"\nPuntuación total: {sum(c[1] for c in criterios)}/{len(criterios)} criterios\n\n")
                
                # Detalles técnicos
                f.write("DETALLES TÉCNICOS\n")
                f.write("-" * 20 + "\n\n")
                
                f.write("Errores RMS por componente:\n")
                for comp, error in convergence_results['rms_errors'].items():
                    f.write(f"  {comp}: {error:.2f}%\n")
                
                f.write("\nErrores máximos por componente:\n")
                for comp, error in convergence_results['max_errors'].items():
                    f.write(f"  {comp}: {error:.2f}%\n")
            
            # Análisis temporal
            if stability_results:
                f.write("\n\nANÁLISIS DE ESTABILIDAD TEMPORAL\n")
                f.write("-" * 35 + "\n\n")
                
                det_change = stability_results['det_gamma']['relative_change']
                K_change = stability_results['trace_K']['relative_change']
                
                f.write(f"Cambio relativo en det(γ): {det_change:.4f}\n")
                f.write(f"Cambio relativo en tr(K): {K_change:.4f}\n")
                f.write(f"Tendencia det(γ): {stability_results['det_gamma']['trend_slope']:.6f}/tiempo\n")
                f.write(f"Tendencia tr(K): {stability_results['trace_K']['trend_slope']:.6f}/tiempo\n")
                
                estabilidad = "ESTABLE" if det_change < 0.01 and K_change < 0.01 else "INESTABLE"
                f.write(f"\nEvaluación general: {estabilidad}\n")
            
            # Conclusiones
            f.write("\n\nCONCLUSIONES\n")
            f.write("-" * 15 + "\n\n")
            
            if convergence_results:
                if rms_avg < 1.0 and iso_error < 0.1:
                    f.write("✓ VALIDACIÓN EXITOSA: La simulación 256³ reproduce la métrica de Schwarzschild\n")
                    f.write("  con precisión suficiente para publicación científica.\n\n")
                elif rms_avg < 5.0:
                    f.write("⚠ VALIDACIÓN PARCIAL: La simulación muestra convergencia hacia Schwarzschild\n")
                    f.write("  pero requiere optimización adicional para precisión publication-ready.\n\n")
                else:
                    f.write("✗ VALIDACIÓN FALLIDA: Errores significativos detectados.\n")
                    f.write("  Se requiere revisión de parámetros y algoritmo.\n\n")
                
                f.write("Mejoras identificadas vs simulación 32³:\n")
                f.write("  - Resolución 512x mayor\n")
                f.write("  - Algoritmo BSSN completo con chunks\n")
                f.write("  - Optimizaciones de memoria y precisión\n\n")
            
            f.write("Recomendaciones para futuras simulaciones:\n")
            f.write("  1. Considerar resolución 512³ si los recursos lo permiten\n")
            f.write("  2. Implementar kernels GPU para aceleración\n")
            f.write("  3. Agregar análisis de ondas gravitacionales\n")
            f.write("  4. Validar con múltiples masas y configuraciones\n\n")
            
            f.write("=" * 80 + "\n")
            f.write(f"Reporte generado: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
        
        print(f"✓ Reporte científico guardado: {report_file}")
        return report_file
    
    def run_complete_analysis(self):
        """Ejecuta el análisis completo de la simulación 256³."""
        print("\n🚀 INICIANDO ANÁLISIS COMPLETO 256³")
        print("=" * 70)
        
        try:
            # 1. Cargar resultados
            if not self.load_simulation_results():
                return False
            
            # 2. Crear sistema de coordenadas
            self.create_coordinate_system()
            
            # 3. Generar referencia de Schwarzschild
            self.generate_schwarzschild_reference()
            
            # 4. Análisis de convergencia
            convergence_results = self.analyze_convergence_to_schwarzschild()
            
            # 5. Análisis de estabilidad temporal
            stability_results = self.analyze_temporal_stability()
            
            # 6. Generar gráficos
            figure_paths = self.create_publication_quality_plots(convergence_results, stability_results)
            
            # 7. Generar reporte
            report_path = self.generate_scientific_report(convergence_results, stability_results)
            
            print("\n✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
            print("=" * 70)
            print(f"📊 Archivos generados:")
            for path in figure_paths:
                print(f"   {path}")
            print(f"   {report_path}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Función principal del analizador."""
    parser = argparse.ArgumentParser(description="Analizador de resultados 256³")
    parser.add_argument('--results-dir', type=str, 
                       default="output/simulation_256cubed/results",
                       help="Directorio con resultados de simulación")
    parser.add_argument('--results-file', type=str, default=None,
                       help="Archivo específico de resultados")
    
    args = parser.parse_args()
    
    # Crear analizador
    analyzer = Schwarzschild256Analyzer(args.results_dir)
    
    # Ejecutar análisis completo
    success = analyzer.run_complete_analysis()
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    import time
    
    sys.exit(main())