#!/usr/bin/env python3
"""
Analizador técnico avanzado de resultados de simulación Einstein.
Realiza un análisis diferencial para cuantificar los efectos de acoplamiento
entre la gravedad local y la expansión global.
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def load_simulation_data(control_file, local_file, cluster_file):
    """Carga los datos de las tres simulaciones."""
    print("📂 Cargando datos de simulación...")
    try:
        control_data = np.load(control_file, allow_pickle=True)
        local_data = np.load(local_file, allow_pickle=True)
        cluster_data = np.load(cluster_file, allow_pickle=True)
        print("✓ Datos cargados exitosamente.")
        return control_data, local_data, cluster_data
    except FileNotFoundError as e:
        print(f"❌ Error: No se encontró el archivo de resultados: {e}")
        return None, None, None

def analyze_metric_deviations(control_data, local_data, cluster_data):
    """Analiza las desviaciones de la métrica entre las simulaciones."""
    print("\n🔬 ANALIZANDO DESVIACIONES DE LA MÉTRICA...")
    
    # Extraer métricas finales
    g_control = control_data['final_gamma_xx']
    g_local = local_data['final_gamma_xx']
    g_cluster = cluster_data['final_gamma_xx']
    
    # Calcular desviaciones
    deviation_local = g_local - g_control
    deviation_cluster = g_cluster - g_control
    
    # Cuantificar las desviaciones
    mean_dev_local = np.mean(np.abs(deviation_local))
    max_dev_local = np.max(np.abs(deviation_local))
    
    mean_dev_cluster = np.mean(np.abs(deviation_cluster))
    max_dev_cluster = np.max(np.abs(deviation_cluster))
    
    print("📊 Resultados del Análisis Diferencial:")
    print(f"  - Desviación media (Masa Local): {mean_dev_local:.6e}")
    print(f"  - Desviación máxima (Masa Local): {max_dev_local:.6e}")
    print(f"  - Desviación media (Cúmulo):    {mean_dev_cluster:.6e}")
    print(f"  - Desviación máxima (Cúmulo):    {max_dev_cluster:.6e}")
    
    return {
        'deviation_local': deviation_local,
        'deviation_cluster': deviation_cluster,
        'mean_dev_local': mean_dev_local,
        'max_dev_local': max_dev_local,
        'mean_dev_cluster': mean_dev_cluster,
        'max_dev_cluster': max_dev_cluster
    }

def analyze_regional_expansion(cluster_data):
    """Busca evidencia de expansión regional anómala."""
    print("\n🌍 ANALIZANDO EXPANSIÓN REGIONAL...")
    
    # Este es un análisis simplificado. Uno más riguroso requeriría
    # calcular el parámetro de Hubble localmente.
    
    g_cluster = cluster_data['final_gamma_xx']
    
    # Definir regiones (simplificado)
    center_slice = g_cluster[:, :, g_cluster.shape[2]//2]
    center_region = center_slice[10:22, 10:22]
    outer_region = np.concatenate([center_slice[:5, :], center_slice[-5:, :]])
    
    expansion_center = np.mean(center_region)
    expansion_outer = np.mean(outer_region)
    
    print("📈 Comparación de Expansión (valor de g_xx):")
    print(f"  - Región Central (cúmulo): {expansion_center:.6f}")
    print(f"  - Regiones Externas:       {expansion_outer:.6f}")
    
    if expansion_center > expansion_outer:
        print("  🎯 ¡EVIDENCIA POSITIVA! La expansión es mayor en la región del cúmulo.")
    else:
        print("  ℹ️ No se detectó una señal clara de expansión regional anómala.")
        
    return {
        'expansion_center': expansion_center,
        'expansion_outer': expansion_outer,
        'positive_evidence': expansion_center > expansion_outer
    }

def save_coupling_dataset(analysis_results, output_file):
    """Guarda el dataset final de acoplamiento."""
    print(f"\n💾 Guardando dataset de acoplamiento en: {output_file}")
    np.savez_compressed(output_file, **analysis_results)
    print("✓ Dataset guardado.")

def create_visualization(control_data, local_data, cluster_data, analysis_results):
    """Crea visualizaciones comparativas."""
    print("\n🎨 GENERANDO VISUALIZACIONES COMPARATIVAS...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Análisis Diferencial de Efectos de Acoplamiento', fontsize=16)
    
    # Métricas finales
    g_control = control_data['final_gamma_xx'][:, :, 15]
    g_local = local_data['final_gamma_xx'][:, :, 15]
    g_cluster = cluster_data['final_gamma_xx'][:, :, 15]
    
    # Desviaciones
    dev_local = analysis_results['deviation_local'][:, :, 15]
    dev_cluster = analysis_results['deviation_cluster'][:, :, 15]
    
    # Visualización de las métricas
    im1 = axes[0, 0].imshow(g_control, cmap='viridis')
    axes[0, 0].set_title('Control (Expansión Pura)')
    plt.colorbar(im1, ax=axes[0, 0])
    
    im2 = axes[0, 1].imshow(g_local, cmap='viridis')
    axes[0, 1].set_title('Masa Local')
    plt.colorbar(im2, ax=axes[0, 1])
    
    im3 = axes[0, 2].imshow(g_cluster, cmap='viridis')
    axes[0, 2].set_title('Cúmulo de Masas')
    plt.colorbar(im3, ax=axes[0, 2])
    
    # Visualización de las desviaciones
    im4 = axes[1, 1].imshow(dev_local, cmap='RdBu_r')
    axes[1, 1].set_title('Desviación (Masa Local - Control)')
    plt.colorbar(im4, ax=axes[1, 1])
    
    im5 = axes[1, 2].imshow(dev_cluster, cmap='RdBu_r')
    axes[1, 2].set_title('Desviación (Cúmulo - Control)')
    plt.colorbar(im5, ax=axes[1, 2])
    
    # Gráfico de expansión regional
    exp_data = analysis_results['regional_expansion']
    axes[1, 0].bar(['Centro', 'Exterior'], [exp_data['expansion_center'], exp_data['expansion_outer']], color=['red', 'blue'])
    axes[1, 0].set_title('Expansión Regional')
    axes[1, 0].set_ylabel('Valor promedio de g_xx')
    
    plt.tight_layout(rect=(0, 0, 1, 0.96))
    output_image = 'acoplamiento_analisis_visual.png'
    plt.savefig(output_image, dpi=200)
    print(f"✓ Visualización guardada en: {output_image}")

def main():
    """Función principal del analizador diferencial."""
    parser = argparse.ArgumentParser(description='Analizador de efectos de acoplamiento.')
    parser.add_argument('--control-file', required=True, help='Resultados de la simulación de control.')
    parser.add_argument('--local-file', required=True, help='Resultados de la simulación con masa local.')
    parser.add_argument('--cluster-file', required=True, help='Resultados de la simulación con cúmulo.')
    parser.add_argument('--output-dataset', default='acoplamiento_local_global.npz', help='Archivo de salida para el dataset de acoplamiento.')
    args = parser.parse_args()

    print("🔬 ANALIZADOR DE EFECTOS DE ACOPLAMIENTO")
    print("=" * 50)
    
    # Cargar datos
    control_data, local_data, cluster_data = load_simulation_data(args.control_file, args.local_file, args.cluster_file)
    if control_data is None:
        return

    # Realizar análisis
    deviation_results = analyze_metric_deviations(control_data, local_data, cluster_data)
    regional_expansion_results = analyze_regional_expansion(cluster_data)
    
    # Consolidar resultados
    final_results = {
        **deviation_results,
        'regional_expansion': regional_expansion_results
    }
    
    # Guardar dataset
    save_coupling_dataset(final_results, args.output_dataset)
    
    # Crear visualizaciones
    create_visualization(control_data, local_data, cluster_data, final_results)
    
    print("\n✅ ANÁLISIS DIFERENCIAL COMPLETADO.")

if __name__ == "__main__":
    main()