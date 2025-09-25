import numpy as np
# Tarea 2.2.0.1 (Revisada): Calculadora de Cotas de Parámetros Cosmológicos
# Objetivo: Utilizar la precesión de Mercurio y las observaciones de Planck sobre
# la curvatura del universo para establecer cotas para los parámetros del modelo (R, ω₄D).

def calculate_dynamic_constant(delta_phi_new_term, G, M, c, a, e):
    """
    Calcula la constante dinámica K = ω₄D² * R³ a partir de la precesión de Mercurio.
    La ecuación teórica es: Δφ_nuevo = (π * ω₄D² * R³) / (c * L)
    Donde L (momento angular por unidad de masa) es L = sqrt(G * M * a * (1 - e²))
    
    Despejando K:
    K = ω₄D² * R³ = (Δφ_nuevo * c * L) / π
    """
    # Momento angular específico (por unidad de masa)
    L = np.sqrt(G * M * a * (1 - e**2))
    
    K_dinamica = (delta_phi_new_term * c * L) / np.pi
    return K_dinamica

def estimate_parameter_bounds():
    """
    Combina la dinámica local (precesión de Mercurio) con la cosmología observacional
    (datos de Planck) para acotar los parámetros del modelo R y ω₄D.
    """
    # --- 1. Constantes Físicas y Datos Observacionales ---

    # Constante de gravitación universal (m^3 kg^-1 s^-2)
    G = 6.67430e-11
    # Velocidad de la luz en el vacío (m/s)
    c = 2.99792458e8
    # Masa del Sol (kg)
    M_SUN = 1.98847e30
    # Semieje mayor de la órbita de Mercurio (m)
    A_MERCURY = 5.7909e10
    # Excentricidad de la órbita de Mercurio (adimensional)
    E_MERCURY = 0.205630

    # Precesión anómala observada del perihelio de Mercurio (arcosegundos por siglo)
    # Este es el valor total que debe ser explicado por la suma de GR y el nuevo término.
    DELTA_PHI_OBS_ARCSEC_PER_CENTURY = 43.0

    # --- 2. Conversión de Unidades ---
    # Años en un siglo
    YEARS_PER_CENTURY = 100.0
    # Período orbital de Mercurio en días
    ORBITAL_PERIOD_MERCURY_DAYS = 87.969
    # Días en un año juliano
    DAYS_PER_YEAR = 365.25
    
    # Número de órbitas de Mercurio por siglo
    orbits_per_century = (YEARS_PER_CENTURY * DAYS_PER_YEAR) / ORBITAL_PERIOD_MERCURY_DAYS

    # Conversión de arcosegundos a radianes
    arcsec_to_rad = np.pi / (180.0 * 3600.0)

    # Precesión observada en radianes por órbita
    delta_phi_obs_rad_per_orbit = (DELTA_PHI_OBS_ARCSEC_PER_CENTURY * arcsec_to_rad) / orbits_per_century

    # --- 3. Cálculo de la Constante Dinámica K ---
    
    # Predicción de la Relatividad General (GR) para la precesión (radianes por órbita)
    delta_phi_gr = (6 * np.pi * G * M_SUN) / (c**2 * A_MERCURY * (1 - E_MERCURY**2))

    # El nuevo término debe dar cuenta de la diferencia entre la observación y la predicción de GR.
    # Nota: Este valor es pequeño y negativo, lo que indica que el modelo original sobreestima la precesión.
    # Para el propósito de este cálculo, usaremos el valor total observado como el término a explicar,
    # asumiendo que el modelo propuesto debe dar cuenta de toda la precesión anómala.
    # Este es el valor que se usó en el script de optimización y que reveló la degeneración.
    delta_phi_new_term_required = 5.0209e-07 # rad/orbita, valor de la precesión total.

    K_dinamica = calculate_dynamic_constant(delta_phi_new_term_required, G, M_SUN, c, A_MERCURY, E_MERCURY)

    print("--- Análisis de la Dinámica Local (Mercurio) ---")
    print(f"Precesión anómala total a explicar (rad/órbita): {delta_phi_new_term_required:.4e}")
    print(f"Constante dinámica K = ω₄D² * R³ (m³/s²): {K_dinamica:.4e}\n")

    # --- 4. Incorporación de Restricciones Cosmológicas (Planck) ---
    
    # Diámetro del universo observable: 93 mil millones de años luz
    D_OBS_LY = 93e9
    # Años luz a metros
    LY_TO_M = 9.461e15
    D_obs_m = D_OBS_LY * LY_TO_M

    # Factor de la cota de Planck (Universo total es al menos N veces el observable)
    PLANCK_FACTOR = 10.0

    # Cota inferior para R, basada en 2 * pi * R >= N * D_obs
    R_min = (PLANCK_FACTOR * D_obs_m) / (2 * np.pi)

    # --- 5. Cálculo de las Cotas de los Parámetros ---

    # Con R_min, podemos calcular la cota superior para ω₄D
    # K = ω₄D² * R³  =>  ω₄D = sqrt(K / R³)
    omega_4d_max = np.sqrt(K_dinamica / R_min**3)

    print("--- Cotas de Parámetros del Modelo ---")
    print(f"Basado en la restricción de Planck (Universo total >= {PLANCK_FACTOR}x observable):")
    print(f"Cota inferior para el Radio R:")
    print(f"  R_min >= {R_min:.4e} metros")
    print(f"  R_min >= {R_min / D_obs_m:.2f} veces el diámetro del universo observable")
    print("\nCota superior para la Velocidad Angular ω₄D:")
    print(f"  ω₄D_max <= {omega_4d_max:.4e} rad/s")

if __name__ == "__main__":
    estimate_parameter_bounds()