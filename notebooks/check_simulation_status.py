#!/usr/bin/env python3
"""
Script simple para verificar el estado de la simulación sin dependencias gráficas.
"""

import numpy as np
import os
import glob
from pathlib import Path
import argparse

def check_simulation_status(resolution):
    """Verifica el estado de la simulación sin dependencias gráficas."""
    output_dir = Path(f"output/local_gravity_{resolution}cubed")
    
    if not output_dir.exists():
        print(f"❌ No se encontró el directorio de salida: {output_dir}")
        return
    
    # Buscar checkpoints
    checkpoint_files = sorted(glob.glob(str(output_dir / "checkpoint_*.npz")))
    
    print(f"📊 Estado de la simulación {resolution}³")
    print("=" * 50)
    
    if not checkpoint_files:
        print("⏳ No se han generado checkpoints aún...")
        return
    
    print(f"✓ Se encontraron {len(checkpoint_files)} checkpoints")
    
    # Analizar el último checkpoint
    latest_checkpoint = checkpoint_files[-1]
    data = np.load(latest_checkpoint)
    
    step = data['step']
    time_sim = data['time']
    det_gamma = np.mean(data['gamma_xx'] * data['gamma_yy'] * data['gamma_zz'])
    gamma_xx_mean = np.mean(data['gamma_xx'])
    gamma_xx_std = np.std(data['gamma_xx'])
    
    print(f"\n📍 Último checkpoint:")
    print(f"   Archivo: {os.path.basename(latest_checkpoint)}")
    print(f"   Paso: {step}")
    print(f"   Tiempo de simulación: {time_sim:.3f}")
    print(f"   det(γ): {det_gamma:.6f}")
    print(f"   γ_xx promedio: {gamma_xx_mean:.6f} ± {gamma_xx_std:.6f}")
    
    # Mostrar progreso de los últimos checkpoints
    if len(checkpoint_files) > 1:
        print(f"\n📈 Últimos checkpoints:")
        for checkpoint in checkpoint_files[-3:]:
            data = np.load(checkpoint)
            print(f"   t={data['time']:6.3f} | paso={data['step']:6d} | "
                  f"det(γ)={np.mean(data['gamma_xx'] * data['gamma_yy'] * data['gamma_zz']):8.6f}")

def main():
    parser = argparse.ArgumentParser(description="Verifica el estado de la simulación.")
    parser.add_argument('--resolution', type=int, required=True, choices=[32, 64, 128],
                        help="Resolución de la simulación a verificar.")
    
    args = parser.parse_args()
    check_simulation_status(args.resolution)

if __name__ == "__main__":
    main()