#!/usr/bin/env python3
"""
Simulador BSSN Multiplataforma con Aceleración GPU
Compatible con Windows/Linux y soporte para CUDA/CuPy y OpenCL

Fecha: 14 de diciembre de 2025
Autor: Universo Centrífugo Research Team
"""

import os
import sys
import time
import platform
import numpy as np
import multiprocessing as mp
from pathlib import Path
import warnings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importar gestor de checkpoints
from .checkpoint_manager import CheckpointManager

# Detectar plataforma
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Suprimir advertencias para mejor rendimiento
warnings.filterwarnings('ignore')

class GPUAccelerator:
    """Gestor de aceleración GPU con soporte para CuPy y OpenCL"""
    
    def __init__(self):
        self.gpu_available = False
        self.gpu_type = None
        self.gpu_memory = None
        self.cupy_available = False
        self.opencl_available = False
        
        self._detect_gpu_capabilities()
    
    def _detect_gpu_capabilities(self):
        """Detecta capacidades GPU disponibles"""
        logger.info("🔍 Detectando capacidades GPU...")
        
        # Intentar importar CuPy (NVIDIA CUDA)
        try:
            import cupy as cp
            self.cupy_available = True
            self.gpu_type = "CUDA"
            self.gpu_available = True
            
            # Obtener información de la GPU
            if hasattr(cp.cuda, 'getDeviceCount'):
                device_count = cp.cuda.getDeviceCount()
                if device_count > 0:
                    device_props = cp.cuda.Device(0).attributes
                    self.gpu_memory = cp.cuda.Device(0).mem_info[1] / (1024**3)  # GB
                    logger.info(f"✅ GPU CUDA detectada: {device_count} dispositivos")
                    logger.info(f"   Memoria GPU: {self.gpu_memory:.1f} GB")
                else:
                    self.gpu_available = False
                    logger.warning("⚠️  CuPy disponible pero no se detectaron dispositivos CUDA")
        except ImportError:
            logger.info("❌ CuPy no disponible")
        
        # Intentar importar PyOpenCL (alternativa multiplataforma)
        if not self.gpu_available:
            try:
                import pyopencl as cl
                self.opencl_available = True
                
                platforms = cl.get_platforms()
                if platforms:
                    devices = platforms[0].get_devices()
                    if devices:
                        self.gpu_type = "OpenCL"
                        self.gpu_available = True
                        self.gpu_memory = devices[0].global_mem_size / (1024**3)  # GB
                        logger.info(f"✅ GPU OpenCL detectada: {len(devices)} dispositivos")
                        logger.info(f"   Memoria GPU: {self.gpu_memory:.1f} GB")
                    else:
                        logger.warning("⚠️  OpenCL disponible pero no se detectaron dispositivos")
                else:
                    logger.warning("⚠️  OpenCL disponible pero no se detectaron plataformas")
            except ImportError:
                logger.info("❌ PyOpenCL no disponible")
        
        if not self.gpu_available:
            logger.info("ℹ️  No se detectó GPU disponible, usando CPU")
    
    def get_array_module(self):
        """Devuelve el módulo de arrays apropiado (numpy o cupy)"""
        if self.cupy_available and self.gpu_available:
            try:
                import cupy as cp
                return cp
            except:
                pass
        return np
    
    def to_gpu(self, array):
        """Mueve un array a GPU si está disponible"""
        if self.cupy_available and self.gpu_available:
            try:
                import cupy as cp
                return cp.asarray(array)
            except:
                pass
        return array
    
    def to_cpu(self, array):
        """Mueve un array a CPU si está en GPU"""
        if self.cupy_available and self.gpu_available:
            try:
                import cupy as cp
                if isinstance(array, cp.ndarray):
                    return cp.asnumpy(array)
            except:
                pass
        return array
    
    def synchronize(self):
        """Sincroniza operaciones GPU si es necesario"""
        if self.cupy_available and self.gpu_available:
            try:
                import cupy as cp
                cp.cuda.Stream.null.synchronize()
            except:
                pass

class EinsteinSimulatorGPU:
    """
    Simulador de las ecuaciones de Einstein con aceleración GPU y checkpoints robustos.
    Compatible con Windows y Linux.
    """
    
    def __init__(self, data_file="simulation_initial_data.npz", 
                 max_cores=None, use_gpu=True, checkpoint_config=None):
        """
        Inicializa el simulador con soporte GPU y checkpoints.
        
        Args:
            data_file: Archivo con datos iniciales
            max_cores: Número máximo de cores a usar
            use_gpu: Usar aceleración GPU si está disponible
            checkpoint_config: Configuración personalizada de checkpoints
        """
        print("🚀 Inicializando Einstein Simulator GPU...")
        print("=" * 60)
        
        # Configuración del sistema
        self.available_cores = mp.cpu_count()
        self.max_cores = max_cores if max_cores else self.available_cores
        
        # Inicializar acelerador GPU
        self.gpu_accelerator = GPUAccelerator()
        self.use_gpu = use_gpu and self.gpu_accelerator.gpu_available
        
        # Obtener módulo de arrays apropiado
        self.xp = self.gpu_accelerator.get_array_module()
        
        print(f"💻 Sistema detectado:")
        print(f"   Plataforma: {platform.system()}")
        print(f"   Cores disponibles: {self.available_cores}")
        print(f"   Cores a utilizar: {self.max_cores}")
        print(f"   GPU: {'✓ Activada' if self.use_gpu else '✗ Desactivada'}")
        if self.use_gpu:
            print(f"   Tipo GPU: {self.gpu_accelerator.gpu_type}")
            print(f"   Memoria GPU: {self.gpu_accelerator.gpu_memory:.1f} GB")
        
        # Inicializar gestor de checkpoints
        checkpoint_config = checkpoint_config or {}
        self.checkpoint_manager = CheckpointManager(**checkpoint_config)
        
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
        
        # Mover datos a GPU si está disponible
        if self.use_gpu:
            self.T_initial = self.gpu_accelerator.to_gpu(self.T_initial)
        
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
        self.gamma_xx = self.xp.ones(self.grid_shape)
        self.gamma_yy = self.xp.ones(self.grid_shape) 
        self.gamma_zz = self.xp.ones(self.grid_shape)
        self.gamma_xy = self.xp.zeros(self.grid_shape)
        self.gamma_xz = self.xp.zeros(self.grid_shape)
        self.gamma_yz = self.xp.zeros(self.grid_shape)
        
        # Curvatura extrínseca (inicialmente cero)
        self.K_xx = self.xp.zeros(self.grid_shape)
        self.K_yy = self.xp.zeros(self.grid_shape)
        self.K_zz = self.xp.zeros(self.grid_shape)
        self.K_xy = self.xp.zeros(self.grid_shape)
        self.K_xz = self.xp.zeros(self.grid_shape)
        self.K_yz = self.xp.zeros(self.grid_shape)
        
        # Variables auxiliares BSSN
        self.phi = self.xp.zeros(self.grid_shape)  # Factor conforme
        self.chi = self.xp.ones(self.grid_shape)   # Factor conforme alternativo
        self.alpha = self.xp.ones(self.grid_shape) # Función de lapse
        self.beta_x = self.xp.zeros(self.grid_shape) # Vector de shift
        self.beta_y = self.xp.zeros(self.grid_shape)
        self.beta_z = self.xp.zeros(self.grid_shape)
        
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
        Optimizado para GPU si está disponible.
        """
        # Usar el módulo apropiado (numpy o cupy)
        xp = self.xp
        
        nx, ny, nz = field.shape
        
        # Derivadas en x
        d_dx = xp.zeros_like(field)
        d_dx[1:-1, :, :] = (field[2:, :, :] - field[:-2, :, :]) / (2 * self.dx)
        
        # Derivadas en y
        d_dy = xp.zeros_like(field)
        d_dy[:, 1:-1, :] = (field[:, 2:, :] - field[:, :-2, :]) / (2 * self.dy)
        
        # Derivadas en z
        d_dz = xp.zeros_like(field)
        d_dz[:, :, 1:-1] = (field[:, :, 2:] - field[:, :, :-2]) / (2 * self.dz)
                
        return d_dx, d_dy, d_dz
    
    def compute_stress_energy_contribution(self, t):
        """
        Calcula la contribución del tensor de energía-momento.
        En nuestro caso, el tensor está promediado en tiempo, pero podemos
        incluir una modulación temporal suave.
        """
        # Modulación temporal suave (opcional)
        time_modulation = 1.0 + 0.1 * self.xp.sin(2 * self.xp.pi * t)
        
        return self.T_initial * time_modulation
    
    def evolve_metric_component_gpu(self, component_data, sources, dt):
        """
        Evoluciona un componente específico de la métrica usando GPU.
        Versión optimizada para procesamiento paralelo en GPU.
        """
        xp = self.xp
        
        # Calcular derivadas espaciales
        d_dx, d_dy, d_dz = self.compute_spatial_derivatives(component_data)
        
        # Términos de disipación artificial (para estabilidad numérica)
        dissipation_term = xp.zeros_like(component_data)
        
        # Calcular laplaciano para disipación
        dissipation_term[1:-1, 1:-1, 1:-1] = self.dissipation * (
            component_data[2:, 1:-1, 1:-1] - 2*component_data[1:-1, 1:-1, 1:-1] + component_data[:-2, 1:-1, 1:-1] +
            component_data[1:-1, 2:, 1:-1] - 2*component_data[1:-1, 1:-1, 1:-1] + component_data[1:-1, :-2, 1:-1] +
            component_data[1:-1, 1:-1, 2:] - 2*component_data[1:-1, 1:-1, 1:-1] + component_data[1:-1, 1:-1, :-2]
        )
        
        # Evolución temporal (Euler forward)
        new_component = component_data + dt * (sources + dissipation_term)
        
        return new_component
    
    def run_single_timestep(self, t):
        """
        Ejecuta un paso temporal completo de la simulación.
        Utiliza aceleración GPU si está disponible.
        """
        # Calcular fuentes del tensor energía-momento
        T_current = self.compute_stress_energy_contribution(t)
        
        # Evolucionar componentes métricos
        self.gamma_xx = self.evolve_metric_component_gpu(
            self.gamma_xx, T_current[:,:,:,0,0], self.dt
        )
        self.gamma_yy = self.evolve_metric_component_gpu(
            self.gamma_yy, T_current[:,:,:,1,1], self.dt
        )
        self.gamma_zz = self.evolve_metric_component_gpu(
            self.gamma_zz, T_current[:,:,:,2,2], self.dt
        )
        self.gamma_xy = self.evolve_metric_component_gpu(
            self.gamma_xy, T_current[:,:,:,0,1], self.dt
        )
        self.gamma_xz = self.evolve_metric_component_gpu(
            self.gamma_xz, T_current[:,:,:,0,2], self.dt
        )
        self.gamma_yz = self.evolve_metric_component_gpu(
            self.gamma_yz, T_current[:,:,:,1,2], self.dt
        )
        
        # Aplicar condiciones de frontera
        self.apply_boundary_conditions()
        
        # Sincronizar GPU si es necesario
        if self.use_gpu:
            self.gpu_accelerator.synchronize()
        
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
        
        # Mover a CPU para cálculos si es necesario
        if self.use_gpu:
            det_gamma = self.gpu_accelerator.to_cpu(det_gamma)
            trace_K = self.gpu_accelerator.to_cpu(trace_K)
            gamma_xx_cpu = self.gpu_accelerator.to_cpu(self.gamma_xx)
        
        return {
            'det_gamma': np.mean(det_gamma),
            'trace_K': np.mean(trace_K),
            'gamma_xx_max': np.max(gamma_xx_cpu) if self.use_gpu else np.max(self.gamma_xx),
            'gamma_xx_min': np.min(gamma_xx_cpu) if self.use_gpu else np.min(self.gamma_xx)
        }
    
    def get_simulation_state(self):
        """Obtiene el estado completo de la simulación para checkpoints"""
        state = {
            'gamma_xx': self.gpu_accelerator.to_cpu(self.gamma_xx),
            'gamma_yy': self.gpu_accelerator.to_cpu(self.gamma_yy),
            'gamma_zz': self.gpu_accelerator.to_cpu(self.gamma_zz),
            'gamma_xy': self.gpu_accelerator.to_cpu(self.gamma_xy),
            'gamma_xz': self.gpu_accelerator.to_cpu(self.gamma_xz),
            'gamma_yz': self.gpu_accelerator.to_cpu(self.gamma_yz),
            'K_xx': self.gpu_accelerator.to_cpu(self.K_xx),
            'K_yy': self.gpu_accelerator.to_cpu(self.K_yy),
            'K_zz': self.gpu_accelerator.to_cpu(self.K_zz),
            'K_xy': self.gpu_accelerator.to_cpu(self.K_xy),
            'K_xz': self.gpu_accelerator.to_cpu(self.K_xz),
            'K_yz': self.gpu_accelerator.to_cpu(self.K_yz),
            'phi': self.gpu_accelerator.to_cpu(self.phi),
            'chi': self.gpu_accelerator.to_cpu(self.chi),
            'alpha': self.gpu_accelerator.to_cpu(self.alpha),
            'beta_x': self.gpu_accelerator.to_cpu(self.beta_x),
            'beta_y': self.gpu_accelerator.to_cpu(self.beta_y),
            'beta_z': self.gpu_accelerator.to_cpu(self.beta_z),
        }
        return state
    
    def restore_simulation_state(self, state):
        """Restaura el estado completo de la simulación desde un checkpoint"""
        self.gamma_xx = self.gpu_accelerator.to_gpu(state['gamma_xx'])
        self.gamma_yy = self.gpu_accelerator.to_gpu(state['gamma_yy'])
        self.gamma_zz = self.gpu_accelerator.to_gpu(state['gamma_zz'])
        self.gamma_xy = self.gpu_accelerator.to_gpu(state['gamma_xy'])
        self.gamma_xz = self.gpu_accelerator.to_gpu(state['gamma_xz'])
        self.gamma_yz = self.gpu_accelerator.to_gpu(state['gamma_yz'])
        self.K_xx = self.gpu_accelerator.to_gpu(state['K_xx'])
        self.K_yy = self.gpu_accelerator.to_gpu(state['K_yy'])
        self.K_zz = self.gpu_accelerator.to_gpu(state['K_zz'])
        self.K_xy = self.gpu_accelerator.to_gpu(state['K_xy'])
        self.K_xz = self.gpu_accelerator.to_gpu(state['K_xz'])
        self.K_yz = self.gpu_accelerator.to_gpu(state['K_yz'])
        self.phi = self.gpu_accelerator.to_gpu(state['phi'])
        self.chi = self.gpu_accelerator.to_gpu(state['chi'])
        self.alpha = self.gpu_accelerator.to_gpu(state['alpha'])
        self.beta_x = self.gpu_accelerator.to_gpu(state['beta_x'])
        self.beta_y = self.gpu_accelerator.to_gpu(state['beta_y'])
        self.beta_z = self.gpu_accelerator.to_gpu(state['beta_z'])
    
    def get_simulation_params(self):
        """Obtiene parámetros de la simulación"""
        return {
            'dt': self.dt,
            't_final': self.t_final,
            'n_steps': self.n_steps,
            'grid_shape': self.grid_shape,
            'dx': self.dx, 'dy': self.dy, 'dz': self.dz,
            'dissipation': self.dissipation,
            'use_gpu': self.use_gpu,
            'gpu_type': self.gpu_accelerator.gpu_type if self.use_gpu else None
        }
    
    def run_simulation(self, save_checkpoints=True, verbose=True, resume_from_checkpoint=None):
        """
        Ejecuta la simulación completa con monitoreo en tiempo real.
        Puede reanudar desde un checkpoint si se proporciona.
        """
        start_step = 0
        t = 0.0
        
        # Intentar cargar desde checkpoint
        if resume_from_checkpoint == "auto":
            # Buscar automáticamente el checkpoint más reciente
            latest_checkpoint = self.checkpoint_manager.get_latest_checkpoint()
            if latest_checkpoint:
                resume_from_checkpoint = latest_checkpoint['filepath']
                logger.info(f"Checkpoint automático encontrado: {resume_from_checkpoint}")
        
        if resume_from_checkpoint:
            state, params = self.checkpoint_manager.load_checkpoint(resume_from_checkpoint)
            if state is not None:
                self.restore_simulation_state(state)
                start_step = int(state.get('step', 0)) + 1
                t = float(state.get('time', 0.0))
                logger.info(f"✓ Checkpoint cargado. Reanudando desde el paso {start_step} (t={t:.4f})")
            else:
                logger.warning("⚠️  No se pudo cargar el checkpoint. Iniciando desde cero.")

        print("\n🚀 Iniciando simulación numérica...")
        print("=" * 60)
        
        start_time = time.time()
        step = start_step
        
        try:
            for step in range(start_step, self.n_steps):
                # Evolucionar un paso temporal
                t = self.run_single_timestep(t)
                
                # Monitoreo y estadísticas
                if step % self.output_every == 0:
                    invariants = self.compute_metric_invariants()
                    
                    elapsed = time.time() - start_time
                    progress = (step + 1) / self.n_steps * 100
                    eta = elapsed / (step + 1) * (self.n_steps - step - 1) if step > 0 else 0
                    
                    if verbose:
                        print(f"Paso {step+1:6d}/{self.n_steps} | "
                              f"t={t:.4f} | "
                              f"Progreso: {progress:5.1f}% | "
                              f"ETA: {eta/60:.1f}min")
                        print(f"  det(γ)={invariants['det_gamma']:.6f} | "
                              f"tr(K)={invariants['trace_K']:.6f}")
                    
                    # Guardar checkpoint
                    if save_checkpoints:
                        checkpoint_file = self.checkpoint_manager.save_checkpoint(
                            step, t, 
                            self.get_simulation_state(),
                            self.get_simulation_params()
                        )
                        if checkpoint_file and verbose:
                            print(f"  Checkpoint guardado: {Path(checkpoint_file).name}")
                    
                    # Almacenar para análisis posterior
                    self.time_evolution.append(t)
                    self.metric_evolution.append(invariants.copy())
                
                # Verificar estabilidad
                gamma_xx_cpu = self.gpu_accelerator.to_cpu(self.gamma_xx) if self.use_gpu else self.gamma_xx
                if not np.all(np.isfinite(gamma_xx_cpu)):
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
            if step > start_step:
                print(f"⏱️  Tiempo total: {total_time/60:.2f} minutos")
                print(f"⚡ Rendimiento: {(step - start_step)*self.total_points/total_time/1000:.1f}k puntos/segundo")
                if self.use_gpu:
                    print(f"🚀 Aceleración GPU: {self.gpu_accelerator.gpu_type}")
            
            # Guardar resultados finales
            self.save_final_results()
    
    def get_final_results_dict(self):
        """Retorna un diccionario con los resultados finales de la simulación."""
        return {
            'time_evolution': np.array(self.time_evolution),
            'metric_evolution': self.metric_evolution,
            'final_gamma_xx': self.gpu_accelerator.to_cpu(self.gamma_xx),
            'final_gamma_yy': self.gpu_accelerator.to_cpu(self.gamma_yy),
            'final_gamma_zz': self.gpu_accelerator.to_cpu(self.gamma_zz),
            'final_gamma_xy': self.gpu_accelerator.to_cpu(self.gamma_xy),
            'final_gamma_xz': self.gpu_accelerator.to_cpu(self.gamma_xz),
            'final_gamma_yz': self.gpu_accelerator.to_cpu(self.gamma_yz),
            'simulation_parameters': self.get_simulation_params(),
            'gpu_info': {
                'gpu_available': self.gpu_accelerator.gpu_available,
                'gpu_type': self.gpu_accelerator.gpu_type,
                'gpu_memory_gb': self.gpu_accelerator.gpu_memory
            }
        }
    
    def save_final_results(self) -> str:
        """Guarda los resultados finales de la simulación"""
        results = self.get_final_results_dict()
        output_file = "simulation_results_gpu.npz"
        np.savez_compressed(output_file, **results)
        print(f"💾 Resultados guardados en: {output_file}")
        return output_file

def main():
    """Función principal para ejecutar la simulación"""
    print("Einstein Simulator GPU - Relatividad General 4D")
    print("Simulación numérica multiplataforma con aceleración GPU")
    print("=" * 60)
    
    # Verificar que existen los datos iniciales
    data_file = "simulation_initial_data.npz"
    if not os.path.exists(data_file):
        print(f"❌ Error: No se encontró {data_file}")
        print("   Ejecute primero: python computational_implementation/simulations/setup_numerical_simulation.py")
        sys.exit(1)
    
    try:
        # Configuración de checkpoints
        checkpoint_config = {
            'checkpoint_dir': 'checkpoints',
            'frequent_interval': 100,  # Cada 100 pasos
            'periodic_interval': 1000,  # Cada 1000 pasos
            'max_checkpoints': 10,
            'compression_level': 6
        }
        
        # Crear y configurar simulador
        simulator = EinsteinSimulatorGPU(
            data_file=data_file,
            max_cores=None,  # Usar todos los cores disponibles
            use_gpu=True,  # Usar GPU si está disponible
            checkpoint_config=checkpoint_config
        )
        
        # Ejecutar simulación
        simulator.run_simulation(
            save_checkpoints=True,
            verbose=True,
            resume_from_checkpoint="auto"  # Reanudar automáticamente desde checkpoint
        )
        
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()