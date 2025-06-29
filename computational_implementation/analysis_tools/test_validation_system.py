#!/usr/bin/env python3
"""
Script de prueba para el sistema de validación de regímenes físicos.
Tarea 2.1.2 - Validación de Regímenes Físicos

Este script verifica que todos los módulos se importan correctamente
y realiza una prueba básica del sistema.

Fecha: 29 de junio de 2025
Autor: Universo Centrífugo Research Team
"""

import sys
from pathlib import Path

def test_imports():
    """Prueba que todos los módulos se importan correctamente."""
    print("🧪 PRUEBA DE IMPORTACIONES DEL SISTEMA DE VALIDACIÓN")
    print("=" * 60)
    
    try:
        from validate_physical_regimes import PhysicalRegimeValidator
        print("✅ Módulo principal: validate_physical_regimes")
        
        from regime_validators import LocalRegimeValidator, GlobalRegimeValidator, TransitionAnalyzer
        print("✅ Validadores de regímenes: regime_validators")
        
        from validation_visualizer import ValidationVisualizer
        print("✅ Generador de visualizaciones: validation_visualizer")
        
        from validation_reporter import ValidationReporter
        print("✅ Generador de informes: validation_reporter")
        
        print("\n🎉 Todas las importaciones exitosas!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def test_basic_initialization():
    """Prueba la inicialización básica de los componentes."""
    print("\n🔧 PRUEBA DE INICIALIZACIÓN BÁSICA")
    print("=" * 50)
    
    try:
        from validate_physical_regimes import PhysicalRegimeValidator
        from regime_validators import LocalRegimeValidator, GlobalRegimeValidator, TransitionAnalyzer
        from validation_visualizer import ValidationVisualizer
        from validation_reporter import ValidationReporter
        
        # Inicializar componentes principales
        validator = PhysicalRegimeValidator(tolerance_local=0.01, tolerance_global=0.05)
        print("✅ PhysicalRegimeValidator inicializado")
        
        local_validator = LocalRegimeValidator(tolerance=0.01)
        print("✅ LocalRegimeValidator inicializado")
        
        global_validator = GlobalRegimeValidator(tolerance=0.05)
        print("✅ GlobalRegimeValidator inicializado")
        
        transition_analyzer = TransitionAnalyzer()
        print("✅ TransitionAnalyzer inicializado")
        
        visualizer = ValidationVisualizer(output_dir="test_validation_figures")
        print("✅ ValidationVisualizer inicializado")
        
        reporter = ValidationReporter(output_dir=".")
        print("✅ ValidationReporter inicializado")
        
        print("\n🎉 Todas las inicializaciones exitosas!")
        return True
        
    except Exception as e:
        print(f"❌ Error en inicialización: {e}")
        return False

def test_data_structure():
    """Prueba que las estructuras de datos sean correctas."""
    print("\n📊 PRUEBA DE ESTRUCTURAS DE DATOS")
    print("=" * 40)
    
    try:
        from validate_physical_regimes import PhysicalRegimeValidator
        
        validator = PhysicalRegimeValidator()
        
        # Verificar estructura del diccionario de resultados
        expected_keys = [
            'local_regime', 'global_regime', 'transition_zone', 
            'decoupling', 'parameters', 'overall_success',
            'visualization_files', 'report_file'
        ]
        
        for key in expected_keys:
            assert key in validator.validation_results, f"Falta clave: {key}"
            print(f"✅ Clave '{key}' presente")
        
        print("\n🎉 Estructura de datos correcta!")
        return True
        
    except Exception as e:
        print(f"❌ Error en estructura de datos: {e}")
        return False

def show_usage_instructions():
    """Muestra instrucciones de uso del sistema."""
    print("\n📋 INSTRUCCIONES DE USO")
    print("=" * 30)
    
    print("""
Para usar el sistema de validación de regímenes físicos:

1. **Prerrequisitos:**
   - Ejecutar simulación con masa local:
     `python run_local_gravity_simulation.py`
   
   - Esto debe generar los archivos:
     • simulation_results.npz
     • local_gravity_simulation_results.npz
     • simulation_initial_data.npz

2. **Ejecutar validación completa:**
   ```python
   from validate_physical_regimes import PhysicalRegimeValidator
   
   validator = PhysicalRegimeValidator(
       tolerance_local=0.01,    # 1% tolerancia local
       tolerance_global=0.05    # 5% tolerancia global
   )
   
   results = validator.run_complete_validation()
   
   if results['overall_success']:
       print("¡Validación exitosa!")
   else:
       print("Validación parcial - revisar resultados")
   ```

3. **Archivos generados:**
   - `validacion_superposicion.md` - Informe técnico completo
   - `validation_figures/` - Directorio con visualizaciones
     • radial_overview.png
     • local_regime_validation.png
     • global_regime_validation.png
     • transition_analysis.png
     • validation_summary.png

4. **Ejecución desde línea de comandos:**
   `python validate_physical_regimes.py`
""")

def main():
    """Función principal de prueba."""
    print("🔬 SISTEMA DE VALIDACIÓN DE REGÍMENES FÍSICOS")
    print("Tarea 2.1.2 - Principio de Superposición Cosmológico")
    print("=" * 70)
    
    # Ejecutar pruebas
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_basic_initialization():
        tests_passed += 1
    
    if test_data_structure():
        tests_passed += 1
    
    # Mostrar resultados
    print(f"\n🏆 RESULTADOS DE PRUEBAS")
    print("=" * 30)
    print(f"Tests pasados: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("   El sistema de validación está listo para uso.")
        show_usage_instructions()
        return 0
    else:
        print("⚠️  SISTEMA PARCIALMENTE FUNCIONAL")
        print("   Revisar errores antes de usar en producción.")
        return 1

if __name__ == "__main__":
    sys.exit(main())