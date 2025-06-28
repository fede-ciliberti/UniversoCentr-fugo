#!/usr/bin/env python3
"""
Script para calcular el Tensor Energía-Momento de una partícula en una 3-esfera
sometida a rotación isoclínica en 4D.

Paso 2.1 del Plan de Desarrollo: Gravedad como Fenómeno Emergente
Fecha: 26 de junio de 2025
"""

import sympy as sp
from sympy import symbols, cos, sin, Matrix, diff, simplify, pprint

def main():
    print("=" * 70)
    print("CÁLCULO DEL TENSOR ENERGÍA-MOMENTO EN ROTACIÓN ISOCLÍNICA 4D")
    print("=" * 70)
    
    # 1. Definir símbolos necesarios (reutilizado del script anterior)
    print("\n1. Definiendo símbolos matemáticos...")
    R = symbols('R', positive=True)  # Radio de la 3-esfera
    psi, theta, phi = symbols('psi theta phi', real=True)  # Coordenadas hiperesféricas
    t = symbols('t', real=True)  # Tiempo
    omega_4d = symbols('omega_4d', real=True)  # Velocidad angular 4D
    
    print(f"   R: Radio de la 3-esfera")
    print(f"   psi, theta, phi: Coordenadas hiperesféricas")
    print(f"   t: Tiempo")
    print(f"   omega_4d: Velocidad angular 4D")
    
    # 2. Definir vector de posición 4D en la 3-esfera (reutilizado)
    print("\n2. Definiendo vector de posición 4D...")
    print("   Orden de coordenadas: (x, y, z, w)")
    
    # Coordenadas cartesianas en 4D (orden x, y, z, w)
    x0 = R * cos(psi) * cos(theta) * cos(phi)  # x
    x1 = R * cos(psi) * cos(theta) * sin(phi)  # y
    x2 = R * cos(psi) * sin(theta)             # z
    x3 = R * sin(psi)                          # w
    
    # Vector de posición 4D
    P = Matrix([x0, x1, x2, x3])
    
    # 3. Definir matriz de rotación isoclínica (reutilizado)
    print("\n3. Definiendo matriz de rotación isoclínica (plano zw)...")
    
    # Ángulo de rotación
    angle = omega_4d * t
    
    # Matriz de rotación para rotación en el plano zw
    Rot = Matrix([
        [1, 0, 0, 0],                    # x no se ve afectada
        [0, 1, 0, 0],                    # y no se ve afectada  
        [0, 0, cos(angle), -sin(angle)], # z se rota con w
        [0, 0, sin(angle), cos(angle)]   # w se rota con z
    ])
    
    # 4. Aplicar rotación y calcular 4-velocidad (reutilizado)
    print("\n4. Calculando 4-velocidad...")
    P_rot = Rot * P
    U = Matrix([diff(P_rot[i], t) for i in range(4)])
    
    print("   4-velocidad U calculada:")
    for i, component in enumerate(['U_x', 'U_y', 'U_z', 'U_w']):
        print(f"   {component} = {simplify(U[i])}")
    
    # 5. NUEVA PARTE: Calcular el producto exterior U ⊗ U (Tensor Energía-Momento sin masa)
    print("\n5. Calculando el Tensor Energía-Momento T^αβ = U^α ⊗ U^β...")
    print("   (sin incluir la masa m y la función delta)")
    
    # Calcular T_matrix = U * U.T (producto exterior)
    U_transpose = U.T  # Traspuesta de U (vector fila)
    T_matrix = U * U_transpose  # Producto exterior: vector columna × vector fila = matriz 4×4
    
    print(f"\n   Dimensiones de U: {U.shape}")
    print(f"   Dimensiones de U.T: {U_transpose.shape}")
    print(f"   Dimensiones de T_matrix: {T_matrix.shape}")
    
    # 6. Simplificar cada elemento de la matriz
    print("\n6. Simplificando cada elemento del tensor...")
    
    T_simplified = Matrix(4, 4, lambda i, j: simplify(T_matrix[i, j]))
    
    # 7. Mostrar resultado final
    print("\n" + "=" * 70)
    print("RESULTADO FINAL: TENSOR ENERGÍA-MOMENTO T^αβ")
    print("=" * 70)
    
    print("\nTensor T^αβ = U^α ⊗ U^β (matriz 4×4):")
    print("Índices: α,β ∈ {x, y, z, w}")
    print("\nMatriz completa:")
    
    # Mostrar la matriz de forma organizada
    labels = ['x', 'y', 'z', 'w']
    
    # Encabezado
    print("\n    ", end="")
    for j in range(4):
        print(f"{'T_' + labels[j]:>15}", end="")
    print()
    
    # Filas de la matriz
    for i in range(4):
        print(f"T_{labels[i]} ", end="")
        for j in range(4):
            element = T_simplified[i, j]
            if element == 0:
                print(f"{'0':>15}", end="")
            else:
                # Mostrar una versión compacta para elementos no nulos
                element_str = str(element)
                if len(element_str) > 12:
                    element_str = element_str[:12] + "..."
                print(f"{element_str:>15}", end="")
        print()
    
    # 8. Mostrar elementos no nulos con detalle
    print("\n" + "-" * 50)
    print("ELEMENTOS NO NULOS DEL TENSOR (detallados):")
    print("-" * 50)
    
    non_zero_count = 0
    for i in range(4):
        for j in range(4):
            element = T_simplified[i, j]
            if element != 0:
                non_zero_count += 1
                print(f"\nT^{labels[i]}{labels[j]} = {element}")
    
    print(f"\nTotal de elementos no nulos: {non_zero_count} de 16")
    
    # 9. Análisis de simetría
    print("\n" + "-" * 50)
    print("ANÁLISIS DE SIMETRÍA:")
    print("-" * 50)
    
    is_symmetric = True
    for i in range(4):
        for j in range(4):
            if simplify(T_simplified[i, j] - T_simplified[j, i]) != 0:
                is_symmetric = False
                break
        if not is_symmetric:
            break
    
    print(f"¿Es simétrico T^αβ = T^βα? {is_symmetric}")
    
    if is_symmetric:
        print("✓ El tensor es simétrico, como se esperaba para un tensor energía-momento.")
    else:
        print("✗ El tensor no es simétrico. Revisar cálculos.")
    
    return T_simplified, U

if __name__ == "__main__":
    tensor_stress_energy, four_velocity = main()
    print("\n" + "=" * 70)
    print("CÁLCULO COMPLETADO")
    print("=" * 70)