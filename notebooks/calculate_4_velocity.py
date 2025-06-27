#!/usr/bin/env python3
"""
Script para calcular la 4-velocidad de una partícula en una 3-esfera
sometida a rotación isoclínica en 4D.

Paso 1.2 del Plan de Desarrollo: Gravedad como Fenómeno Emergente
Fecha: 26 de junio de 2025
"""

import sympy as sp
from sympy import symbols, cos, sin, Matrix, diff, simplify, pprint

def main():
    print("=" * 60)
    print("CÁLCULO DE LA 4-VELOCIDAD EN ROTACIÓN ISOCLÍNICA 4D")
    print("=" * 60)
    
    # 1. Definir símbolos necesarios
    print("\n1. Definiendo símbolos matemáticos...")
    R = symbols('R', positive=True)  # Radio de la 3-esfera
    psi, theta, phi = symbols('psi theta phi', real=True)  # Coordenadas hiperesféricas
    t = symbols('t', real=True)  # Tiempo
    omega_4d = symbols('omega_4d', real=True)  # Velocidad angular 4D
    
    print(f"   R: Radio de la 3-esfera")
    print(f"   psi, theta, phi: Coordenadas hiperesféricas")
    print(f"   t: Tiempo")
    print(f"   omega_4d: Velocidad angular 4D")
    
    # 2. Definir vector de posición 4D en la 3-esfera
    print("\n2. Definiendo vector de posición 4D...")
    print("   Orden de coordenadas: (x, y, z, w)")
    
    # Coordenadas cartesianas en 4D (orden x, y, z, w)
    x0 = R * cos(psi) * cos(theta) * cos(phi)  # x
    x1 = R * cos(psi) * cos(theta) * sin(phi)  # y
    x2 = R * cos(psi) * sin(theta)             # z
    x3 = R * sin(psi)                          # w
    
    # Vector de posición 4D
    P = Matrix([x0, x1, x2, x3])
    
    print("   Vector P = [x, y, z, w]:")
    print("   x =", x0)
    print("   y =", x1)
    print("   z =", x2)
    print("   w =", x3)
    
    # 3. Definir matriz de rotación isoclínica en el plano zw
    print("\n3. Definiendo matriz de rotación isoclínica (plano zw)...")
    
    # Ángulo de rotación
    angle = omega_4d * t
    
    # Matriz de rotación para rotación en el plano zw
    # Afecta las coordenadas z (índice 2) y w (índice 3)
    Rot = Matrix([
        [1, 0, 0, 0],                    # x no se ve afectada
        [0, 1, 0, 0],                    # y no se ve afectada  
        [0, 0, cos(angle), -sin(angle)], # z se rota con w
        [0, 0, sin(angle), cos(angle)]   # w se rota con z
    ])
    
    print("   Matriz de rotación R(t):")
    print("   Rotación en plano zw con ángulo = omega_4d * t")
    pprint(Rot)
    
    # 4. Aplicar rotación al vector de posición
    print("\n4. Aplicando rotación al vector de posición...")
    P_rot = Rot * P
    
    print("   Vector rotado P_rot:")
    for i, component in enumerate(['x', 'y', 'z', 'w']):
        print(f"   {component}_rot = {P_rot[i]}")
    
    # 5. Calcular 4-velocidad (derivada temporal)
    print("\n5. Calculando 4-velocidad U = dP_rot/dt...")
    
    U = Matrix([diff(P_rot[i], t) for i in range(4)])
    
    print("\n   4-velocidad U = [U_x, U_y, U_z, U_w]:")
    print("   U_x =", simplify(U[0]))
    print("   U_y =", simplify(U[1]))
    print("   U_z =", simplify(U[2]))
    print("   U_w =", simplify(U[3]))
    
    # 6. Mostrar resultado final simplificado
    print("\n" + "=" * 60)
    print("RESULTADO FINAL: 4-VELOCIDAD")
    print("=" * 60)
    
    print("\nVector de 4-velocidad U:")
    for i, component in enumerate(['U_x', 'U_y', 'U_z', 'U_w']):
        simplified_component = simplify(U[i])
        print(f"{component} = {simplified_component}")
    
    # Análisis adicional: mostrar la estructura
    print("\n" + "-" * 40)
    print("ANÁLISIS DE LA ESTRUCTURA:")
    print("-" * 40)
    
    print("\nComponentes no nulas:")
    for i, component in enumerate(['U_x', 'U_y', 'U_z', 'U_w']):
        if U[i] != 0:
            print(f"  {component} = {simplify(U[i])}")
    
    print("\nComponentes nulas:")
    for i, component in enumerate(['U_x', 'U_y', 'U_z', 'U_w']):
        if U[i] == 0:
            print(f"  {component} = 0")
    
    return U

if __name__ == "__main__":
    four_velocity = main()
    print("\n" + "=" * 60)
    print("CÁLCULO COMPLETADO")
    print("=" * 60)