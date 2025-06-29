#!/usr/bin/env python3
"""
Validador Principal de Regímenes Físicos - Tarea 2.1.2
Validación de Regímenes Físicos del Principio de Superposición Cosmológico

Este es el script principal que coordina la validación física completa.
Utiliza módulos especializados para cada tipo de análisis.

Objetivo: Demostrar cuantitativamente que el Principio de Superposición Cosmológico
funciona no solo matemáticamente sino también físicamente según las predicciones teóricas.

Fecha: 29 de junio de 2025
Autor: Universo Centrífugo Research Team
Tarea: 2.1.2 - Validación de Regímenes Físicos
"""

import numpy as np
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Importar módulos especializados
try:
    from .regime_validators import LocalRegimeValidator, GlobalRegimeValidator, TransitionAnalyzer
    from .validation_visualizer import ValidationVisualizer
    from .validation_reporter import ValidationReporter
except ImportError:
    # Fallback para ejecución directa
    from regime_validators import LocalRegimeValidator, GlobalRegimeValidator, TransitionAnalyzer
    from validation_visualizer import ValidationVisualizer
    from validation_reporter import ValidationReporter

class PhysicalRegimeValidator:
    """
    Coordinador principal para la validación de regímenes físicos.
    
    Orchestrates the complete physical validation process for the
    Cosmological Superposition Principle implementation.
    """
    
    def __init__(self, tolerance_local=0.01, tolerance_global=0.05):
        """
        Inicializa el validador principal.
        
        Args:
            tolerance_local: Tolerancia para desviación del régimen de Schwarzschild (default: 1%)
            tolerance_global: Tolerancia para desviación del régimen cosmológico (default: 5%)
        """
        self.tolerance_local = tolerance_local
        self.tolerance_global = tolerance_global
        
        print("🔬 VALIDADOR DE REGÍMENES FÍSICOS")
        print("Tarea 2.1.2: Validación del Principio de Superposición Cosmológico")
        print("=" * 70)
        print(f"📊 Tolerancias configuradas:")
        print(f"   • Régimen local: {tolerance_local*100:.1f}%")
        print(f"   • Régimen global: {tolerance_global*100:.1f}%")
        
        # Inicializar componentes especializados
        self.local_validator = LocalRegimeValidator(tolerance_local)
        self.global_validator = GlobalRegimeValidator(tolerance_global)
        self.transition_analyzer = TransitionAnalyzer()
        self.visualizer = ValidationVisualizer()
        self.reporter = ValidationReporter()
        
        # Almacenar resultados
        self.validation_results: Dict[str, Any] = {
            'local_regime': {},
            'global_regime': {},
            'transition_zone': {},
            'decoupling': {},
            'parameters': {},
            'overall_success': False,
            'visualization_files': {},
            'report_file': ''
        }
    
    def load_simulation_data(self):
        """
        Carga los datos de simulación requeridos para el análisis.
        
        Returns:
            dict: Datos de simulación cargados exitosamente o None si falla
        """
        print("\n📁 CARGANDO DATOS DE SIMULACIÓN")
        print("=" * 50)
        
        required_files = {
            'base_results': 'simulation_results.npz',
            'local_results': 'local_gravity_simulation_results.npz',
            'initial_data': 'simulation_initial_data.npz'
        }
        
        data = {}
        
        for file_type, filename in required_files.items():
            try:
                data[file_type] = np.load(filename, allow_pickle=True)
                print(f"✅ {filename} cargado exitosamente")
            except FileNotFoundError:
                print(f"❌ Error: No se encontró {filename}")
                print(f"   Ejecute primero: python run_local_gravity_simulation.py")
                return None
        
        # Extraer parámetros críticos
        local_params = data['local_results']['local_mass_params'].item()
        self.mass_local = local_params['mass']
        self.position_local = local_params['position']
        self.smoothing_radius = local_params['smoothing_radius']
        
        print(f"\n📋 Parámetros de masa local detectados:")
        print(f"   • Masa: M = {self.mass_local}")
        print(f"   • Posición: {self.position_local}")
        print(f"   • Radio de suavizado: σ = {self.smoothing_radius:.4f}")
        
        return data
    
    def run_complete_validation(self):
        """
        Ejecuta la validación completa de regímenes físicos.
        
        Returns:
            dict: Resultados completos de la validación
        """
        print("\n🚀 INICIANDO VALIDACIÓN COMPLETA DE REGÍMENES")
        print("=" * 60)
        
        # 1. Cargar datos
        data = self.load_simulation_data()
        if data is None:
            return {'success': False, 'error': 'Failed to load simulation data'}
        
        # 2. Preparar datos comunes
        common_data = self._prepare_common_data(data)
        
        # 3. Ejecutar validaciones especializadas
        print("\n🔍 Ejecutando validaciones especializadas...")
        
        # Validación del régimen local (Schwarzschild)
        local_results = self.local_validator.validate(common_data)
        
        # Validación del régimen global (cosmológico)
        global_results = self.global_validator.validate(common_data)
        
        # Análisis de la zona de transición
        transition_results = self.transition_analyzer.analyze(common_data)
        
        # Verificación de desacoplamiento
        decoupling_results = self._verify_decoupling(local_results, global_results)
        
        # 4. Consolidar resultados
        self.validation_results = {
            'local_regime': local_results,
            'global_regime': global_results,
            'transition_zone': transition_results,
            'decoupling': decoupling_results,
            'parameters': {
                'mass_local': self.mass_local,
                'position_local': self.position_local,
                'smoothing_radius': self.smoothing_radius,
                'tolerance_local': self.tolerance_local,
                'tolerance_global': self.tolerance_global
            }
        }
        
        # 5. Generar visualizaciones
        print("\n📊 Generando visualizaciones...")
        visualization_files = self.visualizer.create_all_visualizations(
            self.validation_results, common_data
        )
        
        # 6. Generar informe técnico
        print("\n📋 Generando informe técnico...")
        report_file = self.reporter.generate_report(
            self.validation_results, visualization_files
        )
        
        # 7. Evaluación final
        overall_success = self._evaluate_overall_success()
        
        self.validation_results['overall_success'] = overall_success
        self.validation_results['visualization_files'] = visualization_files
        self.validation_results['report_file'] = report_file
        
        return self.validation_results
    
    def _prepare_common_data(self, data):
        """
        Prepara datos comunes para todos los validadores.
        
        Args:
            data: Datos de simulación cargados
            
        Returns:
            dict: Datos procesados y listos para análisis
        """
        # Extraer componentes de la métrica
        metric_components = {
            'gamma_xx': data['base_results']['final_gamma_xx'],
            'gamma_yy': data['base_results']['final_gamma_yy'],
            'gamma_zz': data['base_results']['final_gamma_zz'],
            'gamma_xy': data['base_results']['final_gamma_xy'],
            'gamma_xz': data['base_results']['final_gamma_xz'],
            'gamma_yz': data['base_results']['final_gamma_yz']
        }
        
        # Coordenadas espaciales
        X = data['initial_data']['X']
        Y = data['initial_data']['Y'] 
        Z = data['initial_data']['Z']
        
        # Sistema de coordenadas centrado en la masa
        x_centered = X - self.position_local[0]
        y_centered = Y - self.position_local[1]
        z_centered = Z - self.position_local[2]
        r_field = np.sqrt(x_centered**2 + y_centered**2 + z_centered**2)
        
        # Definir regiones de análisis
        regions, regions_info = self._define_analysis_regions(r_field)
        
        return {
            'metric_components': metric_components,
            'coordinates': {'X': X, 'Y': Y, 'Z': Z},
            'centered_coords': {'x': x_centered, 'y': y_centered, 'z': z_centered},
            'r_field': r_field,
            'regions': regions,
            'regions_info': regions_info,
            'raw_data': data,
            'mass_params': {
                'mass': self.mass_local,
                'position': self.position_local,
                'smoothing_radius': self.smoothing_radius
            }
        }
    
    def _define_analysis_regions(self, r_field):
        """
        Define las regiones de análisis según los criterios establecidos.
        
        Args:
            r_field: Campo de distancias radiales
            
        Returns:
            tuple: (regions_dict, regions_info_dict)
        """
        # Calcular escalas características
        L_box = np.max(r_field)
        sigma = self.smoothing_radius
        
        # Definir límites de regiones
        r_local_min = 3 * sigma
        r_local_max = 0.1 * L_box
        r_global_min = 0.5 * L_box
        
        # Crear máscaras para cada región
        regions = {
            'local': (r_field >= r_local_min) & (r_field <= r_local_max),
            'transition': (r_field > r_local_max) & (r_field < r_global_min),
            'global': (r_field >= r_global_min)
        }
        
        regions_info = {
            'r_local_min': r_local_min,
            'r_local_max': r_local_max,
            'r_global_min': r_global_min,
            'L_box': L_box,
            'sigma': sigma
        }
        
        print(f"\n🎯 Regiones de análisis definidas:")
        for region_name, mask in regions.items():
            n_points = np.sum(mask)
            print(f"   • Región {region_name}: {n_points} puntos")
        
        return regions, regions_info
    
    def _verify_decoupling(self, local_results, global_results):
        """
        Verifica que los regímenes no interfieren entre sí de manera no física.
        
        Args:
            local_results: Resultados de validación local
            global_results: Resultados de validación global
            
        Returns:
            dict: Resultados de verificación de desacoplamiento
        """
        print("\n🔄 VERIFICANDO DESACOPLAMIENTO DE REGÍMENES")
        print("=" * 50)
        
        decoupling_results = {'success': True, 'issues': []}
        
        # Test 1: Consistencia de masa local
        if local_results.get('success', False):
            # Verificar que las diferentes medidas de masa son consistentes
            mass_measurements = local_results.get('mass_measurements', {})
            if len(mass_measurements) > 1:
                masses = list(mass_measurements.values())
                mass_std = np.std(masses)
                mass_consistency = mass_std / self.mass_local
                
                print(f"🧪 Test 1: Consistencia de masa efectiva")
                print(f"   • Desviación estándar: {mass_consistency*100:.2f}%")
                
                if mass_consistency > 0.1:  # 10% de inconsistencia
                    decoupling_results['issues'].append('mass_inconsistency')
                    decoupling_results['success'] = False
                    print(f"   ❌ Inconsistencia excesiva entre medidas")
                else:
                    print(f"   ✅ Masa efectiva consistente")
        
        # Test 2: Independencia del régimen global
        if global_results.get('success', False):
            max_perturbation = global_results.get('max_perturbation', 0)
            
            print(f"\n🧪 Test 2: Independencia del régimen global")
            print(f"   • Perturbación máxima: {max_perturbation:.6f}")
            
            if max_perturbation > self.tolerance_global * 2:
                decoupling_results['issues'].append('global_contamination')
                print(f"   ⚠️  Régimen global posiblemente afectado")
            else:
                print(f"   ✅ Régimen global independiente")
        
        return decoupling_results
    
    def _evaluate_overall_success(self):
        """
        Evalúa el éxito general de la validación.
        
        Returns:
            bool: True si la validación es exitosa globalmente
        """
        local_success = self.validation_results['local_regime'].get('success', False)
        global_success = self.validation_results['global_regime'].get('success', False)
        transition_success = self.validation_results['transition_zone'].get('success', False)
        decoupling_success = self.validation_results['decoupling'].get('success', False)
        
        # Criterio: al menos 3 de 4 tests deben pasar
        successful_tests = sum([local_success, global_success, transition_success, decoupling_success])
        overall_success = successful_tests >= 3
        
        print(f"\n🏆 EVALUACIÓN FINAL")
        print("=" * 30)
        print(f"✅ Tests exitosos: {successful_tests}/4")
        print(f"{'🎉 VALIDACIÓN EXITOSA' if overall_success else '⚠️  VALIDACIÓN PARCIAL'}")
        
        return overall_success

def main():
    """Función principal para ejecutar la validación completa."""
    try:
        validator = PhysicalRegimeValidator()
        results = validator.run_complete_validation()
        
        if results.get('overall_success', False):
            print(f"\n🎯 CONCLUSIÓN: Principio de Superposición Cosmológico VALIDADO")
            print(f"📄 Informe completo: {results.get('report_file', 'N/A')}")
        else:
            print(f"\n⚠️  CONCLUSIÓN: Validación parcial. Revisar resultados.")
        
        return 0 if results.get('overall_success', False) else 1
        
    except Exception as e:
        print(f"❌ Error durante validación: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())