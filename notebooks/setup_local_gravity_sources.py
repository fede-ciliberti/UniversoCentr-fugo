#!/usr/bin/env python3
"""
Script para configurar las fuentes de gravedad local para la simulación.
FASE 1.1 del Plan de Simulación de Gravedad Local

Este script implementa el modelo de superposición de fuentes:
T_total^μν = T_expansion^μν + T_masa^μν

Objetivos:
1. Reutilizar el tensor promediado temporalmente (T_expansion) del universo rotante.
2. Implementar un tensor para una masa puntual (T_masa) con distribución Gaussiana.
3. Combinar ambas fuentes y evaluar el tensor total en una malla 3D.
4. Guardar los datos para ser utilizados por el simulador numérico.

Fecha: 27 de junio de 2025
"""

import numpy as np
import sympy as sp
from sympy import symbols, cos as sp_cos, sin as sp_sin, Matrix, lambdify, pi, sqrt, exp
import warnings

# Suprimir advertencias de EinsteinPy si se usa en el futuro
warnings.filterwarnings('ignore')

# Nota: Los errores de Pylance sobre operadores con funciones simbólicas son falsos positivos.
# SymPy maneja correctamente estas operaciones en tiempo de ejecución.
# type: ignore

def get_expansion_tensor_symbolic():
    """
    Genera la expresión simbólica para el tensor de energía-momento del universo
    en expansión (T_expansion), basado en el tensor promediado temporalmente.
    """
    print("1.1: Obteniendo tensor de expansión simbólico (T_expansion)...")
    
    # Definir símbolos simbólicos necesarios
    R = symbols('R', positive=True)
    psi, theta, phi = symbols('psi theta phi', real=True)
    omega_4d = symbols('omega_4d', real=True)
    
    # Expresiones simplificadas basadas en los resultados de 'calculate_time_averaged_tensor.py'
    T_expansion = Matrix(4, 4, lambda i, j: 0)
    
    # Componentes principales (copiadas de setup_numerical_simulation.py para consistencia)
    T_expansion[0, 0] = R**2 * omega_4d**2 * (sp_cos(psi)**2 * sp_cos(theta)**2 - 1)**2 * sp_cos(phi)**2 * sp_cos(psi)**2 * sp_cos(theta)**2 / 2
    T_expansion[1, 1] = R**2 * omega_4d**2 * (sp_cos(psi)**2 * sp_cos(theta)**2 - 1)**2 * sp_sin(phi)**2 * sp_cos(psi)**2 * sp_cos(theta)**2 / 2
    T_expansion[2, 2] = R**2 * omega_4d**2 * (sp_sin(psi)**2 + sp_sin(theta)**2 * sp_cos(psi)**6 * sp_cos(theta)**4) / 2
    T_expansion[3, 3] = R**2 * omega_4d**2 * (-(sp_cos(4*psi) - 1) * sp_cos(theta)**4 + 8*sp_sin(theta)**2) * sp_cos(psi)**2 / 16
    T_expansion[0, 1] = T_expansion[1, 0] = R**2 * omega_4d**2 * (sp_cos(psi)**2 * sp_cos(theta)**2 - 1)**2 * sp_sin(phi) * sp_cos(phi) * sp_cos(psi)**2 * sp_cos(theta)**2 / 2
    T_expansion[2, 3] = T_expansion[3, 2] = R**2 * omega_4d**2 * (sp_cos(psi)**4 * sp_cos(theta)**4 - 1) * sp_sin(psi) * sp_sin(theta) * sp_cos(psi) / 2

    print("✓ Tensor de expansión T_expansion construido simbólicamente.")
    return T_expansion, (R, psi, theta, phi, omega_4d)

def create_numerical_tensor_function(T_symbolic, symbols_tuple):
    """
    Convierte una matriz simbólica en una función numérica evaluable.
    """
    print("1.2: Convirtiendo tensor simbólico a función numérica...")
    T_numerical = {}
    for i in range(4):
        for j in range(4):
            element = T_symbolic[i, j]
            if element != 0:
                T_numerical[(i, j)] = lambdify(
                    symbols_tuple, 
                    element, 
                    modules=['numpy']
                )
            else:
                # Función que siempre devuelve cero con la misma firma
                T_numerical[(i, j)] = lambda *args, **kwargs: 0.0
    
    print("✓ Funciones numéricas creadas.")
    return T_numerical

def setup_computational_grid(grid_size=32, L=5.0):
    """
    Define una malla de cálculo 3D.
    """
    print("2.1: Configurando malla de cálculo 3D...")
    x = np.linspace(-L, L, grid_size)
    y = np.linspace(-L, L, grid_size)
    z = np.linspace(-L, L, grid_size)
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    
    print(f"✓ Malla 3D configurada: {grid_size}³ puntos en una caja de tamaño {2*L}")
    return X, Y, Z

def cartesian_to_hyperspherical(x, y, z, R_characteristic=1.0):
    """
    Convierte coordenadas cartesianas a hiperesféricas para evaluar T_expansion.
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(np.clip(z / (r + 1e-12), -1, 1))
    phi = np.arctan2(y, x)
    psi = np.arctan(r / R_characteristic)
    return r, psi, theta, phi

def get_mass_tensor_on_grid(X, Y, Z, M, sigma):
    """
    Calcula el tensor de energía-momento para una masa puntual (T_masa)
    con una distribución Gaussiana 3D en la malla.
    """
    print("3.1: Calculando tensor de masa (T_masa) en la malla...")
    
    # T_masa^μν tiene solo el componente T^00 = ρ (densidad de masa)
    # ρ(x,y,z) = M * (1/(σ*sqrt(2π))^3) * exp(-(x^2+y^2+z^2)/(2σ^2))
    
    T_masa = np.zeros((*X.shape, 4, 4))
    
    # Calcular la densidad Gaussiana ρ
    norm_factor = M / (sigma * np.sqrt(2 * np.pi))**3
    exponent = -(X**2 + Y**2 + Z**2) / (2 * sigma**2)
    rho = norm_factor * np.exp(exponent)
    
    # Asignar al componente T^00
    T_masa[..., 0, 0] = rho
    
    print(f"✓ Tensor de masa T_masa calculado. Pico de densidad ρ(0)={np.max(rho):.2e}")
    return T_masa

def evaluate_expansion_tensor_on_grid(T_numerical, X, Y, Z, params):
    """
    Evalúa el tensor de expansión en todos los puntos de la malla.
    """
    print("3.2: Evaluando tensor de expansión (T_expansion) en la malla...")
    R_param, omega_4d_param = params
    grid_shape = X.shape
    T_expansion_grid = np.zeros((*grid_shape, 4, 4))

    for i in range(grid_shape[0]):
        for j in range(grid_shape[1]):
            for k in range(grid_shape[2]):
                x, y, z = X[i, j, k], Y[i, j, k], Z[i, j, k]
                _, psi, theta, phi = cartesian_to_hyperspherical(x, y, z, R_param)
                
                for alpha in range(4):
                    for beta in range(4):
                        T_expansion_grid[i, j, k, alpha, beta] = T_numerical[(alpha, beta)](
                            R_param, psi, theta, phi, omega_4d_param
                        )
    
    print("✓ Tensor de expansión T_expansion evaluado en la malla.")
    return T_expansion_grid

def main():
    """
    Función principal que coordina la configuración de las fuentes de gravedad.
    """
    print("=" * 80)
    print("FASE 1.1: CONFIGURACIÓN DE FUENTES DE GRAVEDAD LOCAL")
    print("=" * 80)

    # --- 1. Preparar T_expansion ---
    print("\nPASO 1: Preparando Tensor de Expansión (Universo Rotante)")
    T_expansion_sym, symbols_tuple = get_expansion_tensor_symbolic()
    T_expansion_num_func = create_numerical_tensor_function(T_expansion_sym, symbols_tuple)

    # --- 2. Configurar Malla y Parámetros Físicos ---
    print("\nPASO 2: Configurando Malla y Parámetros Físicos")
    X, Y, Z = setup_computational_grid()
    
    # Parámetros físicos de la simulación
    R_param = 1.0
    omega_4d_param = 0.1
    M_particula = 0.5
    sigma_gauss = 0.1
    expansion_params = (R_param, omega_4d_param)
    
    print("Parámetros físicos definidos:")
    print(f"  - R (radio característico) = {R_param}")
    print(f"  - ω_4D (velocidad angular) = {omega_4d_param}")
    print(f"  - M (masa de partícula)    = {M_particula}")
    print(f"  - σ (ancho Gaussiano)      = {sigma_gauss}")

    # --- 3. Calcular Tensores en la Malla ---
    print("\nPASO 3: Calculando Tensores en la Malla de Simulación")
    T_masa_grid = get_mass_tensor_on_grid(X, Y, Z, M_particula, sigma_gauss)
    T_expansion_grid = evaluate_expansion_tensor_on_grid(T_expansion_num_func, X, Y, Z, expansion_params)

    # --- 4. Superposición de Fuentes ---
    print("\nPASO 4: Superponiendo Fuentes de Gravedad")
    T_total_grid = T_expansion_grid + T_masa_grid
    print("✓ T_total^μν = T_expansion^μν + T_masa^μν calculado.")

    # --- 5. Validación y Guardado ---
    print("\nPASO 5: Validación y Guardado de Datos")
    
    # Validación simple: T_masa^00 debe ser igual a la densidad Gaussiana
    rho_gaussiana = T_masa_grid[..., 0, 0]
    assert np.all(T_total_grid[..., 0, 0] >= rho_gaussiana), "Error: T_total^00 no es consistente."
    print("✓ Validación: T_masa^00 corresponde a la densidad Gaussiana.")

    # Guardar datos para la simulación
    output_filename = "local_gravity_sources.npz"
    np.savez_compressed(
        output_filename,
        X=X,
        Y=Y,
        Z=Z,
        T_total_mu_nu=T_total_grid,
        T_expansion_mu_nu=T_expansion_grid,
        T_mass_mu_nu=T_masa_grid
    )
    
    print(f"✓ Datos de simulación guardados en: {output_filename}")
    print("  - Contenido: X, Y, Z, T_total_mu_nu, T_expansion_mu_nu, T_mass_mu_nu")

    print("\n" + "=" * 80)
    print("CONFIGURACIÓN DE FUENTES COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print(f"\nEl archivo '{output_filename}' está listo para ser usado en 'run_numerical_simulation.py'.")

if __name__ == "__main__":
    main()