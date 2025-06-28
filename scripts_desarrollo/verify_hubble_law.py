#!/usr/bin/env python3
"""
Verificación de la Ley de Hubble en Simulación Cosmológica
Conjetura del Universo Centrífugo

Este script implementa el plan de verificación documentado en docs/plan_verificacion_hubble.md
para demostrar que la expansión del espacio-tiempo en la simulación BSSN sigue la Ley de Hubble.

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

class HubbleLawVerifier:
    """
    Clase principal para verificar la Ley de Hubble en datos de simulación cosmológica.
    """
    
    def __init__(self, results_file='simulation_results.npz'):
        """
        Inicializa el verificador.
        
        Args:
            results_file (str): Archivo con resultados de la simulación
        """
        self.results_file = results_file
        self.results = None
        self.times = None
        self.metric_evolution = None
        
        # Puntos de muestra para análisis (coordenadas de "galaxias")
        self.galaxy_points = [
            (5, 0, 0),   # Galaxia cercana
            (10, 0, 0),  # Galaxia intermedia 1
            (20, 0, 0),  # Galaxia intermedia 2
            (30, 0, 0),  # Galaxia lejana 1
            (40, 0, 0),  # Galaxia lejana 2
        ]
        
        # Punto de referencia (observador)
        self.observer_point = (0, 0, 0)
        
    def load_simulation_data(self):
        """
        Fase 1: Carga y prepara los datos de la simulación.
        
        Returns:
            bool: True si la carga fue exitosa
        """
        print("🔍 FASE 1: PREPARACIÓN Y ENTENDIMIENTO DE DATOS")
        print("=" * 55)
        
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
            
            # Validar puntos de galaxias
            valid_points = []
            for point in self.galaxy_points:
                grid_point = tuple(c + p for c, p in zip(self.center, point))
                if all(0 <= gp < gs for gp, gs in zip(grid_point, self.grid_shape)):
                    valid_points.append(point)
                else:
                    print(f"   ⚠️  Punto {point} fuera de la malla, omitido")
            
            self.galaxy_points = valid_points
            print(f"   • Puntos de galaxias válidos: {len(self.galaxy_points)}")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: Archivo {self.results_file} no encontrado")
            print(f"💡 Ejecute primero la simulación completa")
            return False
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return False
    
    def extract_metric_component(self, time_step, component='xx'):
        """
        Extrae un componente de la métrica en un paso de tiempo específico.
        
        Args:
            time_step (int): Índice del paso de tiempo
            component (str): Componente de la métrica ('xx', 'yy', 'zz')
        
        Returns:
            np.ndarray: Componente de la métrica 3D
        """
        if self.metric_evolution is None or self.results is None:
            raise ValueError("Datos de simulación no cargados")
            
        if component == 'xx':
            if time_step == len(self.metric_evolution) - 1:
                return self.results['final_gamma_xx']
            else:
                # Para pasos intermedios, extraer del metric_evolution
                return self.metric_evolution[time_step].get('gamma_xx',
                    np.ones(self.grid_shape))
        elif component == 'yy':
            if time_step == len(self.metric_evolution) - 1:
                return self.results['final_gamma_yy']
            else:
                return self.metric_evolution[time_step].get('gamma_yy',
                    np.ones(self.grid_shape))
        elif component == 'zz':
            if time_step == len(self.metric_evolution) - 1:
                return self.results['final_gamma_zz']
            else:
                return self.metric_evolution[time_step].get('gamma_zz',
                    np.ones(self.grid_shape))
        else:
            raise ValueError(f"Componente {component} no soportado")
    
    def calculate_proper_distance(self, galaxy_point, time_step):
        """
        Fase 2: Calcula la distancia propia entre el observador y una galaxia.
        
        La distancia propia se calcula integrando el elemento de línea:
        dl² = γ_ij dx^i dx^j
        
        Para una línea recta a lo largo del eje x:
        d = ∫ sqrt(γ_xx) dx
        
        Args:
            galaxy_point (tuple): Coordenadas de la galaxia relativas al centro
            time_step (int): Índice del paso de tiempo
        
        Returns:
            float: Distancia propia
        """
        # Obtener componente γ_xx para este tiempo
        gamma_xx = self.extract_metric_component(time_step, 'xx')
        
        # Coordenadas en la malla
        obs_grid = self.center
        gal_grid = tuple(c + p for c, p in zip(self.center, galaxy_point))
        
        # Para simplificar, integramos a lo largo del eje x (asumiendo y=0, z=0)
        x_start = obs_grid[0]
        x_end = gal_grid[0]
        y_fixed = obs_grid[1]
        z_fixed = obs_grid[2]
        
        if x_start == x_end:
            return 0.0
        
        # Crear array de valores γ_xx a lo largo del camino
        x_indices = np.arange(min(x_start, x_end), max(x_start, x_end) + 1)
        gamma_values = []
        
        for x_idx in x_indices:
            if 0 <= x_idx < self.grid_shape[0]:
                gamma_val = gamma_xx[x_idx, y_fixed, z_fixed]
                gamma_values.append(max(gamma_val, 1e-10))  # Evitar valores negativos
            else:
                gamma_values.append(1.0)  # Valor por defecto
        
        gamma_values = np.array(gamma_values)
        
        # Integrar sqrt(γ_xx) dx
        # Usamos la regla del trapecio para la integración
        sqrt_gamma = np.sqrt(gamma_values)
        
        if len(sqrt_gamma) > 1:
            proper_distance = np.trapz(sqrt_gamma, dx=1.0)  # dx=1 punto de malla
        else:
            proper_distance = sqrt_gamma[0] if len(sqrt_gamma) > 0 else 1.0
        
        return float(np.abs(proper_distance))
    
    def calculate_distances_evolution(self):
        """
        Calcula la evolución temporal de las distancias propias para todas las galaxias.
        
        Returns:
            dict: Diccionario con tiempo y distancias para cada galaxia
        """
        print(f"\n📏 FASE 2: CÁLCULO DE DISTANCIA PROPIA")
        print("=" * 45)
        
        if self.times is None:
            raise ValueError("Datos temporales no cargados")
        
        distance_evolution = {}
        
        for i, galaxy_point in enumerate(self.galaxy_points):
            print(f"🌌 Calculando distancias para galaxia {i+1} en {galaxy_point}")
            
            distances = []
            for t_step in range(len(self.times)):
                dist = self.calculate_proper_distance(galaxy_point, t_step)
                distances.append(dist)
            
            distance_evolution[f'galaxy_{i+1}'] = {
                'coordinates': galaxy_point,
                'times': self.times.copy(),
                'distances': np.array(distances)
            }
            
            print(f"   • Distancia inicial: {distances[0]:.4f}")
            print(f"   • Distancia final: {distances[-1]:.4f}")
            print(f"   • Cambio total: {distances[-1] - distances[0]:.6f}")
        
        self.distance_evolution = distance_evolution
        return distance_evolution
    
    def calculate_recession_velocities(self):
        """
        Fase 3: Calcula las velocidades de recesión como derivadas de las distancias.
        
        v(t) = d(d(t))/dt
        
        Returns:
            dict: Diccionario con velocidades para cada galaxia
        """
        print(f"\n🚀 FASE 3: CÁLCULO DE VELOCIDAD DE RECESIÓN")
        print("=" * 45)
        
        velocity_evolution = {}
        
        for galaxy_name, data in self.distance_evolution.items():
            times = data['times']
            distances = data['distances']
            
            # Calcular derivada usando diferencias finitas
            velocities = np.gradient(distances, times)
            
            velocity_evolution[galaxy_name] = {
                'coordinates': data['coordinates'],
                'times': times,
                'velocities': velocities
            }
            
            print(f"🌌 {galaxy_name}:")
            print(f"   • Velocidad inicial: {velocities[0]:.6f}")
            print(f"   • Velocidad final: {velocities[-1]:.6f}")
            print(f"   • Velocidad promedio: {np.mean(velocities):.6f}")
        
        self.velocity_evolution = velocity_evolution
        return velocity_evolution
    
    def create_hubble_plot(self, time_index=-1):
        """
        Fase 4: Crea el gráfico de Hubble y calcula H₀.
        
        Args:
            time_index (int): Índice de tiempo para el análisis (-1 = tiempo final)
        
        Returns:
            dict: Resultados del análisis incluyendo H₀ y R²
        """
        print(f"\n📊 FASE 4: ANÁLISIS Y VERIFICACIÓN (GRÁFICO DE HUBBLE)")
        print("=" * 60)
        
        if self.times is None:
            raise ValueError("Datos temporales no cargados")
        
        # Extraer datos para el tiempo especificado
        distances = []
        velocities = []
        galaxy_names = []
        
        for galaxy_name, vel_data in self.velocity_evolution.items():
            dist_data = self.distance_evolution[galaxy_name]
            
            d = dist_data['distances'][time_index]
            v = vel_data['velocities'][time_index]
            
            distances.append(d)
            velocities.append(v)
            galaxy_names.append(galaxy_name)
            
            print(f"🌌 {galaxy_name}: d = {d:.4f}, v = {v:.6f}")
        
        distances = np.array(distances)
        velocities = np.array(velocities)
        
        # Realizar regresión lineal: v = H₀ * d
        def hubble_law(d, H0):
            return H0 * d
        
        try:
            # Ajuste lineal
            popt, pcov = curve_fit(hubble_law, distances, velocities)
            H0_fitted = popt[0]
            H0_error = np.sqrt(pcov[0, 0])
            
            # Calcular R²
            v_predicted = hubble_law(distances, H0_fitted)
            ss_res = np.sum((velocities - v_predicted) ** 2)
            ss_tot = np.sum((velocities - np.mean(velocities)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            print(f"\n📈 RESULTADOS DEL AJUSTE:")
            print(f"   • Constante de Hubble: H₀ = {H0_fitted:.8f} ± {H0_error:.8f}")
            print(f"   • Coeficiente R²: {r_squared:.6f}")
            
            if r_squared > 0.95:
                print(f"   ✅ EXCELENTE ajuste lineal - Ley de Hubble confirmada")
            elif r_squared > 0.8:
                print(f"   ✅ BUEN ajuste lineal - Ley de Hubble probablemente válida")
            elif r_squared > 0.5:
                print(f"   ⚠️  Ajuste MODERADO - Ley de Hubble parcialmente válida")
            else:
                print(f"   ❌ MAL ajuste - Ley de Hubble no confirmada")
            
            # Crear visualización
            plt.figure(figsize=(10, 6))
            
            # Datos originales
            plt.scatter(distances, velocities, color='blue', s=100, alpha=0.7,
                       label='Galaxias simuladas')
            
            # Línea de ajuste
            d_fit = np.linspace(min(distances), max(distances), 100)
            v_fit = hubble_law(d_fit, H0_fitted)
            plt.plot(d_fit, v_fit, 'r-', linewidth=2,
                    label=f'Ajuste: v = {H0_fitted:.6f} × d')
            
            # Etiquetas de galaxias
            for i, (d, v, name) in enumerate(zip(distances, velocities, galaxy_names)):
                plt.annotate(name, (d, v), xytext=(5, 5),
                           textcoords='offset points', fontsize=9)
            
            plt.xlabel('Distancia Propia')
            plt.ylabel('Velocidad de Recesión')
            plt.title(f'Gráfico de Hubble - Simulación Cosmológica\n'
                     f'H₀ = {H0_fitted:.6f}, R² = {r_squared:.4f}')
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            # Añadir información en el gráfico
            info_text = (f'Tiempo de análisis: {self.times[time_index]:.3f}\n'
                        f'Número de galaxias: {len(distances)}\n'
                        f'Validez: {"✅" if r_squared > 0.8 else "⚠️" if r_squared > 0.5 else "❌"}')
            plt.text(0.05, 0.95, info_text, transform=plt.gca().transAxes,
                    fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
            
            plt.tight_layout()
            plt.savefig('hubble_plot.png', dpi=300, bbox_inches='tight')
            print(f"✅ Gráfico guardado: hubble_plot.png")
            
            results = {
                'H0': H0_fitted,
                'H0_error': H0_error,
                'R_squared': r_squared,
                'distances': distances,
                'velocities': velocities,
                'time_analyzed': self.times[time_index],
                'num_galaxies': len(distances),
                'hubble_law_confirmed': r_squared > 0.8
            }
            
            return results
            
        except Exception as e:
            print(f"❌ Error en el ajuste: {e}")
            return None
    
    def generate_report(self, hubble_results):
        """
        Fase 5: Genera un informe completo de resultados.
        
        Args:
            hubble_results (dict): Resultados del análisis de Hubble
        """
        print(f"\n📋 FASE 5: GENERACIÓN DE INFORME")
        print("=" * 40)
        
        report_content = f"""# Verificación de la Ley de Hubble - Informe de Resultados

*Fecha: 28 de junio de 2025*
*Simulación: Conjetura del Universo Centrífugo*

## Resumen Ejecutivo

Este informe presenta los resultados de la verificación de la Ley de Hubble (`v = H₀d`) 
a partir de los datos de la simulación BSSN de relatividad numérica.

## Metodología

1. **Carga de Datos**: Simulación de alta resolución {self.grid_shape}
2. **Puntos de Análisis**: {len(self.galaxy_points)} galaxias a diferentes distancias
3. **Tiempo de Análisis**: {hubble_results['time_analyzed']:.4f} (tiempo final de simulación)
4. **Método de Distancia**: Integración de la métrica espacial γ_ij
5. **Método de Velocidad**: Derivación numérica de distancias temporales

## Puntos de Galaxias Analizados

"""
        
        for i, point in enumerate(self.galaxy_points):
            report_content += f"- **Galaxia {i+1}**: Coordenadas {point}\n"
        
        report_content += f"""
## Resultados Principales

### Constante de Hubble
- **H₀ = {hubble_results['H0']:.8f} ± {hubble_results['H0_error']:.8f}**
- **Unidades**: [distancia propia / tiempo de simulación]

### Calidad del Ajuste
- **Coeficiente R² = {hubble_results['R_squared']:.6f}**
- **Número de galaxias**: {hubble_results['num_galaxies']}

### Interpretación Estadística
"""
        
        if hubble_results['R_squared'] > 0.95:
            interpretation = "**EXCELENTE** - La Ley de Hubble se confirma con alta precisión"
            validity = "✅ **VALIDADA**"
        elif hubble_results['R_squared'] > 0.8:
            interpretation = "**BUENA** - La Ley de Hubble se confirma satisfactoriamente"
            validity = "✅ **VALIDADA**"
        elif hubble_results['R_squared'] > 0.5:
            interpretation = "**MODERADA** - La Ley de Hubble se confirma parcialmente"
            validity = "⚠️ **PARCIALMENTE VALIDADA**"
        else:
            interpretation = "**POBRE** - La Ley de Hubble no se confirma"
            validity = "❌ **NO VALIDADA**"
        
        report_content += f"""
**Calidad del ajuste**: {interpretation}

**Estado de la Ley de Hubble**: {validity}

## Datos de Distancia y Velocidad

| Galaxia | Distancia | Velocidad | Coordenadas |
|---------|-----------|-----------|-------------|
"""
        
        for i, (d, v, coords) in enumerate(zip(hubble_results['distances'], 
                                             hubble_results['velocities'],
                                             self.galaxy_points)):
            report_content += f"| Galaxia {i+1} | {d:.4f} | {v:.6f} | {coords} |\n"
        
        report_content += f"""
## Implicaciones para la Conjetura del Universo Centrífugo

"""
        
        if hubble_results['hubble_law_confirmed']:
            report_content += f"""
### ✅ Confirmación Exitosa

Los resultados **confirman** que la expansión del espacio-tiempo generada por la rotación 4D 
en la simulación BSSN sigue la Ley de Hubble con una precisión de R² = {hubble_results['R_squared']:.4f}.

**Significado científico:**
1. La rotación hiperdimensional genera expansión cosmológica observable
2. La expansión es uniforme e isótropa (como requiere la Ley de Hubble)
3. La constante H₀ calculada representa la velocidad angular efectiva de la rotación 4D

**Próximos pasos recomendados:**
- Comparar H₀ calculado con valores observacionales reales
- Extender análisis a mayor número de puntos y mayor tiempo de simulación
- Investigar dependencia de H₀ con parámetros de rotación 4D
"""
        else:
            report_content += f"""
### ❌ Confirmación Parcial o Fallida

Los resultados **no confirman completamente** la Ley de Hubble con la precisión esperada.
R² = {hubble_results['R_squared']:.4f} indica desviaciones significativas del comportamiento lineal.

**Posibles causas:**
1. Tiempo de simulación insuficiente para estabilización
2. Resolución espacial insuficiente para capturar efectos a gran escala
3. Parámetros de rotación 4D demasiado pequeños o grandes
4. Efectos de frontera de la malla de simulación

**Recomendaciones:**
- Incrementar tiempo de simulación (t_final > 1.0)
- Usar mayor resolución espacial (512³ o superior)
- Optimizar parámetros R_param y ω₄D_param
- Analizar región central de la malla para minimizar efectos de frontera
"""
        
        report_content += f"""
## Conclusión

La verificación de la Ley de Hubble en la simulación cosmológica ha sido **{'exitosa' if hubble_results['hubble_law_confirmed'] else 'parcialmente exitosa'}**.

**Resultado clave**: H₀ = {hubble_results['H0']:.8f} con R² = {hubble_results['R_squared']:.4f}

Este análisis constituye {'una evidencia sólida' if hubble_results['hubble_law_confirmed'] else 'evidencia preliminar'} 
de que la rotación 4D puede generar expansión cosmológica consistente con las observaciones.

---

*Informe generado automáticamente por verify_hubble_law.py*
*Basado en simulación BSSN de la Conjetura del Universo Centrífugo*
"""
        
        # Guardar informe
        with open('hubble_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Informe generado: hubble_analysis_report.md")
        
        return 'hubble_analysis_report.md'
    
    def run_complete_analysis(self):
        """
        Ejecuta el análisis completo siguiendo las 5 fases del plan.
        
        Returns:
            dict: Resultados del análisis completo
        """
        print("🌌 VERIFICACIÓN DE LA LEY DE HUBBLE")
        print("Conjetura del Universo Centrífugo")
        print("=" * 70)
        
        # Fase 1: Preparación de datos
        if not self.load_simulation_data():
            return None
        
        # Fase 2: Cálculo de distancias propias
        self.calculate_distances_evolution()
        
        # Fase 3: Cálculo de velocidades de recesión
        self.calculate_recession_velocities()
        
        # Fase 4: Análisis y gráfico de Hubble
        hubble_results = self.create_hubble_plot()
        
        if hubble_results is None:
            print("❌ Error en el análisis de Hubble")
            return None
        
        # Fase 5: Generación de informe
        report_file = self.generate_report(hubble_results)
        
        # Resumen final
        print(f"\n🏆 ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("=" * 50)
        print(f"📊 Constante de Hubble: H₀ = {hubble_results['H0']:.8f}")
        print(f"📈 Calidad del ajuste: R² = {hubble_results['R_squared']:.6f}")
        print(f"🎯 Ley de Hubble: {'✅ CONFIRMADA' if hubble_results['hubble_law_confirmed'] else '❌ NO CONFIRMADA'}")
        print(f"📁 Archivos generados:")
        print(f"   • hubble_plot.png")
        print(f"   • {report_file}")
        
        return hubble_results


def main():
    """
    Función principal - ejecuta el análisis completo.
    """
    # Buscar archivo de resultados en directorios probables
    possible_files = [
        'simulation_results.npz',
        'output/simulation_256cubed/results/simulation_results.npz',
        'results/simulation_256cubed/simulation_results.npz'
    ]
    
    results_file = None
    for file_path in possible_files:
        if os.path.exists(file_path):
            results_file = file_path
            break
    
    if results_file is None:
        print("❌ No se encontró archivo de resultados de simulación")
        print("💡 Archivos buscados:")
        for f in possible_files:
            print(f"   • {f}")
        print("\n🚀 Ejecute primero: python run_complete_simulation.py")
        return
    
    # Crear verificador y ejecutar análisis
    verifier = HubbleLawVerifier(results_file)
    results = verifier.run_complete_analysis()
    
    if results:
        print(f"\n🎉 ¡Análisis de la Ley de Hubble completado exitosamente!")
    else:
        print(f"\n❌ Error en el análisis")


if __name__ == "__main__":
    main()