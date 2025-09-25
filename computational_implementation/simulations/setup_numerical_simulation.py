#!/usr/bin/env python3
"""
Script de configuración inicial para simulación numérica completa.
Paso 4.1 del Plan de Verificación de Aproximaciones - Aproximación 3

Este script prepara todos los componentes necesarios para una simulación numérica
de las ecuaciones de Einstein, incluyendo:
- Conversión del tensor promediado a función numérica
- Definición de malla de cálculo 3D
- Configuración de datos iniciales (con opción para cúmulos de masa)
- Inicialización del sistema de evolución

Fecha: 29 de junio de 2025
"""

import numpy as np
import sympy as sp
import warnings
import argparse
import json

# Suprimir advertencias
warnings.filterwarnings('ignore')

def get_time_averaged_tensor_symbolic():
    """
    Reutiliza el código de calculate_time_averaged_tensor.py para obtener
    la expresión simbólica de la matriz T_averaged.
    """
    print("Obteniendo tensor promediado temporalmente (expresión simbólica)...")
    
    R, psi, theta, phi, omega_4d = sp.symbols('R psi theta phi omega_4d', real=True, positive=True)
    
    T_averaged = sp.zeros(4)
    
    # Expresiones simplificadas basadas en resultados previos
    T_averaged[0, 0] = R**2 * omega_4d**2 * (sp.cos(psi)**2 * sp.cos(theta)**2 - 1)**2 * sp.cos(phi)**2 * sp.cos(psi)**2 * sp.cos(theta)**2 / 2
    T_averaged[1, 1] = R**2 * omega_4d**2 * (sp.cos(psi)**2 * sp.cos(theta)**2 - 1)**2 * sp.sin(phi)**2 * sp.cos(psi)**2 * sp.cos(theta)**2 / 2
    T_averaged[2, 2] = R**2 * omega_4d**2 * (sp.sin(psi)**2 + sp.sin(theta)**2 * sp.cos(psi)**6 * sp.cos(theta)**4) / 2
    T_averaged[3, 3] = R**2 * omega_4d**2 * (-(sp.cos(4*psi) - 1) * sp.cos(theta)**4 + 8*sp.sin(theta)**2) * sp.cos(psi)**2 / 16
    
    T_averaged[0, 1] = T_averaged[1, 0] = R**2 * omega_4d**2 * (sp.cos(psi)**2 * sp.cos(theta)**2 - 1)**2 * sp.sin(phi) * sp.cos(phi) * sp.cos(psi)**2 * sp.cos(theta)**2 / 2
    T_averaged[0, 2] = T_averaged[2, 0] = R**2 * omega_4d**2 * (sp.cos(psi)**2 * sp.cos(theta)**2 - 1) * sp.sin(theta) * sp.cos(phi) * sp.cos(psi)**4 * sp.cos(theta)**3 / 2
    T_averaged[0, 3] = T_averaged[3, 0] = R**2 * omega_4d**2 * (sp.cos(psi)**2 * sp.cos(theta)**2 - 1) * sp.sin(psi) * sp.cos(phi) * sp.cos(psi)**3 * sp.cos(theta)**3 / 2
    
    T_averaged[1, 2] = T_averaged[2, 1] = R**2 * omega_4d**2 * (sp.cos(psi)**2 * sp.cos(theta)**2 - 1) * sp.sin(phi) * sp.sin(theta) * sp.cos(psi)**4 * sp.cos(theta)**3 / 2
    T_averaged[1, 3] = T_averaged[3, 1] = R**2 * omega_4d**2 * (sp.cos(psi)**2 * sp.cos(theta)**2 - 1) * sp.sin(phi) * sp.sin(psi) * sp.cos(psi)**3 * sp.cos(theta)**3 / 2
    
    T_averaged[2, 3] = T_averaged[3, 2] = R**2 * omega_4d**2 * (sp.cos(psi)**4 * sp.cos(theta)**4 - 1) * sp.sin(psi) * sp.sin(theta) * sp.cos(psi) / 2
    
    print("✓ Tensor simbólico T_averaged construido")
    return T_averaged, (R, psi, theta, phi, omega_4d)

def create_numerical_tensor_function(T_averaged, symbols_tuple):
    """
    Convierte la matriz simbólica T_averaged en una función numérica.
    """
    print("Convirtiendo tensor simbólico a función numérica...")
    T_numerical = sp.lambdify(symbols_tuple, T_averaged, modules=['numpy'])
    print("✓ Funciones numéricas del tensor creadas")
    return T_numerical

def setup_computational_grid():
    """
    Define una malla de cálculo 3D.
    """
    print("Configurando malla de cálculo 3D...")
    grid_size = 32
    L = 10.0
    x = np.linspace(-L, L, grid_size)
    y = np.linspace(-L, L, grid_size)
    z = np.linspace(-L, L, grid_size)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    print(f"✓ Malla 3D configurada: {grid_size}³ puntos en caja de tamaño {2*L}")
    return X, Y, Z, (grid_size, L)

def cartesian_to_hyperspherical(x, y, z):
    """
    Convierte coordenadas cartesianas a hiperesféricas.
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(np.clip(z / (r + 1e-12), -1, 1))
    phi = np.arctan2(y, x)
    R_characteristic = 1.0
    psi = np.arctan(r / R_characteristic)
    return r, psi, theta, phi

def evaluate_tensor_on_grid(T_numerical, X, Y, Z, params):
    """
    Evalúa el tensor numérico en la malla.
    """
    print("Evaluando tensor en puntos de la malla...")
    R_param, omega_4d_param = params
    
    # Parámetro para escalar la constante de Hubble
    H_observed_scale_factor = 70.0  # Valor empírico a ajustar

    r, psi, theta, phi = cartesian_to_hyperspherical(X, Y, Z)
    H_correction = (omega_4d_param / H_observed_scale_factor)**2
    T_grid_raw = np.sqrt(H_correction) * T_numerical(R_param, psi, theta, phi, omega_4d_param)
    
    # Reordenar los ejes a (32, 32, 32, 4, 4) para consistencia
    T_grid = np.moveaxis(T_grid_raw, [0, 1], [-2, -1])
    
    print("✓ Tensor evaluado en todos los puntos de la malla")
    return T_grid

def add_local_masses_to_tensor(T_grid, X, Y, Z, cluster_config):
    """
    Añade múltiples masas locales al tensor de energía-momento.
    """
    print("Añadiendo cúmulo de masas locales al tensor...")
    dx = X[1, 0, 0] - X[0, 0, 0]
    dy = Y[0, 1, 0] - Y[0, 0, 0]
    dz = Z[0, 0, 1] - Z[0, 0, 0]

    for mass_params in cluster_config['masses']:
        M_local = mass_params['mass']
        pos_x, pos_y, pos_z = mass_params['position']
        sigma = mass_params['smoothing_radius']
        
        print(f"  - Añadiendo masa M={M_local} en ({pos_x:.2f}, {pos_y:.2f}, {pos_z:.2f}) con σ={sigma:.3f}")

        r_squared = (X - pos_x)**2 + (Y - pos_y)**2 + (Z - pos_z)**2
        normalization = M_local / (sigma * np.sqrt(2 * np.pi))**3
        density = normalization * np.exp(-r_squared / (2 * sigma**2))
        
        T_grid[:, :, :, 0, 0] += density

        total_mass_check = np.sum(density) * dx * dy * dz
        mass_error = abs(total_mass_check - M_local) / M_local
        if mass_error > 0.1:
            print(f"    ⚠️  Advertencia: Error en conservación de masa para esta fuente: {mass_error*100:.1f}%")

    print("✓ Cúmulo de masas locales añadido.")
    return T_grid

def main():
    """
    Función principal que coordina la configuración inicial de la simulación.
    """
    parser = argparse.ArgumentParser(description='Configuración inicial para simulación numérica.')
    parser.add_argument('--cluster-config', type=str, default=None,
                       help='Ruta a un archivo JSON que define un cúmulo de masas locales.')
    parser.add_argument('--output', type=str, default='simulation_initial_data.npz',
                       help='Nombre del archivo de salida para los datos iniciales.')
    parser.add_argument('--R', type=float, default=1.0, help='Parámetro R del modelo (radio 4D).')
    parser.add_argument('--omega4d', type=float, default=0.1, help='Parámetro ω_4D del modelo (velocidad angular 4D).')
    args = parser.parse_args()

    print("=" * 80)
    print("CONFIGURACIÓN INICIAL PARA SIMULACIÓN NUMÉRICA")
    print("=" * 80)
    
    try:
        # 1. Preparar tensor
        T_averaged, symbols_tuple = get_time_averaged_tensor_symbolic()
        T_numerical = create_numerical_tensor_function(T_averaged, symbols_tuple)
        
        # 2. Configurar malla
        X, Y, Z, grid_params = setup_computational_grid()
        
        # 3. Definir parámetros físicos
        R_param = args.R
        omega_4d_param = args.omega4d
        params = (R_param, omega_4d_param)
        print(f"Usando parámetros físicos: R = {R_param:.4e}, ω_4D = {omega_4d_param:.4e}")
        
        # 4. Evaluar tensor en la malla
        T_grid = evaluate_tensor_on_grid(T_numerical, X, Y, Z, params)
        
        # 5. (Opcional) Añadir cúmulo de masas
        if args.cluster_config:
            print("\n--- Añadiendo Cúmulo de Masas Locales ---")
            with open(args.cluster_config, 'r') as f:
                cluster_config = json.load(f)
            T_grid = add_local_masses_to_tensor(T_grid, X, Y, Z, cluster_config)
            print("-----------------------------------------")

        # 6. Guardar datos
        output_filename = args.output
        np.savez_compressed(
            output_filename,
            X=X, Y=Y, Z=Z,
            T_mu_nu_evaluated=T_grid
        )
        
        print("\n" + "=" * 80)
        print("CONFIGURACIÓN INICIAL COMPLETADA EXITOSAMENTE")
        print(f"✓ Datos guardados en archivo: {output_filename}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Error durante la configuración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()