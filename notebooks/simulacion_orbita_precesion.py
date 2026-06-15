import os
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def modified_equations_of_motion(t, state, G_M, c, alpha, beta, omega_4d):
    """
    Ecuaciones de movimiento en 2D cartesianas modificadas por acoplamiento
    centrífugo y Coriolis hiperdimensional en el Universo Centrífugo.
    
    Estado: [x, y, vx, vy]
    """
    x, y, vx, vy = state
    r2 = x*x + y*y
    r = np.sqrt(r2)
    
    # Evitar división por cero
    if r < 1e-6:
        return [0, 0, 0, 0]
    
    # Velocidad angular orbital: dot_phi = (x * vy - y * vx) / r^2
    dot_phi = (x * vy - y * vx) / r2
    
    # Aceleración gravitatoria base + corrección cinética (alpha)
    # y Coriolis hiperdimensional (beta) en dirección radial:
    # a_radial = -GM/r^2 * (1 + alpha * (r * dot_phi)^2 / c^2) + 4 * beta * omega_4d * r * dot_phi
    
    # Término de gravedad modificada
    term_grav = -(G_M / r2) * (1.0 + alpha * (r2 * dot_phi**2) / (c**2))
    
    # Término de arrastre de Coriolis hiperdimensional
    term_coriolis = 4.0 * beta * omega_4d * r * dot_phi
    
    # Aceleración total en dirección radial (unitaria)
    a_radial = term_grav + term_coriolis
    
    # Descomposición en componentes Cartesianas (ax, ay)
    ax = (a_radial / r) * x
    ay = (a_radial / r) * y
    
    return [vx, vy, ax, ay]

def find_perihelion_event(t, state, G_M, c, alpha, beta, omega_4d):
    """
    Evento para detectar el perihelio (cuando la velocidad radial es cero y cambia de signo).
    v_radial = dot_r = (x * vx + y * vy) / r
    """
    x, y, vx, vy = state
    # Devolvemos el producto interno r . v que es cero en el perihelio/afelio
    return x * vx + y * vy

# Configuramos el evento para que detecte cuando cruza por cero
find_perihelion_event.terminal = False
find_perihelion_event.direction = 1.0 # De negativo a positivo (alejándose del perihelio)

def run_simulation(num_orbits=20, alpha=1.0, beta=1.0, omega_4d=0.05, exagerar=True):
    """
    Ejecuta la simulación orbital y extrae la tasa de precesión.
    
    Nota: omega_4d es el valor instantáneo local. Cosmológicamente,
    ω₄D(t) ∝ 1/R(t)² por conservación del momento angular, pero en
    escalas locales (órbitas planetarias) es efectivamente constante.
    """
    print(f"--- Iniciando simulación orbital ({num_orbits} órbitas) ---")
    print(f"Parámetros: alpha={alpha}, beta={beta}, omega_4d={omega_4d}")
    
    # Unidades normalizadas (G*M = 1)
    G_M = 1.0
    
    if exagerar:
        # Exageramos el efecto para que la precesión sea visible gráficamente en pocas órbitas
        c = 10.0      # Velocidad de la luz baja para magnificar el término relativista alpha
        r0 = 1.0      # Radio inicial (perihelio inicial en el eje X)
        v0 = 0.95     # Velocidad inicial (perpendicular, vy)
    else:
        # Parámetros físicos reales escalados (representativos de Mercurio)
        c = 100.0     # Efecto más sutil
        r0 = 1.0
        v0 = 0.98
        
    state0 = [r0, 0.0, 0.0, v0]
    
    # Tiempo de simulación estimado para num_orbits
    # Período Kepleriano básico T = 2 * pi * r^(3/2) / sqrt(GM) ~ 2 * pi ~ 6.28
    T_kepler = 2 * np.pi * (r0**1.5)
    t_span = (0.0, num_orbits * T_kepler * 1.1)
    
    # Resolver la ecuación diferencial con altísima precisión
    sol = solve_ivp(
        modified_equations_of_motion,
        t_span,
        state0,
        args=(G_M, c, alpha, beta, omega_4d),
        events=find_perihelion_event,
        rtol=1e-11,
        atol=1e-13,
        t_eval=np.linspace(t_span[0], t_span[1], 15000)
    )
    
    # Procesar eventos de perihelio
    perihelion_times = sol.t_events[0]
    perihelion_states = sol.y_events[0]
    
    angles = []
    distances = []
    
    for i, state in enumerate(perihelion_states):
        px, py, pvx, pvy = state
        angle = np.arctan2(py, px)
        # Normalizar ángulo a [0, 2*pi]
        if angle < 0:
            angle += 2 * np.pi
        angles.append(angle)
        distances.append(np.sqrt(px**2 + py**2))
    
    # Calcular tasa de precesión lineal por órbita (por mínimos cuadrados)
    if len(angles) > 1:
        # Desenrollar ángulos para evitar saltos de 2pi
        unwrapped_angles = np.unwrap(angles)
        orbit_indices = np.arange(len(unwrapped_angles))
        slope, intercept = np.polyfit(orbit_indices, unwrapped_angles, 1)
        precession_per_orbit = slope # En radianes por órbita
        precession_deg_per_orbit = np.degrees(precession_per_orbit)
    else:
        precession_per_orbit = 0.0
        precession_deg_per_orbit = 0.0
        unwrapped_angles = angles
        
    print(f"Precesión calculada: {precession_deg_per_orbit:.4f}° por órbita")
    
    # Generar gráficos científicos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5))
    
    # Gráfico 1: Órbita con precesión exagerada
    ax1.plot(sol.y[0], sol.y[1], color='navy', alpha=0.6, label='Trayectoria de la partícula')
    ax1.scatter(0, 0, color='gold', s=150, zorder=5, label='Sol Central')
    
    # Dibujar líneas que conecten el Sol con los perihelios sucesivos
    colors = plt.cm.plasma(np.linspace(0, 1, len(perihelion_states)))
    for idx, state in enumerate(perihelion_states):
        px, py, _, _ = state
        ax1.plot([0, px], [0, py], color=colors[idx], linestyle='--', alpha=0.8)
        ax1.scatter(px, py, color=colors[idx], s=30, zorder=6)
        
    ax1.set_aspect('equal')
    ax1.set_title('🪐 Precesión de la Órbita en el Universo Centrífugo', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Eje X (unidades físicas)', fontsize=10)
    ax1.set_ylabel('Eje Y (unidades físicas)', fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right')
    
    # Gráfico 2: Evolución de los ángulos de perihelio
    ax2.plot(np.arange(len(unwrapped_angles)), np.degrees(unwrapped_angles), 'o-', color='crimson', label='Ángulos medidos')
    if len(angles) > 1:
        ax2.plot(orbit_indices, np.degrees(orbit_indices * slope + intercept), '--', color='darkslategray', alpha=0.7, 
                 label=f'Ajuste lineal: {precession_deg_per_orbit:.4f}°/órbita')
    ax2.set_title('📈 Avance Angular del Perihelio por Órbita', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Número de Órbita', fontsize=10)
    ax2.set_ylabel('Ángulo de Perihelio (Grados)', fontsize=10)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend()
    
    # Guardar gráficos y datos
    os.makedirs('results/orbita_precesion', exist_ok=True)
    plot_path = 'results/orbita_precesion/precesion_orbita.png'
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    
    # Guardar resultados numéricos
    np.savez(
        'results/orbita_precesion/datos_precesion.npz',
        t=sol.t,
        x=sol.y[0],
        y=sol.y[1],
        vx=sol.y[2],
        vy=sol.y[3],
        perihelion_times=perihelion_times,
        perihelion_angles=angles,
        precession_deg_per_orbit=precession_deg_per_orbit
    )
    
    print(f"Resultados guardados de forma exitosa en 'results/orbita_precesion/'")
    print(f"Gráfico científico generado: '{plot_path}'")
    
    return precession_deg_per_orbit

if __name__ == "__main__":
    # Ejecución de prueba por defecto
    run_simulation(num_orbits=15, alpha=2.5, beta=1.2, omega_4d=0.05, exagerar=True)
