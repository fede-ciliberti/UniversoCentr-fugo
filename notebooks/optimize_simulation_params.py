#!/usr/bin/env python3
"""
Optimizador de parámetros de simulación según las características del sistema.
Analiza tu hardware y recomienda configuración óptima.
"""

import numpy as np
import psutil
import multiprocessing as mp
import os
import json
from pathlib import Path

class SimulationOptimizer:
    """
    Analizador de sistema y optimizador de parámetros de simulación.
    """
    
    def __init__(self):
        self.system_info = self.analyze_system()
        self.performance_profile = self.create_performance_profile()
    
    def analyze_system(self):
        """Analiza las características del sistema"""
        print("🔍 Analizando sistema...")
        
        # Información de CPU
        cpu_count = mp.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Información de memoria
        memory = psutil.virtual_memory()
        total_ram_gb = memory.total / (1024**3)
        available_ram_gb = memory.available / (1024**3)
        
        # Información de disco
        disk = psutil.disk_usage('.')
        free_space_gb = disk.free / (1024**3)
        
        info = {
            'cpu_count': cpu_count,
            'cpu_freq_mhz': cpu_freq.current if cpu_freq else None,
            'total_ram_gb': total_ram_gb,
            'available_ram_gb': available_ram_gb,
            'free_space_gb': free_space_gb,
        }
        
        print(f"✅ Sistema analizado:")
        print(f"   CPUs: {cpu_count}")
        print(f"   RAM total: {total_ram_gb:.1f} GB")
        print(f"   RAM disponible: {available_ram_gb:.1f} GB")
        print(f"   Espacio libre: {free_space_gb:.1f} GB")
        
        return info
    
    def create_performance_profile(self):
        """Crea un perfil de rendimiento del sistema"""
        cpu_count = self.system_info['cpu_count']
        ram_gb = self.system_info['available_ram_gb']
        
        # Clasificar sistema
        if cpu_count >= 16 and ram_gb >= 32:
            profile = "high_end"
        elif cpu_count >= 8 and ram_gb >= 16:
            profile = "mid_range"
        elif cpu_count >= 4 and ram_gb >= 8:
            profile = "entry_level"
        else:
            profile = "minimal"
        
        print(f"📊 Perfil del sistema: {profile}")
        return profile
    
    def estimate_memory_usage(self, grid_size):
        """Estima el uso de memoria para una resolución dada"""
        # Cada punto de la malla almacena:
        # - 6 componentes de métrica (gamma_ij): 6 * 8 bytes
        # - 6 componentes de curvatura (K_ij): 6 * 8 bytes  
        # - Variables auxiliares: ~4 * 8 bytes
        # Total por punto: ~128 bytes
        
        points = grid_size**3
        bytes_per_point = 128
        total_bytes = points * bytes_per_point
        
        # Factor de seguridad (arrays temporales, etc.)
        safety_factor = 2.5
        estimated_gb = total_bytes * safety_factor / (1024**3)
        
        return estimated_gb
    
    def recommend_grid_size(self):
        """Recomienda el tamaño óptimo de la malla"""
        available_ram = self.system_info['available_ram_gb']
        
        # Reservar RAM para el sistema operativo
        usable_ram = available_ram * 0.7  # Usar máximo 70% de RAM
        
        # Probar diferentes resoluciones
        test_sizes = [16, 24, 32, 48, 64, 96, 128, 192, 256]
        
        recommended_size = 16
        for size in test_sizes:
            memory_needed = self.estimate_memory_usage(size)
            if memory_needed <= usable_ram:
                recommended_size = size
            else:
                break
        
        print(f"🎯 Resolución recomendada: {recommended_size}³")
        print(f"   Memoria estimada: {self.estimate_memory_usage(recommended_size):.1f} GB")
        print(f"   RAM disponible: {usable_ram:.1f} GB")
        
        return recommended_size
    
    def recommend_timestep(self, grid_size):
        """Recomienda el paso temporal basado en la condición CFL"""
        # En relatividad numérica, dt debe satisfacer: dt < CFL * dx
        # donde CFL ~ 0.25 para estabilidad
        
        # Asumimos dominio [-10, 10] en cada dirección
        domain_size = 20.0
        dx = domain_size / grid_size
        
        cfl_factor = 0.25
        max_dt = cfl_factor * dx
        
        # Redondeamos a un valor "bonito"
        if max_dt >= 0.01:
            recommended_dt = 0.01
        elif max_dt >= 0.005:
            recommended_dt = 0.005
        elif max_dt >= 0.001:
            recommended_dt = 0.001
        else:
            recommended_dt = max_dt
        
        print(f"⏱️  Paso temporal recomendado: dt = {recommended_dt}")
        print(f"   CFL máximo teórico: {max_dt:.4f}")
        
        return recommended_dt
    
    def recommend_simulation_time(self, profile):
        """Recomienda tiempo total de simulación"""
        time_recommendations = {
            "minimal": 0.1,      # 10 unidades de tiempo
            "entry_level": 0.5,  # 50 unidades
            "mid_range": 1.0,    # 100 unidades
            "high_end": 2.0      # 200 unidades
        }
        
        return time_recommendations.get(profile, 0.5)
    
    def estimate_runtime(self, grid_size, dt, t_final, cpu_count):
        """Estima el tiempo de ejecución"""
        total_points = grid_size**3
        n_steps = int(t_final / dt)
        
        # Estimación empírica: ~1000 operaciones por punto por paso
        # Asumiendo ~1 GFLOP/s por core en promedio
        operations_per_step = total_points * 1000
        total_operations = operations_per_step * n_steps
        
        # Rendimiento estimado por core (operaciones/segundo)
        ops_per_core_per_sec = 1e9  # 1 GFLOP/s
        parallel_efficiency = 0.7   # 70% de eficiencia en paralelo
        
        effective_performance = cpu_count * ops_per_core_per_sec * parallel_efficiency
        estimated_seconds = total_operations / effective_performance
        
        return estimated_seconds
    
    def create_optimal_config(self):
        """Crea configuración óptima para el sistema"""
        print("\n🔧 Generando configuración óptima...")
        
        grid_size = self.recommend_grid_size()
        dt = self.recommend_timestep(grid_size)
        t_final = self.recommend_simulation_time(self.performance_profile)
        
        # Estimar tiempo de ejecución
        runtime_seconds = self.estimate_runtime(
            grid_size, dt, t_final, self.system_info['cpu_count']
        )
        runtime_minutes = runtime_seconds / 60
        
        config = {
            # Parámetros de malla
            'grid_size': grid_size,
            'domain_size': 20.0,
            
            # Parámetros temporales
            'dt': dt,
            't_final': t_final,
            'output_every': max(1, int(0.01 / dt)),  # Output cada ~0.01 unidades de tiempo
            
            # Parámetros de estabilidad
            'cfl_factor': 0.25,
            'dissipation': 0.01,
            
            # Parámetros físicos
            'R_param': 1.0,
            'omega_4d_param': 0.1,
            
            # Configuración de paralelización
            'max_cores': self.system_info['cpu_count'],
            'use_numba': True,
            
            # Configuración de salida
            'save_checkpoints': True,
            'checkpoint_every': max(10, int(0.1 / dt)),  # Checkpoint cada ~0.1 unidades
            'verbose': True,
            
            # Metadatos
            'estimated_runtime_minutes': runtime_minutes,
            'estimated_memory_gb': self.estimate_memory_usage(grid_size),
            'system_profile': self.performance_profile,
        }
        
        print(f"✅ Configuración generada:")
        print(f"   Resolución: {grid_size}³ ({grid_size**3:,} puntos)")
        print(f"   Paso temporal: {dt}")
        print(f"   Tiempo total: {t_final}")
        print(f"   Pasos totales: {int(t_final/dt):,}")
        print(f"   Tiempo estimado: {runtime_minutes:.1f} minutos")
        print(f"   Memoria estimada: {config['estimated_memory_gb']:.1f} GB")
        
        return config
    
    def save_config(self, config, filename="optimal_simulation_config.json"):
        """Guarda la configuración en un archivo JSON"""
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"💾 Configuración guardada en: {filename}")
        return filename
    
    def create_run_script(self, config):
        """Crea un script de ejecución personalizado"""
        script_content = f'''#!/usr/bin/env python3
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
    print(f"Sistema: {config['system_profile']}")
    print(f"Resolución: {config['grid_size']}³")
    print(f"Tiempo estimado: {config['estimated_runtime_minutes']:.1f} min")
    print("=" * 60)
    
    # Crear simulador con configuración optimizada
    simulator = EinsteinSimulator(
        data_file="simulation_initial_data.npz",
        max_cores={config['max_cores']}
    )
    
    # Aplicar configuración optimizada
    simulator.dt = {config['dt']}
    simulator.t_final = {config['t_final']}
    simulator.output_every = {config['output_every']}
    simulator.dissipation = {config['dissipation']}
    simulator.cfl_factor = {config['cfl_factor']}
    
    # Reconfigurar número de pasos
    simulator.n_steps = int(simulator.t_final / simulator.dt)
    simulator.n_outputs = simulator.n_steps // simulator.output_every
    
    print(f"Parámetros aplicados:")
    print(f"  dt = {{simulator.dt}}")
    print(f"  t_final = {{simulator.t_final}}")
    print(f"  n_steps = {{simulator.n_steps:,}}")
    print()
    
    # Ejecutar simulación
    simulator.run_simulation(
        save_checkpoints={config['save_checkpoints']},
        verbose={config['verbose']}
    )

if __name__ == "__main__":
    main()
'''
        
        script_filename = "run_optimized_simulation.py"
        with open(script_filename, 'w') as f:
            f.write(script_content)
        
        # Hacer ejecutable en sistemas Unix
        if os.name == 'posix':
            os.chmod(script_filename, 0o755)
        
        print(f"🎯 Script de ejecución creado: {script_filename}")
        return script_filename

def main():
    """Función principal del optimizador"""
    print("🎯 Optimizador de Parámetros de Simulación")
    print("=" * 50)
    
    # Crear optimizador
    optimizer = SimulationOptimizer()
    print()
    
    # Generar configuración óptima
    config = optimizer.create_optimal_config()
    print()
    
    # Guardar configuración
    config_file = optimizer.save_config(config)
    print()
    
    # Crear script de ejecución
    run_script = optimizer.create_run_script(config)
    print()
    
    # Mostrar recomendaciones finales
    print("📋 Instrucciones de uso:")
    print("=" * 30)
    print("1. Instalar dependencias:")
    print("   python notebooks/install_simulation_deps.py")
    print()
    print("2. Test de rendimiento:")
    print("   python notebooks/test_performance.py")
    print()
    print("3. Generar datos iniciales (si no está hecho):")
    print("   python notebooks/setup_numerical_simulation.py")
    print()
    print("4. Ejecutar simulación optimizada:")
    print(f"   python {run_script}")
    print()
    
    # Advertencias según el perfil
    if optimizer.performance_profile == "minimal":
        print("⚠️  ADVERTENCIA: Sistema con recursos limitados")
        print("   - La simulación puede ser muy lenta")
        print("   - Considere usar una resolución menor")
        print("   - Monitee el uso de memoria")
    elif optimizer.performance_profile == "entry_level":
        print("💡 CONSEJO: Sistema de gama de entrada")
        print("   - La simulación debería funcionar bien")
        print("   - Puede tardar varios minutos")
    else:
        print("🚀 EXCELENTE: Sistema potente detectado")
        print("   - La simulación debería ejecutarse eficientemente")
        print("   - Puede experimentar con resoluciones mayores")

if __name__ == "__main__":
    main()