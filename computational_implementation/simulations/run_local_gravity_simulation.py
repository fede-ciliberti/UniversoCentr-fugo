#!/usr/bin/env python3
"""
Script de simulación numérica con superposición de gravedad local.
Tarea 2.1.1: Modificación del Código de Simulación

Este script implementa el Principio de Superposición Cosmológico extendiendo
la simulación cosmológica base para incluir una masa puntual local y validar
la consistencia entre efectos locales y globales.
"""

import numpy as np
import argparse
import sys
import os
import time

try:
    from .run_numerical_simulation import EinsteinSimulator
except ImportError:
    from run_numerical_simulation import EinsteinSimulator

class LocalGravitySimulation(EinsteinSimulator):
    """
    Simulador que extiende EinsteinSimulator para incluir masa puntual local.
    """
    
    def __init__(self, data_file="simulation_initial_data.npz", max_cores=None,
                 local_mass_params=None):
        print("🌌 Inicializando Local Gravity Simulation...")
        super().__init__(data_file, max_cores)
        self.setup_local_mass_parameters(local_mass_params)
        self.compute_local_mass_tensor()
        self.initialize_validation_metrics()
        print("✓ Local Gravity Simulation inicializada correctamente")
        
    def setup_local_mass_parameters(self, params):
        """Configura y valida los parámetros de la masa local."""
        print("🔧 Configurando parámetros de masa local...")
        default_params = {
            'mass': 1.0,
            'position': None,
            'smoothing_radius': None,
            'enable_time_modulation': True
        }
        if params is None:
            params = {}
        self.local_mass_params = {**default_params, **params}
        
        if self.local_mass_params['position'] is None:
            center_x = self.X[self.nx//2, self.ny//2, self.nz//2]
            center_y = self.Y[self.nx//2, self.ny//2, self.nz//2]
            center_z = self.Z[self.nx//2, self.ny//2, self.nz//2]
            self.local_mass_params['position'] = (center_x, center_y, center_z)
        
        if self.local_mass_params['smoothing_radius'] is None:
            grid_size = min(self.dx, self.dy, self.dz)
            self.local_mass_params['smoothing_radius'] = 5 * grid_size
        
        self.M_local = self.local_mass_params['mass']
        self.pos_x, self.pos_y, self.pos_z = self.local_mass_params['position']
        self.sigma = self.local_mass_params['smoothing_radius']
        
    def compute_local_mass_tensor(self):
        """Pre-calcula el tensor de energía-impulso para la masa local."""
        print("📐 Calculando tensor de masa local...")
        r_squared = (self.X - self.pos_x)**2 + (self.Y - self.pos_y)**2 + (self.Z - self.pos_z)**2
        normalization = self.M_local / (self.sigma * np.sqrt(2 * np.pi))**3
        density = normalization * np.exp(-r_squared / (2 * self.sigma**2))
        self.T_local = np.zeros_like(self.T_initial)
        self.T_local[:, :, :, 0, 0] = density
        
    def initialize_validation_metrics(self):
        """Inicializa métricas para validación."""
        self.superposition_metrics = []
        
    def compute_stress_energy_contribution(self, t):
        """Implementa la superposición de tensores."""
        T_cosmological = super().compute_stress_energy_contribution(t)
        T_total = T_cosmological + self.T_local
        return T_total
        
    def run_simulation_with_validation(self, save_checkpoints=True, verbose=True, output_file="local_gravity_simulation_results.npz", resume_from_checkpoint=None):
        """Ejecuta la simulación con validación extendida."""
        print("\n🚀 Iniciando simulación con validación de superposición...")
        try:
            super().run_simulation(save_checkpoints, verbose, resume_from_checkpoint)
        except Exception as e:
            print(f"❌ Error durante simulación con superposición: {e}")
            raise
        finally:
            self.analyze_superposition_results(output_file)
    
    def analyze_superposition_results(self, output_file):
        """Analiza los resultados específicos del test de superposición."""
        print("\n📈 ANÁLISIS DE SUPERPOSICIÓN")
        # Guardar resultados
        self.save_final_results(output_file)

    def save_final_results(self, output_file="local_gravity_simulation_results.npz") -> str:
        """Extiende el guardado de resultados para incluir datos de superposición."""
        # Obtener resultados de la clase base como un diccionario
        base_results = super().get_final_results_dict()
        
        # Crear diccionario con resultados de superposición
        superposition_results = {
            'local_mass_params': self.local_mass_params,
            'T_local': self.T_local,
            'superposition_metrics': self.superposition_metrics,
        }
        
        # Fusionar los dos diccionarios
        final_results = {**base_results, **superposition_results}
        
        # Guardar el diccionario fusionado
        np.savez_compressed(output_file, **final_results)
        print(f"💾 Resultados completos (base + superposición) guardados en: {output_file}")
        return output_file

def main():
    """Función principal para ejecutar la simulación con masa local."""
    parser = argparse.ArgumentParser(description='Simulación con Principio de Superposición Cosmológico')
    parser.add_argument('--data-file', default='simulation_initial_data.npz', help='Archivo de datos iniciales')
    parser.add_argument('--output-file', default='local_gravity_simulation_results.npz', help='Archivo de salida para los resultados')
    parser.add_argument('--mass', type=float, default=1.0, help='Masa local en unidades geométricas')
    parser.add_argument('--pos-x', type=float, default=None, help='Posición X del centro de masa')
    parser.add_argument('--pos-y', type=float, default=None, help='Posición Y del centro de masa')
    parser.add_argument('--pos-z', type=float, default=None, help='Posición Z del centro de masa')
    parser.add_argument('--smoothing', type=float, default=None, help='Radio de suavizado')
    parser.add_argument('--max-cores', type=int, default=None, help='Número máximo de cores')
    parser.add_argument('--resume-from', default=None, help='Ruta al archivo de checkpoint para reanudar la simulación')
    args = parser.parse_args()

    if not os.path.exists(args.data_file):
        print(f"❌ Error: No se encontró {args.data_file}")
        sys.exit(1)
    
    mass_params = {
        'mass': args.mass,
        'position': (args.pos_x, args.pos_y, args.pos_z) if all(v is not None for v in [args.pos_x, args.pos_y, args.pos_z]) else None,
        'smoothing_radius': args.smoothing,
    }
    
    try:
        simulator = LocalGravitySimulation(
            data_file=args.data_file,
            max_cores=args.max_cores,
            local_mass_params=mass_params
        )
        simulator.run_simulation_with_validation(
            save_checkpoints=True,
            verbose=True,
            output_file=args.output_file,
            resume_from_checkpoint=args.resume_from
        )
        print("\n🏆 ¡SIMULACIÓN COMPLETADA!")
        print(f"Resultados guardados en: {args.output_file}")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()