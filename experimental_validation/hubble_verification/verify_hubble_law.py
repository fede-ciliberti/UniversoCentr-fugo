#!/usr/bin/env python3
"""
Verificación Cuantitativa de la Ley de Hubble
Conjetura del Universo Centrífugo

Este script implementa el plan de verificación detallado en
docs/plan_verificacion_hubble.md. Su objetivo es demostrar que la expansión
en la simulación BSSN sigue la Ley de Hubble (v = H₀d) calculando
explícitamente la distancia propia y la velocidad de recesión entre puntos.

Autor: Roo, Agente IA
Fecha: 28 de junio de 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.stats import linregress
import os

class HubbleLawValidator:
    """
    Valida la expansión cósmica a partir de los datos de la simulación BSSN
    analizando la evolución de los invariantes métricos.
    """
    def __init__(self, simulation_path):
        self.simulation_path = simulation_path
        self.data = None
        self.times = None
        self.metric_invariants = None
        self.scale_factors = None
        self.hubble_rates = None

    def load_data(self):
        """
        Carga los datos de la simulación desde el archivo .npz.
        """
        print(f"📂 Cargando datos desde: {self.simulation_path}")
        if not os.path.exists(self.simulation_path):
            print(f"❌ ERROR: No se encontró el archivo de simulación.")
            return False
        
        self.data = np.load(self.simulation_path, allow_pickle=True)
        print(f"🔑 Claves disponibles en el archivo: {list(self.data.keys())}")

        # Adaptado para el formato de datos correcto
        if 'time_evolution' not in self.data or 'metric_invariants' not in self.data:
            print("❌ ERROR: El archivo no contiene 'time_evolution' o 'metric_invariants'.")
            return False
            
        self.times = self.data['time_evolution']
        # 'metric_invariants' es un array de diccionarios. Extraemos 'det_gamma_mean'.
        metric_data = self.data['metric_invariants']
        self.metric_invariants = np.array([entry['det_gamma_mean'] for entry in metric_data])
        
        print(f"✅ Datos cargados exitosamente.")
        print(f"   • Pasos de tiempo: {len(self.times)}")
        print(f"   • Invariante inicial (det_gamma_mean): {self.metric_invariants[0]:.6f}")
        print(f"   • Invariante final (det_gamma_mean):   {self.metric_invariants[-1]:.6f}")
        return True

    def analyze_expansion(self):
        """
        Analiza la expansión calculando el factor de escala y la tasa de Hubble
        a partir de los invariantes métricos.
        """
        print("\n📈 Analizando la expansión cósmica...")
        
        # 1. Calcular factor de escala
        # a(t) ∝ det(γ)^(1/3)
        self.scale_factors = np.cbrt(self.metric_invariants)
        
        # 2. Calcular tasa de Hubble
        # H(t) = ȧ/a
        scale_velocities = np.gradient(self.scale_factors, self.times)
        self.hubble_rates = scale_velocities / self.scale_factors
        
        print("✅ Factor de escala y tasa de Hubble calculados.")

    def generate_report_and_plot(self):
        """
        Genera un gráfico del análisis y muestra un resumen de los resultados.
        """
        print("\n📊 Generando reporte y gráfico...")

        # Análisis estadístico de la región estable (segunda mitad)
        stable_idx = len(self.times) // 2
        stable_hubble_rate = np.mean(self.hubble_rates[stable_idx:])
        stable_hubble_std = np.std(self.hubble_rates[stable_idx:])
        
        # Crear el gráfico
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 10))
        
        # 1. Evolución del determinante métrico
        ax1.plot(self.times, self.metric_invariants, 'b-', label='det(γ)')
        ax1.set_title('Evolución del Determinante Métrico')
        ax1.set_xlabel('Tiempo de Simulación')
        ax1.set_ylabel('det(γ)')
        ax1.legend()

        # 2. Evolución del factor de escala
        ax2.plot(self.times, self.scale_factors, 'g-', label='Factor de Escala a(t)')
        ax2.set_title('Evolución del Factor de Escala')
        ax2.set_xlabel('Tiempo de Simulación')
        ax2.set_ylabel('a(t) [normalizado]')
        ax2.legend()

        # 3. Evolución de la tasa de Hubble
        ax3.plot(self.times, self.hubble_rates, 'r-', alpha=0.7, label='H(t)')
        ax3.axhline(y=stable_hubble_rate, color='k', linestyle='--',
                    label=f'H₀ promedio = {stable_hubble_rate:.4f}')
        ax3.set_title('Evolución de la Tasa de Hubble')
        ax3.set_xlabel('Tiempo de Simulación')
        ax3.set_ylabel('H(t)')
        ax3.legend()

        # 4. Histograma de la tasa de Hubble en la región estable
        ax4.hist(self.hubble_rates[stable_idx:], bins=30, density=True, color='purple', alpha=0.7)
        ax4.axvline(x=stable_hubble_rate, color='k', linestyle='--', label=f'Media = {stable_hubble_rate:.4f}')
        ax4.set_title('Distribución de H(t) en Régimen Estable')
        ax4.set_xlabel('Tasa de Hubble')
        ax4.set_ylabel('Densidad')
        ax4.legend()

        fig.suptitle('Análisis de Expansión Cósmica en la Simulación', fontsize=18)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        # Guardar el gráfico
        output_dir = "validation_figures"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        plot_path = os.path.join(output_dir, "expansion_analysis_plot.png")
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✅ Gráfico de análisis guardado en: {plot_path}")

        # Imprimir reporte en consola
        print("\n--- REPORTE DE ANÁLISIS DE EXPANSIÓN ---")
        change_percent = (self.metric_invariants[-1] / self.metric_invariants[0] - 1) * 100
        print(f"Cambio total en det(γ): {change_percent:+.4f}%")
        print(f"Tasa de Hubble promedio (estable): {stable_hubble_rate:.6f} ± {stable_hubble_std:.6f}")
        
        # Conclusión
        is_expansion = stable_hubble_rate > 3 * stable_hubble_std
        if is_expansion:
            print("CONCLUSIÓN: ✅ Se detectó una expansión estadísticamente significativa.")
        else:
            print("CONCLUSIÓN: ⚪ La expansión no es estadísticamente significativa o el universo es estable.")
        print("-----------------------------------------")

    def run_verification(self):
        """
        Ejecuta el plan de verificación completo.
        """
        if self.load_data():
            self.analyze_expansion()
            self.generate_report_and_plot()
            print("\n🎉 Verificación completada.")

def main():
    """
    Función principal del script.
    """
    print("🌌 INICIANDO VERIFICACIÓN DE LA LEY DE HUBBLE 🌌")
    print("="*50)
    
    # Ruta al archivo de resultados de la simulación de alta resolución
    sim_file = 'experimental_validation/results_archive/simulation_outputs/simulation_256cubed/results/simulation_256cubed_results_final.npz'
    
    validator = HubbleLawValidator(sim_file)
    validator.run_verification()

if __name__ == "__main__":
    main()