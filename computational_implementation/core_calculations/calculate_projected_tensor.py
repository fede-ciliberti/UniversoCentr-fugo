#!/usr/bin/env python3
"""
Script para calcular la proyección del Tensor Energía-Momento sobre la 3-esfera.
Paso 3.2 del Plan de Desarrollo: Gravedad como Fenómeno Emergente

Este script implementa el operador de proyección para obtener el tensor efectivo
que un observador confinado a la 3-esfera puede medir.

Fecha: 26 de junio de 2025
"""

import sympy as sp
from sympy import symbols, cos, sin, Matrix, diff, simplify, pprint, eye, sqrt

def main():
    print("=" * 80)
    print("CÁLCULO DEL TENSOR ENERGÍA-MOMENTO PROYECTADO EN LA 3-ESFERA")
    print("=" * 80)
    
    # 1. Definir símbolos necesarios (reutilizado de scripts anteriores)
    print("\n1. Definiendo símbolos matemáticos...")
    R = symbols('R', positive=True)  # Radio de la 3-esfera
    psi, theta, phi = symbols('psi theta phi', real=True)  # Coordenadas hiperesféricas
    t = symbols('t', real=True)  # Tiempo
    omega_4d = symbols('omega_4d', real=True)  # Velocidad angular 4D
    
    print(f"   R: Radio de la 3-esfera")
    print(f"   psi, theta, phi: Coordenadas hiperesféricas")
    print(f"   t: Tiempo")
    print(f"   omega_4d: Velocidad angular 4D")
    
    # 2. Definir vector de posición 4D original (reutilizado)
    print("\n2. Definiendo vector de posición 4D original...")
    print("   Orden de coordenadas: (x, y, z, w)")
    
    # Coordenadas cartesianas en 4D (orden x, y, z, w)
    x0 = R * cos(psi) * cos(theta) * cos(phi)  # x
    x1 = R * cos(psi) * cos(theta) * sin(phi)  # y
    x2 = R * cos(psi) * sin(theta)             # z
    x3 = R * sin(psi)                          # w
    
    # Vector de posición 4D
    P = Matrix([x0, x1, x2, x3])
    
    print("   Vector P = [x, y, z, w] en la 3-esfera")
    
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
    
    # 4. Calcular 4-velocidad y tensor energía-momento (reutilizado)
    print("\n4. Calculando 4-velocidad y tensor energía-momento...")
    P_rot = Rot * P
    U = Matrix([diff(P_rot[i], t) for i in range(4)])
    
    print("   4-velocidad U calculada")
    
    # Tensor energía-momento T^αβ = U^α ⊗ U^β
    U_transpose = U.T
    T_matrix = U * U_transpose
    T_simplified = Matrix(4, 4, lambda i, j: simplify(T_matrix[i, j]))
    
    print("   Tensor energía-momento T^αβ calculado")
    
    # 5. NUEVA PARTE: Definir vector normal n
    print("\n5. Definiendo vector normal a la superficie de la 3-esfera...")
    
    # El vector normal n a la superficie de la 3-esfera en un punto P 
    # es simplemente el vector de posición normalizado: n = P / R
    n = Matrix([P[i] / R for i in range(4)])
    
    print("   Vector normal n = P / R:")
    for i, component in enumerate(['n_x', 'n_y', 'n_z', 'n_w']):
        print(f"   {component} = {simplify(n[i])}")
    
    # Verificar que n es unitario
    n_norm_squared = sum([n[i]**2 for i in range(4)])
    n_norm_squared_simplified = simplify(n_norm_squared)
    print(f"\n   Verificación: |n|² = {n_norm_squared_simplified}")
    print("   (Debe ser 1 para un vector unitario)")
    
    # 6. Construir el operador de proyección
    print("\n6. Construyendo el operador de proyección Proj = I - n ⊗ n...")
    
    # Matriz identidad 4x4
    I = eye(4)
    
    # Producto exterior n ⊗ n.T (n es vector columna, n.T es vector fila)
    n_transpose = n.T
    n_outer_product = n * n_transpose
    
    print(f"   Dimensiones de I: {I.shape}")
    print(f"   Dimensiones de n: {n.shape}")
    print(f"   Dimensiones de n.T: {n_transpose.shape}")
    print(f"   Dimensiones de n ⊗ n.T: {n_outer_product.shape}")
    
    # Operador de proyección: Proj = I - n ⊗ n.T
    Proj = I - n_outer_product
    
    print("\n   Operador de proyección Proj construido (4×4)")
    
    # 7. Calcular la proyección del tensor: T_projected = Proj * T_matrix * Proj.T
    print("\n7. Calculando la proyección del tensor energía-momento...")
    print("   Operación: T_projected = Proj * T_matrix * Proj.T")
    
    # Primera multiplicación: Proj * T_matrix
    print("   Paso 1: Calculando Proj * T_matrix...")
    intermediate = Proj * T_simplified
    
    # Segunda multiplicación: resultado * Proj.T
    print("   Paso 2: Calculando (Proj * T_matrix) * Proj.T...")
    Proj_transpose = Proj.T
    T_projected = intermediate * Proj_transpose
    
    print(f"   Dimensiones de T_projected: {T_projected.shape}")
    
    # 8. Simplificar cada elemento de la matriz proyectada
    print("\n8. Simplificando cada elemento del tensor proyectado...")
    print("   (Esto puede tomar varios minutos debido a la complejidad...)")
    
    T_projected_simplified = Matrix(4, 4, lambda i, j: simplify(T_projected[i, j]))
    
    # 9. Mostrar el resultado final
    print("\n" + "=" * 80)
    print("RESULTADO FINAL: TENSOR ENERGÍA-MOMENTO PROYECTADO T_projected")
    print("=" * 80)
    
    print("\nTensor T_projected = Proj * T^αβ * Proj.T (matriz 4×4)")
    print("Este tensor representa lo que un observador en la 3-esfera puede medir")
    
    # Mostrar la matriz de forma organizada
    labels = ['x', 'y', 'z', 'w']
    
    # Encabezado
    print("\n    ", end="")
    for j in range(4):
        print(f"{'T_' + labels[j]:>20}", end="")
    print()
    
    # Filas de la matriz
    for i in range(4):
        print(f"T_{labels[i]} ", end="")
        for j in range(4):
            element = T_projected_simplified[i, j]
            if element == 0:
                print(f"{'0':>20}", end="")
            else:
                # Mostrar una versión compacta para elementos no nulos
                element_str = str(element)
                if len(element_str) > 17:
                    element_str = element_str[:17] + "..."
                print(f"{element_str:>20}", end="")
        print()
    
    # 10. Mostrar elementos no nulos con detalle
    print("\n" + "-" * 60)
    print("ELEMENTOS NO NULOS DEL TENSOR PROYECTADO (detallados):")
    print("-" * 60)
    
    non_zero_count = 0
    for i in range(4):
        for j in range(4):
            element = T_projected_simplified[i, j]
            if element != 0:
                non_zero_count += 1
                print(f"\nT_projected^{labels[i]}{labels[j]} =")
                pprint(element)
    
    print(f"\nTotal de elementos no nulos: {non_zero_count} de 16")
    
    # 11. Análisis de simetría del tensor proyectado
    print("\n" + "-" * 60)
    print("ANÁLISIS DE SIMETRÍA DEL TENSOR PROYECTADO:")
    print("-" * 60)
    
    is_symmetric = True
    for i in range(4):
        for j in range(4):
            if simplify(T_projected_simplified[i, j] - T_projected_simplified[j, i]) != 0:
                is_symmetric = False
                break
        if not is_symmetric:
            break
    
    print(f"¿Es simétrico T_projected^αβ = T_projected^βα? {is_symmetric}")
    
    if is_symmetric:
        print("✓ El tensor proyectado es simétrico, preservando las propiedades físicas.")
    else:
        print("✗ El tensor proyectado no es simétrico. Revisar cálculos.")
    
    # 12. Información adicional sobre la proyección
    print("\n" + "-" * 60)
    print("INTERPRETACIÓN FÍSICA:")
    print("-" * 60)
    print("- Este tensor representa la 'sombra' del tensor 4D sobre la 3-esfera")
    print("- Solo contiene componentes tangentes a la superficie de la 3-esfera")
    print("- Las componentes normales a la superficie han sido eliminadas")
    print("- Este es el tensor que un observador confinado a la 3-esfera mediría")
    
    return T_projected_simplified, Proj, n

if __name__ == "__main__":
    print("Iniciando cálculo del tensor proyectado...")
    tensor_projected, projection_operator, normal_vector = main()
    print("\n" + "=" * 80)
    print("CÁLCULO COMPLETADO")
    print("=" * 80)
    print("\nEl tensor energía-momento ha sido proyectado exitosamente sobre la 3-esfera.")
    print("Los resultados muestran cómo la dinámica 4D se manifiesta en nuestro espacio 3D.")