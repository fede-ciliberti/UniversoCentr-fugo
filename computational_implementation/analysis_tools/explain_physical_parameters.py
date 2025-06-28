#!/usr/bin/env python3
"""
Explicación pedagógica de los parámetros físicos fundamentales
en la Conjetura del Universo Centrífugo
"""

import numpy as np
import matplotlib.pyplot as plt

def explain_physical_parameters():
    """Explica los parámetros físicos del modelo de manera pedagógica"""
    
    print("🧠 PARÁMETROS FÍSICOS FUNDAMENTALES")
    print("Conjetura del Universo Centrífugo")
    print("=" * 60)
    
    print("\n📚 CONTEXTO TEÓRICO:")
    print("La conjetura propone que el universo es una 3-esfera rotando en 4D.")
    print("Los parámetros físicos controlan esta rotación y sus efectos observables.")
    
    # 1. R_param (Radio de la 3-esfera)
    print(f"\n1️⃣  R_param (Radio de la 3-esfera)")
    print("=" * 40)
    print("🔍 ¿Qué es?")
    print("   Radio fundamental de la estructura hiperdimensional donde 'vivimos'")
    print("   Es el radio de la 3-esfera embebida en el espacio 4D")
    
    print("\n📏 Significado físico:")
    print("   • Determina la ESCALA del universo en la 4ta dimensión")
    print("   • Análogo al 'radio del universo' pero en 4D")
    print("   • NO es directamente observable desde nuestro espacio 3D")
    
    print("\n🎯 ¿Qué modifica?")
    print("   • INTENSIDAD de los efectos gravitacionales")
    print("   • ESCALA de la energía rotacional")
    print("   • CURVATURA del espacio-tiempo resultante")
    
    print("\n📊 Efecto en la simulación:")
    print("   R_param ↑ → Efectos gravitacionales MÁS FUERTES")
    print("   R_param ↓ → Efectos gravitacionales MÁS DÉBILES")
    
    print("\n🔢 Valor actual: R_param = 1.0")
    print("   (En unidades geométricas donde c = G = 1)")
    
    # 2. omega_4d_param (Velocidad angular 4D)
    print(f"\n2️⃣  omega_4d_param (Velocidad Angular 4D)")
    print("=" * 40)
    print("🔍 ¿Qué es?")
    print("   Velocidad de rotación de la 3-esfera en el espacio 4D")
    print("   Es el parámetro MÁS IMPORTANTE de toda la conjetura")
    
    print("\n📏 Significado físico:")
    print("   • Controla qué tan RÁPIDO gira el universo en 4D")
    print("   • Relacionado DIRECTAMENTE con la constante de Hubble:")
    print("     H₀ = (ω₄D × R₄D)/(2π) × factor_geométrico")
    print("   • Es la FUENTE de la expansión cosmológica observada")
    
    print("\n🎯 ¿Qué modifica?")
    print("   • VELOCIDAD de expansión del universo")
    print("   • INTENSIDAD de la curvatura del espacio-tiempo") 
    print("   • EVOLUCIÓN TEMPORAL de la métrica")
    print("   • ENERGÍA ROTACIONAL total del sistema")
    
    print("\n📊 Efecto en la simulación:")
    print("   ω₄D ↑ → Expansión MÁS RÁPIDA, más curvatura")
    print("   ω₄D ↓ → Expansión MÁS LENTA, menos curvatura")
    print("   ω₄D = 0 → SIN expansión (universo estático)")
    
    print("\n🔢 Valor actual: omega_4d_param = 0.1")
    print("   (En unidades donde el tiempo se mide en unidades geométricas)")

def calculate_physical_relationships():
    """Calcula las relaciones entre parámetros y observables"""
    
    print(f"\n🧮 RELACIONES MATEMÁTICAS FUNDAMENTALES")
    print("=" * 50)
    
    # Valores actuales
    R_param = 1.0
    omega_4d_param = 0.1
    
    print(f"\n📐 Con los valores actuales:")
    print(f"   R_param = {R_param}")
    print(f"   omega_4d_param = {omega_4d_param}")
    
    # Calcular cantidades derivadas
    print(f"\n🔄 Cantidades derivadas:")
    
    # 1. Velocidad tangencial 4D
    v_tangential_4d = omega_4d_param * R_param
    print(f"   Velocidad tangencial 4D: v₄D = ω₄D × R = {v_tangential_4d:.3f}")
    
    # 2. Período de rotación 4D
    period_4d = 2 * np.pi / omega_4d_param
    print(f"   Período rotación 4D: T₄D = 2π/ω₄D = {period_4d:.1f} unidades tiempo")
    
    # 3. Energía cinética rotacional (proporcional)
    kinetic_energy_factor = 0.5 * omega_4d_param**2 * R_param**2
    print(f"   Factor energía cinética: ½ω₄D²R² = {kinetic_energy_factor:.6f}")
    
    # 4. Constante de Hubble efectiva (aproximada)
    H0_effective = omega_4d_param / (2 * np.pi)  # Simplificado
    print(f"   H₀ efectiva (aprox): ω₄D/(2π) = {H0_effective:.6f}")
    
    print(f"\n💡 Interpretación física:")
    print(f"   • El universo rota con período ~{period_4d:.0f} unidades")
    print(f"   • La velocidad tangencial 4D es {v_tangential_4d:.1f}")
    print(f"   • Esto genera una 'expansión' efectiva con H₀ ~ {H0_effective:.3f}")

def show_parameter_effects():
    """Muestra cómo diferentes valores afectan los resultados"""
    
    print(f"\n🎮 EXPLORACIÓN DE PARÁMETROS")
    print("=" * 40)
    
    print(f"\n🧪 Efectos de variar R_param (manteniendo ω₄D = 0.1):")
    
    R_values = [0.5, 1.0, 2.0, 5.0]
    omega_fixed = 0.1
    
    for R in R_values:
        v_tang = omega_fixed * R
        energy_factor = 0.5 * omega_fixed**2 * R**2
        H0_eff = omega_fixed / (2 * np.pi)
        
        print(f"   R = {R:3.1f} → v₄D = {v_tang:5.2f}, Energía ∝ {energy_factor:6.4f}")
    
    print(f"\n🚀 Efectos de variar omega_4d_param (manteniendo R = 1.0):")
    
    omega_values = [0.01, 0.05, 0.1, 0.2, 0.5]
    R_fixed = 1.0
    
    for omega in omega_values:
        v_tang = omega * R_fixed
        energy_factor = 0.5 * omega**2 * R_fixed**2
        H0_eff = omega / (2 * np.pi)
        period = 2 * np.pi / omega
        
        print(f"   ω₄D = {omega:4.2f} → v₄D = {v_tang:5.2f}, H₀ ∝ {H0_eff:6.4f}, T = {period:6.1f}")

def recommend_parameter_exploration():
    """Recomienda valores para explorar"""
    
    print(f"\n🎯 RECOMENDACIONES PARA EXPLORACIÓN")
    print("=" * 45)
    
    print(f"\n📊 Para simulaciones futuras, puedes probar:")
    
    print(f"\n🔬 Exploración sistemática de omega_4d_param:")
    print(f"   • omega_4d = 0.05  → Efectos más sutiles, evolución lenta")
    print(f"   • omega_4d = 0.1   → Valor actual (baseline)")
    print(f"   • omega_4d = 0.2   → Efectos más pronunciados")
    print(f"   • omega_4d = 0.5   → Efectos muy fuertes (¿inestabilidad?)")
    
    print(f"\n🏗️  Exploración sistemática de R_param:")
    print(f"   • R_param = 0.5    → Estructura más compacta")
    print(f"   • R_param = 1.0    → Valor actual (baseline)")
    print(f"   • R_param = 2.0    → Estructura más grande")
    print(f"   • R_param = 5.0    → Efectos a gran escala")
    
    print(f"\n💡 Estrategia recomendada:")
    print(f"   1. Ejecutar 128³ con valores actuales (R=1.0, ω=0.1)")
    print(f"   2. Si los resultados son buenos, probar ω=0.2")
    print(f"   3. Luego probar R=2.0 (manteniendo ω=0.1)")
    print(f"   4. Comparar todos los resultados")
    
    print(f"\n⚠️  Advertencias:")
    print(f"   • Valores muy altos pueden causar inestabilidad numérica")
    print(f"   • Valores muy bajos pueden dar efectos indetectables")
    print(f"   • omega_4d > 1.0 probablemente sea demasiado extremo")

def main():
    """Función principal"""
    explain_physical_parameters()
    calculate_physical_relationships()
    show_parameter_effects()
    recommend_parameter_exploration()
    
    print(f"\n🎓 RESUMEN PEDAGÓGICO:")
    print("=" * 30)
    print(f"• R_param: Controla la ESCALA de la estructura 4D")
    print(f"• omega_4d_param: Controla la VELOCIDAD de rotación 4D")
    print(f"• Ambos determinan la INTENSIDAD de efectos observables")
    print(f"• Los valores actuales (R=1.0, ω=0.1) son conservadores pero detectables")
    
    print(f"\n🚀 PRÓXIMO PASO:")
    print(f"¿Quieres ejecutar 128³ con valores actuales, o modificar algún parámetro?")

if __name__ == "__main__":
    main()