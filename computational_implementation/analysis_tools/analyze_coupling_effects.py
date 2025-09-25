#!/usr/bin/env python3
"""
Análisis de Efectos de Acoplamiento Local-Global
Tarea 2.1.3: Análisis de Efectos de Acoplamiento

Este script cuantifica la interacción entre la gravedad local (de una masa
puntual) y la expansión cosmológica de fondo. Compara una simulación con
masa local contra una simulación de control (solo expansión) para
identificar y medir los efectos de acoplamiento.

Entregable:
- Un archivo de dataset `acoplamiento_local_global.npz` con los resultados
  cuantitativos del análisis.
"""

import numpy as np
import argparse
import os
import sys
import time

# Añadir la ruta de las simulaciones para poder importar las clases
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'simulations')))

try:
    from run_local_gravity_simulation import LocalGravitySimulation
    from run_numerical_simulation import EinsteinSimulator
except ImportError as e:
    print(f"Error al importar módulos de simulación: {e}", file=sys.stderr)
    print("Asegúrese de que el script se ejecuta desde el directorio raíz o que las rutas son correctas.", file=sys.stderr)
    sys.exit(1)

class CouplingAnalyzer(LocalGravitySimulation):
    """
    Analiza los efectos de acoplamiento extendiendo la simulación de gravedad local.
    """
    def __init__(self, data_file, local_mass_params, control_sim_results_path=None):
        print("🔬 Inicializando Coupling Analyzer...")
        super().__init__(data_file=data_file, local_mass_params=local_mass_params)
        self.control_sim_results = self.load_control_results(control_sim_results_path)
        print("✓ Coupling Analyzer inicializado.")

    def load_control_results(self, path):
        """Carga los resultados de la simulación de control (sin masa local)."""
        if path and os.path.exists(path):
            print(f"Cargando resultados de la simulación de control desde {path}...")
            return np.load(path, allow_pickle=True)
        print("⚠️  No se proporcionaron resultados de la simulación de control. El análisis diferencial será limitado.")
        return None

    def analyze_superposition_results(self, output_file):
        """
        Sobrescribe el método de la clase base para realizar el análisis de acoplamiento.
        Este es el núcleo de la Tarea 2.1.3.
        """
        print("\n🔬 INICIANDO ANÁLISIS DE ACOPLAMIENTO LOCAL-GLOBAL")
        print("-" * 50)

        # 1. Cuantificar interacciones: Comparar métricas con la simulación de control
        coupling_effects = {}
        if self.control_sim_results:
            print("1. Cuantificando interacciones vs. simulación de control...")
            # Comparar el determinante de la métrica final
            det_gamma_final_local = self.gamma_xx * self.gamma_yy * self.gamma_zz
            det_gamma_final_control = self.control_sim_results['final_gamma_xx'] * \
                                      self.control_sim_results['final_gamma_yy'] * \
                                      self.control_sim_results['final_gamma_zz']
            
            # El efecto de acoplamiento es la diferencia
            metric_difference = det_gamma_final_local - det_gamma_final_control
            coupling_effects['metric_determinant_difference'] = metric_difference
            
            # Calcular la norma de la diferencia para un valor escalar
            coupling_norm = np.linalg.norm(metric_difference)
            print(f"   - Norma de la diferencia en det(γ): {coupling_norm:.4e}")
            coupling_effects['metric_determinant_difference_norm'] = coupling_norm
        else:
            print("1. Omitiendo análisis diferencial (no hay datos de control).")

        # 2. Identificar correcciones a la ley de Hubble
        print("\n2. Identificando correcciones a la Ley de Hubble...")
        # Esto es una aproximación. Medimos la "expansión" localmente.
        # La expansión se manifiesta como un aumento en det(γ)
        det_gamma_initial = np.ones(self.grid_shape) # Asumiendo que empieza en 1
        det_gamma_final = self.gamma_xx * self.gamma_yy * self.gamma_zz
        
        # Mapa de la tasa de expansión local
        local_expansion_rate = (det_gamma_final - det_gamma_initial) / self.t_final
        coupling_effects['local_expansion_rate_map'] = local_expansion_rate
        
        # Analizar la expansión cerca y lejos de la masa
        center_idx = (self.nx // 2, self.ny // 2, self.nz // 2)
        radius_pixels = int(self.local_mass_params['smoothing_radius'] / self.dx)
        
        mask_near = np.zeros(self.grid_shape, dtype=bool)
        mask_near[center_idx[0]-radius_pixels:center_idx[0]+radius_pixels,
                  center_idx[1]-radius_pixels:center_idx[1]+radius_pixels,
                  center_idx[2]-radius_pixels:center_idx[2]+radius_pixels] = True

        avg_expansion_near = np.mean(local_expansion_rate[mask_near])
        avg_expansion_far = np.mean(local_expansion_rate[~mask_near])
        
        print(f"   - Tasa de expansión promedio (cerca de la masa): {avg_expansion_near:.4e}")
        print(f"   - Tasa de expansión promedio (lejos de la masa): {avg_expansion_far:.4e}")
        
        hubble_correction_factor = avg_expansion_near / avg_expansion_far if avg_expansion_far != 0 else 0
        print(f"   - Factor de corrección de Hubble (cerca/lejos): {hubble_correction_factor:.4f}")
        
        coupling_effects['hubble_correction'] = {
            'avg_expansion_near_mass': avg_expansion_near,
            'avg_expansion_far_mass': avg_expansion_far,
            'correction_factor': hubble_correction_factor
        }

        # 3. Evaluar implicaciones para observaciones galácticas (guardar datos para análisis posterior)
        print("\n3. Guardando datos para evaluación de implicaciones galácticas...")
        # Guardamos los mapas de corrección. El análisis cualitativo se hará en el paper.
        
        # Guardar los resultados del análisis
        self.save_analysis_results(output_file, coupling_effects)

    def save_analysis_results(self, output_file, analysis_data):
        """Guarda los resultados del análisis de acoplamiento en un archivo .npz."""
        print(f"\n💾 Guardando resultados del análisis de acoplamiento en: {output_file}")
        
        # Obtener resultados de la simulación base
        base_results = self.get_final_results_dict()
        
        # Fusionar con los resultados del análisis
        final_results = {**base_results, **analysis_data}
        
        np.savez_compressed(output_file, **final_results)
        print("✓ Resultados del análisis guardados exitosamente.")


def run_control_simulation(args):
    """Ejecuta la simulación de control sin masa local."""
    print("\n--- Ejecutando Simulación de Control (sin masa local) ---")
    output_file = "control_simulation_results.npz"
    if os.path.exists(output_file):
        print(f"✓ Usando resultados de control existentes: {output_file}")
        return output_file

    try:
        control_simulator = EinsteinSimulator(data_file=args.data_file)
        control_simulator.run_simulation(save_checkpoints=False, verbose=False)
        # El resultado se guarda en 'simulation_results.npz' por defecto
        os.rename("simulation_results.npz", output_file)
        print(f"✓ Simulación de control completada. Resultados en {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ Error en la simulación de control: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Análisis de Efectos de Acoplamiento Local-Global.')
    parser.add_argument('--data-file', default='simulation_initial_data.npz', help='Archivo de datos iniciales.')
    parser.add_argument('--output-file', default='acoplamiento_local_global.npz', help='Archivo de salida para el análisis.')
    parser.add_argument('--mass', type=float, default=1.0, help='Masa local.')
    parser.add_argument('--skip-control', action='store_true', help='Omitir la ejecución de la simulación de control.')
    args = parser.parse_args()

    # Primero, ejecutar la simulación de control si es necesario
    control_results_path = None
    if not args.skip_control:
        control_results_path = run_control_simulation(args)
    else:
        print("ℹ️  Omitiendo simulación de control.")
        if os.path.exists("control_simulation_results.npz"):
            control_results_path = "control_simulation_results.npz"

    # Ahora, ejecutar la simulación con masa local y analizarla
    print("\n--- Ejecutando Simulación Principal (con masa local) y Análisis ---")
    
    local_mass_params = {'mass': args.mass}

    try:
        analyzer = CouplingAnalyzer(
            data_file=args.data_file,
            local_mass_params=local_mass_params,
            control_sim_results_path=control_results_path
        )
        # run_simulation_with_validation llama a analyze_superposition_results al final
        analyzer.run_simulation_with_validation(
            save_checkpoints=False,
            verbose=True,
            output_file=args.output_file
        )
        print("\n🏆 ¡ANÁLISIS DE ACOPLAMIENTO COMPLETADO!")
        print(f"Resultados guardados en: {args.output_file}")

    except Exception as e:
        print(f"❌ Error fatal durante el análisis: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()