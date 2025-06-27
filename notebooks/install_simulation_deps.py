#!/usr/bin/env python3
"""
Script de instalación de dependencias para la simulación numérica.
Instala y configura todas las librerías necesarias para máximo rendimiento.
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"   Comando: {cmd}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.8+")
        return False

def detect_system():
    """Detecta el sistema operativo y configuración"""
    print("💻 Detectando sistema...")
    
    system = platform.system()
    architecture = platform.machine()
    cpu_count = os.cpu_count()
    
    print(f"   Sistema: {system}")
    print(f"   Arquitectura: {architecture}")
    print(f"   CPUs: {cpu_count}")
    
    return system, architecture, cpu_count

def install_base_packages():
    """Instala paquetes base necesarios"""
    packages = [
        "numpy>=1.21.0",
        "scipy>=1.7.0", 
        "matplotlib>=3.5.0",
        "numba>=0.56.0",  # Para JIT compilation
        "psutil",         # Para monitoreo del sistema
        "tqdm",           # Para barras de progreso mejoradas
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Instalando {package}"):
            return False
    
    return True

def install_optional_packages():
    """Instala paquetes opcionales para mejor rendimiento"""
    print("\n📦 Instalando paquetes opcionales...")
    
    # Intel Math Kernel Library (si está disponible)
    run_command("pip install mkl", "Intel MKL (opcional)")
    
    # BLAS optimizado
    run_command("pip install openblas", "OpenBLAS (opcional)")
    
    # Memoria compartida mejorada
    run_command("pip install multiprocess", "Multiprocess avanzado (opcional)")

def configure_numba():
    """Configura Numba para máximo rendimiento"""
    print("\n⚡ Configurando Numba...")
    
    # Script de configuración
    config_script = '''
import numba
import os

# Configurar threads para usar todos los cores
numba.set_num_threads(os.cpu_count())

# Verificar configuración
print(f"Numba threads configurados: {numba.get_num_threads()}")
print(f"CPUs disponibles: {os.cpu_count()}")

# Test de rendimiento básico
import numpy as np
from numba import jit
import time

@jit(nopython=True)
def test_function(x):
    return np.sum(x**2)

# Compilar función
data = np.random.random(1000000)
_ = test_function(data)

# Medir rendimiento
start = time.time()
result = test_function(data)
numba_time = time.time() - start

# Comparar con NumPy puro
start = time.time()
numpy_result = np.sum(data**2)
numpy_time = time.time() - start

speedup = numpy_time / numba_time
print(f"Speedup Numba vs NumPy: {speedup:.2f}x")
'''
    
    with open("test_numba_config.py", "w") as f:
        f.write(config_script)
    
    if run_command("python test_numba_config.py", "Test de configuración Numba"):
        os.remove("test_numba_config.py")
        return True
    return False

def create_performance_test():
    """Crea un script de test de rendimiento"""
    test_script = '''#!/usr/bin/env python3
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
'''
    
    with open("notebooks/test_performance.py", "w") as f:
        f.write(test_script)
    
    print("✅ Script de test de rendimiento creado: notebooks/test_performance.py")

def main():
    """Función principal de instalación"""
    print("🚀 Instalador de Dependencias - Simulación Numérica")
    print("=" * 60)
    
    # Verificaciones del sistema
    if not check_python_version():
        sys.exit(1)
    
    system, arch, cpus = detect_system()
    print()
    
    # Instalación de paquetes
    print("📦 Instalando dependencias...")
    if not install_base_packages():
        print("❌ Error en instalación de paquetes base")
        sys.exit(1)
    
    # Paquetes opcionales
    install_optional_packages()
    
    # Configuración de Numba
    print()
    if not configure_numba():
        print("⚠️  Advertencia: Error en configuración de Numba")
    
    # Crear scripts de test
    create_performance_test()
    
    print("\n✅ Instalación completada exitosamente!")
    print("\n📋 Próximos pasos:")
    print("   1. Ejecute: python notebooks/test_performance.py")
    print("   2. Luego: python notebooks/run_numerical_simulation.py")
    print("\n💡 Consejos:")
    print("   - Use resolución 32³ para pruebas iniciales")
    print("   - Monitore RAM durante la simulación")
    print("   - Los checkpoints se guardan automáticamente")

if __name__ == "__main__":
    main()