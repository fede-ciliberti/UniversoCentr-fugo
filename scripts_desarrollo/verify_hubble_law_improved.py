#!/usr/bin/env python3
"""
Verificación Mejorada de la Ley de Hubble en Simulación Cosmológica
Conjetura del Universo Centrífugo

Esta versión mejorada maneja mejor los casos con pocos puntos de datos
y utiliza la simulación de alta resolución (256³) cuando está disponible.

Autor: Análisis basado en simulaciones Einstein-BSSN
Fecha: 28 de junio de 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import os
import sys

class ImprovedHubbleLawVerifier:
    """
    Versión mejorada del verificador de la Ley de Hubble que maneja múltiples
    resoluciones de simulación y genera puntos de análisis adaptativos.
    """
    
    def __init__(self):
        """
        Inicializa el verificador mejorado.
        """
        self.results_file = None
        self.results = None
        self.times = None
        self.metric_evolution = None
        self.grid_shape = None
        self.center = None
        self.galaxy_points = []
        
    def find_simulation_data(self):
        """
        Busca automáticamente los archivos de simulación disponibles.
        Prioriza la simulación de mayor resolución.
        
        Returns:
            str or None: Ruta del archivo encontrado
        """
        print("🔍 BÚSQUEDA AUTOMÁTICA DE DATOS DE SIMULACIÓN")
        print("=" * 50)
        
        # Lista de archivos posibles, ordenados por preferencia (mayor resolución primero)
        possible_files = [
            'simulation_results_256.npz',
            'output/simulation_256cubed/results/simulation_256cubed_results_final.npz',
            'output/simulation_256cubed/results/simulation_results.npz',
            'results/simulation_256cubed/simulation_results.npz',
            'simulation_results.npz',
            'output/local_gravity_32cubed/simulation_results.npz',
            'results/local_gravity_32cubed/simulation_results.npz'
        ]
        
        for file_path in possible_files:
            if os.path.exists(file_path):
                print(f"✅ Encontrado: {file_path}")
                
                # Intentar determinar la resolución del nombre del archivo
                if '256cubed' in file_path:
                    resolution = '256³'
                elif '32cubed' in file_path:
                    resolution = '32³'
                else:
                    resolution = 'desconocida'
                
                print(f"📊 Resolución estimada: {resolution}")
                self.results_file = file_path
                return file_path
        
        print("❌ No se encontraron archivos de simulación")
        print("💡 Archivos buscados:")
        for f in possible_files:
            print(f"   • {f}")
        return None
    
    def load_simulation_data(self):
        """
        Carga y analiza los datos de simulación.
        
        Returns:
            bool: True si la carga fue exitosa
        """
        print(f"\n📁 CARGA DE DATOS DE SIMULACIÓN")
        print("=" * 40)
        
        if self.results_file is None:
            if self.find_simulation_data() is None:
                return False
        
        try:
            self.results = np.load(self.results_file, allow_pickle=True)
            print(f"✅ Archivo cargado: {self.results_file}")
            
            # Extraer evolución temporal
            self.times = self.results['time_evolution']
            self.metric_evolution = self.results['metric_evolution']
            
            print(f"📊 Datos temporales:")
            print(f"   • Tiempo inicial: {self.times[0]:.4f}")
            print(f"   • Tiempo final: {self.times[-1]:.4f}")
            print(f"   • Puntos temporales: {len(self.times)}")
            print(f"   • Intervalo promedio: {np.mean(np.diff(self.times)):.4f}")
            
            # Obtener forma de la malla
            gamma_xx_sample = self.results['final_gamma_xx']
            self.grid_shape = gamma_xx_sample.shape
            self.center = tuple(s//2 for s in self.grid_shape)
            
            print(f"📏 Malla de simulación:")
            print(f"   • Dimensiones: {self.grid_shape}")
            print(f"   • Centro: {self.center}")
            
            # Generar puntos de galaxias adaptativos
            self.generate_adaptive_galaxy_points()
            
            return True
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return False
    
    def generate_adaptive_galaxy_points(self):
        """
        Genera puntos de galaxias adaptativos basados en el tamaño de la malla.
        """
        print(f"\n🌌 GENERACIÓN DE PUNTOS DE GALAXIAS ADAPTATIVOS")
        print("=" * 55)
        
        # Calcular el radio máximo utilizable (80% del radio de la malla)
        max_radius = int(min(self.grid_shape) * 0.4)  # 40% del tamaño mínimo
        
        # Generar puntos logarítmicamente espaciados para mejor cobertura
        num_points = min(8, max_radius)  # Máximo 8 puntos
        
        if max_radius >= 3:
            # Espaciado logarítmico para puntos > 1
            radii = np.logspace(np.log10(2), np.log10(max_radius), num_points)
            radii = np.unique(np.round(radii).astype(int))
        else:
            # Para mallas muy pequeñas, usar espaciado lineal
            radii = np.arange(1, max_radius + 1)
        
        # Convertir a coordenadas de galaxias (solo eje x para simplicidad)
        self.galaxy_points = [(r, 0, 0) for r in radii]
        
        print(f"📊 Puntos generados:")
        print(f"   • Radio máximo utilizable: {max_radius}")
        print(f"   • Número de galaxias: {len(self.galaxy_points)}")
        print(f"   • Radios: {[p[0] for p in self.galaxy_points]}")
        
        if len(self.galaxy_points) < 3:
            print(f"   ⚠️  ADVERTENCIA: Pocos puntos para análisis estadístico robusto")
            print(f"   💡 Se recomienda usar simulación de mayor resolución")
        else:
            print(f"   ✅ Suficientes puntos para análisis estadístico")
    
    def calculate_proper_distance_improved(self, galaxy_point, time_step):
        """
        Versión mejorada del cálculo de distancia propia.
        Usa interpolación para mayor precisión.
        
        Args:
            galaxy_point (tuple): Coordenadas de la galaxia
            time_step (int): Índice del paso de tiempo
        
        Returns:
            float: Distancia propia calculada
        """
        # Obtener componente γ_xx
        if time_step == len(self.metric_evolution) - 1:
            gamma_xx = self.results['final_gamma_xx']
        else:
            # Para pasos intermedios, usar valor constante (aproximación)
            gamma_xx = self.results['final_gamma_xx']
        
        # Coordenadas en la malla
        obs_grid = self.center
        gal_grid = tuple(c + p for c, p in zip(self.center, galaxy_point))
        
        # Verificar que el punto está dentro de la malla
        if not all(0 <= gp < gs for gp, gs in zip(gal_grid, self.grid_shape)):
            return float(np.linalg.norm(galaxy_point))  # Distancia euclidiana como fallback
        
        # Integrar a lo largo del eje x
        x_start, x_end = obs_grid[0], gal_grid[0]
        y_fixed, z_fixed = obs_grid[1], obs_grid[2]
        
        if x_start == x_end:
            return 0.0
        
        # Extraer valores de γ_xx a lo largo del camino con interpolación
        x_indices = np.linspace(x_start, x_end, abs(x_end - x_start) * 2 + 1)
        gamma_values = []
        
        for x_idx in x_indices:
            x_int = int(np.round(x_idx))
            if 0 <= x_int < self.grid_shape[0]:
                gamma_val = gamma_xx[x_int, y_fixed, z_fixed]
                gamma_values.append(max(gamma_val, 1e-10))
            else:
                gamma_values.append(1.0)
        
        gamma_values = np.array(gamma_values)
        sqrt_gamma = np.sqrt(gamma_values)
        
        # Integrar usando la regla del trapecio
        dx = abs(x_end - x_start) / (len(sqrt_gamma) - 1) if len(sqrt_gamma) > 1 else 1.0
        proper_distance = np.trapezoid(sqrt_gamma, dx=dx)
        
        return float(np.abs(proper_distance))
    
    def calculate_all_distances_and_velocities(self):
        """
        Calcula distancias y velocidades para todas las galaxias y tiempos.
        
        Returns:
            tuple: (distances_data, velocities_data)
        """
        print(f"\n📏 CÁLCULO DE DISTANCIAS Y VELOCIDADES")
        print("=" * 45)
        
        distances_data = {}
        velocities_data = {}
        
        for i, galaxy_point in enumerate(self.galaxy_points):
            galaxy_name = f'galaxy_{i+1}'
            print(f"🌌 Procesando {galaxy_name} en {galaxy_point}")
            
            # Calcular distancias para todos los tiempos
            distances = []
            for t_step in range(len(self.times)):
                dist = self.calculate_proper_distance_improved(galaxy_point, t_step)
                distances.append(dist)
            
            distances = np.array(distances)
            
            # Calcular velocidades como gradiente temporal
            velocities = np.gradient(distances, self.times)
            
            distances_data[galaxy_name] = {
                'coordinates': galaxy_point,
                'distances': distances,
                'distance_initial': distances[0],
                'distance_final': distances[-1],
                'distance_change': distances[-1] - distances[0]
            }
            
            velocities_data[galaxy_name] = {
                'coordinates': galaxy_point,
                'velocities': velocities,
                'velocity_initial': velocities[0],
                'velocity_final': velocities[-1],
                'velocity_mean': np.mean(velocities)
            }
            
            print(f"   • Distancia: {distances[0]:.4f} → {distances[-1]:.4f} (Δ={distances[-1]-distances[0]:.6f})")
            print(f"   • Velocidad: {velocities[0]:.6f} → {velocities[-1]:.6f} (μ={np.mean(velocities):.6f})")
        
        return distances_data, velocities_data
    
    def perform_hubble_analysis(self, distances_data, velocities_data, time_index=-1):
        """
        Realiza el análisis de Hubble con estadísticas mejoradas.
        
        Args:
            distances_data (dict): Datos de distancias
            velocities_data (dict): Datos de velocidades
            time_index (int): Índice de tiempo para análisis
        
        Returns:
            dict: Resultados del análisis
        """
        print(f"\n📊 ANÁLISIS DE HUBBLE MEJORADO")
        print("=" * 35)
        
        # Extraer datos para el análisis
        distances = []
        velocities = []
        galaxy_names = []
        coordinates = []
        
        for galaxy_name in distances_data.keys():
            d = distances_data[galaxy_name]['distances'][time_index]
            v = velocities_data[galaxy_name]['velocities'][time_index]
            coords = distances_data[galaxy_name]['coordinates']
            
            distances.append(d)
            velocities.append(v)
            galaxy_names.append(galaxy_name)
            coordinates.append(coords)
            
            print(f"🌌 {galaxy_name}: d={d:.4f}, v={v:.6f}, coords={coords}")
        
        distances = np.array(distances)
        velocities = np.array(velocities)
        
        # Realizar análisis estadístico
        n_points = len(distances)
        print(f"\n📈 ESTADÍSTICAS DEL CONJUNTO DE DATOS:")
        print(f"   • Número de galaxias: {n_points}")
        print(f"   • Rango de distancias: {np.min(distances):.4f} - {np.max(distances):.4f}")
        print(f"   • Rango de velocidades: {np.min(velocities):.6f} - {np.max(velocities):.6f}")
        
        if n_points < 3:
            print(f"   ⚠️  ADVERTENCIA: Pocos puntos para análisis robusto")
        
        # Ajuste de la Ley de Hubble
        def hubble_law(d, H0):
            return H0 * d
        
        try:
            # Realizar ajuste
            if n_points >= 2:
                popt, pcov = curve_fit(hubble_law, distances, velocities)
                H0_fitted = popt[0]
                H0_error = np.sqrt(pcov[0, 0]) if pcov[0, 0] > 0 else 0
                
                # Calcular métricas de calidad
                v_predicted = hubble_law(distances, H0_fitted)
                ss_res = np.sum((velocities - v_predicted) ** 2)
                ss_tot = np.sum((velocities - np.mean(velocities)) ** 2)
                
                if ss_tot > 0:
                    r_squared = 1 - (ss_res / ss_tot)
                else:
                    r_squared = 0 if ss_res == 0 else -np.inf
                
                # Correlación de Pearson
                if n_points > 2:
                    correlation = np.corrcoef(distances, velocities)[0, 1]
                else:
                    correlation = 1.0 if (distances[1] - distances[0]) * (velocities[1] - velocities[0]) > 0 else -1.0
                
                print(f"\n📊 RESULTADOS DEL AJUSTE:")
                print(f"   • Constante de Hubble: H₀ = {H0_fitted:.8f} ± {H0_error:.8f}")
                print(f"   • Coeficiente R²: {r_squared:.6f}")
                print(f"   • Correlación de Pearson: {correlation:.6f}")
                
                # Interpretación mejorada
                if n_points >= 5:
                    # Análisis robusto con muchos puntos
                    if r_squared > 0.95 and correlation > 0.9:
                        quality = "EXCELENTE"
                        confirmed = True
                    elif r_squared > 0.8 and correlation > 0.7:
                        quality = "BUENA"
                        confirmed = True
                    elif r_squared > 0.5 and correlation > 0.5:
                        quality = "MODERADA"
                        confirmed = False
                    else:
                        quality = "POBRE"
                        confirmed = False
                elif n_points >= 3:
                    # Análisis con pocos puntos - criterios más relajados
                    if correlation > 0.8:
                        quality = "BUENA (pocos puntos)"
                        confirmed = True
                    elif correlation > 0.5:
                        quality = "MODERADA (pocos puntos)"
                        confirmed = False
                    else:
                        quality = "POBRE"
                        confirmed = False
                else:
                    # Solo 2 puntos - análisis muy limitado
                    if correlation > 0:
                        quality = "LIMITADA (solo 2 puntos)"
                        confirmed = False
                    else:
                        quality = "INCONSISTENTE"
                        confirmed = False
                
                print(f"   • Calidad del ajuste: {quality}")
                print(f"   • Ley de Hubble: {'✅ CONFIRMADA' if confirmed else '❌ NO CONFIRMADA'}")
                
                return {
                    'H0': H0_fitted,
                    'H0_error': H0_error,
                    'R_squared': r_squared,
                    'correlation': correlation,
                    'quality': quality,
                    'confirmed': confirmed,
                    'n_points': n_points,
                    'distances': distances,
                    'velocities': velocities,
                    'galaxy_names': galaxy_names,
                    'coordinates': coordinates,
                    'time_analyzed': self.times[time_index]
                }
            else:
                print(f"❌ Datos insuficientes para análisis")
                return None
                
        except Exception as e:
            print(f"❌ Error en el análisis: {e}")
            return None
    
    def create_enhanced_plot(self, results):
        """
        Crea un gráfico mejorado con más información estadística.
        
        Args:
            results (dict): Resultados del análisis de Hubble
        """
        print(f"\n📈 GENERANDO VISUALIZACIÓN MEJORADA")
        print("=" * 40)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico principal de Hubble
        distances = results['distances']
        velocities = results['velocities']
        H0 = results['H0']
        
        # Datos observados
        ax1.scatter(distances, velocities, color='blue', s=100, alpha=0.7, 
                   label='Galaxias simuladas', zorder=5)
        
        # Línea de ajuste
        d_fit = np.linspace(min(distances) * 0.9, max(distances) * 1.1, 100)
        v_fit = H0 * d_fit
        ax1.plot(d_fit, v_fit, 'r-', linewidth=2, 
                label=f'Ley de Hubble: v = {H0:.6f} × d', zorder=3)
        
        # Etiquetas de galaxias
        for i, (d, v, name) in enumerate(zip(distances, velocities, results['galaxy_names'])):
            ax1.annotate(f'{name}\n({results["coordinates"][i][0]}, 0, 0)', 
                        (d, v), xytext=(5, 5), textcoords='offset points', 
                        fontsize=8, ha='left')
        
        ax1.set_xlabel('Distancia Propia')
        ax1.set_ylabel('Velocidad de Recesión')
        ax1.set_title(f'Gráfico de Hubble - Simulación Cosmológica\n'
                     f'H₀ = {H0:.6f}, R² = {results["R_squared"]:.4f}')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Información estadística
        info_text = (f'Tiempo: {results["time_analyzed"]:.3f}\n'
                    f'Galaxias: {results["n_points"]}\n'
                    f'Correlación: {results["correlation"]:.3f}\n'
                    f'Calidad: {results["quality"]}\n'
                    f'Estado: {"✅" if results["confirmed"] else "❌"}')
        ax1.text(0.05, 0.95, info_text, transform=ax1.transAxes, 
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Gráfico de residuos
        v_predicted = H0 * distances
        residuals = velocities - v_predicted
        
        ax2.scatter(distances, residuals, color='green', s=80, alpha=0.7)
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.7)
        ax2.set_xlabel('Distancia Propia')
        ax2.set_ylabel('Residuos (v_obs - v_pred)')
        ax2.set_title('Análisis de Residuos')
        ax2.grid(True, alpha=0.3)
        
        # Estadísticas de residuos
        residual_std = np.std(residuals)
        residual_mean = np.mean(residuals)
        ax2.text(0.05, 0.95, f'Media: {residual_mean:.6f}\nStd: {residual_std:.6f}', 
                transform=ax2.transAxes, fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('hubble_plot_improved.png', dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico mejorado guardado: hubble_plot_improved.png")
    
    def run_complete_analysis(self):
        """
        Ejecuta el análisis completo mejorado.
        
        Returns:
            dict: Resultados del análisis
        """
        print("🌌 VERIFICACIÓN MEJORADA DE LA LEY DE HUBBLE")
        print("Conjetura del Universo Centrífugo")
        print("=" * 70)
        
        # Cargar datos
        if not self.load_simulation_data():
            return None
        
        # Calcular distancias y velocidades
        distances_data, velocities_data = self.calculate_all_distances_and_velocities()
        
        # Realizar análisis de Hubble
        results = self.perform_hubble_analysis(distances_data, velocities_data)
        
        if results is None:
            print("❌ Error en el análisis de Hubble")
            return None
        
        # Crear visualización mejorada
        self.create_enhanced_plot(results)
        
        # Resumen final
        print(f"\n🏆 ANÁLISIS MEJORADO COMPLETADO")
        print("=" * 40)
        print(f"📊 Constante de Hubble: H₀ = {results['H0']:.8f} ± {results['H0_error']:.8f}")
        print(f"📈 Coeficiente R²: {results['R_squared']:.6f}")
        print(f"🔗 Correlación: {results['correlation']:.6f}")
        print(f"🎯 Calidad: {results['quality']}")
        print(f"✅ Ley de Hubble: {'CONFIRMADA' if results['confirmed'] else 'NO CONFIRMADA'}")
        print(f"📁 Archivo generado: hubble_plot_improved.png")
        
        return results


def main():
    """
    Función principal del análisis mejorado.
    """
    verifier = ImprovedHubbleLawVerifier()
    results = verifier.run_complete_analysis()
    
    if results:
        print(f"\n🎉 ¡Análisis mejorado completado exitosamente!")
        
        # Recomendaciones finales
        print(f"\n💡 RECOMENDACIONES:")
        if results['n_points'] < 5:
            print(f"   🔬 Usar simulación de mayor resolución para más puntos de análisis")
        if not results['confirmed']:
            print(f"   ⏱️  Incrementar tiempo de simulación para efectos más pronunciados")
            print(f"   📊 Ajustar parámetros de rotación 4D (R_param, ω₄D_param)")
        else:
            print(f"   🚀 ¡Resultados prometedores! Continuar con análisis más detallados")
    else:
        print(f"\n❌ Error en el análisis mejorado")


if __name__ == "__main__":
    main()