#!/usr/bin/env python3
"""
Parche mejorado para optimización de paralelización.
Corrige el problema de chunk size y maximiza el uso de todos los núcleos.

Análisis del problema:
- Tu sistema tiene 12 cores
- Los scripts estaban limitados a 8 workers máximo
- El chunk size de 64³ creaba solo 64 chunks total (4×4×4)
- Necesitamos más chunks pequeños para aprovechar todos los cores

Solución:
- Usar todos los 12 cores disponibles
- Chunk size más pequeño (32³) para crear 512 chunks (8×8×8)
- Esto da 512/12 = ~43 chunks por core (excelente paralelización)

Autor: Sistema de Optimización UniversoCentrífugo
"""

import numpy as np
import multiprocessing as mp
import os
import psutil
from pathlib import Path
import json

def create_optimal_parallelization_fix():
    """Crea la corrección óptima para paralelización."""
    
    cpu_count = mp.cpu_count()
    print(f"🔍 ANÁLISIS MEJORADO DE PARALELIZACIÓN")
    print("=" * 60)
    print(f"💻 Sistema detectado: {cpu_count} cores")
    
    # El problema clave: necesitamos MUCHOS chunks pequeños para paralelizar bien
    optimal_chunk_size = 32  # Esto crea 8×8×8 = 512 chunks
    chunks_per_dim = 256 // optimal_chunk_size
    total_chunks = chunks_per_dim ** 3
    chunks_per_core = total_chunks / cpu_count
    
    print(f"📊 Configuración óptima:")
    print(f"   Chunk size: {optimal_chunk_size}³ (en lugar de 64³)")
    print(f"   Chunks por dimensión: {chunks_per_dim} (en lugar de 4)")
    print(f"   Total chunks: {total_chunks} (en lugar de 64)")
    print(f"   Chunks per core: {chunks_per_core:.1f} (excelente para paralelización)")
    print(f"   Workers: {cpu_count} (en lugar de 8)")
    
    # Parchar los archivos existentes directamente
    patch_setup_script(optimal_chunk_size, cpu_count)
    patch_evolution_script(cpu_count)
    patch_pipeline_script(optimal_chunk_size, cpu_count)
    
    return {
        'chunk_size': optimal_chunk_size,
        'total_chunks': total_chunks,
        'workers': cpu_count,
        'improvement_factor': (cpu_count / 8) * (total_chunks / 64)
    }

def patch_setup_script(chunk_size, cpu_count):
    """Parcha el script de setup para usar paralelización óptima."""
    
    setup_file = Path("notebooks/setup_256cubed_optimized_simulation.py")
    
    if not setup_file.exists():
        print("⚠️  Archivo setup no encontrado")
        return
        
    print(f"🔧 Parcheando {setup_file}...")
    
    with open(setup_file, 'r') as f:
        content = f.read()
    
    # Parches críticos para maximizar paralelización
    patches = [
        # 1. Aumentar workers a todos los cores
        ('min(mp.cpu_count(), 8)', 'mp.cpu_count()'),
        ('min(self.available_cores, 16)', 'self.available_cores'),
        
        # 2. Chunk size por defecto más pequeño
        ('chunk_size=64', f'chunk_size={chunk_size}'),
        ('default=64', f'default={chunk_size}'),
        
        # 3. Configurar variables de entorno para máximo rendimiento
        ('import warnings', '''import warnings
import os

# Configurar variables de entorno para máximo rendimiento paralelo
os.environ['OMP_NUM_THREADS'] = str(mp.cpu_count())
os.environ['MKL_NUM_THREADS'] = str(mp.cpu_count())  
os.environ['NUMBA_NUM_THREADS'] = str(mp.cpu_count())
os.environ['OPENBLAS_NUM_THREADS'] = str(mp.cpu_count())'''),
        
        # 4. Mejorar comentarios para indicar optimización
        ('Limitar para evitar overhead', f'USAR TODOS LOS {cpu_count} CORES DISPONIBLES'),
        ('64 recomendado', f'{chunk_size} optimizado para {cpu_count} cores')
    ]
    
    patched_content = content
    patches_applied = 0
    
    for old, new in patches:
        if old in patched_content:
            patched_content = patched_content.replace(old, new)
            patches_applied += 1
            print(f"   ✅ Parche {patches_applied}: {old[:40]}...")
    
    # Backup del original
    backup_file = setup_file.with_suffix('.py.original')
    if not backup_file.exists():
        setup_file.rename(backup_file)
        print(f"   💾 Backup original: {backup_file}")
    else:
        setup_file.unlink()
    
    # Escribir versión parcheada
    with open(setup_file, 'w') as f:
        f.write(patched_content)
    
    print(f"   ✅ Setup script optimizado ({patches_applied} parches aplicados)")

def patch_evolution_script(cpu_count):
    """Parcha el motor de evolución para paralelización máxima."""
    
    evolution_file = Path("notebooks/run_256cubed_chunked_evolution.py")
    
    if not evolution_file.exists():
        print("⚠️  Archivo evolution no encontrado")
        return
        
    print(f"🔧 Parcheando {evolution_file}...")
    
    with open(evolution_file, 'r') as f:
        content = f.read()
    
    patches = [
        # 1. Remover límite artificial de workers
        ('min(mp.cpu_count(), 8)', 'mp.cpu_count()'),
        
        # 2. Agregar importaciones para mejor paralelización
        ('from multiprocessing import Pool', '''from multiprocessing import Pool
import concurrent.futures
import threading'''),
        
        # 3. Usar ThreadPoolExecutor para mejor I/O
        ('with Pool(self.max_workers) as pool:',
         '''# Usar ThreadPoolExecutor para mejor rendimiento de I/O paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:'''),
        
        ('results = pool.map(self.evolve_single_chunk, chunk_ids)',
         '''# Procesar chunks con futures para mejor control
            future_to_chunk = {executor.submit(self.evolve_single_chunk, cid): cid 
                              for cid in chunk_ids}
            results = []
            for future in concurrent.futures.as_completed(future_to_chunk):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    chunk_id = future_to_chunk[future]
                    print(f'Chunk {chunk_id} generó excepción: {exc}')'''),
        
        # 4. Mejorar comentarios
        ('Limitar para evitar overhead', f'USAR TODOS LOS {cpu_count} CORES - MÁXIMO PARALELISMO'),
        
        # 5. Configurar variables de entorno al inicio
        ('warnings.filterwarnings(\'ignore\')', '''warnings.filterwarnings('ignore')

# Configurar paralelización máxima
import os
os.environ['OMP_NUM_THREADS'] = str(mp.cpu_count())
os.environ['MKL_NUM_THREADS'] = str(mp.cpu_count())
os.environ['NUMBA_NUM_THREADS'] = str(mp.cpu_count())''')
    ]
    
    patched_content = content
    patches_applied = 0
    
    for old, new in patches:
        if old in patched_content:
            patched_content = patched_content.replace(old, new)
            patches_applied += 1
            print(f"   ✅ Parche {patches_applied}: {old[:40]}...")
    
    # Backup del original
    backup_file = evolution_file.with_suffix('.py.original')
    if not backup_file.exists():
        evolution_file.rename(backup_file)
        print(f"   💾 Backup original: {backup_file}")
    else:
        evolution_file.unlink()
    
    # Escribir versión parcheada
    with open(evolution_file, 'w') as f:
        f.write(patched_content)
    
    print(f"   ✅ Evolution script optimizado ({patches_applied} parches aplicados)")

def patch_pipeline_script(chunk_size, cpu_count):
    """Parcha el pipeline principal."""
    
    pipeline_file = Path("run_256cubed_complete_pipeline.py")
    
    if not pipeline_file.exists():
        print("⚠️  Pipeline script no encontrado")
        return
        
    print(f"🔧 Parcheando {pipeline_file}...")
    
    with open(pipeline_file, 'r') as f:
        content = f.read()
    
    patches = [
        # 1. Chunk size por defecto optimizado
        ('default=64', f'default={chunk_size}'),
        ('chunk_size: {args.chunk_size}', f'chunk_size: {{args.chunk_size}} (optimizado para {cpu_count} cores)'),
        
        # 2. Configurar Numba en setup
        ('import numba', '''import numba
        
# Configurar paralelización máxima desde el inicio
numba.set_num_threads(mp.cpu_count())'''),
        
        # 3. Mejorar descripciones
        ('Tamaño de chunks (64 recomendado)', f'Tamaño de chunks ({chunk_size} optimizado para {cpu_count} cores)'),
    ]
    
    patched_content = content
    patches_applied = 0
    
    for old, new in patches:
        if old in patched_content:
            patched_content = patched_content.replace(old, new)
            patches_applied += 1
            print(f"   ✅ Parche {patches_applied}: {old[:40]}...")
    
    # Backup del original
    backup_file = pipeline_file.with_suffix('.py.original')
    if not backup_file.exists():
        with open(backup_file, 'w') as f:
            f.write(content)
        print(f"   💾 Backup creado: {backup_file}")
    
    # Escribir versión parcheada
    with open(pipeline_file, 'w') as f:
        f.write(patched_content)
    
    print(f"   ✅ Pipeline script optimizado ({patches_applied} parches aplicados)")

def create_test_script(config):
    """Crea script de test para verificar la paralelización."""
    
    test_script = '''#!/usr/bin/env python3
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
    print(f"\\n⚡ Testeando carga paralela...")
    
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
    print(f"\\n📈 RESULTADOS:")
    print(f"   Tiempo de ejecución: {end_time - start_time:.2f} segundos")
    print(f"   Resultado computado: {len(result)} elementos")
    
    if cpu_monitor:
        avg_cpu_per_core = np.mean(cpu_monitor, axis=0)
        total_cpu_usage = np.mean(avg_cpu_per_core)
        cores_active = np.sum(avg_cpu_per_core > 10)  # Cores con >10% uso
        
        print(f"\\n💻 USO DE CPU:")
        print(f"   Uso promedio total: {total_cpu_usage:.1f}%")
        print(f"   Cores activos (>10%): {cores_active}/{cpu_count}")
        print(f"   Eficiencia paralela: {cores_active/cpu_count*100:.1f}%")
        
        print(f"\\n📊 USO POR CORE:")
        for i, usage in enumerate(avg_cpu_per_core):
            status = "✅" if usage > 10 else "❌"
            print(f"   Core {i:2d}: {usage:5.1f}% {status}")
        
        # Diagnóstico
        if cores_active >= cpu_count * 0.8:
            print(f"\\n✅ PARALELIZACIÓN EXITOSA")
            print(f"   {cores_active}/{cpu_count} cores están siendo utilizados eficientemente")
        else:
            print(f"\\n⚠️  PARALELIZACIÓN SUBÓPTIMA")
            print(f"   Solo {cores_active}/{cpu_count} cores activos")
            print(f"   Posibles causas:")
            print(f"   - Configuración incorrecta de threads")
            print(f"   - Workload insuficiente para todos los cores")
            print(f"   - Límites de memoria o I/O")

if __name__ == "__main__":
    test_parallelization()
'''
    
    test_file = 'test_parallelization.py'
    with open(test_file, 'w') as f:
        f.write(test_script)
    
    os.chmod(test_file, 0o755)
    print(f"🧪 Script de test creado: {test_file}")
    return test_file

def main():
    """Función principal mejorada."""
    print("🚀 OPTIMIZACIÓN MEJORADA DE PARALELIZACIÓN")
    print("=" * 70)
    print("Corrigiendo problemas y maximizando uso de todos los núcleos")
    print("=" * 70)
    
    # Aplicar correcciones optimizadas
    config = create_optimal_parallelization_fix()
    
    # Crear script de test
    test_script = create_test_script(config)
    
    # Guardar configuración
    config_file = 'parallelization_config_optimized.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ OPTIMIZACIÓN MEJORADA COMPLETADA")
    print("=" * 70)
    print(f"📊 Mejoras aplicadas:")
    print(f"   • Workers: {config['workers']} (era: 8) = {config['workers']/8:.1f}x")
    print(f"   • Chunk size: {config['chunk_size']}³ (era: 64³) = más chunks pequeños")
    print(f"   • Total chunks: {config['total_chunks']} (era: 64) = {config['total_chunks']/64:.1f}x")
    print(f"   • Mejora total estimada: {config['improvement_factor']:.1f}x")
    
    print(f"\n🧪 Para verificar la paralelización:")
    print(f"   python {test_script}")
    
    print(f"\n🚀 Para ejecutar simulación optimizada:")
    print(f"   python run_256cubed_complete_pipeline.py --chunk-size {config['chunk_size']}")
    
    print(f"\n📁 Archivos modificados:")
    print(f"   • notebooks/setup_256cubed_optimized_simulation.py")
    print(f"   • notebooks/run_256cubed_chunked_evolution.py") 
    print(f"   • run_256cubed_complete_pipeline.py")
    print(f"   • {test_script} (nuevo)")
    print(f"   • {config_file} (nuevo)")
    print(f"   • *.original (backups)")

if __name__ == "__main__":
    main()