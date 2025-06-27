#!/usr/bin/env python3
"""
Estimador de tiempo y recursos para simulaciones de diferentes resoluciones.
Basado en los resultados de tu simulación 32³ que tardó 6.63 minutos.
"""

import numpy as np
import psutil
import multiprocessing as mp

def estimate_memory_usage(grid_size):
    """Estima el uso de memoria para una resolución dada"""
    # Cada punto almacena aproximadamente:
    # - 6 componentes γ_ij (gamma): 6 * 8 bytes
    # - 6 componentes K_ij (curvatura): 6 * 8 bytes  
    # - Variables auxiliares BSSN: ~4 * 8 bytes
    # - Arrays temporales: factor 2x
    # Total por punto: ~128 bytes con factor de seguridad
    
    points = grid_size**3
    bytes_per_point = 128
    total_bytes = points * bytes_per_point
    
    # Factor de seguridad para arrays temporales y cálculos intermedios
    safety_factor = 3.0
    estimated_gb = total_bytes * safety_factor / (1024**3)
    
    return estimated_gb, points

def estimate_computation_time(grid_size, reference_size=32, reference_time_minutes=6.63):
    """
    Estima el tiempo computacional basado en escalamiento teórico.
    
    El tiempo escala aproximadamente como:
    - Espacial: O(N³) donde N es grid_size
    - Temporal: O(N_steps) 
    - Total: O(N³ × N_steps)
    
    Para simulaciones tipo BSSN, el escalamiento suele ser ligeramente peor
    que linear debido a comunicación entre cores y operaciones de derivadas.
    """
    
    # Escalamiento de puntos espaciales
    spatial_scaling = (grid_size / reference_size) ** 3
    
    # Factor de escalamiento no-linear (típico en simulaciones BSSN)
    # Incluye efectos de cache, comunicación entre cores, etc.
    nonlinear_factor = (spatial_scaling) ** 0.2  # Escalamiento sublinear
    
    # Estimación conservadora
    estimated_minutes = reference_time_minutes * spatial_scaling * nonlinear_factor
    
    return estimated_minutes

def analyze_system_capacity():
    """Analiza la capacidad del sistema actual"""
    # Información de memoria
    memory = psutil.virtual_memory()
    total_ram_gb = memory.total / (1024**3)
    available_ram_gb = memory.available / (1024**3)
    
    # Información de CPU
    cpu_count = mp.cpu_count()
    
    # Usar máximo 70% de RAM disponible para estar seguros
    usable_ram_gb = available_ram_gb * 0.7
    
    return {
        'total_ram_gb': total_ram_gb,
        'available_ram_gb': available_ram_gb,
        'usable_ram_gb': usable_ram_gb,
        'cpu_count': cpu_count
    }

def recommend_optimal_resolution(system_info):
    """Recomienda la resolución óptima según el sistema"""
    usable_ram = system_info['usable_ram_gb']
    
    # Probar diferentes resoluciones
    test_sizes = [32, 48, 64, 96, 128, 192, 256]
    
    recommendations = []
    
    for size in test_sizes:
        memory_needed, points = estimate_memory_usage(size)
        time_minutes = estimate_computation_time(size)
        time_hours = time_minutes / 60
        
        # Clasificar viabilidad
        if memory_needed <= usable_ram:
            if time_hours < 0.5:
                viability = "🟢 RÁPIDO"
            elif time_hours < 2.0:
                viability = "🟡 MODERADO"
            elif time_hours < 8.0:
                viability = "🟠 LARGO"
            else:
                viability = "🔴 MUY LARGO"
            
            feasible = True
        else:
            viability = "❌ SIN MEMORIA"
            feasible = False
        
        recommendations.append({
            'size': size,
            'points': points,
            'memory_gb': memory_needed,
            'time_minutes': time_minutes,
            'time_hours': time_hours,
            'viability': viability,
            'feasible': feasible
        })
    
    return recommendations

def print_detailed_analysis():
    """Imprime análisis detallado de opciones de simulación"""
    print("🔬 ESTIMADOR DE ESCALAMIENTO - SIMULACIÓN EINSTEIN")
    print("=" * 70)
    
    # Analizar sistema
    system_info = analyze_system_capacity()
    
    print(f"\n💻 CAPACIDAD DEL SISTEMA:")
    print(f"   RAM total: {system_info['total_ram_gb']:.1f} GB")
    print(f"   RAM disponible: {system_info['available_ram_gb']:.1f} GB")
    print(f"   RAM utilizable: {system_info['usable_ram_gb']:.1f} GB")
    print(f"   CPUs: {system_info['cpu_count']}")
    
    # Obtener recomendaciones
    recommendations = recommend_optimal_resolution(system_info)
    
    print(f"\n📊 ESTIMACIONES POR RESOLUCIÓN:")
    print(f"{'Resolución':<12} {'Puntos':<12} {'Memoria':<10} {'Tiempo':<15} {'Estado':<15}")
    print("-" * 70)
    
    for rec in recommendations:
        size_str = f"{rec['size']}³"
        points_str = f"{rec['points']:,}"
        memory_str = f"{rec['memory_gb']:.1f} GB"
        
        if rec['time_hours'] < 1:
            time_str = f"{rec['time_minutes']:.0f} min"
        else:
            time_str = f"{rec['time_hours']:.1f} h"
        
        print(f"{size_str:<12} {points_str:<12} {memory_str:<10} {time_str:<15} {rec['viability']:<15}")
    
    # Recomendaciones específicas
    print(f"\n💡 RECOMENDACIONES ESPECÍFICAS:")
    
    # Encontrar la resolución más alta factible con tiempo razonable
    feasible_recs = [r for r in recommendations if r['feasible']]
    
    if not feasible_recs:
        print(f"   ❌ Tu sistema no puede manejar resoluciones mayores")
        print(f"   🔧 Considera usar un servidor con más RAM")
        return
    
    # Categorizar recomendaciones
    quick_recs = [r for r in feasible_recs if r['time_hours'] < 0.5]
    moderate_recs = [r for r in feasible_recs if 0.5 <= r['time_hours'] < 2.0]
    long_recs = [r for r in feasible_recs if 2.0 <= r['time_hours'] < 8.0]
    
    if quick_recs:
        best_quick = max(quick_recs, key=lambda x: x['size'])
        print(f"\n🟢 PARA PRUEBAS RÁPIDAS (<30 min):")
        print(f"   Resolución recomendada: {best_quick['size']}³")
        print(f"   Tiempo estimado: {best_quick['time_minutes']:.0f} minutos")
        print(f"   Memoria necesaria: {best_quick['memory_gb']:.1f} GB")
        print(f"   Mejora sobre 32³: {(best_quick['size']/32)**3:.1f}x más puntos")
    
    if moderate_recs:
        best_moderate = max(moderate_recs, key=lambda x: x['size'])
        print(f"\n🟡 PARA RESULTADOS DETALLADOS (30min-2h):")
        print(f"   Resolución recomendada: {best_moderate['size']}³")
        print(f"   Tiempo estimado: {best_moderate['time_hours']:.1f} horas")
        print(f"   Memoria necesaria: {best_moderate['memory_gb']:.1f} GB")
        print(f"   Mejora sobre 32³: {(best_moderate['size']/32)**3:.1f}x más puntos")
    
    if long_recs:
        best_long = max(long_recs, key=lambda x: x['size'])
        print(f"\n🟠 PARA MÁXIMA PRECISIÓN (2-8h):")
        print(f"   Resolución recomendada: {best_long['size']}³")
        print(f"   Tiempo estimado: {best_long['time_hours']:.1f} horas")
        print(f"   Memoria necesaria: {best_long['memory_gb']:.1f} GB")
        print(f"   Mejora sobre 32³: {(best_long['size']/32)**3:.1f}x más puntos")
    
    # Comparación de resolución científica
    print(f"\n🔬 IMPACTO CIENTÍFICO POR RESOLUCIÓN:")
    print(f"   32³ → 48³: Verifica tendencias básicas")
    print(f"   48³ → 64³: Confirma patrones espaciales")
    print(f"   64³ → 96³: Detecta efectos radiales tipo Schwarzschild")
    print(f"   96³ → 128³: Análisis cuantitativo preciso")
    print(f"   128³+: Efectos sutiles y validación rigorosa")

def generate_configuration_file(target_resolution):
    """Genera archivo de configuración para la resolución objetivo"""
    memory_needed, points = estimate_memory_usage(target_resolution)
    time_estimated = estimate_computation_time(target_resolution)
    
    # Ajustar parámetros según resolución
    if target_resolution <= 48:
        dt = 0.01
        t_final = 1.0
    elif target_resolution <= 64:
        dt = 0.008  # Más estable para alta resolución
        t_final = 1.5
    elif target_resolution <= 96:
        dt = 0.005
        t_final = 2.0
    else:
        dt = 0.004
        t_final = 2.5
    
    n_steps = int(t_final / dt)
    
    config = {
        'grid_size': target_resolution,
        'domain_size': 20.0,
        'dt': dt,
        't_final': t_final,
        'n_steps': n_steps,
        'output_every': max(1, n_steps // 100),  # ~100 outputs
        'checkpoint_every': max(10, n_steps // 20),  # ~20 checkpoints
        'estimated_time_minutes': time_estimated,
        'estimated_memory_gb': memory_needed,
        'R_param': 1.0,
        'omega_4d_param': 0.1
    }
    
    return config

def main():
    """Función principal"""
    print_detailed_analysis()
    
    print(f"\n❓ SELECCIÓN DE RESOLUCIÓN:")
    print(f"   Basándote en la tabla anterior, ¿qué resolución prefieres?")
    print(f"   Opciones típicas:")
    print(f"   • 48³: Rápida verificación de la tendencia")
    print(f"   • 64³: Buen balance tiempo/precisión") 
    print(f"   • 96³: Alta precisión para análisis detallado")

if __name__ == "__main__":
    main()