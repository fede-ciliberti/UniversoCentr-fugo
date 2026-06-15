import os
import numpy as np
import matplotlib.pyplot as plt

def run_cosmic_stability_simulation():
    """
    Simula la evolución cosmológica de la velocidad de giro (omega_4D), la tensión de brana (Tb)
    y la constante gravitacional efectiva (G_eff) a medida que el universo se expande.
    Comprueba numéricamente la cancelación exacta planteada por Fede.
    """
    print("--- Iniciando Simulación de Estabilidad Temporal de la Gravedad ---")
    
    # Parámetros físicos en el presente (t = t_hoy, R = R_0 = 1.0)
    R_0 = 1.0          # Radio de escala normalizado de hoy
    omega_0 = 1.0      # Velocidad angular normalizada de hoy
    T_0 = 1.0          # Tensión de brana normalizada de hoy
    c = 1.0            # Velocidad de la luz normalizada
    
    # Calculamos la Constante Gravitatoria del presente (G_0)
    # G_eff_0 = (c^2 * omega_0^2 * R_0) / (4 * pi * T_0)
    G_0 = (c**2 * omega_0**2 * R_0) / (4.0 * np.pi * T_0)
    
    # Momento angular cosmológico constante L (calculado de las condiciones del presente)
    # L = 1/2 * M * R_0^2 * omega_0. Normalizamos la masa total M = 1
    M = 1.0
    L = 0.5 * M * (R_0**2) * omega_0
    
    # Energía elástica total constante E_elástica de la brana
    # T_0 = E_elástica / V_3D_0 -> T_0 = E_elástica / (2 * pi^2 * R_0^3)
    # E_elástica = T_0 * 2 * pi^2 * R_0^3
    E_elastica = T_0 * 2.0 * (np.pi**2) * (R_0**3)
    
    # Rango de expansión cósmica (desde el universo temprano R = 0.05 hasta R = 5.0 veces el tamaño actual)
    R_series = np.linspace(0.05, 5.0, 1000)
    
    omega_series = []
    T_series = []
    G_series = []
    
    # Simular la evolución física para cada radio del universo
    for R in R_series:
        # 1. Conservación del Momento Angular (Corrección de Fede): omega_4D = 2L / (M * R^2)
        omega = (2.0 * L) / (M * R**2)
        omega_series.append(omega)
        
        # 2. Conservación de la Energía Elástica (Dilución elástica): T_b = E_elastica / (2 * pi^2 * R^3)
        T_b = E_elastica / (2.0 * np.pi**2 * R**3)
        T_series.append(T_b)
        
        # 3. Cálculo de la Gravedad Efectiva resultante: G_eff = (c^2 * omega^2 * R) / (4 * pi * T_b)
        G_eff = (c**2 * omega**2 * R) / (4.0 * np.pi * T_b)
        G_series.append(G_eff)
        
    omega_series = np.array(omega_series)
    T_series = np.array(T_series)
    G_series = np.array(G_series)
    
    # Calcular desviación estándar y fluctuación numérica máxima para demostrar constancia matemática
    max_fluctuation = np.max(np.abs(G_series - G_series[0]))
    std_dev = np.std(G_series)
    
    print(f"Gravedad inicial en R=0.05: {G_series[0]:.8f}")
    print(f"Gravedad actual en R=1.00: {G_series[193]:.8f}")
    print(f"Gravedad final en R=5.00: {G_series[-1]:.8f}")
    print(f"Fluctuación matemática máxima de G_eff: {max_fluctuation:.2e} (Precisión de máquina)")
    print(f"Desviación estándar de G_eff: {std_dev:.2e}")
    
    # Generar gráficos científicos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5))
    
    # Gráfico 1: Evolución del giro y de la tensión superficial
    color1 = 'tab:blue'
    ax1.set_xlabel('Radio del Universo R (Normalizado)', fontsize=11)
    ax1.set_ylabel('Velocidad Angular ω₄D (Normalizada)', color=color1, fontsize=11)
    line1 = ax1.plot(R_series, omega_series, color=color1, linewidth=2, label='Velocidad Angular (ω₄D ∝ 1/R²)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    # Eje secundario para la tensión Tb
    ax1_twin = ax1.twinx()
    color2 = 'tab:green'
    ax1_twin.set_ylabel('Tensión de Brana Tb (Normalizada)', color=color2, fontsize=11)
    line2 = ax1_twin.plot(R_series, T_series, color=color2, linewidth=2, linestyle='--', label='Tensión de Brana (Tb ∝ 1/R³)')
    ax1_twin.tick_params(axis='y', labelcolor=color2)
    
    # Juntar leyendas de ambos ejes
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')
    ax1.set_title('🌀 Evolución Cósmica de la Rotación y la Rigidez Elástica', fontsize=12, fontweight='bold')
    
    # Gráfico 2: Estabilidad de la Gravedad Efectiva resultante
    ax2.plot(R_series, G_series, color='tab:red', linewidth=3, label='Constante Gravitatoria G_eff(t)')
    # Línea horizontal del valor de referencia para enfatizar la constancia
    ax2.axhline(y=G_0, color='black', linestyle=':', alpha=0.7, label=f'G_0 Referencia ({G_0:.4f})')
    
    ax2.set_xlabel('Radio del Universo R (Normalizado)', fontsize=11)
    ax2.set_ylabel('G_eff resultante (Normalizada)', fontsize=11)
    ax2.set_title('🏆 Demostración de Estabilidad de la Gravedad Efectiva G_eff(t)', fontsize=12, fontweight='bold')
    ax2.set_ylim(0, G_0 * 1.5)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='center right')
    
    # Añadir cuadro de texto explicativo con los hallazgos
    text_info = (
        "Cancelación Matemática Exacta:\n"
        f"• ω₄D² ∝ 1/R⁴ (Pérdida de giro centrífugo)\n"
        f"• T_b  ∝ 1/R³ (Ablandamiento elástico brana)\n"
        f"• G_eff(t) ∝ ω₄D² * R / T_b ∝ (1/R⁴) * R / (1/R³) = Constante\n"
        f"• Desviación estándar: {std_dev:.1e} (Perfectamente Estable)"
    )
    ax2.text(0.3, G_0 * 0.2, text_info, fontsize=10, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
    
    # Guardar gráficos y resultados
    os.makedirs('results/estabilidad_gravedad', exist_ok=True)
    plot_path = 'results/estabilidad_gravedad/estabilidad_geff.png'
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    
    # Guardar datos binarios
    np.savez(
        'results/estabilidad_gravedad/datos_estabilidad.npz',
        R=R_series,
        omega=omega_series,
        Tb=T_series,
        G_eff=G_series
    )
    
    print(f"Resultados guardados de forma exitosa en 'results/estabilidad_gravedad/'")
    print(f"Gráfico científico generado: '{plot_path}'")

if __name__ == "__main__":
    run_cosmic_stability_simulation()
