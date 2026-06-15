#!/usr/bin/env python3
"""
Test de paralelización para verificar que se usan todos los cores.
"""

import multiprocessing as mp
import time
import numpy as np
from numba import jit, prange, set_num_threads, get_num_threads
import psutil
import os

def test_parallelization():
    """Testa que la paralelización funciona correctamente."""
    print("🧪 TEST DE PARALELIZACIÓN")
    print("=" * 50)
    
    cpu_count = mp.cpu_count()
    print(f"💻 CPU cores detectados: {cpu_count}")
    
    # Configurar Numba
    set_num_threads(cpu_count)
    numba_threads = get_num_threads()
    print(f"🔧 Numba threads configurados: {numba_threads}")
    
    # Variables de entorno
    env_vars = ['OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMBA_NUM_THREADS']
    for var in env_vars:
        value = os.environ.get(var, 'No configurado')
        print(f"🌍 {var}: {value}")
    
    # Test de carga paralela
    print(f"\n⚡ Testeando carga paralela...")
    
    @jit(nopython=True, parallel=True)
    def parallel_workload(size):
        """Carga de trabajo paralela intensiva."""
        result = np.zeros(size)
        for i in prange(size):
            # Simular trabajo computacional intensivo
            for j in range(1000):
                result[i] += np.sin(i * j * 0.001)
        return result
    
    # Monitorear CPU durante la ejecución
    def monitor_cpu():
        """Monitorea el uso de CPU durante 10 segundos."""
        cpu_usage = []
        for _ in range(10):
            usage = psutil.cpu_percent(interval=1, percpu=True)
            cpu_usage.append(usage)
        return cpu_usage
    
    # Ejecutar test con monitoreo
    print("🏃 Ejecutando workload paralelo (10 segundos)...")
    print("📊 Monitoreando uso de CPU por core...")
    
    import threading
    
    # Iniciar monitoreo en hilo separado
    cpu_monitor = []
    def cpu_monitor_thread():
        cpu_monitor.extend(monitor_cpu())
    
    monitor_thread = threading.Thread(target=cpu_monitor_thread)
    monitor_thread.start()
    
    # Ejecutar workload paralelo
    start_time = time.time()
    result = parallel_workload(100000)
    end_time = time.time()
    
    monitor_thread.join()
    
    # Analizar resultados
    print(f"\n📈 RESULTADOS:")
    print(f"   Tiempo de ejecución: {end_time - start_time:.2f} segundos")
    print(f"   Resultado computado: {len(result)} elementos")
    
    if cpu_monitor:
        avg_cpu_per_core = np.mean(cpu_monitor, axis=0)
        total_cpu_usage = np.mean(avg_cpu_per_core)
        cores_active = np.sum(avg_cpu_per_core > 10)  # Cores con >10% uso
        
        print(f"\n💻 USO DE CPU:")
        print(f"   Uso promedio total: {total_cpu_usage:.1f}%")
        print(f"   Cores activos (>10%): {cores_active}/{cpu_count}")
        print(f"   Eficiencia paralela: {cores_active/cpu_count*100:.1f}%")
        
        print(f"\n📊 USO POR CORE:")
        for i, usage in enumerate(avg_cpu_per_core):
            status = "✅" if usage > 10 else "❌"
            print(f"   Core {i:2d}: {usage:5.1f}% {status}")
        
        # Diagnóstico
        if cores_active >= cpu_count * 0.8:
            print(f"\n✅ PARALELIZACIÓN EXITOSA")
            print(f"   {cores_active}/{cpu_count} cores están siendo utilizados eficientemente")
        else:
            print(f"\n⚠️  PARALELIZACIÓN SUBÓPTIMA")
            print(f"   Solo {cores_active}/{cpu_count} cores activos")
            print(f"   Posibles causas:")
            print(f"   - Configuración incorrecta de threads")
            print(f"   - Workload insuficiente para todos los cores")
            print(f"   - Límites de memoria o I/O")

if __name__ == "__main__":
    test_parallelization()
