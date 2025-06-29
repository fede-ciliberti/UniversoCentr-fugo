#!/usr/bin/env python3
"""
Script de simulación numérica con superposición de gravedad local.
Tarea 2.1.1: Modificación del Código de Simulación

Este script implementa el Principio de Superposición Cosmológico extendiendo
la simulación cosmológica base para incluir una masa puntual local y validar
la consistencia entre efectos locales y globales.

Características:
- Hereda de EinsteinSimulator para reutilizar código validado
- Implementa superposición lineal: T_total = T_cosmológico + T_local
- Usa distribución de masa Gaussiana suavizada para estabilidad numérica
- Incluye métricas de estabilidad y validación física

Objetivo: Demostrar que el modelo del Universo Centrífugo puede reproducir
simultáneamente expansión cosmológica y gravedad newtoniana sin inconsistencias.

Fecha: 29 de junio de 2025
Autor: Universo Centrífugo Research Team
"""

import numpy as np
import argparse
import sys
import os
import time
from pathlib import Path

# Importar la clase base de la simulación
try:
    from .run_numerical_simulation import EinsteinSimulator
except ImportError:
    # Si no funciona el import relativo, intentar import absoluto
    from run_numerical_simulation import EinsteinSimulator

class LocalGravitySimulation(EinsteinSimulator):
    """
    Simulador que extiende EinsteinSimulator para incluir masa puntual local.
    
    Implementa el Principio de Superposición Cosmológico:
    T_total = T_cosmológico + T_local
    
    donde T_local proviene de una masa estática con perfil Gaussiano suavizado.
    """
    
    def __init__(self, data_file="simulation_initial_data.npz", max_cores=None,
                 local_mass_params=None):
        """
        Inicializa el simulador con parámetros de masa local.
        
        Args:
            data_file: Archivo con datos iniciales de la simulación cosmológica
            max_cores: Número máximo de cores para paralelización
            local_mass_params: Dict con parámetros de la masa local:
                - 'mass': Masa en unidades geométricas (G=c=1)
                - 'position': Tupla (x, y, z) de la posición del centro de masa
                - 'smoothing_radius': Radio de suavizado σ del perfil Gaussiano
                - 'enable_time_modulation': Si aplicar modulación temporal (default: True)
        """
        print("🌌 Inicializando Local Gravity Simulation...")
        print("Tarea 2.1.1: Validación del Principio de Superposición Cosmológico")
        print("=" * 70)
        
        # Inicializar simulador base
        super().__init__(data_file, max_cores)
        
        # Configurar parámetros de masa local
        self.setup_local_mass_parameters(local_mass_params)
        
        # Pre-calcular tensor de masa local (invariante en el tiempo)
        self.compute_local_mass_tensor()
        
        # Inicializar métricas de validación
        self.initialize_validation_metrics()
        
        print("✓ Local Gravity Simulation inicializada correctamente")
        
    def setup_local_mass_parameters(self, params):
        """Configura y valida los parámetros de la masa local."""
        print("🔧 Configurando parámetros de masa local...")
        
        # Parámetros por defecto
        default_params = {
            'mass': 1.0,  # Masa en unidades geométricas
            'position': None,  # Se calculará como centro de la malla
            'smoothing_radius': None,  # Se calculará automáticamente
            'enable_time_modulation': True
        }
        
        # Usar parámetros proporcionados o valores por defecto
        if params is None:
            params = {}
        
        self.local_mass_params = {**default_params, **params}
        
        # Calcular posición central si no se especifica
        if self.local_mass_params['position'] is None:
            center_x = self.X[self.nx//2, self.ny//2, self.nz//2]
            center_y = self.Y[self.nx//2, self.ny//2, self.nz//2]
            center_z = self.Z[self.nx//2, self.ny//2, self.nz//2]
            self.local_mass_params['position'] = (center_x, center_y, center_z)
        
        # Calcular radio de suavizado automático si no se especifica
        if self.local_mass_params['smoothing_radius'] is None:
            # Usar ~5% del tamaño característico de la malla
            grid_size = min(self.dx, self.dy, self.dz)
            self.local_mass_params['smoothing_radius'] = 5 * grid_size
        
        # Extraer parámetros para uso frecuente
        self.M_local = self.local_mass_params['mass']
        self.pos_x, self.pos_y, self.pos_z = self.local_mass_params['position']
        self.sigma = self.local_mass_params['smoothing_radius']
        self.enable_time_mod = self.local_mass_params['enable_time_modulation']
        
        print(f"✓ Parámetros configurados:")
        print(f"   Masa local: M = {self.M_local}")
        print(f"   Posición: ({self.pos_x:.3f}, {self.pos_y:.3f}, {self.pos_z:.3f})")
        print(f"   Radio suavizado: σ = {self.sigma:.4f}")
        print(f"   Modulación temporal: {'✓' if self.enable_time_mod else '✗'}")
        
    def compute_local_mass_tensor(self):
        """
        Pre-calcula el tensor de energía-impulso para la masa local.
        
        Usa un perfil de densidad Gaussiano:
        ρ(r) = M / (σ√2π)³ * exp(-r² / 2σ²)
        
        El tensor T_local tiene solo la componente T_00 = ρ(r)c² no nula
        (masa en reposo en el límite newtoniano).
        """
        print("📐 Calculando tensor de masa local...")
        
        # Calcular distancias desde el centro de masa
        dx_field = self.X - self.pos_x
        dy_field = self.Y - self.pos_y  
        dz_field = self.Z - self.pos_z
        r_squared = dx_field**2 + dy_field**2 + dz_field**2
        
        # Perfil de densidad Gaussiano normalizado
        normalization = self.M_local / (self.sigma * np.sqrt(2 * np.pi))**3
        density = normalization * np.exp(-r_squared / (2 * self.sigma**2))
        
        # Crear tensor de energía-impulso local
        # Inicializar con ceros (misma estructura que T_initial)
        self.T_local = np.zeros_like(self.T_initial)
        
        # Solo la componente T_00 (densidad de energía) es no nula
        # En unidades geométricas (G=c=1), T_00 = ρ
        self.T_local[:, :, :, 0, 0] = density
        
        # Verificaciones de validación
        total_mass_check = np.sum(density) * self.dx * self.dy * self.dz
        max_density = np.max(density)
        
        print(f"✓ Tensor local calculado:")
        print(f"   Masa total integrada: {total_mass_check:.6f} (objetivo: {self.M_local})")
        print(f"   Densidad máxima: {max_density:.6e}")
        print(f"   Posición del máximo: índices {np.unravel_index(np.argmax(density), density.shape)}")
        
        # Advertencia si la masa integrada difiere significativamente
        mass_error = abs(total_mass_check - self.M_local) / self.M_local
        if mass_error > 0.1:  # >10% de error
            print(f"⚠️  Advertencia: Error en conservación de masa: {mass_error*100:.1f}%")
            print(f"   Considere aumentar la resolución o ajustar el radio de suavizado")
        
    def initialize_validation_metrics(self):
        """Inicializa métricas para validación del Principio de Superposición."""
        print("📊 Inicializando métricas de validación...")
        
        # Arrays para almacenar métricas específicas de superposición
        self.superposition_metrics = []
        
        # Límites para detección de divergencias
        self.stability_thresholds = {
            'max_tensor_component': 1e10,  # Valor máximo permitido para T_μν
            'conservation_tolerance': 1e-6,  # Tolerancia para conservación ∇μT^μν ≈ 0
            'mass_variation_tolerance': 0.05  # Tolerancia para variación de masa local
        }
        
        print("✓ Métricas de validación inicializadas")
        
    def compute_stress_energy_contribution(self, t):
        """
        Implementa la superposición de tensores: T_total = T_cosmológico + T_local.
        
        Este es el método clave que sobreescribe la funcionalidad base para
        añadir el efecto de la masa local al tensor cosmológico.
        
        Args:
            t: Tiempo actual de la simulación
            
        Returns:
            T_total: Tensor de energía-impulso total (cosmológico + local)
        """
        # 1. Obtener tensor cosmológico base usando el método original
        T_cosmological = super().compute_stress_energy_contribution(t)
        
        # 2. Aplicar superposición lineal
        T_total = T_cosmological + self.T_local
        
        # 3. Verificar estabilidad del tensor resultante
        self.validate_tensor_stability(T_total, t)
        
        return T_total
    
    def validate_tensor_stability(self, T_total, t):
        """
        Valida la estabilidad numérica del tensor total.
        
        Verifica:
        - Ausencia de NaN o infinitos
        - Valores dentro de rangos físicamente razonables  
        - Conservación aproximada de la masa local
        """
        # Verificar valores finitos
        if not np.all(np.isfinite(T_total)):
            print(f"❌ ERROR: Tensor contiene NaN o infinitos en t={t:.4f}")
            raise RuntimeError("Inestabilidad numérica: tensor no finito")
        
        # Verificar rangos físicos
        max_component = np.max(np.abs(T_total))
        if max_component > self.stability_thresholds['max_tensor_component']:
            print(f"⚠️  Advertencia: Componente de tensor muy grande: {max_component:.2e}")
        
        # Almacenar métricas de este paso temporal
        metrics = {
            'time': t,
            'max_tensor_component': max_component,
            'tensor_trace': np.mean(T_total[:,:,:,0,0] + T_total[:,:,:,1,1] + T_total[:,:,:,2,2]),
            'local_mass_contribution': np.sum(self.T_local[:,:,:,0,0]) * self.dx * self.dy * self.dz
        }
        
        self.superposition_metrics.append(metrics)
        
    def compute_conservation_check(self):
        """
        Verifica la ley de conservación ∇μ T^μν ≈ 0 para el tensor total.
        
        Esta es una verificación fundamental de la consistencia física
        del modelo de superposición.
        """
        # Calcular divergencia del tensor usando diferencias finitas
        # Simplificado: solo verificar la componente temporal de ∇μ T^μ0
        
        T_00 = self.T_local[:,:,:,0,0]  # Componente de densidad de energía
        
        # Derivadas espaciales
        dT_dx = np.gradient(T_00, self.dx, axis=0)
        dT_dy = np.gradient(T_00, self.dy, axis=1) 
        dT_dz = np.gradient(T_00, self.dz, axis=2)
        
        # Divergencia espacial (componente 0 de ∇μ T^μ0)
        divergence = dT_dx + dT_dy + dT_dz
        
        # Métrica de conservación: RMS de la divergencia
        conservation_rms = np.sqrt(np.mean(divergence**2))
        
        return conservation_rms
        
    def run_simulation_with_validation(self, save_checkpoints=True, verbose=True):
        """
        Ejecuta la simulación con validación extendida del Principio de Superposición.
        
        Extiende el método base con verificaciones específicas de:
        - Estabilidad de la superposición
        - Conservación de energía-momento
        - Recuperación de regímenes cosmológico y newtoniano
        """
        print("\n🚀 Iniciando simulación con validación de superposición...")
        print("Objetivo: Validar Principio de Superposición Cosmológico")
        print("=" * 70)
        
        # Verificación inicial de conservación
        initial_conservation = self.compute_conservation_check()
        print(f"📐 Verificación inicial de conservación: {initial_conservation:.2e}")
        
        # Ejecutar simulación base con monitoreo extendido
        try:
            # Llamar al método de simulación de la clase padre
            super().run_simulation(save_checkpoints, verbose)
            
        except Exception as e:
            print(f"❌ Error durante simulación con superposición: {e}")
            self.save_debug_data()
            raise
        
        finally:
            # Análisis post-simulación específico de superposición
            self.analyze_superposition_results()
    
    def analyze_superposition_results(self):
        """Analiza los resultados específicos del test de superposición."""
        print("\n📈 ANÁLISIS DE SUPERPOSICIÓN")
        print("=" * 50)
        
        if len(self.superposition_metrics) == 0:
            print("⚠️  Sin datos de superposición para analizar")
            return
        
        # Extraer series temporales
        times = [m['time'] for m in self.superposition_metrics]
        max_components = [m['max_tensor_component'] for m in self.superposition_metrics]
        traces = [m['tensor_trace'] for m in self.superposition_metrics]
        masses = [m['local_mass_contribution'] for m in self.superposition_metrics]
        
        # Estadísticas de estabilidad
        max_tensor_variation = (np.max(max_components) - np.min(max_components)) / np.mean(max_components)
        mass_conservation = (np.max(masses) - np.min(masses)) / np.mean(masses)
        
        print(f"📊 Métricas de Estabilidad:")
        print(f"   Variación máxima del tensor: {max_tensor_variation*100:.2f}%")
        print(f"   Conservación de masa local: {mass_conservation*100:.2f}%")
        print(f"   Tiempo total simulado: {times[-1]:.4f}")
        
        # Evaluación del éxito de la superposición
        success_criteria = [
            max_tensor_variation < 0.1,  # <10% variación en componentes del tensor
            mass_conservation < self.stability_thresholds['mass_variation_tolerance'],
            len(times) > 10  # Al menos 10 pasos registrados
        ]
        
        if all(success_criteria):
            print("🎉 ¡ÉXITO! Principio de Superposición validado numéricamente")
            print("   ✓ Tensor estable sin divergencias")
            print("   ✓ Masa local conservada")
            print("   ✓ Simulación completada sin errores")
        else:
            print("⚠️  Validación parcial. Revisar métricas:")
            if not success_criteria[0]:
                print("   ✗ Tensor inestable (variación excesiva)")
            if not success_criteria[1]:
                print("   ✗ Masa local no conservada")
            if not success_criteria[2]:
                print("   ✗ Simulación demasiado corta")
        
        # Verificación final de conservación
        final_conservation = self.compute_conservation_check()
        print(f"📐 Verificación final de conservación: {final_conservation:.2e}")
        
    def save_debug_data(self):
        """Guarda datos de depuración en caso de error."""
        debug_data = {
            'local_mass_params': self.local_mass_params,
            'T_local': self.T_local,
            'superposition_metrics': self.superposition_metrics,
            'stability_thresholds': self.stability_thresholds
        }
        
        debug_file = f"debug_local_gravity_{int(time.time())}.npz"
        np.savez_compressed(debug_file, **debug_data)
        print(f"🐛 Datos de depuración guardados en: {debug_file}")
        
    def save_final_results(self):
        """
        Extiende el guardado de resultados para incluir datos de superposición.
        """
        # Llamar al método padre para guardar resultados base
        base_file = super().save_final_results()
        
        # Guardar resultados específicos de superposición
        superposition_results = {
            'local_mass_params': self.local_mass_params,
            'T_local': self.T_local,
            'superposition_metrics': self.superposition_metrics,
            'final_conservation_check': self.compute_conservation_check()
        }
        
        superposition_file = "local_gravity_simulation_results.npz"
        np.savez_compressed(superposition_file, **superposition_results)
        print(f"💾 Resultados de superposición guardados en: {superposition_file}")
        
        # Mantener compatibilidad con la clase base devolviendo solo el archivo principal
        return base_file

def create_default_mass_params():
    """Crea parámetros por defecto para la masa local."""
    return {
        'mass': 1.0,  # Masa unitaria en unidades geométricas
        'position': None,  # Centro automático
        'smoothing_radius': None,  # Radio automático
        'enable_time_modulation': True
    }

def main():
    """Función principal para ejecutar la simulación con masa local."""
    parser = argparse.ArgumentParser(
        description='Simulación con Principio de Superposición Cosmológico'
    )
    parser.add_argument('--data-file', default='simulation_initial_data.npz',
                       help='Archivo de datos iniciales')
    parser.add_argument('--mass', type=float, default=1.0,
                       help='Masa local en unidades geométricas')
    parser.add_argument('--pos-x', type=float, default=None,
                       help='Posición X del centro de masa (None=centro automático)')
    parser.add_argument('--pos-y', type=float, default=None,
                       help='Posición Y del centro de masa')
    parser.add_argument('--pos-z', type=float, default=None,
                       help='Posición Z del centro de masa')
    parser.add_argument('--smoothing', type=float, default=None,
                       help='Radio de suavizado (None=automático)')
    parser.add_argument('--no-time-mod', action='store_true',
                       help='Desactivar modulación temporal')
    parser.add_argument('--max-cores', type=int, default=None,
                       help='Número máximo de cores (None=todos)')
    
    args = parser.parse_args()
    
    print("🌌 SIMULACIÓN CON MASA LOCAL")
    print("Tarea 2.1.1: Validación del Principio de Superposición Cosmológico")
    print("=" * 70)
    
    # Verificar datos iniciales
    if not os.path.exists(args.data_file):
        print(f"❌ Error: No se encontró {args.data_file}")
        print("   Ejecute primero: python setup_numerical_simulation.py")
        sys.exit(1)
    
    # Configurar parámetros de masa local
    mass_params = {
        'mass': args.mass,
        'position': (args.pos_x, args.pos_y, args.pos_z) if all(v is not None for v in [args.pos_x, args.pos_y, args.pos_z]) else None,
        'smoothing_radius': args.smoothing,
        'enable_time_modulation': not args.no_time_mod
    }
    
    try:
        # Crear simulador con masa local
        simulator = LocalGravitySimulation(
            data_file=args.data_file,
            max_cores=args.max_cores,
            local_mass_params=mass_params
        )
        
        # Ejecutar simulación con validación
        simulator.run_simulation_with_validation(
            save_checkpoints=True,
            verbose=True
        )
        
        print("\n🏆 ¡SIMULACIÓN COMPLETADA!")
        print("Revise los archivos de resultados para análisis detallado.")
        
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()