#!/usr/bin/env python3
"""
Verificación Final de la Ley de Hubble - Versión Adaptada
Conjetura del Universo Centrífugo

Esta versión trabaja con diferentes formatos de datos de simulación
y analiza los invariantes métricos disponibles.

Autor: Análisis basado en simulaciones Einstein-BSSN
Fecha: 28 de junio de 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

class FinalHubbleLawVerifier:
    """
    Verificador final que trabaja con diferentes formatos de datos.
    """
    
    def __init__(self):
        self.results_file = None
        self.results = None
        self.times = None
        self.metric_invariants = None
        self.grid_shape = None
        self.analysis_results = {}
        
    def find_and_analyze_data(self):
        """
        Encuentra y analiza todos los archivos de simulación disponibles.
        """
        print("🌌 VERIFICACIÓN FINAL DE LA LEY DE HUBBLE")
        print("Conjetura del Universo Centrífugo")
        print("=" * 70)
        
        files_to_analyze = [
            ('simulation_results_256.npz', 'Simulación 256³ (muestras)'),
            ('simulation_results.npz', 'Simulación 32³ (completa)')
        ]
        
        successful_analyses = 0
        
        for filename, description in files_to_analyze:
            if os.path.exists(filename):
                print(f"\n📊 ANALIZANDO: {description}")
                print("=" * 50)
                
                try:
                    result = self.analyze_single_file(filename, description)
                    if result:
                        self.analysis_results[filename] = result
                        successful_analyses += 1
                        print(f"✅ Análisis exitoso de {filename}")
                    else:
                        print(f"❌ Análisis falló para {filename}")
                except Exception as e:
                    print(f"❌ Error analizando {filename}: {e}")
            else:
                print(f"⚠️ Archivo no encontrado: {filename}")
        
        if successful_analyses > 0:
            self.create_comprehensive_report()
            print(f"\n🎉 Análisis completado. {successful_analyses} archivo(s) procesado(s) exitosamente.")
        else:
            print(f"\n❌ No se pudo analizar ningún archivo de simulación.")
        
        return successful_analyses > 0
    
    def analyze_single_file(self, filename, description):
        """
        Analiza un solo archivo de simulación.
        
        Args:
            filename (str): Nombre del archivo
            description (str): Descripción del archivo
        
        Returns:
            dict: Resultados del análisis o None si falló
        """
        try:
            data = np.load(filename, allow_pickle=True)
            print(f"📁 Archivo cargado: {filename}")
            print(f"🔑 Claves disponibles: {list(data.keys())}")

            # Extraer metadatos de la simulación si existen
            topology = data.get('topology', 'sphere') # Asumir esfera si no se especifica
            grid_shape = data.get('grid_shape', None)
            
            print(f"   • Topología detectada: {topology.capitalize()}")
            if grid_shape is not None:
                print(f"   • Dimensiones de la grilla: {grid_shape}")

            # Análisis según el tipo de archivo
            if 'metric_invariants' in data.keys():
                return self.analyze_metric_invariants_data(data, description, topology, filename)
            elif 'metric_evolution' in data.keys():
                return self.analyze_full_evolution_data(data, description, topology, filename)
            else:
                print(f"⚠️ Formato de archivo no reconocido")
                return None
                
        except Exception as e:
            print(f"❌ Error cargando {filename}: {e}")
            return None
    
    def analyze_metric_invariants_data(self, data, description, topology, filename):
        """
        Analiza datos basados en invariantes métricos (formato 256³).
        
        Args:
            data: Datos cargados del archivo NPZ
            description (str): Descripción del conjunto de datos
            topology (str): Topología de la simulación ('sphere' o 'torus')
            filename (str): Nombre del archivo de origen
        
        Returns:
            dict: Resultados del análisis
        """
        print(f"📊 ANÁLISIS DE INVARIANTES MÉTRICOS")
        print("=" * 40)
        
        times = data['time_evolution']
        metric_invariants = data['metric_invariants']
        
        print(f"📈 Datos temporales:")
        print(f"   • Tiempo inicial: {times[0]:.4f}")
        print(f"   • Tiempo final: {times[-1]:.4f}")
        print(f"   • Puntos temporales: {len(times)}")
        print(f"   • Intervalo promedio: {np.mean(np.diff(times)):.6f}")
        
        print(f"📊 Invariantes métricos:")
        print(f"   • Valor inicial: {metric_invariants[0]:.8f}")
        print(f"   • Valor final: {metric_invariants[-1]:.8f}")
        print(f"   • Cambio total: {metric_invariants[-1] - metric_invariants[0]:.8f}")
        print(f"   • Cambio relativo: {((metric_invariants[-1] - metric_invariants[0])/metric_invariants[0])*100:.6f}%")
        
        # El determinante de la métrica está relacionado con la expansión
        # Para un universo en expansión: det(γ) ∝ a³, donde a es el factor de escala
        # Por tanto, la tasa de expansión es proporcional a d(det(γ)^(1/3))/dt
        
        # Calcular factor de escala efectivo
        scale_factors = np.cbrt(metric_invariants)  # a ∝ det(γ)^(1/3)
        
        # Calcular tasa de expansión (análogo a H)
        scale_velocities = np.gradient(scale_factors, times)
        hubble_rates = scale_velocities / scale_factors  # H = ȧ/a
        
        # Promediar en la segunda mitad de la simulación (más estable)
        stable_region = len(times) // 2
        stable_hubble = np.mean(hubble_rates[stable_region:])
        hubble_std = np.std(hubble_rates[stable_region:])
        
        print(f"\n🔍 ANÁLISIS DE EXPANSIÓN:")
        print(f"   • Factor de escala inicial: {scale_factors[0]:.8f}")
        print(f"   • Factor de escala final: {scale_factors[-1]:.8f}")
        print(f"   • Tasa de Hubble promedio: {stable_hubble:.8f} ± {hubble_std:.8f}")
        
        # Determinar si hay expansión significativa
        expansion_detected = abs(stable_hubble) > 3 * hubble_std and abs(stable_hubble) > 1e-6
        
        if expansion_detected:
            if stable_hubble > 0:
                print(f"   ✅ EXPANSIÓN DETECTADA (tasa positiva)")
                expansion_type = "expansión"
            else:
                print(f"   📉 CONTRACCIÓN DETECTADA (tasa negativa)")
                expansion_type = "contracción"
        else:
            print(f"   ⚪ SIN EXPANSIÓN SIGNIFICATIVA")
            expansion_type = "estático"
        
        # Análisis de la calidad de los datos
        noise_level = hubble_std / abs(stable_hubble) if abs(stable_hubble) > 0 else np.inf
        
        if noise_level < 0.1:
            data_quality = "EXCELENTE"
        elif noise_level < 0.5:
            data_quality = "BUENA"
        elif noise_level < 1.0:
            data_quality = "ACEPTABLE"
        else:
            data_quality = "RUIDOSA"
        
        print(f"   📊 Calidad de datos: {data_quality} (ruido/señal: {noise_level:.3f})")
        
        # Crear gráfico específico para este análisis
        self.create_invariants_plot(times, metric_invariants, scale_factors, 
                                  hubble_rates, description, filename.replace('.npz', ''))
        
        return {
            'type': 'invariants',
            'description': description,
            'filename': filename,
            'times': times,
            'metric_invariants': metric_invariants,
            'scale_factors': scale_factors,
            'hubble_rates': hubble_rates,
            'stable_hubble': stable_hubble,
            'hubble_std': hubble_std,
            'expansion_detected': expansion_detected,
            'expansion_type': expansion_type,
            'data_quality': data_quality,
            'noise_level': noise_level,
            'topology': topology
        }
    
    def analyze_full_evolution_data(self, data, description, topology, filename):
        """
        Analiza datos de evolución completa (formato 32³).
        
        Args:
            data: Datos cargados del archivo NPZ
            description (str): Descripción del conjunto de datos
            topology (str): Topología de la simulación ('sphere' o 'torus')
            filename (str): Nombre del archivo de origen
        """
        print(f"📊 ANÁLISIS DE EVOLUCIÓN COMPLETA")
        print("=" * 40)
        
        times = data['time_evolution']
        metric_evolution = data['metric_evolution']
        
        # Extraer determinantes
        det_gammas = [m['det_gamma'] for m in metric_evolution]
        
        print(f"📈 Datos temporales:")
        print(f"   • Tiempo inicial: {times[0]:.4f}")
        print(f"   • Tiempo final: {times[-1]:.4f}")
        print(f"   • Puntos temporales: {len(times)}")
        
        print(f"📊 Determinante métrico:")
        print(f"   • Valor inicial: {det_gammas[0]:.8f}")
        print(f"   • Valor final: {det_gammas[-1]:.8f}")
        print(f"   • Cambio total: {det_gammas[-1] - det_gammas[0]:.8f}")
        
        # Análisis similar al de invariantes
        scale_factors = np.cbrt(det_gammas)
        scale_velocities = np.gradient(scale_factors, times)
        hubble_rates = scale_velocities / scale_factors
        
        stable_region = len(times) // 2
        stable_hubble = np.mean(hubble_rates[stable_region:])
        hubble_std = np.std(hubble_rates[stable_region:])
        
        expansion_detected = abs(stable_hubble) > 3 * hubble_std and abs(stable_hubble) > 1e-6
        
        self.create_evolution_plot(times, det_gammas, scale_factors, 
                                 hubble_rates, description, filename.replace('.npz', ''))
        
        return {
            'type': 'evolution',
            'description': description,
            'filename': filename,
            'times': times,
            'det_gammas': det_gammas,
            'scale_factors': scale_factors,
            'hubble_rates': hubble_rates,
            'stable_hubble': stable_hubble,
            'hubble_std': hubble_std,
            'expansion_detected': expansion_detected,
            'topology': topology
        }
    
    def create_invariants_plot(self, times, invariants, scale_factors, hubble_rates, 
                              description, filename_base):
        """
        Crea un gráfico para el análisis de invariantes métricos.
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Evolución de invariantes métricos
        ax1.plot(times, invariants, 'b-', linewidth=2, label='det(γ)')
        ax1.set_xlabel('Tiempo')
        ax1.set_ylabel('Determinante métrico')
        ax1.set_title('Evolución del Determinante Métrico')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 2. Factor de escala
        ax2.plot(times, scale_factors, 'g-', linewidth=2, label='a(t) ∝ det(γ)^(1/3)')
        ax2.set_xlabel('Tiempo')
        ax2.set_ylabel('Factor de escala')
        ax2.set_title('Factor de Escala Cósmico')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 3. Tasa de Hubble
        ax3.plot(times, hubble_rates, 'r-', linewidth=1, alpha=0.7, label='H(t) = ȧ/a')
        stable_region = len(times) // 2
        stable_mean = np.mean(hubble_rates[stable_region:])
        ax3.axhline(y=stable_mean, color='orange', linestyle='--', linewidth=2, 
                   label=f'H promedio = {stable_mean:.6f}')
        ax3.set_xlabel('Tiempo')
        ax3.set_ylabel('Tasa de Hubble')
        ax3.set_title('Evolución de la Tasa de Hubble')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # 4. Distribución de tasas de Hubble
        ax4.hist(hubble_rates[stable_region:], bins=20, alpha=0.7, color='purple', 
                density=True, label='Distribución estable')
        ax4.axvline(x=stable_mean, color='orange', linestyle='--', linewidth=2,
                   label=f'Media = {stable_mean:.6f}')
        ax4.set_xlabel('Tasa de Hubble')
        ax4.set_ylabel('Densidad')
        ax4.set_title('Distribución de H en Régimen Estable')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.suptitle(f'Análisis Completo: {description}', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        output_file = f'hubble_analysis_{filename_base}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico guardado: {output_file}")
        
        plt.close()
    
    def create_evolution_plot(self, times, det_gammas, scale_factors, hubble_rates, 
                             description, filename_base):
        """
        Crea un gráfico para el análisis de evolución completa.
        """
        # Similar al anterior pero adaptado para datos de evolución
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        ax1.plot(times, det_gammas, 'b-', linewidth=2)
        ax1.set_title('Determinante Métrico')
        ax1.set_xlabel('Tiempo')
        ax1.grid(True, alpha=0.3)
        
        ax2.plot(times, scale_factors, 'g-', linewidth=2)
        ax2.set_title('Factor de Escala')
        ax2.set_xlabel('Tiempo')
        ax2.grid(True, alpha=0.3)
        
        ax3.plot(times, hubble_rates, 'r-', linewidth=1, alpha=0.7)
        ax3.set_title('Tasa de Hubble')
        ax3.set_xlabel('Tiempo')
        ax3.grid(True, alpha=0.3)
        
        plt.suptitle(f'Análisis: {description}', fontsize=14)
        plt.tight_layout()
        
        output_file = f'hubble_analysis_{filename_base}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico guardado: {output_file}")
        
        plt.close()
    
    def create_comprehensive_report(self):
        """
        Crea un reporte comprensivo de todos los análisis.
        """
        print(f"\n📋 GENERANDO REPORTE COMPRENSIVO")
        print("=" * 40)
        
        report_content = f"""# Reporte Final: Verificación de la Ley de Hubble
*Fecha: 28 de junio de 2025*
*Conjetura del Universo Centrífugo*

## Resumen Ejecutivo

Este reporte presenta el análisis final de la evidencia de expansión cosmológica en las simulaciones BSSN de la Conjetura del Universo Centrífugo.

## Análisis Realizados

"""
        
        for filename, results in self.analysis_results.items():
            report_content += f"""
### {results['description']}
**Archivo:** `{filename}`

**Metadatos de Simulación:**
- **Topología:** {results.get('topology', 'Esfera (asumida)').capitalize()}

**Resultados:**
- **Tasa de Hubble:** {results['stable_hubble']:.8f} ± {results['hubble_std']:.8f}
- **Expansión detectada:** {'✅ SÍ' if results['expansion_detected'] else '❌ NO'}
- **Tipo de evolución:** {results.get('expansion_type', 'N/A')}
- **Calidad de datos:** {results.get('data_quality', 'N/A')}

**Interpretación:**
"""
            
            if results.get('topology') == 'torus':
                report_content += """
**Nota sobre Topología Toroidal:** El análisis actual se basa en el determinante de la métrica, una propiedad global que asume homogeneidad. Si bien este método es válido para medir la expansión del volumen total, no captura efectos locales complejos ni el cálculo de distancias geodésicas propias de una topología toroidal. Los resultados deben interpretarse como una medida de la expansión promedio del espacio.
"""

            if results['expansion_detected']:
                if results['stable_hubble'] > 0:
                    report_content += f"""
La simulación muestra evidencia clara de **expansión cosmológica** con una tasa de Hubble positiva y estable. Esto es consistente con las predicciones de la Conjetura del Universo Centrífugo, donde la rotación 4D genera expansión observable del espacio-tiempo.

**Significado científico:** La rotación hiperdimensional efectivamente produce el tipo de expansión uniforme predicha por la teoría.
"""
                else:
                    report_content += f"""
La simulación muestra **contracción** en lugar de expansión. Esto podría indicar que los parámetros de rotación 4D necesitan ajuste o que hay efectos no considerados en el modelo actual.
"""
            else:
                report_content += f"""
No se detectó expansión significativa en esta simulación. Esto podría deberse a:
1. Parámetros de rotación 4D demasiado pequeños
2. Tiempo de simulación insuficiente para estabilización
3. Resolución espacial/temporal inadecuada
4. Efectos numéricos que dominan sobre la señal física
"""
        
        # Conclusiones generales
        total_analyses = len(self.analysis_results)
        expansion_detected_count = sum(1 for r in self.analysis_results.values() if r['expansion_detected'])
        
        report_content += f"""

## Conclusiones Generales

**Resumen estadístico:**
- Total de simulaciones analizadas: {total_analyses}
- Simulaciones con expansión detectada: {expansion_detected_count}
- Tasa de éxito: {(expansion_detected_count/total_analyses)*100:.1f}%

"""
        
        if expansion_detected_count > 0:
            report_content += f"""
### ✅ Evidencia Positiva Encontrada

Al menos una simulación muestra evidencia clara de expansión cosmológica consistente con las predicciones de la Conjetura del Universo Centrífugo. Esto sugiere que:

1. **El mecanismo es viable:** La rotación 4D puede generar expansión observable
2. **Los parámetros importan:** Las simulaciones exitosas proporcionan rangos de parámetros válidos
3. **La verificación es posible:** El enfoque numérico puede validar aspectos de la teoría

### Recomendaciones para investigación futura:

1. **Optimización de parámetros:** Usar los resultados exitosos para calibrar parámetros de rotación 4D
2. **Mayor resolución:** Ejecutar simulaciones de mayor resolución espacial y temporal
3. **Análisis paramétrico:** Explorar sistemáticamente el espacio de parámetros (R₄D, ω₄D)
4. **Comparación observacional:** Calcular valores de H₀ comparables con observaciones reales
"""
        else:
            report_content += f"""
### ⚠️ Sin Evidencia Clara

Ninguna de las simulaciones analizadas mostró evidencia convincente de expansión cosmológica. Esto no refuta necesariamente la Conjetura del Universo Centrífugo, pero indica que:

1. **Los parámetros necesitan ajuste:** Los valores actuales de R₄D y ω₄D pueden ser inadecuados
2. **Mayor tiempo de simulación:** Los efectos pueden requerir más tiempo para manifestarse
3. **Resolución insuficiente:** Se necesita mayor resolución para capturar efectos sutiles
4. **Revisión teórica:** Puede ser necesario refinar aspectos del modelo matemático

### Próximos pasos recomendados:

1. **Incrementar parámetros de rotación 4D** por factores de 2-10
2. **Extender tiempo de simulación** hasta t_final = 5.0 o mayor
3. **Usar resoluciones 512³ o superiores** cuando sea computacionalmente factible
4. **Revisar la implementación** del tensor energía-momento rotacional
"""
        
        report_content += f"""

## Metodología Validada

El análisis desarrollado proporciona un framework robusto para:

1. **Detección automática** de diferentes formatos de datos de simulación
2. **Cálculo consistente** de tasas de expansión basadas en invariantes métricos
3. **Evaluación estadística** de la significancia de los resultados
4. **Visualización comprensiva** de la evolución temporal

Este metodología puede aplicarse a simulaciones futuras de mayor resolución y diferentes configuraciones de parámetros.

---

*Análisis realizado con el framework de verificación de la Ley de Hubble*
*Basado en simulaciones BSSN de la Conjetura del Universo Centrífugo*
"""
        
        # Guardar reporte
        with open('hubble_verification_final_report.md', 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ Reporte final generado: hubble_verification_final_report.md")


def main():
    """
    Función principal del análisis final.
    """
    verifier = FinalHubbleLawVerifier()
    success = verifier.find_and_analyze_data()
    
    if success:
        print(f"\n🎉 ¡Análisis final completado exitosamente!")
        print(f"📁 Archivos generados:")
        print(f"   • hubble_verification_final_report.md")
        print(f"   • Gráficos de análisis (hubble_analysis_*.png)")
    else:
        print(f"\n❌ No se pudo completar el análisis")


if __name__ == "__main__":
    main()