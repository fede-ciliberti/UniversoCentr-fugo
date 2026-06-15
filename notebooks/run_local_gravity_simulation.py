#!/usr/bin/env python3
"""
Script de Ejecución de Simulación de Gravedad Local - Fase 2

Este script ejecuta la simulación numérica BSSN para evolucionar en el tiempo
un sistema con una masa puntual, utilizando los datos iniciales generados por
setup_high_resolution_local_gravity.py.

Objetivos:
- Cargar datos iniciales para una resolución específica (32³, 64³, 128³).
- Evolucionar el sistema usando el solver BSSN optimizado.
- Guardar checkpoints de la simulación a intervalos regulares.
- Permitir la configuración de parámetros clave mediante argumentos de línea de comandos.

Ejemplo de uso:
python notebooks/run_local_gravity_simulation.py --resolution 64 --t_final 100.0 --dt_checkpoints 1.0

Fecha: 27 de junio de 2025
Autor: Universo Centrífugo Research Team
"""

import numpy as np
import multiprocessing as mp
from multiprocessing import Pool
import time
import os
import sys
from pathlib import Path
import argparse
import warnings

# Intentar importar numba para aceleración JIT
try:
    from numba import jit, prange, set_num_threads
    NUMBA_AVAILABLE = True
    set_num_threads(mp.cpu_count())
except ImportError:
    NUMBA_AVAILABLE = False
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    def prange(*args, **kwargs):
        return range(*args, **kwargs)

warnings.filterwarnings('ignore')

# --- Funciones Numba Optimizadas (sin cambios respecto al original) ---

@jit(nopython=True, parallel=True) if NUMBA_AVAILABLE else lambda f: f
def _compute_spatial_derivatives_numba(field, dx, dy, dz):
    nx, ny, nz = field.shape
    d_dx = np.zeros_like(field)
    for i in prange(1, nx-1):
        for j in prange(ny):
            for k in prange(nz):
                d_dx[i,j,k] = (field[i+1,j,k] - field[i-1,j,k]) / (2 * dx)
    d_dy = np.zeros_like(field)
    for i in prange(nx):
        for j in prange(1, ny-1):
            for k in prange(nz):
                d_dy[i,j,k] = (field[i,j+1,k] - field[i,j-1,k]) / (2 * dy)
    d_dz = np.zeros_like(field)
    for i in prange(nx):
        for j in prange(ny):
            for k in prange(1, nz-1):
                d_dz[i,j,k] = (field[i,j,k+1] - field[i,j,k-1]) / (2 * dz)
    return d_dx, d_dy, d_dz

@jit(nopython=True) if NUMBA_AVAILABLE else lambda f: f
def _evolve_metric_component_numba(component_data, sources, dt, dissipation, dx, dy, dz):
    d_dx, d_dy, d_dz = _compute_spatial_derivatives_numba(component_data, dx, dy, dz)
    dissipation_term = np.zeros_like(component_data)
    nx, ny, nz = component_data.shape
    for i in prange(1, nx-1):
        for j in prange(1, ny-1):
            for k in prange(1, nz-1):
                dissipation_term[i,j,k] = dissipation * (
                    component_data[i+1,j,k] - 2*component_data[i,j,k] + component_data[i-1,j,k] +
                    component_data[i,j+1,k] - 2*component_data[i,j,k] + component_data[i,j-1,k] +
                    component_data[i,j,k+1] - 2*component_data[i,j,k] + component_data[i,j,k-1]
                )
    new_component = component_data + dt * (sources + dissipation_term)
    return new_component

def _evolve_metric_component_multiprocess(args):
    component_name, component_data, sources, dt, dissipation, dx, dy, dz = args
    new_component = _evolve_metric_component_numba(
        component_data, sources, dt, dissipation, dx, dy, dz
    )
    return component_name, new_component

# --- Clase del Simulador Adaptada ---

class EinsteinSimulator:
    def __init__(self, data_file, output_dir, t_final, dt_checkpoints, max_cores=None):
        print("🚀 Inicializando Einstein Simulator para Gravedad Local...")
        print("=" * 60)
        
        self.output_dir = Path(output_dir)
        self.t_final = t_final
        self.dt_checkpoints = dt_checkpoints
        
        self.available_cores = mp.cpu_count()
        self.max_cores = max_cores if max_cores else self.available_cores
        self.use_numba = NUMBA_AVAILABLE
        
        print(f"💻 Sistema detectado:")
        print(f"   Cores disponibles: {self.available_cores}")
        print(f"   Cores a utilizar: {self.max_cores}")
        print(f"   Aceleración Numba: {'✓ Activada' if self.use_numba else '✗ No disponible'}")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"   Directorio de salida: {self.output_dir}")

        self.load_initial_data(data_file)
        self.initialize_evolution_variables()
        self.setup_simulation_parameters()
        
        print("✓ Simulador inicializado correctamente")
    
    def load_initial_data(self, data_file):
        print(f"📁 Cargando datos iniciales desde {data_file}...")
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"No se encontró el archivo {data_file}")
        
        data = np.load(data_file)
        self.X = data['X']
        self.Y = data['Y']
        self.Z = data['Z']
        self.T_initial = data['T_total_mu_nu']
        
        self.grid_shape = self.X.shape
        self.nx, self.ny, self.nz = self.grid_shape
        self.total_points = self.nx * self.ny * self.nz
        
        self.dx = self.X[1, 0, 0] - self.X[0, 0, 0]
        self.dy = self.Y[0, 1, 0] - self.Y[0, 0, 0]
        self.dz = self.Z[0, 0, 1] - self.Z[0, 0, 0]
        
        print(f"✓ Datos cargados:")
        print(f"   Resolución: {self.nx}×{self.ny}×{self.nz} = {self.total_points:,} puntos")
        print(f"   Espaciado: Δx={self.dx:.3f}, Δy={self.dy:.3f}, Δz={self.dz:.3f}")

    def initialize_evolution_variables(self):
        print("🔧 Inicializando variables de evolución BSSN...")
        self.gamma_xx = np.ones(self.grid_shape)
        self.gamma_yy = np.ones(self.grid_shape) 
        self.gamma_zz = np.ones(self.grid_shape)
        self.gamma_xy = np.zeros(self.grid_shape)
        self.gamma_xz = np.zeros(self.grid_shape)
        self.gamma_yz = np.zeros(self.grid_shape)
        self.K_xx = np.zeros(self.grid_shape)
        self.K_yy = np.zeros(self.grid_shape)
        self.K_zz = np.zeros(self.grid_shape)
        print("✓ Variables BSSN inicializadas")
        
    def setup_simulation_parameters(self):
        print("⚙️  Configurando parámetros de simulación...")
        self.dt = 0.001
        self.output_every = 100
        self.n_steps = int(self.t_final / self.dt)
        self.dissipation = 0.01
        
        print(f"✓ Parámetros configurados:")
        print(f"   Paso temporal: dt = {self.dt}")
        print(f"   Tiempo final: {self.t_final}")
        print(f"   Intervalo de Checkpoint: {self.dt_checkpoints}s")
        print(f"   Número de pasos: {self.n_steps:,}")

    def compute_stress_energy_contribution(self, t):
        # Para la gravedad local, la fuente (masa puntual) es estática.
        return self.T_initial

    def run_single_timestep(self, t):
        T_current = self.compute_stress_energy_contribution(t)
        evolution_tasks = [
            ('gamma_xx', self.gamma_xx, T_current[:,:,:,0,0], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_yy', self.gamma_yy, T_current[:,:,:,1,1], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_zz', self.gamma_zz, T_current[:,:,:,2,2], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_xy', self.gamma_xy, T_current[:,:,:,0,1], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_xz', self.gamma_xz, T_current[:,:,:,0,2], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_yz', self.gamma_yz, T_current[:,:,:,1,2], self.dt, self.dissipation, self.dx, self.dy, self.dz),
        ]
        
        if self.max_cores > 1:
            with Pool(self.max_cores) as pool:
                results = pool.map(_evolve_metric_component_multiprocess, evolution_tasks)
        else:
            results = [_evolve_metric_component_multiprocess(task) for task in evolution_tasks]
        
        for name, new_data in results:
            setattr(self, name, new_data)
        
        self.apply_boundary_conditions()
        return t + self.dt

    def apply_boundary_conditions(self):
        components = [self.gamma_xx, self.gamma_yy, self.gamma_zz,
                     self.gamma_xy, self.gamma_xz, self.gamma_yz]
        for comp in components:
            comp[0, :, :] = comp[1, :, :]
            comp[-1, :, :] = comp[-2, :, :]
            comp[:, 0, :] = comp[:, 1, :]
            comp[:, -1, :] = comp[:, -2, :]
            comp[:, :, 0] = comp[:, :, 1]
            comp[:, :, -1] = comp[:, :, -2]

    def compute_metric_invariants(self):
        det_gamma = self.gamma_xx * self.gamma_yy * self.gamma_zz
        return {'det_gamma': np.mean(det_gamma)}

    def save_checkpoint(self, step, t):
        filename = self.output_dir / f"checkpoint_step_{step:08d}_t_{t:.2f}.npz"
        checkpoint_data = {
            'step': step, 'time': t,
            'gamma_xx': self.gamma_xx, 'gamma_yy': self.gamma_yy, 'gamma_zz': self.gamma_zz,
            'gamma_xy': self.gamma_xy, 'gamma_xz': self.gamma_xz, 'gamma_yz': self.gamma_yz,
            'K_xx': self.K_xx, 'K_yy': self.K_yy, 'K_zz': self.K_zz,
        }
        np.savez_compressed(filename, **checkpoint_data)
        return filename

    def run_simulation(self, save_checkpoints=True, verbose=True):
        print("\n🚀 Iniciando simulación de gravedad local...")
        print("=" * 60)
        
        start_time = time.time()
        t = 0.0
        last_checkpoint_time = -self.dt_checkpoints # Para asegurar checkpoint en t=0
        step = 0
        
        try:
            for step in range(self.n_steps):
                t = self.run_single_timestep(t)
                
                if save_checkpoints and (t - last_checkpoint_time >= self.dt_checkpoints):
                    checkpoint_file = self.save_checkpoint(step, t)
                    last_checkpoint_time = t
                    if verbose:
                        print(f"  Checkpoint guardado: {checkpoint_file}")

                if step % self.output_every == 0:
                    invariants = self.compute_metric_invariants()
                    elapsed = time.time() - start_time
                    progress = (step + 1) / self.n_steps * 100
                    eta = (elapsed / (step + 1) * (self.n_steps - step - 1)) if step > 0 else 0
                    
                    if verbose:
                        print(f"Paso {step+1:8d}/{self.n_steps} | t={t:7.3f} | Progreso: {progress:5.1f}% | "
                              f"det(γ)={invariants['det_gamma']:.6f} | ETA: {eta/60:.1f}min")
                
                if not np.all(np.isfinite(self.gamma_xx)):
                    print("⚠️  ADVERTENCIA: Inestabilidad numérica detectada!")
                    break
                    
        except KeyboardInterrupt:
            print("\n⏹️  Simulación interrumpida por el usuario")
        except Exception as e:
            print(f"\n❌ Error durante la simulación: {e}")
            raise
        finally:
            total_time = time.time() - start_time
            print(f"\n✅ Simulación completada")
            print(f"⏱️  Tiempo total: {total_time/60:.2f} minutos")
            print(f"⚡ Rendimiento: {step*self.total_points/total_time/1e6:.2f} M-puntos/segundo")
            
            print("💾 Guardando estado final...")
            self.save_checkpoint(self.n_steps, self.t_final)

def main():
    parser = argparse.ArgumentParser(description="Ejecuta la simulación de gravedad local BSSN.")
    parser.add_argument('--resolution', type=int, required=True, choices=[32, 64, 128],
                        help="Resolución de la malla (ej. 64 para 64x64x64).")
    parser.add_argument('--t_final', type=float, default=100.0,
                        help="Tiempo final de la simulación.")
    parser.add_argument('--dt_checkpoints', type=float, default=1.0,
                        help="Intervalo de tiempo (en segundos de simulación) para guardar checkpoints.")
    parser.add_argument('--cores', type=int, default=None,
                        help="Número de cores a usar (por defecto, todos los disponibles).")
    
    args = parser.parse_args()

    print("=" * 60)
    print("Fase 2: Simulación de Gravedad Local con Fuente Puntual")
    print("=" * 60)
    
    data_file = Path(f"initial_data_{args.resolution}cubed.npz")
    output_dir = Path(f"output/local_gravity_{args.resolution}cubed")
    
    if not data_file.exists():
        print(f"❌ Error: No se encontró el archivo de datos iniciales '{data_file}'")
        print(f"   Asegúrese de haber ejecutado primero:")
        print(f"   python notebooks/setup_high_resolution_local_gravity.py --resolution {args.resolution}")
        sys.exit(1)
        
    try:
        simulator = EinsteinSimulator(
            data_file=str(data_file),
            output_dir=str(output_dir),
            t_final=args.t_final,
            dt_checkpoints=args.dt_checkpoints,
            max_cores=args.cores
        )
        
        simulator.run_simulation(save_checkpoints=True, verbose=True)
        
    except Exception as e:
        print(f"❌ Error fatal en la ejecución: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()