#!/usr/bin/env python3
"""
Motor de evolución optimizado para paralelización máxima.
Configuración calculada para 12 cores.
"""

import numpy as np
import multiprocessing as mp
from multiprocessing import Pool, shared_memory
import time
import os
from pathlib import Path
from numba import jit, prange, set_num_threads
import concurrent.futures
import warnings

warnings.filterwarnings('ignore')

class OptimizedChunkedEvolutionEngine:
    """Motor de evolución con paralelización máxima."""
    
    def __init__(self, simulator):
        self.sim = simulator
        self.current_time = 0.0
        self.current_step = 0
        
        # PARALELIZACIÓN MÁXIMA
        self.max_workers = mp.cpu_count()  # USAR TODOS LOS CORES
        set_num_threads(mp.cpu_count())     # NUMBA CON TODOS LOS THREADS
        
        # Configurar variables de entorno
        os.environ['OMP_NUM_THREADS'] = str(mp.cpu_count())
        os.environ['MKL_NUM_THREADS'] = str(mp.cpu_count())
        
        print(f"🔧 Motor de evolución - PARALELIZACIÓN MÁXIMA:")
        print(f"   Workers paralelos: {self.max_workers} (100% de cores)")
        print(f"   Chunks totales: {self.sim.total_chunks}")
        print(f"   Paralelización efectiva: {min(self.sim.total_chunks, self.max_workers)} chunks simultáneos")
        
        if self.sim.total_chunks >= self.max_workers:
            print("✅ Paralelización óptima: suficientes chunks para todos los cores")
        else:
            print("⚠️  Paralelización subóptima: considere reducir chunk_size")
    
    def evolve_single_timestep_optimized(self):
        """Evoluciona usando paralelización máxima."""
        start_time = time.time()
        
        chunk_ids = list(range(self.sim.total_chunks))
        
        # Usar ThreadPoolExecutor para mejor rendimiento de I/O
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Enviar todos los chunks en paralelo
            future_to_chunk = {executor.submit(self.evolve_single_chunk_fast, cid): cid 
                              for cid in chunk_ids}
            
            # Recoger resultados conforme se completan
            completed_chunks = 0
            for future in concurrent.futures.as_completed(future_to_chunk):
                chunk_id = future_to_chunk[future]
                try:
                    result = future.result()
                    completed_chunks += 1
                except Exception as exc:
                    print(f'Chunk {chunk_id} generó excepción: {exc}')
        
        self.current_time += self.sim.dt
        self.current_step += 1
        
        evolution_time = time.time() - start_time
        return evolution_time
    
    def evolve_single_chunk_fast(self, chunk_id):
        """Versión optimizada para evolución de chunk individual."""
        # Implementación optimizada con menos overhead
        bounds = self.sim.get_chunk_bounds(chunk_id)
        core_slice = bounds['core']
        ext_slice = bounds['extended']
        local_core = bounds['local_core']
        
        # Extraer datos de manera más eficiente
        chunk_data = self._extract_chunk_data_fast(ext_slice)
        
        # Evolucionar con algoritmo optimizado
        evolved_data = self._evolve_chunk_bssn_optimized(chunk_data, local_core)
        
        # Escribir resultados de manera más eficiente
        self._write_chunk_results_fast(evolved_data, core_slice)
        
        return chunk_id
    
    @jit(nopython=True, parallel=True)
    def _compute_evolution_optimized(self, gamma_xx, gamma_yy, gamma_zz, 
                                   K_xx, K_yy, K_zz, alpha, dt, dx):
        """Función de evolución optimizada con Numba paralelo."""
        nx, ny, nz = gamma_xx.shape
        
        # Arrays de salida
        gamma_xx_new = np.zeros_like(gamma_xx)
        gamma_yy_new = np.zeros_like(gamma_yy)
        gamma_zz_new = np.zeros_like(gamma_zz)
        
        # Evolución en paralelo usando todos los threads
        for i in prange(1, nx-1):
            for j in prange(1, ny-1):
                for k in prange(1, nz-1):
                    # Algoritmo BSSN simplificado pero estable
                    trace_K = K_xx[i,j,k] + K_yy[i,j,k] + K_zz[i,j,k]
                    
                    A_xx = K_xx[i,j,k] - gamma_xx[i,j,k] * trace_K / 3.0
                    A_yy = K_yy[i,j,k] - gamma_yy[i,j,k] * trace_K / 3.0
                    A_zz = K_zz[i,j,k] - gamma_zz[i,j,k] * trace_K / 3.0
                    
                    # Evolución con disipación mínima
                    gamma_xx_new[i,j,k] = gamma_xx[i,j,k] - 2.0 * dt * alpha[i,j,k] * A_xx
                    gamma_yy_new[i,j,k] = gamma_yy[i,j,k] - 2.0 * dt * alpha[i,j,k] * A_yy
                    gamma_zz_new[i,j,k] = gamma_zz[i,j,k] - 2.0 * dt * alpha[i,j,k] * A_zz
        
        return gamma_xx_new, gamma_yy_new, gamma_zz_new
    
    # [Resto de métodos optimizados...]

def main():
    print("🧪 MOTOR DE EVOLUCIÓN OPTIMIZADO - PARALELIZACIÓN MÁXIMA")
    print(f"⚡ Configurado para {mp.cpu_count()} cores")

if __name__ == "__main__":
    main()
