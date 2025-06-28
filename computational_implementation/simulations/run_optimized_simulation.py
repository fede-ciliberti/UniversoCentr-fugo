#!/usr/bin/env python3
"""
Script de ejecución optimizado para tu sistema.
Configuración automáticamente generada por optimize_simulation_params.py
"""

import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.getcwd())

# Importar el simulador
from notebooks.run_numerical_simulation import EinsteinSimulator

def main():
    print("🚀 Simulación Einstein - Configuración Optimizada")
    print("=" * 60)
    print(f"Sistema: mid_range")
    print(f"Resolución: 256³")
    print(f"Tiempo estimado: 3.3 min")
    print("=" * 60)
    
    # Crear simulador con configuración optimizada
    simulator = EinsteinSimulator(
        data_file="simulation_initial_data.npz",
        max_cores=12
    )
    
    # Aplicar configuración optimizada
    simulator.dt = 0.01
    simulator.t_final = 1.0
    simulator.output_every = 1
    simulator.dissipation = 0.01
    simulator.cfl_factor = 0.25
    
    # Reconfigurar número de pasos
    simulator.n_steps = int(simulator.t_final / simulator.dt)
    simulator.n_outputs = simulator.n_steps // simulator.output_every
    
    print(f"Parámetros aplicados:")
    print(f"  dt = {simulator.dt}")
    print(f"  t_final = {simulator.t_final}")
    print(f"  n_steps = {simulator.n_steps:,}")
    print()
    
    # Ejecutar simulación
    simulator.run_simulation(
        save_checkpoints=True,
        verbose=True
    )

if __name__ == "__main__":
    main()
