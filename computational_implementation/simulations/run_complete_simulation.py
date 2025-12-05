#!/usr/bin/env python3
"""
Script maestro para ejecutar la simulación completa de Einstein.
Coordina todos los pasos desde la instalación hasta la ejecución.

Pasos del proceso:
1. Verificar/instalar dependencias
2. Optimizar parámetros según el sistema
3. Generar datos iniciales
4. Ejecutar simulación optimizada
5. Analizar resultados

Uso: python run_complete_simulation.py [--skip-install] [--skip-optimize]
"""

import subprocess
import sys
import os
import argparse
import time
from pathlib import Path

def run_command(cmd, description, critical=True):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔧 {description}...")
    print(f"Comando: {cmd}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} - Completado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(f"Código de salida: {e.returncode}")
        if critical:
            print("🛑 Error crítico. Deteniendo ejecución.")
            sys.exit(1)
        return False

def check_file_exists(filepath, description):
    """Verifica que un archivo exista"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ No encontrado {description}: {filepath}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Ejecuta simulación completa de Einstein')
    parser.add_argument('--skip-install', action='store_true', 
                       help='Omitir instalación de dependencias')
    parser.add_argument('--skip-optimize', action='store_true',
                       help='Omitir optimización de parámetros')
    parser.add_argument('--resolution', type=int, default=None,
                       help='Forzar resolución específica (ej: 32)')
    parser.add_argument('--time-limit', type=float, default=None,
                       help='Tiempo máximo de simulación en horas')
    
    args = parser.parse_args()
    
    print("🚀 SIMULACIÓN COMPLETA DE EINSTEIN")
    print("Universo Centrífugo - Verificación Aproximación 3")
    print("=" * 60)
    
    start_time = time.time()
    
    # PASO 1: Instalación de dependencias
    if not args.skip_install:
        print("\n📦 PASO 1: INSTALACIÓN DE DEPENDENCIAS")
        print("=" * 40)
        
        if not run_command("python computational_implementation/simulations/install_simulation_deps.py",
                           "Instalando dependencias"):
            return False
        
        print("\n🔬 Ejecutando test de rendimiento...")
        run_command("python computational_implementation/analysis_tools/test_performance.py",
                   "Test de rendimiento del sistema", critical=False)
    else:
        print("\n⏭️  PASO 1: OMITIDO - Instalación de dependencias")
    
    # PASO 2: Optimización de parámetros
    if not args.skip_optimize:
        print("\n🎯 PASO 2: OPTIMIZACIÓN DE PARÁMETROS")
        print("=" * 40)
        
        if not run_command("python computational_implementation/simulations/optimize_simulation_params.py",
                           "Optimizando parámetros del sistema"):
            return False
    else:
        print("\n⏭️  PASO 2: OMITIDO - Optimización de parámetros")
    
    # PASO 3: Verificar/generar datos iniciales
    print("\n📊 PASO 3: DATOS INICIALES")
    print("=" * 40)
    
    data_file = "simulation_initial_data.npz"
    if check_file_exists(data_file, "Datos iniciales"):
        print("ℹ️  Usando datos iniciales existentes")
    else:
        print("🔄 Generando datos iniciales...")
        if not run_command("python computational_implementation/simulations/setup_numerical_simulation.py",
                           "Generando datos iniciales"):
            return False
     
     # PASO 4: Ejecutar simulación
     print("\n🚀 PASO 4: EJECUCIÓN DE SIMULACIÓN")
     print("=" * 40)
     
     # Decidir qué script ejecutar
     optimized_script = "run_optimized_simulation.py"
    default_script = "computational_implementation/simulations/run_numerical_simulation.py"
    
    if os.path.exists(optimized_script) and not args.skip_optimize:
        simulation_cmd = f"python {optimized_script}"
        print("🎯 Usando configuración optimizada")
    else:
        simulation_cmd = f"python {default_script}"
        print("⚙️  Usando configuración por defecto")
    
    # Modificar comando según argumentos
    if args.time_limit:
        # Aquí podrías agregar lógica para limitar tiempo
        print(f"⏰ Límite de tiempo: {args.time_limit} horas")
    
    print(f"\n🚀 Iniciando simulación...")
    print(f"Hora de inicio: {time.strftime('%H:%M:%S')}")
    
    simulation_start = time.time()
    success = run_command(simulation_cmd, "Ejecutando simulación Einstein")
    simulation_time = time.time() - simulation_start
    
    if success:
        print(f"\n✅ SIMULACIÓN COMPLETADA")
        print(f"Tiempo de simulación: {simulation_time/60:.1f} minutos")
    else:
        print(f"\n❌ SIMULACIÓN FALLÓ")
        return False
    
    # PASO 5: Análisis de resultados
    print("\n📈 PASO 5: ANÁLISIS DE RESULTADOS")
    print("=" * 40)
    
    results_file = "simulation_results.npz"
    if check_file_exists(results_file, "Resultados de simulación"):
        # Crear script de análisis rápido
        analysis_script = """
import numpy as np
import matplotlib.pyplot as plt

print("📊 Análisis rápido de resultados...")

# Cargar resultados
data = np.load('simulation_results.npz', allow_pickle=True)
times = data['time_evolution']
metrics = data['metric_evolution']

if len(times) > 0:
    print(f"Tiempo simulado: 0 → {times[-1]:.3f}")
    print(f"Puntos temporales: {len(times)}")
    
    # Crear gráfico de evolución
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Determinante de la métrica
    det_gammas = [m['det_gamma'] for m in metrics]
    ax1.plot(times, det_gammas, 'b-', linewidth=2)
    ax1.set_title('Determinante de la Métrica')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('det(γ)')
    ax1.grid(True)
    
    # Métrica final
    gamma_xx = data['final_gamma_xx']
    center_slice = gamma_xx[:, :, gamma_xx.shape[2]//2]
    im = ax2.imshow(center_slice, cmap='RdBu_r', origin='lower')
    ax2.set_title('γ_xx final (corte central)')
    plt.colorbar(im, ax=ax2)
    
    plt.tight_layout()
    plt.savefig('simulation_analysis.png', dpi=150, bbox_inches='tight')
    print("✅ Gráfico guardado: simulation_analysis.png")
    
    # Verificar signos de curvatura
    gamma_deviation = np.std(gamma_xx)
    print(f"Desviación estándar γ_xx: {gamma_deviation:.6f}")
    
    if gamma_deviation > 1e-6:
        print("🎉 ¡Curvatura detectada! La simulación muestra deformación del espacio-tiempo")
    else:
        print("ℹ️  Curvatura mínima. Considera mayor resolución o tiempo de simulación")

else:
    print("⚠️  Sin datos de evolución temporal")
"""
        
        with open("quick_analysis.py", "w") as f:
            f.write(analysis_script)
        
        run_command("python quick_analysis.py", "Análisis de resultados", critical=False)
        
        # Limpiar archivo temporal
        if os.path.exists("quick_analysis.py"):
            os.remove("quick_analysis.py")
    
    # RESUMEN FINAL
    total_time = time.time() - start_time
    print(f"\n🎉 PROCESO COMPLETO FINALIZADO")
    print("=" * 60)
    print(f"⏱️  Tiempo total: {total_time/60:.1f} minutos")
    print(f"📁 Archivos generados:")
    
    output_files = [
        "simulation_initial_data.npz",
        "simulation_results.npz", 
        "optimal_simulation_config.json",
        "run_optimized_simulation.py",
        "simulation_analysis.png"
    ]
    
    for filename in output_files:
        if os.path.exists(filename):
            size_mb = os.path.getsize(filename) / (1024*1024)
            print(f"   ✅ {filename} ({size_mb:.1f} MB)")
        else:
            print(f"   ❌ {filename} (no generado)")
    
    print(f"\n📋 PRÓXIMOS PASOS:")
    print("1. Revisar simulation_analysis.png")
    print("2. Analizar simulation_results.npz en detalle")
    print("3. Comparar con métrica de Schwarzschild teórica")
    print("4. Si es necesario, ejecutar con mayor resolución")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🏆 ¡MISIÓN CUMPLIDA!")
        sys.exit(0)
    else:
        print("\n💥 MISIÓN FALLIDA")
        sys.exit(1)