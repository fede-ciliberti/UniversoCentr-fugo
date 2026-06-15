#!/usr/bin/env python3
"""
Script de ejecución para simulación 256³ optimizada.
Generado automáticamente el 2025-06-27 21:09:28
"""

import sys
import os
sys.path.append(os.getcwd())

from notebooks.setup_256cubed_optimized_simulation import OptimizedEinstein256Simulator
from notebooks.run_256cubed_chunked_evolution import ChunkedEvolutionEngine

def main():
    print("🚀 SIMULACIÓN EINSTEIN 256³ - CONFIGURACIÓN OPTIMIZADA")
    print("=" * 70)
    
    # Inicializar simulador
    simulator = OptimizedEinstein256Simulator(
        chunk_size=32,
        memory_limit_gb=24.520980834960938,
        use_mixed_precision=True
    )
    
    # Configurar almacenamiento
    simulator.setup_memory_mapped_storage()
    
    # Cargar fuentes
    simulator.load_stress_energy_tensor()
    
    # Configurar parámetros
    simulator.setup_simulation_parameters()
    
    # Crear motor de evolución
    evolution_engine = ChunkedEvolutionEngine(simulator)
    
    # Ejecutar simulación
    evolution_engine.run_full_simulation()

if __name__ == "__main__":
    main()
