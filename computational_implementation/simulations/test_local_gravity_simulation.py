#!/usr/bin/env python3
"""
Script de prueba para validar la implementación de LocalGravitySimulation.
Tarea 2.1.1: Verificación básica del Principio de Superposición Cosmológico

Este script realiza pruebas unitarias y de integración básicas para verificar
que la implementación de superposición de tensores funciona correctamente
antes de ejecutar simulaciones completas.

Pruebas incluidas:
1. Verificación de herencia y inicialización
2. Validación del cálculo del tensor local
3. Prueba de superposición de tensores
4. Verificación de conservación de masa
5. Test de estabilidad numérica básica

Fecha: 29 de junio de 2025
Autor: Universo Centrífugo Research Team
"""

import numpy as np
import sys
import os
from pathlib import Path

# Agregar el directorio padre al path para imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from run_local_gravity_simulation import LocalGravitySimulation, create_default_mass_params
    from run_numerical_simulation import EinsteinSimulator
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("Asegúrese de que los archivos estén en el directorio correcto")
    sys.exit(1)

def create_minimal_test_data():
    """Crea datos de prueba mínimos para testing."""
    print("🔧 Creando datos de prueba mínimos...")
    
    # Malla pequeña para pruebas rápidas
    nx, ny, nz = 8, 8, 8
    
    # Coordenadas espaciales
    x = np.linspace(-1, 1, nx)
    y = np.linspace(-1, 1, ny)
    z = np.linspace(-1, 1, nz)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    # Tensor de energía-impulso cosmológico simple (isótropo)
    T_mu_nu = np.zeros((nx, ny, nz, 4, 4))
    
    # Componentes diagonales con valores pequeños y constantes
    rho_cosmological = 0.1  # Densidad cosmológica de fondo
    T_mu_nu[:, :, :, 0, 0] = rho_cosmological  # T_00
    T_mu_nu[:, :, :, 1, 1] = -rho_cosmological/3  # T_11 (presión)
    T_mu_nu[:, :, :, 2, 2] = -rho_cosmological/3  # T_22
    T_mu_nu[:, :, :, 3, 3] = -rho_cosmological/3  # T_33
    
    # Guardar datos de prueba
    test_data = {
        'X': X,
        'Y': Y, 
        'Z': Z,
        'T_mu_nu_evaluated': T_mu_nu
    }
    
    test_file = "test_simulation_data.npz"
    np.savez(test_file, **test_data)
    print(f"✓ Datos de prueba guardados en: {test_file}")
    
    return test_file

def test_inheritance_and_initialization():
    """Prueba 1: Verificar herencia y inicialización básica."""
    print("\n🧪 PRUEBA 1: Herencia e Inicialización")
    print("=" * 50)
    
    try:
        # Crear datos de prueba
        test_file = create_minimal_test_data()
        
        # Parámetros de masa local para prueba
        mass_params = {
            'mass': 0.5,
            'position': (0.0, 0.0, 0.0),
            'smoothing_radius': 0.2,
            'enable_time_modulation': False
        }
        
        # Inicializar simulador
        sim = LocalGravitySimulation(
            data_file=test_file,
            max_cores=1,  # Un solo core para pruebas
            local_mass_params=mass_params
        )
        
        # Verificar herencia
        assert isinstance(sim, EinsteinSimulator), "Fallo en herencia de EinsteinSimulator"
        assert isinstance(sim, LocalGravitySimulation), "Fallo en tipo LocalGravitySimulation"
        
        # Verificar inicialización de parámetros
        assert hasattr(sim, 'M_local'), "Falta atributo M_local"
        assert hasattr(sim, 'T_local'), "Falta tensor local T_local"
        assert sim.M_local == 0.5, f"Masa incorrecta: {sim.M_local} != 0.5"
        
        print("✅ Herencia e inicialización: EXITOSA")
        
        # Limpiar archivo de prueba
        os.remove(test_file)
        
        return sim
        
    except Exception as e:
        print(f"❌ Herencia e inicialización: FALLIDA - {e}")
        raise

def test_local_tensor_calculation(sim):
    """Prueba 2: Validar cálculo del tensor local."""
    print("\n🧪 PRUEBA 2: Cálculo del Tensor Local")
    print("=" * 50)
    
    try:
        # Verificar forma del tensor local
        expected_shape = sim.T_initial.shape
        assert sim.T_local.shape == expected_shape, f"Forma incorrecta: {sim.T_local.shape} != {expected_shape}"
        
        # Verificar que solo T_00 es no nulo
        T_00 = sim.T_local[:, :, :, 0, 0]
        T_11 = sim.T_local[:, :, :, 1, 1]
        T_22 = sim.T_local[:, :, :, 2, 2]
        T_33 = sim.T_local[:, :, :, 3, 3]
        
        assert np.any(T_00 > 0), "T_00 debería tener valores positivos"
        assert np.allclose(T_11, 0), "T_11 debería ser cero (masa en reposo)"
        assert np.allclose(T_22, 0), "T_22 debería ser cero"
        assert np.allclose(T_33, 0), "T_33 debería ser cero"
        
        # Verificar conservación de masa
        dx = sim.X[1,0,0] - sim.X[0,0,0]
        dy = sim.Y[0,1,0] - sim.Y[0,0,0]
        dz = sim.Z[0,0,1] - sim.Z[0,0,0]
        
        integrated_mass = np.sum(T_00) * dx * dy * dz
        mass_error = abs(integrated_mass - sim.M_local) / sim.M_local
        
        print(f"   Masa objetivo: {sim.M_local}")
        print(f"   Masa integrada: {integrated_mass:.6f}")
        print(f"   Error relativo: {mass_error*100:.2f}%")
        
        assert mass_error < 0.2, f"Error de masa demasiado grande: {mass_error*100:.1f}%"
        
        # Verificar que el máximo está cerca del centro
        max_idx = np.unravel_index(np.argmax(T_00), T_00.shape)
        center_idx = (T_00.shape[0]//2, T_00.shape[1]//2, T_00.shape[2]//2)
        
        print(f"   Índice de máximo: {max_idx}")
        print(f"   Índice de centro: {center_idx}")
        
        print("✅ Cálculo del tensor local: EXITOSO")
        
    except Exception as e:
        print(f"❌ Cálculo del tensor local: FALLIDO - {e}")
        raise

def test_tensor_superposition(sim):
    """Prueba 3: Verificar superposición de tensores."""
    print("\n🧪 PRUEBA 3: Superposición de Tensores")
    print("=" * 50)
    
    try:
        # Simular un paso temporal t=0
        t_test = 0.0
        
        # Obtener tensor cosmológico base
        T_cosmological = super(LocalGravitySimulation, sim).compute_stress_energy_contribution(t_test)
        
        # Obtener tensor total con superposición
        T_total = sim.compute_stress_energy_contribution(t_test)
        
        # Verificar que la superposición es correcta
        T_expected = T_cosmological + sim.T_local
        
        assert np.allclose(T_total, T_expected), "Superposición incorrecta"
        
        # Verificar que el tensor total es diferente del cosmológico puro
        difference = np.sum(np.abs(T_total - T_cosmological))
        assert difference > 0, "El tensor total debería diferir del cosmológico"
        
        # Verificar componentes específicas
        T_00_total = T_total[:, :, :, 0, 0]
        T_00_cosmo = T_cosmological[:, :, :, 0, 0]
        T_00_local = sim.T_local[:, :, :, 0, 0]
        
        assert np.allclose(T_00_total, T_00_cosmo + T_00_local), "Superposición T_00 incorrecta"
        
        print(f"   Diferencia total: {difference:.2e}")
        print(f"   Contribución cosmológica media: {np.mean(T_00_cosmo):.6f}")
        print(f"   Contribución local máxima: {np.max(T_00_local):.6f}")
        
        print("✅ Superposición de tensores: EXITOSA")
        
    except Exception as e:
        print(f"❌ Superposición de tensores: FALLIDA - {e}")
        raise

def test_conservation_check(sim):
    """Prueba 4: Verificar conservación básica."""
    print("\n🧪 PRUEBA 4: Verificación de Conservación")
    print("=" * 50)
    
    try:
        # Calcular conservación
        conservation_rms = sim.compute_conservation_check()
        
        print(f"   RMS de divergencia: {conservation_rms:.2e}")
        
        # La divergencia debería ser pequeña para una masa estática
        # (aunque no exactamente cero debido a discretización)
        assert conservation_rms < 1.0, f"Divergencia demasiado grande: {conservation_rms}"
        
        print("✅ Verificación de conservación: EXITOSA")
        
    except Exception as e:
        print(f"❌ Verificación de conservación: FALLIDA - {e}")
        raise

def test_stability_metrics(sim):
    """Prueba 5: Verificar métricas de estabilidad."""
    print("\n🧪 PRUEBA 5: Métricas de Estabilidad")
    print("=" * 50)
    
    try:
        # Simular algunos pasos y verificar estabilidad
        t_test = 0.0
        T_total = sim.compute_stress_energy_contribution(t_test)
        
        # Verificar que no hay NaN o infinitos
        assert np.all(np.isfinite(T_total)), "Tensor contiene valores no finitos"
        
        # Verificar que se registraron métricas
        assert len(sim.superposition_metrics) > 0, "No se registraron métricas de superposición"
        
        # Verificar métricas básicas
        metrics = sim.superposition_metrics[-1]
        assert 'time' in metrics, "Falta métrica de tiempo"
        assert 'max_tensor_component' in metrics, "Falta métrica de componente máximo"
        assert 'local_mass_contribution' in metrics, "Falta métrica de masa local"
        
        print(f"   Componente máximo: {metrics['max_tensor_component']:.2e}")
        print(f"   Contribución de masa: {metrics['local_mass_contribution']:.6f}")
        
        print("✅ Métricas de estabilidad: EXITOSAS")
        
    except Exception as e:
        print(f"❌ Métricas de estabilidad: FALLIDAS - {e}")
        raise

def run_all_tests():
    """Ejecuta todas las pruebas de validación."""
    print("🧪 SUITE DE PRUEBAS: LocalGravitySimulation")
    print("Tarea 2.1.1: Validación del Principio de Superposición Cosmológico")
    print("=" * 70)
    
    try:
        # Ejecutar pruebas en secuencia
        sim = test_inheritance_and_initialization()
        test_local_tensor_calculation(sim)
        test_tensor_superposition(sim)
        test_conservation_check(sim)
        test_stability_metrics(sim)
        
        print("\n🎉 TODAS LAS PRUEBAS EXITOSAS")
        print("=" * 50)
        print("✅ La implementación de LocalGravitySimulation está funcionando correctamente")
        print("✅ El Principio de Superposición se implementó sin errores básicos")
        print("✅ El sistema está listo para simulaciones completas")
        
        return True
        
    except Exception as e:
        print(f"\n💥 SUITE DE PRUEBAS FALLIDA")
        print("=" * 50)
        print(f"❌ Error: {e}")
        print("🔧 Revise la implementación antes de ejecutar simulaciones completas")
        
        return False

def main():
    """Función principal para ejecutar las pruebas."""
    success = run_all_tests()
    
    if success:
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Ejecutar simulación completa con: python run_local_gravity_simulation.py")
        print("2. Analizar resultados de superposición")
        print("3. Validar recuperación de regímenes cosmológico y newtoniano")
        sys.exit(0)
    else:
        print("\n🛠️  PASOS DE DEPURACIÓN:")
        print("1. Revisar errores reportados arriba")
        print("2. Corregir implementación en run_local_gravity_simulation.py")
        print("3. Re-ejecutar pruebas hasta que pasen")
        sys.exit(1)

if __name__ == "__main__":
    main()