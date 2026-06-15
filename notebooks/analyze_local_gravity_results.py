#!/usr/bin/env python3
"""
FASE 3: Análisis de Resultados y Validación Científica
Comparación de la métrica emergente vs. métrica de Schwarzschild teórica

Este script implementa el análisis cuantitativo para responder la pregunta fundamental:
¿La métrica emergente corresponde a Schwarzschild?
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from pathlib import Path
import argparse
from scipy.interpolate import griddata
import matplotlib.patches as patches
from matplotlib.colors import LogNorm
from matplotlib.patches import Circle

# Configuración para gráficos científicos
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

class SchwarzschildAnalysis:
    """Análisis científico de la emergencia de la métrica de Schwarzschild."""
    
    def __init__(self, resolution, mass_particle=0.5, G=1.0):
        """
        Inicializa el análisis.
        
        Parameters:
        -----------
        resolution : int
            Resolución de la malla de simulación
        mass_particle : float
            Masa de la partícula simulada (default: 0.5)
        G : float
            Constante gravitacional (default: 1.0 en unidades de simulación)
        """
        self.resolution = resolution
        self.M = mass_particle
        self.G = G
        self.output_dir = Path(f"output/local_gravity_{resolution}cubed")
        self.results_dir = Path(f"results/local_gravity_{resolution}cubed")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Rango radial para análisis (evitar singularidad y bordes)
        self.r_min = 0.5
        self.r_max = 8.0
        
        print(f"🔬 Iniciando análisis científico para simulación {resolution}³")
        print(f"   Masa de partícula: M = {self.M}")
        print(f"   Rango radial: {self.r_min} < r < {self.r_max}")
        print(f"   Directorio resultados: {self.results_dir}")
    
    def load_simulation_data(self):
        """Carga el último checkpoint de la simulación."""
        checkpoint_files = sorted(glob.glob(str(self.output_dir / "checkpoint_*.npz")))
        
        if not checkpoint_files:
            raise FileNotFoundError(f"No se encontraron checkpoints en {self.output_dir}")
        
        latest_checkpoint = checkpoint_files[-1]
        print(f"📁 Cargando checkpoint: {os.path.basename(latest_checkpoint)}")
        
        data = np.load(latest_checkpoint)
        
        # Extraer datos de simulación
        self.step = data['step']
        self.time_sim = data['time']
        self.gamma_xx = data['gamma_xx']
        self.gamma_yy = data['gamma_yy'] 
        self.gamma_zz = data['gamma_zz']
        self.gamma_xy = data.get('gamma_xy', np.zeros_like(self.gamma_xx))
        self.gamma_xz = data.get('gamma_xz', np.zeros_like(self.gamma_xx))
        self.gamma_yz = data.get('gamma_yz', np.zeros_like(self.gamma_xx))
        
        # Construir grilla de coordenadas
        self.L = 10.0  # Tamaño del dominio
        self.dx = self.L / self.resolution
        x = np.linspace(-self.L/2 + self.dx/2, self.L/2 - self.dx/2, self.resolution)
        y = np.linspace(-self.L/2 + self.dx/2, self.L/2 - self.dx/2, self.resolution)
        z = np.linspace(-self.L/2 + self.dx/2, self.L/2 - self.dx/2, self.resolution)
        
        self.X, self.Y, self.Z = np.meshgrid(x, y, z, indexing='ij')
        self.R = np.sqrt(self.X**2 + self.Y**2 + self.Z**2)
        
        print(f"✓ Datos cargados - Paso: {self.step}, Tiempo: {self.time_sim:.3f}")
        print(f"   Resolución de grilla: {self.resolution}³")
        print(f"   Tamaño de dominio: {self.L} x {self.L} x {self.L}")
        
        return data
    
    def schwarzschild_metric_cartesian(self):
        """
        Calcula la métrica de Schwarzschild en coordenadas cartesianas isotrópicas.
        
        En coordenadas isotrópicas:
        g_tt = -(1 - 2GM/r) / (1 + GM/2r)²
        g_ij = δ_ij * (1 + GM/2r)⁴
        
        Returns:
        --------
        dict con componentes de la métrica teórica
        """
        print("📐 Calculando métrica de Schwarzschild teórica...")
        
        # Evitar singularidad en r=0
        R_safe = np.where(self.R < 1e-6, 1e-6, self.R)
        
        # Parámetro gravitacional
        GM = self.G * self.M
        
        # Coordenadas isotrópicas de Schwarzschild
        psi = 1 + GM / (2 * R_safe)  # Factor conforme
        
        # Componente temporal (con factor de lapse)
        g_tt = -(1 - GM / (2 * R_safe))**2 / psi**2
        
        # Componentes espaciales (métricas conformes)
        g_xx = psi**4
        g_yy = psi**4  
        g_zz = psi**4
        
        # Componentes cruzadas (cero para simetría esférica)
        g_xy = np.zeros_like(g_xx)
        g_xz = np.zeros_like(g_xx)
        g_yz = np.zeros_like(g_xx)
        
        print(f"✓ Métrica teórica calculada")
        print(f"   g_tt en r=1: {g_tt[self.resolution//2, self.resolution//2, self.resolution//2]:.6f}")
        print(f"   g_xx en r=1: {g_xx[self.resolution//2, self.resolution//2, self.resolution//2]:.6f}")
        
        return {
            'g_tt': g_tt,
            'g_xx': g_xx,
            'g_yy': g_yy,
            'g_zz': g_zz,
            'g_xy': g_xy,
            'g_xz': g_xz,
            'g_yz': g_yz
        }
    
    def calculate_errors(self, metric_theory):
        """Calcula errores cuantitativos entre métrica simulada y teórica."""
        print("📊 Calculando errores cuantitativos...")
        
        # Máscara para región de análisis
        mask = (self.R >= self.r_min) & (self.R <= self.r_max)
        
        # Errores absolutos
        error_xx = np.abs(self.gamma_xx - metric_theory['g_xx'])
        error_yy = np.abs(self.gamma_yy - metric_theory['g_yy']) 
        error_zz = np.abs(self.gamma_zz - metric_theory['g_zz'])
        
        # Errores relativos (evitar división por cero)
        theory_xx_safe = np.where(np.abs(metric_theory['g_xx']) < 1e-10, 1e-10, metric_theory['g_xx'])
        theory_yy_safe = np.where(np.abs(metric_theory['g_yy']) < 1e-10, 1e-10, metric_theory['g_yy'])
        theory_zz_safe = np.where(np.abs(metric_theory['g_zz']) < 1e-10, 1e-10, metric_theory['g_zz'])
        
        rel_error_xx = error_xx / np.abs(theory_xx_safe)
        rel_error_yy = error_yy / np.abs(theory_yy_safe)
        rel_error_zz = error_zz / np.abs(theory_zz_safe)
        
        # Estadísticas en región de análisis
        stats = {
            'error_xx_mean': np.mean(error_xx[mask]),
            'error_xx_max': np.max(error_xx[mask]),
            'error_xx_rms': np.sqrt(np.mean(error_xx[mask]**2)),
            'rel_error_xx_mean': np.mean(rel_error_xx[mask]) * 100,  # Porcentaje
            'rel_error_xx_max': np.max(rel_error_xx[mask]) * 100,
            'rel_error_xx_rms': np.sqrt(np.mean(rel_error_xx[mask]**2)) * 100,
            
            'error_yy_mean': np.mean(error_yy[mask]),
            'error_yy_max': np.max(error_yy[mask]),
            'rel_error_yy_mean': np.mean(rel_error_yy[mask]) * 100,
            
            'error_zz_mean': np.mean(error_zz[mask]),
            'error_zz_max': np.max(error_zz[mask]),
            'rel_error_zz_mean': np.mean(rel_error_zz[mask]) * 100,
        }
        
        print(f"✓ Errores calculados:")
        print(f"   Error relativo RMS g_xx: {stats['rel_error_xx_rms']:.3f}%")
        print(f"   Error relativo RMS g_yy: {stats['rel_error_yy_mean']:.3f}%")
        print(f"   Error relativo RMS g_zz: {stats['rel_error_zz_mean']:.3f}%")
        
        return {
            'error_xx': error_xx,
            'error_yy': error_yy,
            'error_zz': error_zz,
            'rel_error_xx': rel_error_xx,
            'rel_error_yy': rel_error_yy,
            'rel_error_zz': rel_error_zz,
            'stats': stats
        }
    
    def test_isotropy(self):
        """Test de isotropía: verifica diferencias direccionales."""
        print("🔄 Evaluando isotropía...")
        
        # Extraer perfiles radiales en diferentes direcciones
        center = self.resolution // 2
        
        # Dirección X (eje x)
        profile_x = self.gamma_xx[center:, center, center]
        r_x = self.R[center:, center, center]
        
        # Dirección Y (eje y)  
        profile_y = self.gamma_yy[center, center:, center]
        r_y = self.R[center, center:, center]
        
        # Dirección Z (eje z)
        profile_z = self.gamma_zz[center, center, center:]
        r_z = self.R[center, center, center:]
        
        # Comparar en puntos específicos
        r_test_points = [1.0, 2.0, 3.0, 4.0]
        isotropy_errors = []
        
        for r_test in r_test_points:
            # Interpolar valores en el radio de prueba
            if len(r_x) > 1 and len(r_y) > 1 and len(r_z) > 1:
                val_x = np.interp(r_test, r_x, profile_x)
                val_y = np.interp(r_test, r_y, profile_y)
                val_z = np.interp(r_test, r_z, profile_z)
                
                # Calcular diferencias relativas
                mean_val = (val_x + val_y + val_z) / 3
                if mean_val > 1e-10:
                    diff_xy = abs(val_x - val_y) / mean_val * 100
                    diff_xz = abs(val_x - val_z) / mean_val * 100
                    diff_yz = abs(val_y - val_z) / mean_val * 100
                    max_diff = max(diff_xy, diff_xz, diff_yz)
                    isotropy_errors.append(max_diff)
        
        isotropy_error_max = max(isotropy_errors) if isotropy_errors else 0
        
        print(f"✓ Test de isotropía completado")
        print(f"   Error máximo de isotropía: {isotropy_error_max:.3f}%")
        
        return {
            'profile_x': profile_x,
            'profile_y': profile_y, 
            'profile_z': profile_z,
            'r_x': r_x,
            'r_y': r_y,
            'r_z': r_z,
            'isotropy_errors': isotropy_errors,
            'isotropy_error_max': isotropy_error_max
        }
    
    def generate_scientific_plots(self, metric_theory, errors, isotropy):
        """Genera gráficos publication-ready para validación científica."""
        print("📈 Generando visualizaciones científicas...")
        
        # 1. Perfil radial: g_xx(r) simulado vs teórico
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Validación Científica: Métrica Emergente vs. Schwarzschild\n'
                    f'Resolución {self.resolution}³, M = {self.M}, t = {self.time_sim:.3f}', 
                    fontsize=16)
        
        # Perfil radial en el plano z=0
        center = self.resolution // 2
        r_profile = self.R[center:, center, center]
        gamma_xx_profile = self.gamma_xx[center:, center, center]
        theory_xx_profile = metric_theory['g_xx'][center:, center, center]
        
        # Máscara para región válida
        mask_profile = (r_profile >= self.r_min) & (r_profile <= self.r_max)
        
        axes[0,0].plot(r_profile[mask_profile], gamma_xx_profile[mask_profile], 
                      'b-', linewidth=2, label='Simulación', alpha=0.8)
        axes[0,0].plot(r_profile[mask_profile], theory_xx_profile[mask_profile], 
                      'r--', linewidth=2, label='Schwarzschild', alpha=0.8)
        axes[0,0].set_xlabel('Radio r')
        axes[0,0].set_ylabel('g_xx')
        axes[0,0].set_title('Perfil Radial: Componente g_xx')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. Mapa 2D: Contornos de g_xx en plano z=0
        x_slice = self.X[:, :, center]
        y_slice = self.Y[:, :, center]
        gamma_xx_slice = self.gamma_xx[:, :, center]
        
        contours = axes[0,1].contourf(x_slice, y_slice, gamma_xx_slice, 
                                     levels=20, cmap='viridis')
        plt.colorbar(contours, ax=axes[0,1])
        axes[0,1].set_xlabel('x')
        axes[0,1].set_ylabel('y') 
        axes[0,1].set_title('Mapa 2D: g_xx en plano z=0')
        axes[0,1].set_aspect('equal')
        
        # Añadir círculos de radio constante
        for r in [1, 2, 3, 4]:
            circle = Circle((0, 0), r, fill=False, color='white',
                           linestyle='--', alpha=0.6)
            axes[0,1].add_patch(circle)
        
        # 3. Test de isotropía
        if len(isotropy['r_x']) > 1:
            axes[1,0].plot(isotropy['r_x'], isotropy['profile_x'], 
                          'b-', label='Dirección X', linewidth=2)
            axes[1,0].plot(isotropy['r_y'], isotropy['profile_y'], 
                          'g-', label='Dirección Y', linewidth=2)
            axes[1,0].plot(isotropy['r_z'], isotropy['profile_z'], 
                          'r-', label='Dirección Z', linewidth=2)
            axes[1,0].set_xlabel('Radio r')
            axes[1,0].set_ylabel('Componente de métrica')
            axes[1,0].set_title(f'Test de Isotropía\nError máximo: {isotropy["isotropy_error_max"]:.3f}%')
            axes[1,0].legend()
            axes[1,0].grid(True, alpha=0.3)
        
        # 4. Error relativo vs radio
        error_profile = errors['rel_error_xx'][center:, center, center]
        axes[1,1].semilogy(r_profile[mask_profile], 
                          error_profile[mask_profile] * 100, 
                          'ko-', markersize=4, linewidth=1.5, alpha=0.7)
        axes[1,1].axhline(y=1.0, color='r', linestyle='--', 
                         label='Criterio 1%', alpha=0.8)
        axes[1,1].set_xlabel('Radio r')
        axes[1,1].set_ylabel('Error Relativo (%)')
        axes[1,1].set_title('Error Relativo vs. Radio')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar figura
        fig_path = self.results_dir / f'scientific_validation_{self.resolution}cubed.png'
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico guardado: {fig_path}")
        
        plt.show()
        
        return fig_path
    
    def evaluate_success_criteria(self, errors, isotropy):
        """Evalúa los criterios de éxito científicos definidos en el plan."""
        print("\n🎯 Evaluando criterios de éxito científicos...")
        print("=" * 50)
        
        # Criterios del plan original
        criterion_gxx_1pct = errors['stats']['rel_error_xx_rms'] < 1.0
        criterion_gyy_1pct = errors['stats']['rel_error_yy_mean'] < 1.0  
        criterion_isotropy = isotropy['isotropy_error_max'] < 0.1
        
        print(f"📊 RESULTADOS DE VALIDACIÓN:")
        print(f"   Error RMS en g_xx: {errors['stats']['rel_error_xx_rms']:.3f}% "
              f"{'✓' if criterion_gxx_1pct else '✗'} (<1%)")
        print(f"   Error medio en g_yy: {errors['stats']['rel_error_yy_mean']:.3f}% "
              f"{'✓' if criterion_gyy_1pct else '✗'} (<1%)")
        print(f"   Error de isotropía: {isotropy['isotropy_error_max']:.3f}% "
              f"{'✓' if criterion_isotropy else '✗'} (<0.1%)")
        
        # Evaluación global
        all_criteria_met = criterion_gxx_1pct and criterion_gyy_1pct and criterion_isotropy
        
        print(f"\n🏆 VEREDICTO CIENTÍFICO:")
        if all_criteria_met:
            print("   ✅ ÉXITO: La métrica emergente corresponde a Schwarzschild")
            print("   📋 Todos los criterios de validación han sido cumplidos")
        else:
            print("   ⚠️  PARCIAL: La métrica muestra características de Schwarzschild")
            print("   📋 Algunos criterios requieren refinamiento")
        
        return {
            'criterion_gxx_1pct': criterion_gxx_1pct,
            'criterion_gyy_1pct': criterion_gyy_1pct,
            'criterion_isotropy': criterion_isotropy,
            'all_criteria_met': all_criteria_met,
            'overall_success': all_criteria_met
        }
    
    def save_analysis_report(self, errors, isotropy, criteria):
        """Guarda reporte científico detallado."""
        report_path = self.results_dir / f'scientific_analysis_report_{self.resolution}cubed.txt'
        
        with open(report_path, 'w') as f:
            f.write("REPORTE DE ANÁLISIS CIENTÍFICO\n")
            f.write("=" * 50 + "\n")
            f.write(f"Fecha: {os.popen('date').read().strip()}\n")
            f.write(f"Simulación: {self.resolution}³ resolución\n")
            f.write(f"Masa partícula: M = {self.M}\n")
            f.write(f"Tiempo simulación: t = {self.time_sim:.3f}\n")
            f.write(f"Paso: {self.step}\n\n")
            
            f.write("PARÁMETROS DE ANÁLISIS\n")
            f.write("-" * 25 + "\n")
            f.write(f"Rango radial: {self.r_min} < r < {self.r_max}\n")
            f.write(f"Constante G: {self.G}\n\n")
            
            f.write("ERRORES CUANTITATIVOS\n")
            f.write("-" * 25 + "\n")
            f.write(f"Error RMS g_xx: {errors['stats']['rel_error_xx_rms']:.6f}%\n")
            f.write(f"Error máximo g_xx: {errors['stats']['rel_error_xx_max']:.6f}%\n")
            f.write(f"Error medio g_yy: {errors['stats']['rel_error_yy_mean']:.6f}%\n")
            f.write(f"Error medio g_zz: {errors['stats']['rel_error_zz_mean']:.6f}%\n\n")
            
            f.write("TEST DE ISOTROPÍA\n")
            f.write("-" * 25 + "\n")
            f.write(f"Error máximo isotropía: {isotropy['isotropy_error_max']:.6f}%\n\n")
            
            f.write("CRITERIOS DE VALIDACIÓN\n")
            f.write("-" * 25 + "\n")
            f.write(f"Error g_xx < 1%: {'✓' if criteria['criterion_gxx_1pct'] else '✗'}\n")
            f.write(f"Error g_yy < 1%: {'✓' if criteria['criterion_gyy_1pct'] else '✗'}\n")
            f.write(f"Isotropía < 0.1%: {'✓' if criteria['criterion_isotropy'] else '✗'}\n\n")
            
            f.write("CONCLUSIÓN CIENTÍFICA\n")
            f.write("-" * 25 + "\n")
            if criteria['overall_success']:
                f.write("✅ ÉXITO: La métrica emergente corresponde a Schwarzschild\n")
                f.write("Todos los criterios de validación científica han sido cumplidos.\n")
            else:
                f.write("⚠️ PARCIAL: La métrica muestra características de Schwarzschild\n")
                f.write("Algunos criterios requieren refinamiento o mayor resolución.\n")
        
        print(f"✓ Reporte guardado: {report_path}")
        return report_path
    
    def run_complete_analysis(self):
        """Ejecuta el análisis científico completo."""
        print("\n🚀 INICIANDO ANÁLISIS CIENTÍFICO COMPLETO")
        print("=" * 60)
        
        # Cargar datos de simulación
        self.load_simulation_data()
        
        # Calcular métrica teórica de Schwarzschild
        metric_theory = self.schwarzschild_metric_cartesian()
        
        # Calcular errores cuantitativos
        errors = self.calculate_errors(metric_theory)
        
        # Test de isotropía
        isotropy = self.test_isotropy()
        
        # Generar visualizaciones científicas
        self.generate_scientific_plots(metric_theory, errors, isotropy)
        
        # Evaluar criterios de éxito
        criteria = self.evaluate_success_criteria(errors, isotropy)
        
        # Guardar reporte
        self.save_analysis_report(errors, isotropy, criteria)
        
        print(f"\n🏁 ANÁLISIS CIENTÍFICO COMPLETADO")
        print(f"   Resultados guardados en: {self.results_dir}")
        
        return {
            'metric_theory': metric_theory,
            'errors': errors,
            'isotropy': isotropy,
            'criteria': criteria
        }

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Análisis científico de la emergencia de gravedad local",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python analyze_local_gravity_results.py --resolution 32
  python analyze_local_gravity_results.py --resolution 64 --mass 0.5
        """
    )
    
    parser.add_argument('--resolution', type=int, required=True,
                       choices=[32, 64, 128],
                       help='Resolución de la simulación a analizar')
    parser.add_argument('--mass', type=float, default=0.5,
                       help='Masa de la partícula (default: 0.5)')
    parser.add_argument('--G', type=float, default=1.0,
                       help='Constante gravitacional (default: 1.0)')
    
    args = parser.parse_args()
    
    # Ejecutar análisis
    analysis = SchwarzschildAnalysis(
        resolution=args.resolution,
        mass_particle=args.mass,
        G=args.G
    )
    
    results = analysis.run_complete_analysis()
    
    return results

if __name__ == "__main__":
    results = main()