#!/usr/bin/env python3
"""
Monitor en tiempo real de checkpoints de la simulación BSSN completa.
Analiza la evolución de la métrica y verifica consistencia con la conjetura.
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import time

def cargar_checkpoint(archivo):
    """Carga un checkpoint específico"""
    try:
        data = np.load(archivo, allow_pickle=True)
        return data
    except Exception as e:
        print(f"Error cargando {archivo}: {e}")
        return None

def extraer_numero_paso(filename):
    """Extrae el número de paso del nombre del archivo"""
    # checkpoint_step_000030.npz -> 30
    import re
    match = re.search(r'step_(\d+)', filename)
    if match:
        return int(match.group(1))
    return 0

def analizar_evolucion_checkpoints():
    """Analiza la evolución usando todos los checkpoints disponibles"""
    print("🔍 ANALIZADOR DE CHECKPOINTS EN TIEMPO REAL")
    print("Conjetura del Universo Centrífugo - Algoritmo BSSN Completo")
    print("=" * 70)
    
    # Encontrar todos los checkpoints
    checkpoints = glob.glob("checkpoint_step_*.npz")
    checkpoints.sort(key=extraer_numero_paso)
    
    if not checkpoints:
        print("❌ No se encontraron checkpoints")
        return False
    
    print(f"📁 Checkpoints encontrados: {len(checkpoints)}")
    for cp in checkpoints:
        step = extraer_numero_paso(cp)
        size_mb = os.path.getsize(cp) / (1024*1024)
        print(f"   Paso {step:3d}: {os.path.basename(cp)} ({size_mb:.1f} MB)")
    
    # Analizar cada checkpoint
    tiempos = []
    det_gammas = []
    trace_Ks = []
    pasos = []
    
    print(f"\n📊 ANÁLISIS DE EVOLUCIÓN TEMPORAL:")
    print(f"{'Paso':<6} {'Tiempo':<8} {'det(γ)':<12} {'tr(K)':<12} {'Δdet(γ)':<12}")
    print("-" * 60)
    
    det_gamma_inicial = None
    
    for i, checkpoint_file in enumerate(checkpoints):
        step = extraer_numero_paso(checkpoint_file)
        data = cargar_checkpoint(checkpoint_file)
        
        if data is None:
            continue
        
        # Extraer información del checkpoint
        if 'time' in data:
            tiempo = float(data['time'])
        else:
            tiempo = step * 0.01  # Estimación si no está disponible
        
        # Calcular determinante de la métrica
        if 'gamma_xx' in data:
            gamma_xx = data['gamma_xx']
            gamma_yy = data['gamma_yy'] 
            gamma_zz = data['gamma_zz']
            
            # Aproximación diagonal para determinante
            det_gamma = np.mean(gamma_xx * gamma_yy * gamma_zz)
        else:
            print(f"   ⚠️  Paso {step}: datos métricos no encontrados")
            continue
        
        # Calcular traza de curvatura extrínseca
        if 'K_xx' in data:
            K_xx = data['K_xx']
            K_yy = data['K_yy']
            K_zz = data['K_zz']
            trace_K = np.mean(K_xx + K_yy + K_zz)
        else:
            trace_K = 0.0
        
        # Calcular cambio respecto al inicial
        if det_gamma_inicial is None:
            det_gamma_inicial = det_gamma
            delta_det = 0.0
        else:
            delta_det = det_gamma - det_gamma_inicial
        
        # Guardar datos
        pasos.append(step)
        tiempos.append(tiempo)
        det_gammas.append(det_gamma)
        trace_Ks.append(trace_K)
        
        # Mostrar progreso
        print(f"{step:<6} {tiempo:<8.4f} {det_gamma:<12.8f} {trace_K:<12.8f} {delta_det:<12.8f}")
    
    # Análisis de tendencias
    if len(det_gammas) > 1:
        print(f"\n📈 ANÁLISIS DE TENDENCIAS:")
        
        # Calcular tasa de cambio
        delta_det_total = det_gammas[-1] - det_gammas[0]
        delta_tiempo = tiempos[-1] - tiempos[0] if len(tiempos) > 1 else 1.0
        tasa_expansion = delta_det_total / delta_tiempo if delta_tiempo > 0 else 0
        
        print(f"   Determinante inicial: {det_gammas[0]:.8f}")
        print(f"   Determinante final: {det_gammas[-1]:.8f}")
        print(f"   Cambio total: {delta_det_total:.8f}")
        print(f"   Cambio relativo: {(delta_det_total/det_gammas[0])*100:.6f}%")
        print(f"   Tasa de expansión: {tasa_expansion:.8f}/unidad_tiempo")
        
        # Determinar tendencia
        if abs(delta_det_total) < 1e-10:
            print(f"   📊 ESTÁTICO: Sin evolución significativa")
            tendencia = "estático"
        elif delta_det_total > 0:
            print(f"   📈 EXPANSIÓN: Métrica creciente (¡Consistente con conjetura!)")
            tendencia = "expansión"
        else:
            print(f"   📉 CONTRACCIÓN: Métrica decreciente")
            tendencia = "contracción"
        
        # Análisis de linealidad
        if len(det_gammas) > 2:
            # Ajuste lineal
            coeficientes = np.polyfit(tiempos, det_gammas, 1)
            pendiente, intercepto = coeficientes
            
            # Calcular R²
            det_ajustado = np.polyval(coeficientes, tiempos)
            ss_res = np.sum((det_gammas - det_ajustado) ** 2)
            ss_tot = np.sum((det_gammas - np.mean(det_gammas)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 1
            
            print(f"\n🔬 ANÁLISIS DE LINEALIDAD:")
            print(f"   Pendiente: {pendiente:.8f}")
            print(f"   R²: {r_squared:.6f}")
            
            if r_squared > 0.99:
                print(f"   ✅ EVOLUCIÓN LINEAL EXCELENTE")
            elif r_squared > 0.95:
                print(f"   ✅ EVOLUCIÓN APROXIMADAMENTE LINEAL")
            else:
                print(f"   ⚠️  EVOLUCIÓN NO LINEAL")
        
        # Crear visualización
        crear_grafico_evolucion(tiempos, det_gammas, trace_Ks, pasos)
        
        return {
            'tendencia': tendencia,
            'tasa_expansion': tasa_expansion,
            'cambio_relativo': (delta_det_total/det_gammas[0])*100,
            'r_squared': r_squared if len(det_gammas) > 2 else None,
            'num_checkpoints': len(checkpoints)
        }
    
    return False

def crear_grafico_evolucion(tiempos, det_gammas, trace_Ks, pasos):
    """Crea gráfico de la evolución temporal"""
    print(f"\n📊 Generando visualización...")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Gráfico 1: Evolución del determinante
    ax1.plot(tiempos, det_gammas, 'b-o', linewidth=2, markersize=4, label='det(γ)')
    ax1.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='Métrica plana')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('det(γ)')
    ax1.set_title('Evolución del Determinante de la Métrica (Algoritmo BSSN Completo)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Ajuste lineal si hay suficientes puntos
    if len(tiempos) > 2:
        coef = np.polyfit(tiempos, det_gammas, 1)
        ajuste = np.polyval(coef, tiempos)
        ax1.plot(tiempos, ajuste, 'r--', alpha=0.7, label=f'Ajuste lineal (m={coef[0]:.2e})')
        ax1.legend()
    
    # Gráfico 2: Evolución de la curvatura extrínseca
    ax2.plot(tiempos, trace_Ks, 'g-s', linewidth=2, markersize=4, label='tr(K)')
    ax2.axhline(y=0.0, color='r', linestyle='--', alpha=0.5, label='Sin curvatura')
    ax2.set_xlabel('Tiempo')
    ax2.set_ylabel('tr(K)')
    ax2.set_title('Evolución de la Curvatura Extrínseca')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('evolucion_checkpoints.png', dpi=150, bbox_inches='tight')
    print(f"✅ Gráfico guardado: evolucion_checkpoints.png")

def monitorear_simulacion_activa():
    """Monitorea la simulación en curso"""
    print(f"\n🔄 MONITOREO DE SIMULACIÓN ACTIVA")
    print("=" * 50)
    
    ultimo_checkpoint = None
    
    while True:
        # Buscar el checkpoint más reciente
        checkpoints = glob.glob("checkpoint_step_*.npz")
        if checkpoints:
            checkpoints.sort(key=lambda x: os.path.getmtime(x))
            checkpoint_actual = checkpoints[-1]
            
            if checkpoint_actual != ultimo_checkpoint:
                step = extraer_numero_paso(checkpoint_actual)
                timestamp = time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(checkpoint_actual)))
                
                print(f"🔄 Nuevo checkpoint: Paso {step} a las {timestamp}")
                
                # Análisis rápido del checkpoint
                data = cargar_checkpoint(checkpoint_actual)
                if data and 'gamma_xx' in data:
                    gamma_xx = data['gamma_xx']
                    gamma_yy = data['gamma_yy']
                    gamma_zz = data['gamma_zz']
                    det_gamma = np.mean(gamma_xx * gamma_yy * gamma_zz)
                    print(f"   det(γ) = {det_gamma:.8f}")
                
                ultimo_checkpoint = checkpoint_actual
        
        time.sleep(60)  # Revisar cada minuto

def main():
    """Función principal"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        monitorear_simulacion_activa()
    else:
        resultado = analizar_evolucion_checkpoints()
        
        if resultado:
            print(f"\n🎯 EVALUACIÓN DE LA CONJETURA:")
            print("=" * 40)
            
            if resultado['tendencia'] == 'expansión':
                print(f"✅ CONSISTENTE: La métrica muestra expansión")
                print(f"🎯 Cambio relativo: {resultado['cambio_relativo']:.6f}%")
                print(f"📈 Tasa de expansión: {resultado['tasa_expansion']:.8f}")
                
                if resultado['r_squared'] and resultado['r_squared'] > 0.95:
                    print(f"✅ LINEALIDAD EXCELENTE: R² = {resultado['r_squared']:.6f}")
                    print(f"🌌 PREDICCIÓN: Rotación 4D genera expansión cosmológica lineal")
                
            elif resultado['tendencia'] == 'contracción':
                print(f"❌ INCONSISTENTE: La métrica muestra contracción")
                print(f"🤔 Posibles causas: Parámetros incorrectos o error numérico")
                
            else:
                print(f"⚠️  SIN EVOLUCIÓN: Métrica estática")
                print(f"🤔 Posibles causas: Parámetros muy pequeños o tiempo insuficiente")
            
            print(f"\n📊 Checkpoints analizados: {resultado['num_checkpoints']}")
            print(f"📈 Visualización: evolucion_checkpoints.png")

if __name__ == "__main__":
    main()