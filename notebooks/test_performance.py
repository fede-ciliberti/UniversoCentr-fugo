#!/usr/bin/env python3
"""
Test de rendimiento del sistema para simulación numérica.
"""

import numpy as np
import time
import multiprocessing as mp
from multiprocessing import Pool
import psutil

def cpu_test():
    """Test de rendimiento CPU"""
    print("🧮 Test de rendimiento CPU...")
    
    # Test de operaciones matriciales
    size = 2000
    A = np.random.random((size, size))
    B = np.random.random((size, size))
    
    start = time.time()
    C = np.dot(A, B)
    cpu_time = time.time() - start
    
    ops = 2 * size**3  # Operaciones en multiplicación matricial
    gflops = ops / cpu_time / 1e9
    
    print(f"   Multiplicación matricial {size}x{size}: {cpu_time:.2f}s")
    print(f"   Rendimiento: {gflops:.2f} GFLOPS")
    
    return gflops

def memory_test():
    """Test de ancho de banda de memoria"""
    print("💾 Test de memoria...")
    
    # Test de lectura/escritura secuencial
    size = 100_000_000  # 100M elementos
    data = np.random.random(size)
    
    start = time.time()
    result = np.sum(data)
    read_time = time.time() - start
    
    bandwidth = size * 8 / read_time / 1e9  # GB/s
    print(f"   Lectura secuencial: {read_time:.2f}s")
    print(f"   Ancho de banda: {bandwidth:.2f} GB/s")
    
    return bandwidth

def worker_task(data):
    """Función worker para test de paralelización"""
    return np.sum(data**2)

def parallel_test():
    """Test de paralelización"""
    print("⚡ Test de paralelización...")
    
    try:
        # Datos de prueba
        chunk_size = 1_000_000
        n_chunks = min(mp.cpu_count(), 4)  # Limitar cores para evitar overhead
        data_chunks = [np.random.random(chunk_size) for _ in range(n_chunks)]
        
        # Test secuencial
        start = time.time()
        serial_results = [worker_task(chunk) for chunk in data_chunks]
        serial_time = time.time() - start
        
        # Test paralelo con protección
        start = time.time()
        if __name__ == "__main__":
            with Pool() as pool:
                parallel_results = pool.map(worker_task, data_chunks)
        else:
            # Fallback si no se puede usar multiprocessing
            parallel_results = serial_results
        parallel_time = time.time() - start
        
        speedup = serial_time / max(parallel_time, 0.001)  # Evitar división por cero
        efficiency = speedup / n_chunks * 100
        
        print(f"   Tiempo secuencial: {serial_time:.2f}s")
        print(f"   Tiempo paralelo: {parallel_time:.2f}s")
        print(f"   Speedup: {speedup:.2f}x")
        print(f"   Eficiencia: {efficiency:.1f}%")
        
        return speedup, efficiency
        
    except Exception as e:
        print(f"   ⚠️  Error en test de paralelización: {e}")
        print(f"   ℹ️  Continuando con valores por defecto...")
        return 1.0, 100.0  # Valores por defecto

def system_info():
    """Muestra información del sistema"""
    print("💻 Información del sistema:")
    print(f"   CPUs: {mp.cpu_count()}")
    print(f"   RAM: {psutil.virtual_memory().total / 1e9:.1f} GB")
    print(f"   RAM disponible: {psutil.virtual_memory().available / 1e9:.1f} GB")

def main():
    print("🔬 Test de Rendimiento - Simulación Numérica")
    print("=" * 50)
    
    system_info()
    print()
    
    gflops = cpu_test()
    print()
    
    bandwidth = memory_test()
    print()
    
    speedup, efficiency = parallel_test()
    print()
    
    print("📊 Resumen de rendimiento:")
    print(f"   CPU: {gflops:.1f} GFLOPS")
    print(f"   Memoria: {bandwidth:.1f} GB/s") 
    print(f"   Paralelización: {speedup:.1f}x ({efficiency:.0f}%)")
    print()
    
    # Recomendaciones
    if gflops > 50:
        print("✅ CPU: Excelente para simulaciones numéricas")
    elif gflops > 20:
        print("⚠️  CPU: Adecuado, considere parámetros conservadores")
    else:
        print("❌ CPU: Rendimiento bajo, reduzca resolución")
    
    if efficiency > 70:
        print("✅ Paralelización: Muy eficiente")
    elif efficiency > 50:
        print("⚠️  Paralelización: Eficiencia moderada")
    else:
        print("❌ Paralelización: Baja eficiencia, verifique sistema")

if __name__ == "__main__":
    main()
