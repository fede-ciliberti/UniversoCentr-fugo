#!/usr/bin/env python3
"""
Herramientas de diagnóstico para verificar el rendimiento y validez de simulaciones BSSN.
Analiza integridad de datos, benchmarks de rendimiento y evolución temporal.
"""

import numpy as np
import time
import os
import sys
from numba import jit, prange
import psutil
import multiprocessing as mp

def verificar_datos_simulacion():
    """Verifica la integridad de los datos generados"""
    print("🔍 VERIFICACIÓN DE DATOS DE SIMULACIÓN")
    print("=" * 50)
    
    # Verificar archivos existentes de simulaciones válidas
    archivos_esperados = [
        'simulation_results.npz',
        'simulation_initial_data.npz'
    ]
    
    for archivo in archivos_esperados:
        if os.path.exists(archivo):
            size_mb = os.path.getsize(archivo) / (1024*1024)
            print(f"✅ {archivo}: {size_mb:.2f} MB")
        else:
            print(f"❌ {archivo}: NO ENCONTRADO")
            return False
    
    # Cargar y analizar datos iniciales
    print(f"\n📊 ANÁLISIS DE DATOS INICIALES:")
    try:
        data_inicial = np.load('simulation_initial_data.npz')
        
        # Verificar dimensiones
        grid_size = int(data_inicial['grid_size'])
        gamma_xx = data_inicial['gamma_xx']
        
        print(f"   Grid size declarado: {grid_size}")
        print(f"   Shape real γ_xx: {gamma_xx.shape}")
        print(f"   Puntos totales: {np.prod(gamma_xx.shape):,}")
        print(f"   Memoria γ_xx: {gamma_xx.nbytes / (1024*1024):.2f} MB")
        
        # Verificar que los datos no sean triviales
        gamma_stats = {
            'min': np.min(gamma_xx),
            'max': np.max(gamma_xx), 
            'mean': np.mean(gamma_xx),
            'std': np.std(gamma_xx)
        }
        
        print(f"   Estadísticas γ_xx:")
        for stat, val in gamma_stats.items():
            print(f"     {stat}: {val:.8f}")
        
        # Verificar tensor energía-momento
        T_xx = data_inicial['T_xx']
        T_stats = {
            'min': np.min(T_xx),
            'max': np.max(T_xx),
            'mean': np.mean(T_xx),
            'std': np.std(T_xx)
        }
        
        print(f"   Estadísticas T_xx:")
        for stat, val in T_stats.items():
            print(f"     {stat}: {val:.8f}")
            
        if gamma_stats['std'] < 1e-10:
            print(f"   ⚠️  γ_xx demasiado uniforme - posible problema")
        
        if T_stats['std'] < 1e-10:
            print(f"   ⚠️  T_xx demasiado uniforme - posible problema")
            
    except Exception as e:
        print(f"   ❌ Error cargando datos iniciales: {e}")
        return False
    
    # Cargar y analizar resultados
    print(f"\n📈 ANÁLISIS DE RESULTADOS:")
    try:
        resultados = np.load('simulation_results.npz', allow_pickle=True)
        
        times = resultados['time_evolution']
        metric_evolution = resultados['metric_evolution']
        
        print(f"   Puntos temporales: {len(times)}")
        print(f"   Tiempo inicial: {times[0]:.4f}")
        print(f"   Tiempo final: {times[-1]:.4f}")
        print(f"   Intervalo promedio: {np.mean(np.diff(times)):.4f}")
        
        # Verificar si hay evolución real
        det_gammas = [m['det_gamma'] for m in metric_evolution]
        trace_Ks = [m['trace_K'] for m in metric_evolution]
        
        det_change = max(det_gammas) - min(det_gammas)
        trace_K_max = max([abs(k) for k in trace_Ks])
        
        print(f"   Cambio máximo det(γ): {det_change:.8f}")
        print(f"   Máximo |tr(K)|: {trace_K_max:.8f}")
        
        if det_change < 1e-10:
            print(f"   ⚠️  Sin evolución significativa de det(γ)")
        
        if trace_K_max < 1e-10:
            print(f"   ⚠️  Sin curvatura significativa")
            
        # Verificar consistencia de datos finales
        gamma_final = resultados['final_gamma_xx']
        print(f"   Shape γ_xx final: {gamma_final.shape}")
        print(f"   Memoria γ_xx final: {gamma_final.nbytes / (1024*1024):.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error cargando resultados: {e}")
        return False

def benchmark_operaciones_basicas(grid_size=32):
    """Benchmark de operaciones para estimar tiempo esperado"""
    print(f"\n⏱️  BENCHMARK DE OPERACIONES BÁSICAS")
    print("=" * 50)
    
    total_points = grid_size**3
    
    print(f"   Creando arrays {grid_size}³ = {total_points:,} puntos...")
    
    # Test creación de arrays
    start_time = time.time()
    test_array = np.random.random((grid_size, grid_size, grid_size))
    creation_time = time.time() - start_time
    
    print(f"   Tiempo creación array: {creation_time:.4f} seg")
    print(f"   Memoria array: {test_array.nbytes / (1024*1024):.2f} MB")
    
    # Test operaciones elementales
    start_time = time.time()
    result = test_array * 2.0 + 1.0
    elementwise_time = time.time() - start_time
    
    print(f"   Tiempo ops elementales: {elementwise_time:.4f} seg")
    
    # Test reducción (mean)
    start_time = time.time()
    mean_val = np.mean(test_array)
    reduction_time = time.time() - start_time
    
    print(f"   Tiempo reducción (mean): {reduction_time:.4f} seg")
    print(f"   Valor mean: {mean_val:.6f}")
    
    # Estimar tiempo total esperado
    n_steps = 187
    ops_per_step = 10  # Estimación conservadora de operaciones por paso
    
    estimated_time = n_steps * ops_per_step * elementwise_time
    
    print(f"\n📊 ESTIMACIÓN TIEMPO TOTAL:")
    print(f"   Pasos temporales: {n_steps}")
    print(f"   Ops por paso (estimado): {ops_per_step}")
    print(f"   Tiempo estimado: {estimated_time:.1f} seg = {estimated_time/60:.1f} min")
    print(f"   Tiempo real observado: ~6 seg")
    print(f"   Ratio real/estimado: {6/estimated_time:.2f}")
    
    if estimated_time > 60:
        print(f"   🚨 ANOMALÍA: Simulación demasiado rápida")
        return False
    else:
        print(f"   ✅ Tiempo consistente con operaciones simples")
        return True

@jit(nopython=True, parallel=True)
def test_numba_performance(grid_size, n_iterations):
    """Test de rendimiento con decorador Numba"""
    # Crear arrays de prueba
    array1 = np.ones((grid_size, grid_size, grid_size))
    array2 = np.ones((grid_size, grid_size, grid_size))
    result = np.zeros((grid_size, grid_size, grid_size))
    
    # Loop de evolución simulado
    for iteration in range(n_iterations):
        for i in prange(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    result[i,j,k] = array1[i,j,k] * 0.999 + array2[i,j,k] * 0.001
        
        # Actualizar arrays
        array1[:] = result[:]
    
    return np.mean(result)

def test_compilacion_numba():
    """Verifica si Numba está compilando correctamente"""
    print(f"\n🚀 TEST DE COMPILACIÓN NUMBA")
    print("=" * 50)
    
    grid_size = 32  # Pequeño para test rápido
    n_iterations = 10
    
    print(f"   Test con {grid_size}³ puntos, {n_iterations} iteraciones")
    
    # Primera ejecución (compilación)
    print("   Primera ejecución (compilación)...")
    start_time = time.time()
    result1 = test_numba_performance(grid_size, n_iterations)
    compile_time = time.time() - start_time
    
    # Segunda ejecución (compilado)
    print("   Segunda ejecución (compilado)...")
    start_time = time.time()
    result2 = test_numba_performance(grid_size, n_iterations)
    compiled_time = time.time() - start_time
    
    print(f"   Tiempo con compilación: {compile_time:.4f} seg")
    print(f"   Tiempo ya compilado: {compiled_time:.4f} seg")
    print(f"   Speedup compilación: {compile_time/compiled_time:.1f}x")
    print(f"   Resultado 1: {result1:.8f}")
    print(f"   Resultado 2: {result2:.8f}")
    print(f"   Diferencia: {abs(result1-result2):.2e}")
    
    if compiled_time > 0.1:
        print(f"   ⚠️  Rendimiento Numba menor al esperado")
        return False
    else:
        print(f"   ✅ Numba funcionando correctamente")
        return True

def verificar_evolucion_temporal():
    """Verifica si realmente se ejecutaron todos los pasos temporales"""
    print(f"\n🔄 VERIFICACIÓN DE EVOLUCIÓN TEMPORAL")
    print("=" * 50)
    
    try:
        resultados = np.load('simulation_results.npz', allow_pickle=True)
        metric_evolution = resultados['metric_evolution']
        
        print(f"   Puntos de evolución guardados: {len(metric_evolution)}")
        
        # Verificar que hay datos en cada punto
        for i, point in enumerate(metric_evolution[:5]):  # Primeros 5
            det_gamma = point['det_gamma']
            trace_K = point['trace_K']
            print(f"   Punto {i}: det(γ)={det_gamma:.8f}, tr(K)={trace_K:.8f}")
        
        if len(metric_evolution) > 5:
            print("   ...")
            # Últimos 2
            for i, point in enumerate(metric_evolution[-2:], len(metric_evolution)-2):
                det_gamma = point['det_gamma']
                trace_K = point['trace_K']
                print(f"   Punto {i}: det(γ)={det_gamma:.8f}, tr(K)={trace_K:.8f}")
        
        # Verificar tendencias
        det_gammas = [m['det_gamma'] for m in metric_evolution]
        
        # ¿Hay tendencia monotónica?
        diffs = np.diff(det_gammas)
        positive_changes = np.sum(diffs > 0)
        negative_changes = np.sum(diffs < 0)
        
        print(f"\n   Análisis de tendencias:")
        print(f"   Cambios positivos: {positive_changes}")
        print(f"   Cambios negativos: {negative_changes}")
        print(f"   Cambios nulos: {len(diffs) - positive_changes - negative_changes}")
        
        if positive_changes == 0 and negative_changes == 0:
            print(f"   🚨 SIN EVOLUCIÓN: Todos los valores iguales")
            return False
        elif abs(positive_changes - negative_changes) < 2:
            print(f"   ⚠️  EVOLUCIÓN ERRÁTICA: Sin tendencia clara")
            return False
        else:
            print(f"   ✅ EVOLUCIÓN DETECTADA: Tendencia clara")
            return True
            
    except Exception as e:
        print(f"   ❌ Error verificando evolución: {e}")
        return False

def diagnóstico_completo():
    """Ejecuta diagnóstico completo de la simulación"""
    print("🔬 DIAGNÓSTICO COMPLETO DE SIMULACIÓN 64³")
    print("Investigando anomalía de velocidad (6 segundos)")
    print("=" * 60)
    
    # Tests individuales
    tests = [
        ("Datos de simulación", verificar_datos_simulacion),
        ("Benchmark operaciones", benchmark_operaciones_basicas),
        ("Compilación Numba", test_compilacion_numba),
        ("Evolución temporal", verificar_evolucion_temporal)
    ]
    
    resultados = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name.upper()} {'='*20}")
        try:
            resultado = test_func()
            resultados[test_name] = resultado
            print(f"✅ {test_name}: {'PASS' if resultado else 'FAIL'}")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            resultados[test_name] = False
    
    # Resumen final
    print(f"\n🎯 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 40)
    
    total_tests = len(tests)
    passed_tests = sum(resultados.values())
    
    print(f"Tests ejecutados: {total_tests}")
    print(f"Tests pasados: {passed_tests}")
    print(f"Tasa de éxito: {passed_tests/total_tests*100:.1f}%")
    
    # Diagnóstico final
    if passed_tests == total_tests:
        print(f"\n🟢 SIMULACIÓN APARENTEMENTE CORRECTA")
        print("La velocidad puede deberse a optimización efectiva")
    elif passed_tests >= total_tests * 0.75:
        print(f"\n🟡 SIMULACIÓN PARCIALMENTE CORRECTA")
        print("Algunos problemas detectados, pero funcional")
    else:
        print(f"\n🔴 PROBLEMAS SERIOS DETECTADOS")
        print("La simulación probablemente no se ejecutó correctamente")
    
    return resultados

def main():
    """Función principal del diagnóstico"""
    resultados = diagnóstico_completo()
    
    print(f"\n💡 RECOMENDACIONES BASADAS EN RESULTADOS:")
    
    if not resultados.get("Datos de simulación", False):
        print("• Regenerar datos iniciales con verificación paso a paso")
    
    if not resultados.get("Benchmark operaciones", False):
        print("• Implementar contadores de operaciones explícitos")
    
    if not resultados.get("Compilación Numba", False):
        print("• Revisar configuración de Numba y paralelización")
    
    if not resultados.get("Evolución temporal", False):
        print("• Verificar que loops temporales realmente se ejecuten")
    
    # Sugerencia de próximo paso
    if sum(resultados.values()) < len(resultados) * 0.75:
        print(f"\n🎯 ACCIÓN RECOMENDADA:")
        print("Implementar simulación con debug verbose para rastrear cada paso")

if __name__ == "__main__":
    main()