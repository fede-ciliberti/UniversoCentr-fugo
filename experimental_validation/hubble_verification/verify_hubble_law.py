#!/usr/bin/env python3
"""
Verificación de la Ley de Hubble - Versión Final
Conjetura del Universo Centrífugo

Este script analiza las simulaciones BSSN para verificar si la rotación 4D
genera expansión cosmológica consistente con la Ley de Hubble.

Autor: Análisis basado en simulaciones Einstein-BSSN
Fecha: 28 de junio de 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

def analyze_simulation(filepath):
    """
    Analiza una simulación BSSN desde un archivo de resultados.
    
    Args:
        filepath (str): Ruta al archivo .npz de resultados.

    Returns:
        dict: Resultados del análisis o None si falló.
    """
    print(f"📊 ANALIZANDO SIMULACIÓN: {filepath}")
    print("=" * (25 + len(filepath)))
    
    try:
        data = np.load(filepath, allow_pickle=True)
        
        # Compatibilidad con diferentes formatos de salida
        if 'metric_evolution' in data: # Formato antiguo
            times = data['time_evolution']
            metric_evolution = data['metric_evolution']
            det_gammas = np.array([m['det_gamma'] for m in metric_evolution])
        elif 'metric_invariants' in data: # Formato nuevo
            times = data['time_evolution']
            metric_data = data['metric_invariants']
            det_gammas = np.array([entry['det_gamma_mean'] for entry in metric_data])
        else:
            raise ValueError("Formato de archivo de resultados no reconocido.")

        print(f"📈 Evolución temporal:")
        print(f"   • Tiempo: {times[0]:.4f} → {times[-1]:.4f}")
        print(f"   • det(γ): {det_gammas[0]:.8f} → {det_gammas[-1]:.8f}")
        print(f"   • Cambio: {det_gammas[-1] - det_gammas[0]:.8f}")
        print(f"   • Cambio relativo: {((det_gammas[-1] - det_gammas[0])/det_gammas[0])*100:.6f}%")
        
        # Calcular factor de escala y tasa de Hubble
        scale_factors = np.cbrt(det_gammas)
        scale_velocities = np.gradient(scale_factors, times)
        hubble_rates = scale_velocities / scale_factors
        
        # Estadísticas de la región estable (segunda mitad)
        stable_idx = len(times) // 2
        stable_hubble = np.mean(hubble_rates[stable_idx:])
        hubble_std = np.std(hubble_rates[stable_idx:])
        
        # === ANÁLISIS DE CALIDAD DE DATOS ===
        noise_level = hubble_std / abs(stable_hubble) if abs(stable_hubble) > 1e-9 else np.inf
        
        if noise_level < 0.1:
            data_quality = "EXCELENTE"
        elif noise_level < 0.5:
            data_quality = "BUENA"
        elif noise_level < 1.0:
            data_quality = "ACEPTABLE"
        else:
            data_quality = "RUIDOSA"
        
        print(f"🔍 Análisis de expansión:")
        print(f"   • Tasa de Hubble: {stable_hubble:.8f} ± {hubble_std:.8f}")
        print(f"   • Calidad de datos: {data_quality} (ruido/señal: {noise_level:.3f})")
        
        # Determinar si hay expansión significativa
        expansion_significant = abs(stable_hubble) > 3 * hubble_std and abs(stable_hubble) > 1e-6
        
        if expansion_significant:
            if stable_hubble > 0:
                print(f"   ✅ EXPANSIÓN DETECTADA")
                result = "EXPANSIÓN"
            else:
                print(f"   📉 CONTRACCIÓN DETECTADA")
                result = "CONTRACCIÓN"
        else:
            print(f"   ⚪ SIN EXPANSIÓN SIGNIFICATIVA")
            result = "ESTÁTICO"
        
        # Crear gráfico
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        ax1.plot(times, det_gammas, 'b-', linewidth=2)
        ax1.set_title('Determinante Métrico')
        ax1.set_xlabel('Tiempo')
        ax1.set_ylabel('det(γ)')
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(times, scale_factors, 'g-', linewidth=2)
        ax2.set_title('Factor de Escala')
        ax2.set_xlabel('Tiempo')
        ax2.set_ylabel('a(t)')
        ax2.grid(True, alpha=0.3)
        
        ax3.plot(times, hubble_rates, 'r-', linewidth=1, alpha=0.7, label='H(t)')
        ax3.axhline(y=stable_hubble, color='orange', linestyle='--', linewidth=2, label=f'H promedio = {stable_hubble:.6f}')
        ax3.axvline(x=times[stable_idx], color='gray', linestyle=':', alpha=0.5, label='Inicio región estable')
        ax3.fill_between(times[stable_idx:], stable_hubble - hubble_std, stable_hubble + hubble_std, alpha=0.2, color='orange', label=f'±1σ = {hubble_std:.6f}')
        ax3.set_title('Tasa de Hubble')
        ax3.set_xlabel('Tiempo')
        ax3.set_ylabel('H(t)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        ax4.hist(hubble_rates[stable_idx:], bins=20, alpha=0.7, color='purple', density=True, label='Distribución estable')
        ax4.axvline(x=stable_hubble, color='orange', linestyle='--', linewidth=2, label=f'Media = {stable_hubble:.6f}')
        ax4.set_xlabel('Tasa de Hubble')
        ax4.set_ylabel('Densidad')
        ax4.set_title(f'Distribución H (Calidad: {data_quality})')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plot_filename = f"hubble_analysis_{os.path.basename(filepath).replace('.npz', '.png')}"
        plt.suptitle(f'Análisis de Expansión - {os.path.basename(filepath)}', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico guardado: {plot_filename}")
        
        return {
            'filepath': filepath,
            'stable_hubble': stable_hubble,
            'hubble_std': hubble_std,
            'expansion_detected': expansion_significant,
            'result': result,
            'change_percent': ((det_gammas[-1] - det_gammas[0])/det_gammas[0])*100,
            'data_quality': data_quality,
            'noise_level': noise_level,
            'plot_filename': plot_filename
        }
        
    except Exception as e:
        print(f"❌ Error al procesar {filepath}: {e}")
        return None

def generate_single_report(results):
    """
    Genera un reporte para una única simulación.
    
    Args:
        results (dict): Resultados del análisis de una simulación.
    """
    if not results:
        return

    print(f"\n📋 GENERANDO REPORTE PARA: {results['filepath']}")
    print("=" * (28 + len(results['filepath'])))
    
    report = f"""# Verificación de la Ley de Hubble - Reporte de Validación
*Conjetura del Universo Centrífugo*
*Fecha de Análisis: {__import__('datetime').date.today().strftime('%d de %B de %Y')}*

## Resumen de Validación

Este reporte detalla el análisis de la expansión cosmológica para la simulación contenida en `{os.path.basename(results['filepath'])}`. El objetivo es verificar si los parámetros del modelo producen una tasa de expansión consistente con la Ley de Hubble.

## Metodología

La verificación se basa en el análisis de invariantes métricos de la simulación BSSN. Se calcula:

1.  **Factor de escala**: `a(t) ∝ det(γ)^(1/3)`
2.  **Tasa de Hubble**: `H(t) = ȧ/a`
3.  **Análisis estadístico**: Promedio y desviación estándar en la segunda mitad de la simulación (región estable).
4.  **Calidad de datos**: Ratio ruido/señal (`σ_H / |H|`) para validar la robustez del resultado.

---

## Resultados del Análisis

### Simulación: `{os.path.basename(results['filepath'])}`

![Análisis Visual]({results['plot_filename']})

**Métricas Cuantitativas:**
- **Tasa de Hubble (H₀)**: `{results['stable_hubble']:.8f} ± {results['hubble_std']:.8f}`
- **Cambio métrico total**: `{results['change_percent']:.6f}%`
- **Calidad de datos**: `{results['data_quality']}` (ruido/señal: `{results['noise_level']:.3f}`)

**Conclusión de la Simulación:**
- **Resultado**: `{results['result']}`
- **Expansión Significativa**: `{'✅ SÍ' if results['expansion_detected'] else '❌ NO'}`

---

## Interpretación y Conclusión General
"""
    
    if results['expansion_detected']:
        report += """
### ✅ EVIDENCIA POSITIVA DE EXPANSIÓN

La simulación muestra **evidencia estadísticamente robusta** de expansión cosmológica. La tasa de Hubble calculada es significativamente distinta de cero y la calidad de los datos es alta, lo que confiere fiabilidad al resultado.

**Implicaciones:**
- El conjunto de parámetros utilizados en esta simulación es capaz de generar una expansión del espacio-tiempo.
- Este resultado es un paso crucial para validar la consistencia interna del modelo del Universo Centrífugo.
"""
    else:
        report += """
### ⚠️ EVIDENCIA DE EXPANSIÓN NO CONCLUYENTE O AUSENTE

Los resultados actuales **no proporcionan evidencia convincente** de expansión cosmológica. La tasa de Hubble calculada es indistinguible de cero, dado el ruido numérico de la simulación.

**Posibles Causas y Pasos Siguientes:**
1.  **Parámetros Físicos**: Los valores de `R` y `ω₄D` usados podrían corresponder a un régimen donde la expansión es extremadamente lenta, por debajo del umbral de detección de la simulación. Esto es, en sí mismo, un resultado físico importante.
2.  **Duración de la Simulación**: El efecto de expansión podría manifestarse a escalas de tiempo más largas que las simuladas.
3.  **Resolución Numérica**: Aunque la calidad de los datos sea buena, una resolución mayor podría reducir el ruido y revelar una señal débil.

**Recomendación:** Documentar este resultado como una **restricción clave del modelo**. El espacio de parámetros que satisface otras observaciones (ej. planitud) parece predecir una `H₀` incompatiblemente baja.
"""

    report += f"""
---

## Protocolo de Verificación

Este análisis sigue un protocolo estándar y reproducible:
- **Criterio de significancia**: Señal de Hubble (`|H|`) debe ser mayor a 3 desviaciones estándar del ruido (`3σ_H`).
- **Criterios de calidad**:
    - **EXCELENTE**: ruido/señal < 0.1
    - **BUENA**: ruido/señal < 0.5
    - **ACEPTABLE**: ruido/señal < 1.0
    - **RUIDOSA**: ruido/señal ≥ 1.0

*Este reporte y los artefactos asociados (`{results['plot_filename']}`) han sido generados automáticamente por `verify_hubble_law.py`.*
"""
    
    report_filename = f"reporte_hubble_{os.path.basename(results['filepath']).replace('.npz', '.md')}"
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Reporte guardado: {report_filename}")
    return report_filename

def main():
    """
    Función principal que ejecuta el análisis completo para un archivo de simulación.
    """
    parser = argparse.ArgumentParser(
        description="Verificación de la Ley de Hubble para simulaciones del Universo Centrífugo.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--filepath',
        type=str,
        required=True,
        help="Ruta al archivo de resultados de la simulación (.npz)."
    )
    args = parser.parse_args()

    print("🌌 VERIFICACIÓN DE LA LEY DE HUBBLE")
    print("Conjetura del Universo Centrífugo - Script de Análisis")
    print("=" * 60)
    
    # Analizar la simulación proporcionada
    results = analyze_simulation(args.filepath)
    
    # Generar reporte comprensivo
    if results:
        report_file = generate_single_report(results)
        
        # Resumen ejecutivo en pantalla
        print(f"\n🎯 RESUMEN EJECUTIVO PARA {os.path.basename(args.filepath)}:")
        if results['expansion_detected']:
            print(f"   ✅ RESULTADO: Evidencia sólida de expansión cosmológica.")
        else:
            print(f"   ⚠️ RESULTADO: Evidencia no concluyente o ausente.")
        
        print(f"\n📁 ARCHIVOS GENERADOS:")
        print(f"   • {report_file} (reporte principal)")
        print(f"   • {results['plot_filename']} (análisis visual)")
    else:
        print(f"\n❌ No se pudo completar el análisis para {args.filepath}.")

    print(f"\n🎉 ¡Verificación de la Ley de Hubble completada!")

if __name__ == "__main__":
    main()