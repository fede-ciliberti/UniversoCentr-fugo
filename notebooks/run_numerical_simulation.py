#!/usr/bin/env python3
"""
Script de simulación numérica completa - Relatividad General 4D
Aproximación 3: Simulación Numérica Optimizada para CPU Multi-core

Este script implementa una versión simplificada del formalismo BSSN para evolucionar
las ecuaciones de Einstein en el tiempo, usando los datos iniciales generados por
setup_numerical_simulation.py

Optimizaciones implementadas:
- Paralelización masiva con multiprocessing
- JIT compilation con numba
- Procesamiento vectorizado con numpy
- Gestión eficiente de memoria

Fecha: 26 de junio de 2025
Autor: Universo Centrífugo Research Team
"""

import numpy as np
import multiprocessing as mp
from multiprocessing import Pool, shared_memory
import time
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import warnings

# Intentar importar numba para aceleración JIT
try:
    from numba import jit, prange, set_num_threads
    NUMBA_AVAILABLE = True
    # Configurar numba para usar todos los cores
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

# Funciones numba independientes (fuera de la clase)
@jit(nopython=True, parallel=True) if NUMBA_AVAILABLE else lambda f: f
def _compute_spatial_derivatives_numba(field, dx, dy, dz):
    """
    Calcula derivadas espaciales usando diferencias finitas centradas.
    Optimizado con numba para paralelización automática.
    """
    nx, ny, nz = field.shape
    
    # Derivadas en x
    d_dx = np.zeros_like(field)
    for i in prange(1, nx-1):
        for j in prange(ny):
            for k in prange(nz):
                d_dx[i,j,k] = (field[i+1,j,k] - field[i-1,j,k]) / (2 * dx)
    
    # Derivadas en y
    d_dy = np.zeros_like(field)
    for i in prange(nx):
        for j in prange(1, ny-1):
            for k in prange(nz):
                d_dy[i,j,k] = (field[i,j+1,k] - field[i,j-1,k]) / (2 * dy)
    
    # Derivadas en z
    d_dz = np.zeros_like(field)
    for i in prange(nx):
        for j in prange(ny):
            for k in prange(1, nz-1):
                d_dz[i,j,k] = (field[i,j,k+1] - field[i,j,k-1]) / (2 * dz)
                
    return d_dx, d_dy, d_dz

@jit(nopython=True) if NUMBA_AVAILABLE else lambda f: f
def _evolve_metric_component_numba(component_data, sources, dt, dissipation, dx, dy, dz):
    """
    Evoluciona un componente específico de la métrica.
    Optimizado con numba y diseñado para paralelización.
    """
    # Calcular derivadas espaciales
    d_dx, d_dy, d_dz = _compute_spatial_derivatives_numba(component_data, dx, dy, dz)
    
    # Términos de disipación artificial (para estabilidad numérica)
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
    
    # Evolución temporal (Euler forward)
    new_component = component_data + dt * (sources + dissipation_term)
    
    return new_component

def _evolve_metric_component_multiprocess(args):
    """
    Función independiente para evolución de componentes métricos.
    Diseñada para ser usada con multiprocessing.
    """
    component_name, component_data, sources, dt, dissipation, dx, dy, dz = args
    
    # Llamar a la función optimizada con numba
    new_component = _evolve_metric_component_numba(
        component_data, sources, dt, dissipation, dx, dy, dz
    )
    
    return component_name, new_component

class EinsteinSimulator:
    """
    Simulador de las ecuaciones de Einstein usando formalismo BSSN simplificado.
    Optimizado para ejecución paralela en CPU multi-core.
    """
    
    def __init__(self, data_file="simulation_initial_data.npz", max_cores=None):
        """
        Inicializa el simulador cargando los datos iniciales.
        
        Args:
            data_file: Archivo con datos iniciales generado por setup_numerical_simulation.py
            max_cores: Número máximo de cores a usar (None = todos disponibles)
        """
        print("🚀 Inicializando Einstein Simulator...")
        print("=" * 60)
        
        # Configuración del sistema
        self.available_cores = mp.cpu_count()
        self.max_cores = max_cores if max_cores else self.available_cores
        self.use_numba = NUMBA_AVAILABLE
        
        print(f"💻 Sistema detectado:")
        print(f"   Cores disponibles: {self.available_cores}")
        print(f"   Cores a utilizar: {self.max_cores}")
        print(f"   Aceleración Numba: {'✓ Activada' if self.use_numba else '✗ No disponible'}")
        
        # Cargar datos iniciales
        self.load_initial_data(data_file)
        
        # Inicializar variables de evolución
        self.initialize_evolution_variables()
        
        # Configurar parámetros de simulación
        self.setup_simulation_parameters()
        
        print("✓ Simulador inicializado correctamente")
    
    def load_initial_data(self, data_file):
        """Carga los datos iniciales desde el archivo .npz"""
        print(f"📁 Cargando datos iniciales desde {data_file}...")
        
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"No se encontró el archivo {data_file}")
        
        # Cargar datos
        data = np.load(data_file)
        self.X = data['X']
        self.Y = data['Y'] 
        self.Z = data['Z']
        self.T_initial = data['T_mu_nu_evaluated']
        
        # Extraer parámetros de la malla
        self.grid_shape = self.X.shape
        self.nx, self.ny, self.nz = self.grid_shape
        self.total_points = self.nx * self.ny * self.nz
        
        # Calcular espaciado de la malla
        self.dx = self.X[1, 0, 0] - self.X[0, 0, 0]
        self.dy = self.Y[0, 1, 0] - self.Y[0, 0, 0]
        self.dz = self.Z[0, 0, 1] - self.Z[0, 0, 0]
        
        print(f"✓ Datos cargados:")
        print(f"   Resolución: {self.nx}×{self.ny}×{self.nz} = {self.total_points:,} puntos")
        print(f"   Espaciado: Δx={self.dx:.3f}, Δy={self.dy:.3f}, Δz={self.dz:.3f}")
        print(f"   Memoria tensor: {self.T_initial.nbytes / (1024**2):.1f} MB")
    
    def initialize_evolution_variables(self):
        """Inicializa las variables de evolución del formalismo BSSN"""
        print("🔧 Inicializando variables de evolución BSSN...")
        
        # Variables métricas principales (simplificadas)
        # En BSSN: γ_ij (métrica espacial), K_ij (curvatura extrínseca)
        
        # Métrica espacial (inicialmente plana con perturbaciones pequeñas)
        self.gamma_xx = np.ones(self.grid_shape)
        self.gamma_yy = np.ones(self.grid_shape) 
        self.gamma_zz = np.ones(self.grid_shape)
        self.gamma_xy = np.zeros(self.grid_shape)
        self.gamma_xz = np.zeros(self.grid_shape)
        self.gamma_yz = np.zeros(self.grid_shape)
        
        # Curvatura extrínseca (inicialmente cero)
        self.K_xx = np.zeros(self.grid_shape)
        self.K_yy = np.zeros(self.grid_shape)
        self.K_zz = np.zeros(self.grid_shape)
        self.K_xy = np.zeros(self.grid_shape)
        self.K_xz = np.zeros(self.grid_shape)
        self.K_yz = np.zeros(self.grid_shape)
        
        # Variables auxiliares BSSN
        self.phi = np.zeros(self.grid_shape)  # Factor conforme
        self.chi = np.ones(self.grid_shape)   # Factor conforme alternativo
        self.alpha = np.ones(self.grid_shape) # Función de lapse
        self.beta_x = np.zeros(self.grid_shape) # Vector de shift
        self.beta_y = np.zeros(self.grid_shape)
        self.beta_z = np.zeros(self.grid_shape)
        
        print("✓ Variables BSSN inicializadas")
        
    def setup_simulation_parameters(self):
        """Configura parámetros de la simulación"""
        print("⚙️  Configurando parámetros de simulación...")
        
        # Parámetros temporales
        self.dt = 0.001  # Paso temporal (muy pequeño para estabilidad)
        self.t_final = 1.0  # Tiempo final de simulación  
        self.output_every = 10  # Guardar datos cada N pasos
        
        # Calcular número de pasos
        self.n_steps = int(self.t_final / self.dt)
        self.n_outputs = self.n_steps // self.output_every
        
        # Parámetros de estabilidad (necesarios para BSSN)
        self.cfl_factor = 0.25  # Factor CFL para estabilidad
        self.dissipation = 0.01  # Disipación artificial
        
        # Arrays para almacenar resultados
        self.time_evolution = []
        self.metric_evolution = []
        
        print(f"✓ Parámetros configurados:")
        print(f"   Paso temporal: dt = {self.dt}")
        print(f"   Tiempo final: {self.t_final}")
        print(f"   Número de pasos: {self.n_steps:,}")
        print(f"   Salidas cada: {self.output_every} pasos")
        print(f"   Total salidas: {self.n_outputs}")

    def compute_spatial_derivatives(self, field):
        """
        Calcula derivadas espaciales usando diferencias finitas centradas.
        Optimizado con numba para paralelización automática.
        """
        return _compute_spatial_derivatives_numba(field, self.dx, self.dy, self.dz)

    def compute_stress_energy_contribution(self, t):
        """
        Calcula la contribución del tensor de energía-momento.
        En nuestro caso, el tensor está promediado en tiempo, pero podemos
        incluir una modulación temporal suave.
        """
        # Modulación temporal suave (opcional)
        time_modulation = 1.0 + 0.1 * np.sin(2 * np.pi * t)
        
        return self.T_initial * time_modulation

    def evolve_metric_component(self, args):
        """
        Evoluciona un componente específico de la métrica.
        Versión simplificada que usa las funciones numba optimizadas.
        """
        component_name, component_data, sources, dt = args
        
        # Usar la función numba optimizada
        new_component = _evolve_metric_component_numba(
            component_data, sources, dt, self.dissipation, self.dx, self.dy, self.dz
        )
        
        return component_name, new_component

    def run_single_timestep(self, t):
        """
        Ejecuta un paso temporal completo de la simulación.
        Utiliza paralelización para evolucionar diferentes componentes.
        """
        # Calcular fuentes del tensor energía-momento
        T_current = self.compute_stress_energy_contribution(t)
        
        # Preparar argumentos para evolución paralela (con parámetros adicionales para numba)
        evolution_tasks = [
            ('gamma_xx', self.gamma_xx, T_current[:,:,:,0,0], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_yy', self.gamma_yy, T_current[:,:,:,1,1], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_zz', self.gamma_zz, T_current[:,:,:,2,2], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_xy', self.gamma_xy, T_current[:,:,:,0,1], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_xz', self.gamma_xz, T_current[:,:,:,0,2], self.dt, self.dissipation, self.dx, self.dy, self.dz),
            ('gamma_yz', self.gamma_yz, T_current[:,:,:,1,2], self.dt, self.dissipation, self.dx, self.dy, self.dz),
        ]
        
        # Evolución paralela de componentes usando función independiente
        if self.max_cores > 1:
            with Pool(self.max_cores) as pool:
                results = pool.map(_evolve_metric_component_multiprocess, evolution_tasks)
        else:
            results = [_evolve_metric_component_multiprocess(task) for task in evolution_tasks]
        
        # Actualizar componentes
        for name, new_data in results:
            setattr(self, name, new_data)
        
        # Aplicar condiciones de frontera (simplificadas)
        self.apply_boundary_conditions()
        
        return t + self.dt

    def apply_boundary_conditions(self):
        """Aplica condiciones de frontera a las variables de evolución"""
        # Condiciones de frontera de salida (outgoing wave)
        # Simplificado: extrapolación de orden cero en las fronteras
        
        components = [self.gamma_xx, self.gamma_yy, self.gamma_zz,
                     self.gamma_xy, self.gamma_xz, self.gamma_yz]
        
        for comp in components:
            # Fronteras en x
            comp[0, :, :] = comp[1, :, :]
            comp[-1, :, :] = comp[-2, :, :]
            
            # Fronteras en y
            comp[:, 0, :] = comp[:, 1, :]
            comp[:, -1, :] = comp[:, -2, :]
            
            # Fronteras en z
            comp[:, :, 0] = comp[:, :, 1]
            comp[:, :, -1] = comp[:, :, -2]

    def compute_metric_invariants(self):
        """Calcula invariantes de la métrica para monitoreo"""
        # Determinante de la métrica espacial (simplificado para métrica diagonal)
        det_gamma = self.gamma_xx * self.gamma_yy * self.gamma_zz
        
        # Traza de la curvatura extrínseca
        trace_K = self.K_xx + self.K_yy + self.K_zz
        
        return {
            'det_gamma': np.mean(det_gamma),
            'trace_K': np.mean(trace_K),
            'gamma_xx_max': np.max(self.gamma_xx),
            'gamma_xx_min': np.min(self.gamma_xx)
        }

    def save_checkpoint(self, step, t):
        """Guarda un checkpoint de la simulación"""
        checkpoint_data = {
            'step': step,
            'time': t,
            'gamma_xx': self.gamma_xx,
            'gamma_yy': self.gamma_yy,
            'gamma_zz': self.gamma_zz,
            'gamma_xy': self.gamma_xy,
            'gamma_xz': self.gamma_xz,
            'gamma_yz': self.gamma_yz,
            'K_xx': self.K_xx,
            'K_yy': self.K_yy,
            'K_zz': self.K_zz,
        }
        
        filename = f"checkpoint_step_{step:06d}.npz"
        np.savez_compressed(filename, **checkpoint_data)
        return filename

    def run_simulation(self, save_checkpoints=True, verbose=True):
        """
        Ejecuta la simulación completa con monitoreo en tiempo real.
        """
        print("\n🚀 Iniciando simulación numérica...")
        print("=" * 60)
        
        start_time = time.time()
        t = 0.0
        
        # Configurar visualización en tiempo real
        if verbose:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle('Evolución de la Métrica Espacial', fontsize=14)
            plt.ion()
        
        try:
            for step in range(self.n_steps):
                # Evolucionar un paso temporal
                t = self.run_single_timestep(t)
                
                # Monitoreo y estadísticas
                if step % self.output_every == 0:
                    invariants = self.compute_metric_invariants()
                    
                    elapsed = time.time() - start_time
                    progress = (step + 1) / self.n_steps * 100
                    eta = elapsed / (step + 1) * (self.n_steps - step - 1)
                    
                    if verbose:
                        print(f"Paso {step+1:6d}/{self.n_steps} | "
                              f"t={t:.4f} | "
                              f"Progreso: {progress:5.1f}% | "
                              f"ETA: {eta/60:.1f}min")
                        print(f"  det(γ)={invariants['det_gamma']:.6f} | "
                              f"tr(K)={invariants['trace_K']:.6f}")
                    
                    # Actualizar visualización
                    if verbose and step % (self.output_every * 5) == 0:
                        self.update_visualization(axes, t, invariants)
                    
                    # Guardar checkpoint
                    if save_checkpoints and step % (self.output_every * 10) == 0:
                        checkpoint_file = self.save_checkpoint(step, t)
                        if verbose:
                            print(f"  Checkpoint guardado: {checkpoint_file}")
                    
                    # Almacenar para análisis posterior
                    self.time_evolution.append(t)
                    self.metric_evolution.append(invariants.copy())
                
                # Verificar estabilidad
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
            if verbose:
                plt.ioff()
                plt.show()
            
            print(f"\n✅ Simulación completada")
            print(f"⏱️  Tiempo total: {total_time/60:.2f} minutos")
            print(f"⚡ Rendimiento: {step*self.total_points/total_time/1000:.1f}k puntos/segundo")
            
            # Guardar resultados finales
            self.save_final_results()

    def update_visualization(self, axes, t, invariants):
        """Actualiza la visualización en tiempo real"""
        axes[0,0].clear()
        axes[0,0].imshow(self.gamma_xx[:,:,self.nz//2], cmap='RdBu_r')
        axes[0,0].set_title(f'γ_xx (z=0, t={t:.3f})')
        
        axes[0,1].clear()
        axes[0,1].imshow(self.gamma_yy[:,:,self.nz//2], cmap='RdBu_r')
        axes[0,1].set_title(f'γ_yy (z=0)')
        
        axes[1,0].clear()
        axes[1,0].imshow(self.gamma_zz[:,:,self.nz//2], cmap='RdBu_r')
        axes[1,0].set_title(f'γ_zz (z=0)')
        
        # Gráfico de evolución temporal
        axes[1,1].clear()
        if len(self.time_evolution) > 1:
            det_gammas = [m['det_gamma'] for m in self.metric_evolution]
            axes[1,1].plot(self.time_evolution, det_gammas, 'b-')
            axes[1,1].set_title('det(γ) vs tiempo')
            axes[1,1].set_xlabel('Tiempo')
            axes[1,1].grid(True)
        
        plt.tight_layout()
        plt.pause(0.01)

    def save_final_results(self):
        """Guarda los resultados finales de la simulación"""
        results = {
            'time_evolution': np.array(self.time_evolution),
            'metric_evolution': self.metric_evolution,
            'final_gamma_xx': self.gamma_xx,
            'final_gamma_yy': self.gamma_yy,
            'final_gamma_zz': self.gamma_zz,
            'final_gamma_xy': self.gamma_xy,
            'final_gamma_xz': self.gamma_xz,
            'final_gamma_yz': self.gamma_yz,
            'simulation_parameters': {
                'dt': self.dt,
                't_final': self.t_final,
                'n_steps': self.n_steps,
                'grid_shape': self.grid_shape,
                'dx': self.dx, 'dy': self.dy, 'dz': self.dz
            }
        }
        
        output_file = "simulation_results.npz"
        np.savez_compressed(output_file, **results)
        print(f"💾 Resultados guardados en: {output_file}")
        
        return output_file

def main():
    """Función principal para ejecutar la simulación"""
    print("Einstein Simulator - Relatividad General 4D")
    print("Simulación numérica optimizada para CPU multi-core")
    print("=" * 60)
    
    # Verificar que existen los datos iniciales
    data_file = "simulation_initial_data.npz"
    if not os.path.exists(data_file):
        print(f"❌ Error: No se encontró {data_file}")
        print("   Ejecute primero: python notebooks/setup_numerical_simulation.py")
        sys.exit(1)
    
    try:
        # Crear y configurar simulador
        simulator = EinsteinSimulator(
            data_file=data_file,
            max_cores=None  # Usar todos los cores disponibles
        )
        
        # Ejecutar simulación
        simulator.run_simulation(
            save_checkpoints=True,
            verbose=True
        )
        
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()