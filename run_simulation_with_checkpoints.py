#!/usr/bin/env python3
"""
Script para ejecutar simulación BSSN con sistema de checkpoints y optimización GPU
Ejecuta pruebas de validación del sistema de checkpoints y recuperación
"""

import sys
import os
import time
import json
import subprocess
import signal
import psutil
from pathlib import Path

# Añadir el directorio actual al path
sys.path.append(os.getcwd())

def check_disk_space():
    """Verifica espacio en disco disponible"""
    stat = os.statvfs('.')
    free_space_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
    print(f"💾 Espacio en disco disponible: {free_space_gb:.1f} GB")
    return free_space_gb > 1.0  # Requerir al menos 1 GB libre

def monitor_resources(pid, duration=10):
    """Monitorea recursos del proceso durante un tiempo determinado"""
    try:
        process = psutil.Process(pid)
        cpu_usage = []
        memory_usage = []
        
        for _ in range(duration):
            cpu_usage.append(process.cpu_percent())
            memory_usage.append(process.memory_info().rss / (1024**2))  # MB
            time.sleep(1)
        
        return {
            'avg_cpu': sum(cpu_usage) / len(cpu_usage),
            'max_cpu': max(cpu_usage),
            'avg_memory_mb': sum(memory_usage) / len(memory_usage),
            'max_memory_mb': max(memory_usage)
        }
    except:
        return None

def run_simulation_test():
    """Ejecuta la simulación de prueba con checkpoints"""
    print("🚀 Etapa 1: Ejecutando simulación de prueba con checkpoints")
    print("=" * 60)
    
    # Verificar espacio en disco
    if not check_disk_space():
        print("❌ Espacio en disco insuficiente")
        return False
    
    # Configuración para prueba rápida
    config = {
        "grid_size": 32,
        "domain_size": 20.0,
        "dt": 0.01,
        "t_final": 0.5,  # Reducido para prueba rápida
        "output_every": 5,
        "cfl_factor": 0.25,
        "dissipation": 0.01,
        "max_cores": 4,
        "use_gpu": True,
        "checkpoint_config": {
            'checkpoint_dir': 'checkpoints',
            'frequent_interval': 10,  # Cada 10 pasos para prueba
            'periodic_interval': 50,  # Cada 50 pasos
            'max_checkpoints': 5,
            'compression_level': 6
        }
    }
    
    # Guardar configuración temporal
    with open("temp_checkpoint_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    try:
        # Importar y ejecutar simulador
        from computational_implementation.simulations.run_simulation_windows_gpu import EinsteinSimulatorGPU
        
        print(f"⚙️  Configuración:")
        print(f"   Resolución: {config['grid_size']}³")
        print(f"   Tiempo final: {config['t_final']}")
        print(f"   Checkpoints: cada {config['checkpoint_config']['frequent_interval']} pasos")
        print(f"   GPU: {'Activada' if config['use_gpu'] else 'Desactivada'}")
        print()
        
        # Crear simulador
        simulator = EinsteinSimulatorGPU(
            data_file="simulation_initial_data.npz",
            max_cores=config['max_cores'],
            use_gpu=config['use_gpu'],
            checkpoint_config=config['checkpoint_config']
        )
        
        # Configurar parámetros personalizados
        simulator.dt = config['dt']
        simulator.t_final = config['t_final']
        simulator.output_every = config['output_every']
        
        # Reconfigurar número de pasos
        simulator.n_steps = int(simulator.t_final / simulator.dt)
        simulator.n_outputs = simulator.n_steps // simulator.output_every
        
        print(f"📊 Parámetros finales:")
        print(f"   dt = {simulator.dt}")
        print(f"   t_final = {simulator.t_final}")
        print(f"   n_steps = {simulator.n_steps:,}")
        print()
        
        # Ejecutar simulación con monitoreo
        start_time = time.time()
        
        # Iniciar simulación en proceso separado para monitoreo
        import multiprocessing
        simulation_process = multiprocessing.Process(
            target=simulator.run_simulation,
            kwargs={
                'save_checkpoints': True,
                'verbose': True,
                'resume_from_checkpoint': None
            }
        )
        
        simulation_process.start()
        pid = simulation_process.pid
        
        print(f"🔄 Simulación iniciada con PID: {pid}")
        
        # Monitorear recursos durante los primeros 10 segundos
        print("📊 Monitoreando recursos...")
        resource_stats = monitor_resources(pid, duration=10)
        
        if resource_stats:
            print(f"   CPU promedio: {resource_stats['avg_cpu']:.1f}%")
            print(f"   CPU máximo: {resource_stats['max_cpu']:.1f}%")
            print(f"   Memoria promedio: {resource_stats['avg_memory_mb']:.1f} MB")
            print(f"   Memoria máxima: {resource_stats['max_memory_mb']:.1f} MB")
        
        # Esperar a que termine la simulación
        simulation_process.join(timeout=300)  # Timeout de 5 minutos
        
        if simulation_process.is_alive():
            print("⏹️  Timeout alcanzado, deteniendo simulación...")
            simulation_process.terminate()
            simulation_process.join(timeout=10)
            if simulation_process.is_alive():
                simulation_process.kill()
        
        total_time = time.time() - start_time
        
        if simulation_process.exitcode == 0:
            print(f"✅ Simulación completada en {total_time:.1f} segundos")
            
            # Verificar checkpoints generados
            checkpoint_files = list(Path('checkpoints').glob('checkpoint_*.chk'))
            print(f"📁 Checkpoints generados: {len(checkpoint_files)}")
            
            return True
        else:
            print(f"❌ Simulación falló con código: {simulation_process.exitcode}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la simulación: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Limpiar configuración temporal
        if os.path.exists("temp_checkpoint_config.json"):
            os.remove("temp_checkpoint_config.json")

def test_checkpoint_recovery():
    """Prueba el sistema de recuperación desde checkpoints"""
    print("\n🔄 Etapa 2: Probando recuperación desde checkpoints")
    print("=" * 60)
    
    try:
        from computational_implementation.simulations.run_simulation_windows_gpu import EinsteinSimulatorGPU
        
        # Buscar el checkpoint más reciente
        checkpoint_files = list(Path('checkpoints').glob('checkpoint_*.chk'))
        if not checkpoint_files:
            print("❌ No se encontraron checkpoints para probar recuperación")
            return False
        
        # Ordenar por número de paso y tomar el más reciente
        checkpoint_files.sort(key=lambda x: int(x.stem.split('_')[3]))
        latest_checkpoint = str(checkpoint_files[-1])
        
        print(f"📁 Usando checkpoint: {Path(latest_checkpoint).name}")
        
        # Crear simulador para recuperación
        simulator = EinsteinSimulatorGPU(
            data_file="simulation_initial_data.npz",
            max_cores=4,
            use_gpu=True,
            checkpoint_config={
                'checkpoint_dir': 'checkpoints',
                'frequent_interval': 10,
                'periodic_interval': 50,
                'max_checkpoints': 5,
                'compression_level': 6
            }
        )
        
        # Configurar para continuar desde checkpoint
        simulator.dt = 0.01
        simulator.t_final = 1.0  # Tiempo mayor para probar continuación
        simulator.output_every = 5
        simulator.n_steps = int(simulator.t_final / simulator.dt)
        simulator.n_outputs = simulator.n_steps // simulator.output_every
        
        print(f"🔄 Reanudando simulación desde checkpoint...")
        start_time = time.time()
        
        # Ejecutar desde checkpoint
        simulator.run_simulation(
            save_checkpoints=True,
            verbose=True,
            resume_from_checkpoint=latest_checkpoint
        )
        
        recovery_time = time.time() - start_time
        print(f"✅ Recuperación completada en {recovery_time:.1f} segundos")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la recuperación: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_complete_simulation():
    """Ejecuta una simulación completa"""
    print("\n🚀 Etapa 3: Ejecutando simulación completa")
    print("=" * 60)
    
    try:
        from computational_implementation.simulations.run_simulation_windows_gpu import EinsteinSimulatorGPU
        
        # Configuración para simulación completa
        simulator = EinsteinSimulatorGPU(
            data_file="simulation_initial_data.npz",
            max_cores=4,
            use_gpu=True,
            checkpoint_config={
                'checkpoint_dir': 'checkpoints',
                'frequent_interval': 100,
                'periodic_interval': 1000,
                'max_checkpoints': 10,
                'compression_level': 6
            }
        )
        
        # Configurar para simulación completa
        simulator.dt = 0.001
        simulator.t_final = 1.0
        simulator.output_every = 10
        simulator.n_steps = int(simulator.t_final / simulator.dt)
        simulator.n_outputs = simulator.n_steps // simulator.output_every
        
        print(f"📊 Configuración completa:")
        print(f"   Resolución: {simulator.nx}×{simulator.ny}×{simulator.nz}")
        print(f"   Tiempo final: {simulator.t_final}")
        print(f"   Paso temporal: {simulator.dt}")
        print(f"   Pasos totales: {simulator.n_steps:,}")
        print(f"   Checkpoints: cada 100 y 1000 pasos")
        print()
        
        # Ejecutar simulación completa
        start_time = time.time()
        
        simulator.run_simulation(
            save_checkpoints=True,
            verbose=True,
            resume_from_checkpoint="auto"  # Reanudar automáticamente si existe
        )
        
        total_time = time.time() - start_time
        
        print(f"\n✅ Simulación completa finalizada")
        print(f"⏱️  Tiempo total: {total_time/60:.2f} minutos")
        print(f"⚡ Rendimiento: {simulator.n_steps * simulator.total_points / total_time / 1000:.1f}k puntos/segundo")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la simulación completa: {e}")
        import traceback
        traceback.print_exc()
        return False

def validate_results():
    """Valida los resultados generados"""
    print("\n🔍 Etapa 4: Validando resultados generados")
    print("=" * 60)
    
    try:
        import numpy as np
        
        # Verificar archivo de resultados
        result_files = [
            "simulation_results_gpu.npz",
            "simulation_results.npz"
        ]
        
        results_found = False
        for result_file in result_files:
            if os.path.exists(result_file):
                print(f"📁 Archivo de resultados encontrado: {result_file}")
                
                # Cargar y verificar contenido
                data = np.load(result_file)
                
                print("📊 Contenido del archivo:")
                for key in data.files:
                    if isinstance(data[key], np.ndarray):
                        print(f"   {key}: {data[key].shape} {data[key].dtype}")
                    else:
                        print(f"   {key}: {type(data[key])}")
                
                # Verificar datos esperados
                expected_keys = ['time_evolution', 'metric_evolution', 'final_gamma_xx']
                missing_keys = [key for key in expected_keys if key not in data.files]
                
                if missing_keys:
                    print(f"⚠️  Claves faltantes: {missing_keys}")
                else:
                    print("✅ Todas las claves esperadas presentes")
                
                # Verificar integridad de datos
                if 'time_evolution' in data:
                    time_data = data['time_evolution']
                    if len(time_data) > 0:
                        print(f"✅ Evolución temporal: {len(time_data)} puntos")
                        print(f"   Tiempo inicial: {time_data[0]:.4f}")
                        print(f"   Tiempo final: {time_data[-1]:.4f}")
                    else:
                        print("⚠️  No hay datos de evolución temporal")
                
                results_found = True
                break
        
        if not results_found:
            print("❌ No se encontraron archivos de resultados")
            return False
        
        # Verificar checkpoints
        checkpoint_files = list(Path('checkpoints').glob('checkpoint_step_*.npz'))
        print(f"\n📁 Checkpoints encontrados: {len(checkpoint_files)}")
        
        if checkpoint_files:
            # Verificar tamaño de checkpoints
            total_size = sum(f.stat().st_size for f in checkpoint_files) / (1024**2)
            print(f"   Tamaño total: {total_size:.1f} MB")
            
            # Verificar más reciente
            checkpoint_files.sort(key=lambda x: int(x.stem.split('_')[-1]))
            latest = checkpoint_files[-1]
            print(f"   Más reciente: {latest.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la validación: {e}")
        import traceback
        traceback.print_exc()
        return False

def cleanup_test_files():
    """Limpia archivos de prueba"""
    print("\n🧹 Limpiando archivos de prueba...")
    
    # Limpiar checkpoints de prueba (mantener los de simulación completa)
    checkpoint_files = list(Path('checkpoints').glob('checkpoint_step_*.npz'))
    for checkpoint in checkpoint_files:
        step_num = int(checkpoint.stem.split('_')[-1])
        if step_num < 1000:  # Mantener checkpoints de simulación completa
            try:
                checkpoint.unlink()
                print(f"   Eliminado: {checkpoint.name}")
            except:
                pass
    
    # Limpiar archivos temporales
    temp_files = ["temp_checkpoint_config.json"]
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"   Eliminado: {temp_file}")
            except:
                pass

def main():
    """Función principal que ejecuta todas las etapas"""
    print("🚀 Simulación BSSN con Checkpoints y GPU")
    print("Validación completa del sistema de checkpoints y recuperación")
    print("=" * 60)
    
    results = {
        'simulation_test': False,
        'checkpoint_recovery': False,
        'complete_simulation': False,
        'results_validation': False
    }
    
    try:
        # Etapa 1: Simulación de prueba con checkpoints
        results['simulation_test'] = run_simulation_test()
        
        if results['simulation_test']:
            # Etapa 2: Prueba de recuperación desde checkpoints
            results['checkpoint_recovery'] = test_checkpoint_recovery()
        
        if results['checkpoint_recovery']:
            # Etapa 3: Simulación completa
            results['complete_simulation'] = run_complete_simulation()
        
        if results['complete_simulation']:
            # Etapa 4: Validación de resultados
            results['results_validation'] = validate_results()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 60)
        
        for stage, success in results.items():
            status = "✅ ÉXITO" if success else "❌ FALLO"
            print(f"{stage.replace('_', ' ').title()}: {status}")
        
        overall_success = all(results.values())
        
        if overall_success:
            print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
            print("✅ Sistema de checkpoints validado")
            print("✅ Recuperación desde checkpoints verificada")
            print("✅ Simulación completa ejecutada")
            print("✅ Resultados generados y validados")
        else:
            print("\n⚠️  ALGUNAS PRUEBAS FALLARON")
            print("Revisar los logs para más detalles")
        
        # Limpiar archivos de prueba
        cleanup_test_files()
        
        return overall_success
        
    except KeyboardInterrupt:
        print("\n⏹️  Proceso interrumpido por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)