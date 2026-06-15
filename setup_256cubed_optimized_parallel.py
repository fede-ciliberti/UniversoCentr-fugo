#!/usr/bin/env python3
"""
Setup optimizado para máxima paralelización - Generado automáticamente.
Configuración calculada para 12 cores.
"""

import numpy as np
import multiprocessing as mp
from multiprocessing import Pool, shared_memory
import time
import os
import sys
from pathlib import Path
import psutil
import argparse
import json
from numba import jit, prange, set_num_threads
import warnings

warnings.filterwarnings('ignore')

class OptimizedEinstein256SimulatorParallel:
    """
    Simulador Einstein optimizado con paralelización máxima.
    """
    
    def __init__(self, chunk_size=72, memory_limit_gb=None, use_mixed_precision=True):
        print("🚀 Simulador Einstein 256³ - PARALELIZACIÓN MÁXIMA")
        print("=" * 70)
        
        # Configuración optimizada del sistema
        self.grid_size = 256
        self.chunk_size = chunk_size
        self.use_mixed_precision = use_mixed_precision
        
        # Detectar recursos y usar TODOS
        self.available_cores = mp.cpu_count()
        self.available_memory_gb = psutil.virtual_memory().total / (1024**3)
        self.memory_limit_gb = memory_limit_gb or min(self.available_memory_gb * 0.8, 64)
        
        # Configuración optimizada de chunks
        self.chunks_per_dim = self.grid_size // self.chunk_size
        self.total_chunks = self.chunks_per_dim ** 3
        self.overlap_cells = 4
        
        # PARALELIZACIÓN MÁXIMA
        self.max_workers = self.available_cores  # USAR TODOS LOS CORES
        set_num_threads(self.available_cores)     # NUMBA CON TODOS LOS THREADS
        
        print(f"💻 Configuración de paralelización:")
        print(f"   Cores disponibles: {self.available_cores}")
        print(f"   Workers paralelos: {self.max_workers} (100% de cores)")
        print(f"   Numba threads: {self.available_cores} (100% de cores)")
        print(f"   RAM disponible: {self.available_memory_gb:.1f} GB")
        print(f"   Límite de memoria: {self.memory_limit_gb:.1f} GB")
        
        print(f"📊 Configuración optimizada de chunks:")
        print(f"   Grid total: {self.grid_size}³ = {self.grid_size**3:,} puntos")
        print(f"   Chunk size: {self.chunk_size}³ = {self.chunk_size**3:,} puntos")
        print(f"   Total de chunks: {self.total_chunks}")
        print(f"   Chunks por core: {self.total_chunks/self.available_cores:.1f}")
        
        if self.total_chunks < self.available_cores:
            print("⚠️  ADVERTENCIA: Pocos chunks para paralelización óptima")
            print("   Considere reducir chunk_size para más paralelismo")
        else:
            print("✅ Configuración óptima para paralelización")
        
        # Configurar variables de entorno para máximo rendimiento
        os.environ['OMP_NUM_THREADS'] = str(self.available_cores)
        os.environ['MKL_NUM_THREADS'] = str(self.available_cores)
        os.environ['NUMBA_NUM_THREADS'] = str(self.available_cores)
        
    def setup_memory_mapped_storage_optimized(self):
        """Configura almacenamiento memory-mapped optimizado para paralelización."""
        print("💾 Configurando almacenamiento memory-mapped optimizado...")
        
        # Crear directorio de datos con permisos optimizados
        self.data_dir = Path("simulation_256cubed_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Tipo de datos optimizado
        self.dtype = np.float32 if self.use_mixed_precision else np.float64
        
        print("   Creando arrays memory-mapped con optimización paralela...")
        shape = (self.grid_size, self.grid_size, self.grid_size)
        
        # Variables métricas principales con modo optimizado
        self.gamma_xx = self._create_memmap_optimized('gamma_xx.dat', shape)
        self.gamma_yy = self._create_memmap_optimized('gamma_yy.dat', shape)
        self.gamma_zz = self._create_memmap_optimized('gamma_zz.dat', shape)
        self.gamma_xy = self._create_memmap_optimized('gamma_xy.dat', shape)
        self.gamma_xz = self._create_memmap_optimized('gamma_xz.dat', shape)
        self.gamma_yz = self._create_memmap_optimized('gamma_yz.dat', shape)
        
        # Curvatura extrínseca K_ij
        self.K_xx = self._create_memmap_optimized('K_xx.dat', shape)
        self.K_yy = self._create_memmap_optimized('K_yy.dat', shape)
        self.K_zz = self._create_memmap_optimized('K_zz.dat', shape)
        self.K_xy = self._create_memmap_optimized('K_xy.dat', shape)
        self.K_xz = self._create_memmap_optimized('K_xz.dat', shape)
        self.K_yz = self._create_memmap_optimized('K_yz.dat', shape)
        
        # Variables auxiliares BSSN
        self.phi = self._create_memmap_optimized('phi.dat', shape)
        self.chi = self._create_memmap_optimized('chi.dat', shape)
        self.K_trace = self._create_memmap_optimized('K_trace.dat', shape)
        
        # Variables de gauge
        self.alpha = self._create_memmap_optimized('alpha.dat', shape)
        self.beta_x = self._create_memmap_optimized('beta_x.dat', shape)
        self.beta_y = self._create_memmap_optimized('beta_y.dat', shape)
        self.beta_z = self._create_memmap_optimized('beta_z.dat', shape)
        
        # Campos auxiliares
        self.Gamma_x = self._create_memmap_optimized('Gamma_x.dat', shape)
        self.Gamma_y = self._create_memmap_optimized('Gamma_y.dat', shape)
        self.Gamma_z = self._create_memmap_optimized('Gamma_z.dat', shape)
        
        # Inicializar en paralelo
        self._initialize_flat_spacetime_parallel()
        
        total_size_gb = len([f for f in self.data_dir.glob('*.dat')]) * \
                       self.grid_size**3 * self.dtype().itemsize / (1024**3)
        print(f"   Total de archivos memory-mapped: {total_size_gb:.1f} GB")
        print("✅ Almacenamiento optimizado configurado")
        
    def _create_memmap_optimized(self, filename, shape):
        """Crea memory-mapped array optimizado para acceso paralelo."""
        filepath = self.data_dir / filename
        
        # Usar mode 'w+' con optimizaciones de OS
        mmap_array = np.memmap(filepath, dtype=self.dtype, mode='w+', shape=shape)
        
        # Forzar pre-asignación para mejor rendimiento paralelo
        if hasattr(mmap_array, 'flush'):
            mmap_array.flush()
            
        return mmap_array
    
    @jit(nopython=True, parallel=True)
    def _initialize_arrays_parallel(self, array, value):
        """Inicializa arrays en paralelo usando Numba."""
        flat = array.ravel()
        for i in prange(flat.size):
            flat[i] = value
    
    def _initialize_flat_spacetime_parallel(self):
        """Inicializa condiciones de espacio-tiempo plano en paralelo."""
        print("🌌 Inicializando condiciones en paralelo...")
        
        # Inicializar todos los arrays en paralelo
        self._initialize_arrays_parallel(self.gamma_xx, 1.0)
        self._initialize_arrays_parallel(self.gamma_yy, 1.0)
        self._initialize_arrays_parallel(self.gamma_zz, 1.0)
        self._initialize_arrays_parallel(self.gamma_xy, 0.0)
        self._initialize_arrays_parallel(self.gamma_xz, 0.0)
        self._initialize_arrays_parallel(self.gamma_yz, 0.0)
        
        # Curvatura extrínseca en paralelo
        self._initialize_arrays_parallel(self.K_xx, 0.0)
        self._initialize_arrays_parallel(self.K_yy, 0.0)
        self._initialize_arrays_parallel(self.K_zz, 0.0)
        self._initialize_arrays_parallel(self.K_xy, 0.0)
        self._initialize_arrays_parallel(self.K_xz, 0.0)
        self._initialize_arrays_parallel(self.K_yz, 0.0)
        
        # Variables auxiliares en paralelo
        self._initialize_arrays_parallel(self.phi, 0.0)
        self._initialize_arrays_parallel(self.chi, 1.0)
        self._initialize_arrays_parallel(self.K_trace, 0.0)
        
        # Gauge en paralelo
        self._initialize_arrays_parallel(self.alpha, 1.0)
        self._initialize_arrays_parallel(self.beta_x, 0.0)
        self._initialize_arrays_parallel(self.beta_y, 0.0)
        self._initialize_arrays_parallel(self.beta_z, 0.0)
        
        # Campos auxiliares en paralelo
        self._initialize_arrays_parallel(self.Gamma_x, 0.0)
        self._initialize_arrays_parallel(self.Gamma_y, 0.0)
        self._initialize_arrays_parallel(self.Gamma_z, 0.0)
        
        print("✅ Inicialización paralela completada")

    # [Resto de métodos adaptados para paralelización máxima...]
    # [El resto del código sigue la misma lógica pero optimizado]

def main():
    """Función principal optimizada."""
    parser = argparse.ArgumentParser(description="Setup 256³ con paralelización máxima")
    parser.add_argument('--chunk-size', type=int, default=72, 
                       help="Tamaño de chunks optimizado")
    parser.add_argument('--memory-limit', type=float, default=None,
                       help="Límite de memoria en GB")
    parser.add_argument('--no-mixed-precision', action='store_true',
                       help="Deshabilitar precisión mixta")
    
    args = parser.parse_args()
    
    print("🚀 CONFIGURADOR 256³ - PARALELIZACIÓN MÁXIMA")
    print("=" * 70)
    print(f"⚡ Optimizado para {mp.cpu_count()} cores")
    print("=" * 70)
    
    # Crear simulador optimizado
    simulator = OptimizedEinstein256SimulatorParallel(
        chunk_size=args.chunk_size,
        memory_limit_gb=args.memory_limit,
        use_mixed_precision=not args.no_mixed_precision
    )
    
    # Configurar almacenamiento optimizado
    simulator.setup_memory_mapped_storage_optimized()
    
    print("\n✅ CONFIGURACIÓN OPTIMIZADA COMPLETADA")
    print("⚡ Rendimiento esperado: {config['max_workers']/8:.1f}x mejor paralelización")

if __name__ == "__main__":
    main()
