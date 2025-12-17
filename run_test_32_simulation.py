#!/usr/bin/env python3
"""
Script de ejecución para prueba de simulación con resolución 32³
Configuración específica para prueba rápida
"""

import sys
import os
import json

# Añadir el directorio actual al path
sys.path.append(os.getcwd())

# Importar el simulador
from computational_implementation.simulations.run_numerical_simulation import EinsteinSimulator

def main():
    print("🚀 Simulación Einstein - Prueba 32³")
    print("=" * 60)
    
    # Cargar configuración de prueba
    with open("test_32_config.json", "r") as f:
        config = json.load(f)
    
    print(f"Resolución: {config['grid_size']}³")
    print(f"Tiempo estimado: {config['estimated_runtime_minutes']:.1f} min")
    print("=" * 60)
    
    # Crear simulador con configuración de prueba
    simulator = EinsteinSimulator(
        data_file="simulation_initial_data.npz",
        max_cores=config['max_cores']
    )
    
    # Aplicar configuración de prueba
    simulator.dt = config['dt']
    simulator.t_final = config['t_final']
    simulator.output_every = config['output_every']
    simulator.dissipation = config['dissipation']
    simulator.cfl_factor = config['cfl_factor']
    
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
        save_checkpoints=config['save_checkpoints'],
        verbose=config['verbose']
    )

if __name__ == "__main__":
    main()