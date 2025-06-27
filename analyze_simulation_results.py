#!/usr/bin/env python3
"""
Analizador técnico avanzado de resultados de simulación Einstein.
Genera reporte detallado para interpretar resultados en el contexto 
de la Conjetura del Universo Centrífugo.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import ndimage
import os
import sys

def load_simulation_data():
    """Carga los datos de la simulación"""
    try:
        # Cargar resultados principales
        results = np.load('simulation_results.npz', allow_pickle=True)
        
        # Cargar datos iniciales para comparación
        initial_data = np.load('simulation_initial_data.npz')
        
        return results, initial_data
    except FileNotFoundError as e:
        print(f"❌ Error: No se encontraron archivos de resultados: {e}")
        return None, None

def analyze_metric_evolution(results):
    """Analiza la evolución de la métrica espacial"""
    print("🔍 ANÁLISIS DE EVOLUCIÓN DE LA MÉTRICA")
    print("=" * 50)
    
    # Extraer datos temporales
    times = results['time_evolution']
    metric_evolution = results['metric_evolution']
    
    print(f"📊 Datos temporales:")
    print(f"   • Tiempo inicial: {times[0]:.4f}")
    print(f"   • Tiempo final: {times[-1]:.4f}")
    print(f"   • Puntos temporales: {len(times)}")
    print(f"   • Intervalo promedio: {np.mean(np.diff(times)):.4f}")
    
    # Analizar determinante de la métrica
    det_gammas = [m['det_gamma'] for m in metric_evolution]
    det_initial = det_gammas[0]
    det_final = det_gammas[-1]
    det_deviation = det_final - det_initial
    det_max_dev = max(det_gammas) - min(det_gammas)
    
    print(f"\n📈 Determinante de la métrica det(γ):")
    print(f"   • Valor inicial: {det_initial:.8f}")
    print(f"   • Valor final: {det_final:.8f}")
    print(f"   • Cambio total: {det_deviation:.8f}")
    print(f"   • Máxima desviación: {det_max_dev:.8f}")
    print(f"   • Cambio relativo: {(det_deviation/det_initial)*100:.6f}%")
    
    # Interpretar cambios
    if abs(det_deviation) > 1e-6:
        print(f"   🎯 SIGNIFICATIVO: Detectada evolución de la métrica")
        if det_deviation > 0:
            print(f"   📈 La métrica se EXPANDIÓ (consistente con expansión cosmológica)")
        else:
            print(f"   📉 La métrica se CONTRAJO")
    else:
        print(f"   ⚠️  CAMBIO MÍNIMO: Evolución muy pequeña o nula")
    
    # Analizar traza de curvatura extrínseca
    trace_Ks = [m['trace_K'] for m in metric_evolution]
    trace_K_final = trace_Ks[-1]
    trace_K_max = max([abs(k) for k in trace_Ks])
    
    print(f"\n📊 Traza de curvatura extrínseca tr(K):")
    print(f"   • Valor final: {trace_K_final:.8f}")
    print(f"   • Máximo absoluto: {trace_K_max:.8f}")
    
    if trace_K_max > 1e-6:
        print(f"   🎯 CURVATURA DETECTADA: Hay deformación del espacio-tiempo")
    else:
        print(f"   ⚠️  SIN CURVATURA SIGNIFICATIVA")
    
    return {
        'times': times,
        'det_gammas': det_gammas,
        'trace_Ks': trace_Ks,
        'det_deviation': det_deviation,
        'significant_evolution': abs(det_deviation) > 1e-6
    }

def analyze_spatial_distribution(results):
    """Analiza la distribución espacial de la métrica final"""
    print(f"\n🗺️  ANÁLISIS ESPACIAL DE LA MÉTRICA FINAL")
    print("=" * 50)
    
    # Extraer componentes finales de la métrica
    gamma_xx = results['final_gamma_xx']
    gamma_yy = results['final_gamma_yy'] 
    gamma_zz = results['final_gamma_zz']
    gamma_xy = results['final_gamma_xy']
    gamma_xz = results['final_gamma_xz']
    gamma_yz = results['final_gamma_yz']
    
    shape = gamma_xx.shape
    center = tuple(s//2 for s in shape)
    
    print(f"📏 Dimensiones de la malla: {shape}")
    print(f"🎯 Centro de la malla: {center}")
    
    # Estadísticas por componente
    components = {
        'γ_xx': gamma_xx,
        'γ_yy': gamma_yy, 
        'γ_zz': gamma_zz,
        'γ_xy': gamma_xy,
        'γ_xz': gamma_xz,
        'γ_yz': gamma_yz
    }
    
    print(f"\n📊 Estadísticas por componente métrico:")
    analysis_results = {}
    
    for name, component in components.items():
        mean_val = np.mean(component)
        std_val = np.std(component)
        min_val = np.min(component)
        max_val = np.max(component)
        center_val = component[center]
        
        print(f"\n   {name}:")
        print(f"      • Media: {mean_val:.8f}")
        print(f"      • Desv. estándar: {std_val:.8f}")
        print(f"      • Mín: {min_val:.8f}")
        print(f"      • Máx: {max_val:.8f}")
        print(f"      • Centro: {center_val:.8f}")
        
        # Detectar patrones
        if name in ['γ_xx', 'γ_yy', 'γ_zz']:
            expected = 1.0  # Métrica plana
            deviation = abs(mean_val - expected)
            if deviation > 1e-6:
                print(f"      🎯 DESVIACIÓN de métrica plana: {deviation:.8f}")
            else:
                print(f"      ✅ Aproximadamente métrica plana")
        else:
            if std_val > 1e-6:
                print(f"      🎯 TÉRMINOS CRUZADOS no nulos detectados")
            else:
                print(f"      ✅ Términos cruzados aproximadamente nulos")
        
        analysis_results[name] = {
            'mean': mean_val,
            'std': std_val,
            'center': center_val,
            'deviation': std_val
        }
    
    return analysis_results

def analyze_schwarzschild_signature(results, initial_data):
    """Busca firmas características de una métrica tipo Schwarzschild"""
    print(f"\n🎯 BÚSQUEDA DE FIRMA SCHWARZSCHILD")
    print("=" * 50)
    
    gamma_xx = results['final_gamma_xx']
    gamma_yy = results['final_gamma_yy']
    gamma_zz = results['final_gamma_zz']
    shape = gamma_xx.shape
    center = tuple(s//2 for s in shape)
    
    # Extraer perfil radial desde el centro
    center_x, center_y, center_z = center
    
    # Crear malla de distancias radiales
    x_coords = np.arange(shape[0]) - center_x
    y_coords = np.arange(shape[1]) - center_y
    z_coords = np.arange(shape[2]) - center_z
    
    X, Y, Z = np.meshgrid(x_coords, y_coords, z_coords, indexing='ij')
    R = np.sqrt(X**2 + Y**2 + Z**2)
    
    # Extraer valores de la métrica en función del radio
    radii = []
    g_xx_values = []
    g_yy_values = []
    g_zz_values = []
    
    for r in range(1, min(shape)//2):
        mask = (R >= r-0.5) & (R < r+0.5)
        if np.any(mask):
            radii.append(r)
            g_xx_values.append(np.mean(gamma_xx[mask]))
            g_yy_values.append(np.mean(gamma_yy[mask]))
            g_zz_values.append(np.mean(gamma_zz[mask]))
    
    radii = np.array(radii)
    g_xx_values = np.array(g_xx_values)
    
    print(f"📏 Análisis radial:")
    print(f"   • Puntos radiales analizados: {len(radii)}")
    print(f"   • Radio máximo: {radii[-1] if len(radii) > 0 else 0}")
    
    # Buscar tendencias tipo 1/r
    if len(radii) > 3:
        # Ajustar función tipo Schwarzschild: g_xx = 1 + A/r
        try:
            from scipy.optimize import curve_fit
            
            def schwarzschild_like(r, A, B):
                return B + A/r
            
            # Ajustar solo donde tenemos datos válidos
            valid_mask = (radii > 0) & np.isfinite(g_xx_values)
            if np.sum(valid_mask) > 2:
                popt, _ = curve_fit(schwarzschild_like, radii[valid_mask], 
                                  g_xx_values[valid_mask])
                A_fit, B_fit = popt
                
                print(f"\n📈 Ajuste tipo Schwarzschild g_xx = B + A/r:")
                print(f"   • A (parámetro 1/r): {A_fit:.8f}")
                print(f"   • B (offset): {B_fit:.8f}")
                
                if abs(A_fit) > 1e-6:
                    print(f"   🎯 POSIBLE FIRMA SCHWARZSCHILD detectada!")
                    print(f"   📊 Parámetro A indica curvatura tipo masa/distancia")
                else:
                    print(f"   ⚠️  No se detectó dependencia 1/r significativa")
                    
                return True, A_fit, B_fit
            else:
                print(f"   ❌ Datos insuficientes para ajuste")
                return False, 0, 0
                
        except ImportError:
            print(f"   ⚠️  scipy no disponible para ajuste")
            return False, 0, 0
    else:
        print(f"   ❌ Puntos insuficientes para análisis radial")
        return False, 0, 0

def interpret_centrifugal_hypothesis(analysis_data, spatial_data, schwarzschild_data):
    """Interpreta los resultados en el contexto de la Conjetura del Universo Centrífugo"""
    print(f"\n🌌 INTERPRETACIÓN: CONJETURA UNIVERSO CENTRÍFUGO")
    print("=" * 60)
    
    print(f"🔍 EVALUACIÓN DE PREDICCIONES TEÓRICAS:")
    
    # 1. ¿Hay evolución temporal de la métrica?
    has_evolution = analysis_data['significant_evolution']
    det_change = analysis_data['det_deviation']
    
    print(f"\n1️⃣  Evolución temporal de la métrica:")
    if has_evolution:
        print(f"   ✅ SÍ - Detectada evolución temporal")
        print(f"   📊 Cambio en det(γ): {det_change:.8f}")
        if det_change > 0:
            print(f"   🎯 CONSISTENTE con expansión por rotación 4D")
            print(f"   💡 La métrica se expandió, como predice la rotación centrífuga")
        else:
            print(f"   ⚠️  Contracción detectada (no esperada)")
    else:
        print(f"   ❌ NO - Sin evolución significativa detectada")
        print(f"   🤔 Posibles causas:")
        print(f"      • Tiempo de simulación muy corto")
        print(f"      • Parámetros de rotación 4D muy pequeños")
        print(f"      • Necesita mayor resolución espacial/temporal")
    
    # 2. ¿Hay curvatura del espacio-tiempo?
    max_deviation = max([spatial_data[comp]['std'] for comp in spatial_data])
    
    print(f"\n2️⃣  Curvatura del espacio-tiempo:")
    if max_deviation > 1e-6:
        print(f"   ✅ SÍ - Curvatura detectada")
        print(f"   📊 Máxima desviación: {max_deviation:.8f}")
        print(f"   🎯 CONSISTENTE con efectos gravitacionales por rotación 4D")
    else:
        print(f"   ❌ NO - Sin curvatura significativa")
        print(f"   🤔 La rotación 4D no generó curvatura observable")
    
    # 3. ¿Hay firma tipo Schwarzschild?
    has_schwarzschild, A_param, B_param = schwarzschild_data
    
    print(f"\n3️⃣  Firma tipo Schwarzschild:")
    if has_schwarzschild and abs(A_param) > 1e-6:
        print(f"   ✅ SÍ - Detectada dependencia radial")
        print(f"   📊 Parámetro A = {A_param:.8f}")
        print(f"   🎯 CONSISTENTE con gravedad emergente de rotación 4D")
        print(f"   💡 La curvatura decae con la distancia como esperado")
    else:
        print(f"   ❌ NO - Sin firma Schwarzschild clara")
        print(f"   🤔 Posibles causas:")
        print(f"      • Masa efectiva muy pequeña")
        print(f"      • Dominio computacional muy pequeño")
        print(f"      • Efectos de frontera dominantes")
    
    # Evaluación global
    print(f"\n🏆 EVALUACIÓN GLOBAL DE LA CONJETURA:")
    
    positive_indicators = 0
    if has_evolution: positive_indicators += 1
    if max_deviation > 1e-6: positive_indicators += 1  
    if has_schwarzschild and abs(A_param) > 1e-6: positive_indicators += 1
    
    if positive_indicators >= 2:
        print(f"   🎉 RESULTADOS PROMETEDORES ({positive_indicators}/3)")
        print(f"   ✅ La simulación muestra indicios consistentes con la conjetura")
        print(f"   🚀 Recomendación: Continuar con mayor resolución/tiempo")
    elif positive_indicators == 1:
        print(f"   ⚠️  RESULTADOS MIXTOS ({positive_indicators}/3)")
        print(f"   🤔 Algunos indicios positivos, pero necesita mejoras")
        print(f"   🔧 Recomendación: Ajustar parámetros de simulación")
    else:
        print(f"   ❌ RESULTADOS NEGATIVOS ({positive_indicators}/3)")
        print(f"   💡 La simulación no mostró efectos predichos")
        print(f"   🔬 Recomendación: Revisar modelo teórico o parámetros")
    
    return positive_indicators

def create_visualization(results, analysis_data, spatial_data):
    """Crea visualizaciones comprehensivas de los resultados"""
    print(f"\n📊 GENERANDO VISUALIZACIONES...")
    
    # Configurar la figura con múltiples subplots
    fig = plt.figure(figsize=(16, 12))
    gs = gridspec.GridSpec(3, 3, figure=fig)
    
    # 1. Evolución temporal del determinante
    ax1 = fig.add_subplot(gs[0, 0])
    times = analysis_data['times']
    det_gammas = analysis_data['det_gammas']
    ax1.plot(times, det_gammas, 'b-', linewidth=2, label='det(γ)')
    ax1.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='Métrica plana')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('det(γ)')
    ax1.set_title('Evolución del Determinante')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 2. Evolución temporal de la traza K
    ax2 = fig.add_subplot(gs[0, 1])
    trace_Ks = analysis_data['trace_Ks']
    ax2.plot(times, trace_Ks, 'g-', linewidth=2, label='tr(K)')
    ax2.axhline(y=0.0, color='r', linestyle='--', alpha=0.5, label='Sin curvatura')
    ax2.set_xlabel('Tiempo')
    ax2.set_ylabel('tr(K)')
    ax2.set_title('Evolución Curvatura Extrínseca')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # 3. Distribución espacial de γ_xx (corte central)
    ax3 = fig.add_subplot(gs[0, 2])
    gamma_xx = results['final_gamma_xx']
    center_slice = gamma_xx[:, :, gamma_xx.shape[2]//2]
    im1 = ax3.imshow(center_slice, cmap='RdBu_r', origin='lower')
    ax3.set_title('γ_xx (corte z=centro)')
    plt.colorbar(im1, ax=ax3)
    
    # 4. Distribución espacial de γ_yy
    ax4 = fig.add_subplot(gs[1, 0])
    gamma_yy = results['final_gamma_yy']
    center_slice_yy = gamma_yy[:, :, gamma_yy.shape[2]//2]
    im2 = ax4.imshow(center_slice_yy, cmap='RdBu_r', origin='lower')
    ax4.set_title('γ_yy (corte z=centro)')
    plt.colorbar(im2, ax=ax4)
    
    # 5. Distribución espacial de γ_zz
    ax5 = fig.add_subplot(gs[1, 1])
    gamma_zz = results['final_gamma_zz']
    center_slice_zz = gamma_zz[:, :, gamma_zz.shape[2]//2]
    im3 = ax5.imshow(center_slice_zz, cmap='RdBu_r', origin='lower')
    ax5.set_title('γ_zz (corte z=centro)')
    plt.colorbar(im3, ax=ax5)
    
    # 6. Histograma de desviaciones
    ax6 = fig.add_subplot(gs[1, 2])
    all_deviations = []
    for comp_name in ['γ_xx', 'γ_yy', 'γ_zz']:
        comp_data = spatial_data[comp_name]
        expected = 1.0 if comp_name in ['γ_xx', 'γ_yy', 'γ_zz'] else 0.0
        deviations = abs(comp_data['mean'] - expected)
        all_deviations.append(deviations)
    
    ax6.bar(['γ_xx', 'γ_yy', 'γ_zz'], 
            [abs(spatial_data['γ_xx']['mean'] - 1),
             abs(spatial_data['γ_yy']['mean'] - 1), 
             abs(spatial_data['γ_zz']['mean'] - 1)],
            color=['blue', 'green', 'red'], alpha=0.7)
    ax6.set_ylabel('Desviación de métrica plana')
    ax6.set_title('Desviaciones por Componente')
    ax6.grid(True, alpha=0.3)
    
    # 7. Perfil radial de γ_xx
    ax7 = fig.add_subplot(gs[2, :])
    
    # Calcular perfil radial
    shape = gamma_xx.shape
    center = tuple(s//2 for s in shape)
    center_x, center_y, center_z = center
    
    x_coords = np.arange(shape[0]) - center_x
    y_coords = np.arange(shape[1]) - center_y  
    z_coords = np.arange(shape[2]) - center_z
    
    X, Y, Z = np.meshgrid(x_coords, y_coords, z_coords, indexing='ij')
    R = np.sqrt(X**2 + Y**2 + Z**2)
    
    radii = []
    g_xx_radial = []
    g_yy_radial = []
    g_zz_radial = []
    
    for r in range(1, min(shape)//2):
        mask = (R >= r-0.5) & (R < r+0.5)
        if np.any(mask):
            radii.append(r)
            g_xx_radial.append(np.mean(gamma_xx[mask]))
            g_yy_radial.append(np.mean(gamma_yy[mask]))
            g_zz_radial.append(np.mean(gamma_zz[mask]))
    
    if len(radii) > 0:
        ax7.plot(radii, g_xx_radial, 'b-o', label='γ_xx', markersize=4)
        ax7.plot(radii, g_yy_radial, 'g-s', label='γ_yy', markersize=4)
        ax7.plot(radii, g_zz_radial, 'r-^', label='γ_zz', markersize=4)
        ax7.axhline(y=1.0, color='k', linestyle='--', alpha=0.5, label='Métrica plana')
        ax7.set_xlabel('Radio (puntos de malla)')
        ax7.set_ylabel('Valor métrico')
        ax7.set_title('Perfil Radial de Componentes Métricas')
        ax7.grid(True, alpha=0.3)
        ax7.legend()
    
    plt.tight_layout()
    plt.savefig('detailed_simulation_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✅ Visualización guardada: detailed_simulation_analysis.png")
    
    return 'detailed_simulation_analysis.png'

def main():
    """Función principal del analizador"""
    print("🔬 ANALIZADOR TÉCNICO AVANZADO - SIMULACIÓN EINSTEIN")
    print("Conjetura del Universo Centrífugo")
    print("=" * 70)
    
    # Cargar datos
    results, initial_data = load_simulation_data()
    if results is None:
        return
    
    print(f"✅ Datos cargados exitosamente")
    print(f"📁 Archivos de resultados encontrados")
    
    # Análisis temporal
    analysis_data = analyze_metric_evolution(results)
    
    # Análisis espacial
    spatial_data = analyze_spatial_distribution(results)
    
    # Búsqueda de firma Schwarzschild
    schwarzschild_data = analyze_schwarzschild_signature(results, initial_data)
    
    # Interpretación en contexto de la conjetura
    score = interpret_centrifugal_hypothesis(analysis_data, spatial_data, schwarzschild_data)
    
    # Crear visualizaciones
    viz_file = create_visualization(results, analysis_data, spatial_data)
    
    # Reporte final
    print(f"\n📋 REPORTE TÉCNICO COMPLETADO")
    print("=" * 40)
    print(f"📊 Puntuación de consistencia: {score}/3")
    print(f"📈 Visualización generada: {viz_file}")
    print(f"🔬 Análisis detallado completado")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES PARA PRÓXIMAS SIMULACIONES:")
    if score < 2:
        print(f"   🔧 Incrementar resolución espacial (64³ o 128³)")
        print(f"   ⏱️  Incrementar tiempo de simulación (t_final = 5.0)")
        print(f"   📊 Revisar parámetros físicos (R_param, omega_4d_param)")
    else:
        print(f"   🚀 ¡Resultados prometedores!")
        print(f"   📈 Intentar mayor resolución para más detalles")
        print(f"   🔬 Analizar efectos a mayor escala temporal")

if __name__ == "__main__":
    main()