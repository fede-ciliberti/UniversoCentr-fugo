import numpy as np
import json
import os
from scipy.optimize import minimize

# Tarea: Encontrar el par único (R, ω₄D) que satisface dos restricciones:
# 1. La precesión del perihelio de Mercurio.
# 2. La curva de rotación de una galaxia (UGC 128).

# --- 1. Constantes Físicas (consistentes con el script anterior) ---
G = 6.67430e-11  # m^3 kg^-1 s^-2
c = 2.99792458e8  # m/s
M_SUN = 1.98847e30 # kg
A_MERCURY = 5.7909e10 # m
E_MERCURY = 0.205630 # adimensional
KPC_TO_M = 3.086e19 # Conversión de kiloparsec a metros
KM_S_TO_M_S = 1000 # Conversión de km/s a m/s

def load_galaxy_data(filepath):
    """Carga los datos de la curva de rotación de la galaxia desde un archivo .dat de SPARC."""
    data = np.loadtxt(filepath, comments='#')
    
    # Extraer columnas y convertir unidades
    radius_kpc = data[:, 0]
    v_obs_kms = data[:, 1]
    v_err_kms = data[:, 2]
    v_gas_kms = data[:, 3]
    v_disk_kms = data[:, 4]
    v_bulge_kms = data[:, 5]
    
    # Conversión a unidades del SI (m y m/s)
    radius_m = radius_kpc * KPC_TO_M
    v_obs_ms = v_obs_kms * KM_S_TO_M_S
    v_err_ms = v_err_kms * KM_S_TO_M_S
    
    # Calcular la velocidad bariónica total al cuadrado
    v_baryon_sq_ms = (v_gas_kms**2 + v_disk_kms**2 + v_bulge_kms**2) * (KM_S_TO_M_S**2)
    
    return radius_m, v_obs_ms, v_err_ms, v_baryon_sq_ms

def theoretical_velocity_sq(r, R, omega_4d, v_baryon_sq):
    """
    Calcula el cuadrado de la velocidad orbital teórica.
    V_modelo² = V_bariónica² + V_nuevo_efecto²
    
    Asumimos que el nuevo efecto añade un término de aceleración a_4d = (ω₄D² * R³) / r²,
    lo que contribuye a la velocidad como V_nuevo_efecto² = r * a_4d.
    """
    # Contribución del nuevo término
    # Se evita la división por cero si r es muy pequeño
    if r < 1e-10:
        v_new_effect_sq = 0
    else:
        v_new_effect_sq = (omega_4d**2 * R**3) / r
        
    return v_baryon_sq + v_new_effect_sq

def chi_squared(params, galaxy_radii, v_obs_sq, v_err_sq, v_baryon_sq):
    """
    Función de coste: Calcula el Chi-cuadrado para un par (R, ω₄D).
    """
    R, omega_4d = params
    
    # Evitar valores no físicos durante la optimización
    if R <= 0 or omega_4d < 0:
        return np.inf

    chi2_total = 0
    for i, r in enumerate(galaxy_radii):
        v_model_sq = theoretical_velocity_sq(r, R, omega_4d, v_baryon_sq[i])
        
        # Usamos v^2 para evitar raíces cuadradas innecesarias
        # La propagación de errores es (err(v^2)) approx (2*v*err(v))^2
        v_obs = np.sqrt(v_obs_sq[i])
        v_err = np.sqrt(v_err_sq[i])
        err_v_obs_sq = (2 * v_obs * v_err)**2

        if err_v_obs_sq < 1e-20: # Evitar división por cero si el error es nulo
            continue

        chi2_term = ((v_obs_sq[i] - v_model_sq)**2) / err_v_obs_sq
        chi2_total += chi2_term
        
    return chi2_total

def mercury_precession_constraint(params):
    """
    Función de restricción: La combinación (R, ω₄D) debe satisfacer la precesión de Mercurio.
    Δφ_nuevo(R, ω₄D) - constante_observada = 0
    """
    R, omega_4d = params
    
    # Valor de la precesión anómala a explicar (rad/órbita).
    # Este es el valor total observado, asumiendo que el nuevo modelo
    # debe explicar toda la precesión.
    delta_phi_new_term_required = 5.0209e-07
    
    # Momento angular específico de Mercurio
    L_mercury = np.sqrt(G * M_SUN * A_MERCURY * (1 - E_MERCURY**2))
    
    # Precesión predicha por el nuevo término
    delta_phi_predicted = (np.pi * omega_4d**2 * R**3) / (c * L_mercury)
    
    # La función de restricción debe ser igual a cero para una solución válida
    return delta_phi_predicted - delta_phi_new_term_required

def main():
    """
    Función principal para ejecutar el análisis.
    """
    # --- Cargar Datos ---
    galaxy_data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'downloads', 'Rotmod_LTG', 'UGC00128_rotmod.dat')
    radii, v_obs, v_err, v_baryon_sq = load_galaxy_data(galaxy_data_path)
    v_obs_sq = v_obs**2
    v_err_sq = v_err**2
    
    # Usar el primer par de parámetros prometedores como punto de partida
    params_path = os.path.join(os.path.dirname(__file__), 'promising_parameters.json')
    with open(params_path, 'r') as f:
        initial_params_list = json.load(f)
    
    if not initial_params_list:
        print("El archivo de parámetros prometedores está vacío. No se puede continuar.")
        return
        
    initial_guess = [initial_params_list[0]['R'], initial_params_list[0]['omega_4d']]

    print("Iniciando optimización...")
    print(f"Suposición inicial: R = {initial_guess[0]:.2e}, ω₄D = {initial_guess[1]:.2e}")

    # --- Ejecutar Optimización ---
    # Argumentos para la función chi_squared
    args = (radii, v_obs_sq, v_err_sq, v_baryon_sq)
    
    # Restricción para el optimizador
    constraints = ({'type': 'eq', 'fun': mercury_precession_constraint})
    
    # Límites para los parámetros (deben ser positivos)
    bounds = ((1e10, None), (0, None)) # R > 0, ω₄D >= 0

    result = minimize(chi_squared, initial_guess, args=args, method='SLSQP',
                      constraints=constraints, bounds=bounds)

    # --- Mostrar Resultados ---
    print("\n--- Resultado de la Optimización ---")
    if result.success:
        best_R, best_omega_4d = result.x
        min_chi2 = result.fun
        
        print(f"Optimización exitosa: {result.message}")
        print(f"Mejor ajuste encontrado para el par de parámetros:")
        print(f"  R      = {best_R:.4e} m")
        print(f"  ω₄D    = {best_omega_4d:.4e} rad/s")
        print(f"Valor mínimo de Chi-cuadrado (χ²): {min_chi2:.4f}")
        
        # Verificación de la restricción
        constraint_check = mercury_precession_constraint(result.x)
        print(f"Verificación de la restricción de Mercurio (debe ser ~0): {constraint_check:.2e}")

    else:
        print(f"La optimización falló: {result.message}")

if __name__ == "__main__":
    main()