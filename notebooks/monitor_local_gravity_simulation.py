#!/usr/bin/env python3
"""
Script de Monitoreo de Simulación de Gravedad Local

Este script permite monitorear el progreso de simulaciones en ejecución
y analizar los checkpoints generados.

Funcionalidades:
- Mostrar el estado actual de la simulación
- Listar checkpoints disponibles
- Analizar la evolución temporal de invariantes métricos
- Estimar tiempo restante de simulación

Uso:
python notebooks/monitor_local_gravity_simulation.py --resolution 64
python notebooks/monitor_local_gravity_simulation.py --resolution 64 --analyze

Fecha: 27 de junio de 2025
Autor: Universo Centrífugo Research Team
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import glob
from pathlib import Path
import time

def list_checkpoints(output_dir):
    """Lista todos los checkpoints disponibles en el directorio de salida."""
    checkpoint_files = sorted(glob.glob(str(output_dir / "checkpoint_*.npz")))
    return checkpoint_files

def analyze_checkpoint(checkpoint_file):
    """Analiza un checkpoint individual y extrae información clave."""
    data = np.load(checkpoint_file)
    
    info = {
        'file': checkpoint_file,
        'step': data['step'],
        'time': data['time'],
        'det_gamma': np.mean(data['gamma_xx'] * data['gamma_yy'] * data['gamma_zz']),
        'gamma_xx_stats': {
            'mean': np.mean(data['gamma_xx']),
            'std': np.std(data['gamma_xx']),
            'min': np.min(data['gamma_xx']),
            'max': np.max(data['gamma_xx'])
        }
    }
    return info

def monitor_simulation_progress(resolution):
    """Monitorea el progreso de una simulación en ejecución."""
    output_dir = Path(f"output/local_gravity_{resolution}cubed")
    
    if not output_dir.exists():
        print(f"❌ No se encontró el directorio de salida: {output_dir}")
        return
    
    print(f"📊 Monitoreando simulación de resolución {resolution}³")
    print("=" * 60)
    
    checkpoints = list_checkpoints(output_dir)
    
    if not checkpoints:
        print("⏳ No se han generado checkpoints aún...")
        return
    
    print(f"✓ Se encontraron {len(checkpoints)} checkpoints")
    
    # Analizar el último checkpoint
    latest_checkpoint = checkpoints[-1]
    info = analyze_checkpoint(latest_checkpoint)
    
    print(f"\n📍 Estado actual (último checkpoint):")
    print(f"   Archivo: {os.path.basename(info['file'])}")
    print(f"   Paso: {info['step']}")
    print(f"   Tiempo de simulación: {info['time']:.3f}")
    print(f"   det(γ): {info['det_gamma']:.6f}")
    print(f"   γ_xx: μ={info['gamma_xx_stats']['mean']:.4f}, "
          f"σ={info['gamma_xx_stats']['std']:.4f}")
    
    # Mostrar evolución temporal si hay múltiples checkpoints
    if len(checkpoints) > 1:
        print(f"\n📈 Evolución temporal (últimos 5 checkpoints):")
        for checkpoint in checkpoints[-5:]:
            info = analyze_checkpoint(checkpoint)
            print(f"   t={info['time']:6.3f} | det(γ)={info['det_gamma']:8.6f} | "
                  f"γ_xx={info['gamma_xx_stats']['mean']:6.4f}")

def analyze_simulation_evolution(resolution):
    """Analiza la evolución completa de la simulación."""
    output_dir = Path(f"output/local_gravity_{resolution}cubed")
    checkpoints = list_checkpoints(output_dir)
    
    if len(checkpoints) < 2:
        print("❌ Se necesitan al menos 2 checkpoints para el análisis.")
        return
    
    print(f"🔬 Analizando evolución completa de la simulación {resolution}³")
    print("=" * 60)
    
    # Extraer datos de evolución
    times = []
    det_gammas = []
    gamma_xx_means = []
    
    for checkpoint in checkpoints:
        info = analyze_checkpoint(checkpoint)
        times.append(info['time'])
        det_gammas.append(info['det_gamma'])
        gamma_xx_means.append(info['gamma_xx_stats']['mean'])
    
    times = np.array(times)
    det_gammas = np.array(det_gammas)
    gamma_xx_means = np.array(gamma_xx_means)
    
    # Crear gráficos
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Evolución de la Simulación de Gravedad Local ({resolution}³)', fontsize=14)
    
    # det(γ) vs tiempo
    axes[0,0].plot(times, det_gammas, 'b-', marker='o', markersize=3)
    axes[0,0].set_xlabel('Tiempo de simulación')
    axes[0,0].set_ylabel('det(γ)')
    axes[0,0].set_title('Determinante de la métrica espacial')
    axes[0,0].grid(True, alpha=0.3)
    
    # γ_xx medio vs tiempo
    axes[0,1].plot(times, gamma_xx_means, 'r-', marker='s', markersize=3)
    axes[0,1].set_xlabel('Tiempo de simulación')
    axes[0,1].set_ylabel('⟨γ_xx⟩')
    axes[0,1].set_title('Componente γ_xx promedio')
    axes[0,1].grid(True, alpha=0.3)
    
    # Desviación del valor inicial
    initial_det_gamma = det_gammas[0]
    relative_change = (det_gammas - initial_det_gamma) / initial_det_gamma * 100
    
    axes[1,0].plot(times, relative_change, 'g-', marker='^', markersize=3)
    axes[1,0].set_xlabel('Tiempo de simulación')
    axes[1,0].set_ylabel('Cambio relativo en det(γ) (%)')
    axes[1,0].set_title('Estabilidad de la métrica')
    axes[1,0].grid(True, alpha=0.3)
    
    # Histograma de γ_xx del último checkpoint
    latest_data = np.load(checkpoints[-1])
    gamma_xx_flat = latest_data['gamma_xx'].flatten()
    
    axes[1,1].hist(gamma_xx_flat, bins=50, alpha=0.7, color='purple', edgecolor='black')
    axes[1,1].set_xlabel('γ_xx')
    axes[1,1].set_ylabel('Frecuencia')
    axes[1,1].set_title(f'Distribución de γ_xx (t={times[-1]:.3f})')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar gráfico
    plot_filename = output_dir / f"evolution_analysis_{resolution}cubed.png"
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"📊 Gráfico guardado en: {plot_filename}")
    
    # Estadísticas de resumen
    print(f"\n📋 Estadísticas de la simulación:")
    print(f"   Duración total: {times[-1]:.3f} unidades de tiempo")
    print(f"   Número de checkpoints: {len(checkpoints)}")
    print(f"   Cambio relativo en det(γ): {relative_change[-1]:.4f}%")
    print(f"   Estabilidad: {'✓ Estable' if abs(relative_change[-1]) < 1.0 else '⚠ Inestable'}")

def main():
    parser = argparse.ArgumentParser(description="Monitorea simulaciones de gravedad local.")
    parser.add_argument('--resolution', type=int, required=True, choices=[32, 64, 128],
                        help="Resolución de la simulación a monitorear.")
    parser.add_argument('--analyze', action='store_true',
                        help="Realizar análisis completo con gráficos.")
    parser.add_argument('--watch', action='store_true',
                        help="Monitoreo continuo (actualiza cada 30 segundos).")
    
    args = parser.parse_args()
    
    if args.analyze:
        analyze_simulation_evolution(args.resolution)
    elif args.watch:
        print("🔄 Modo de monitoreo continuo (Ctrl+C para salir)")
        try:
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                monitor_simulation_progress(args.resolution)
                print("\n⏰ Actualizando en 30 segundos...")
                time.sleep(30)
        except KeyboardInterrupt:
            print("\n👋 Monitoreo detenido.")
    else:
        monitor_simulation_progress(args.resolution)

if __name__ == "__main__":
    main()