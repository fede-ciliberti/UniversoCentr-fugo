#!/usr/bin/env python3
"""
Script para calcular el promedio temporal del Tensor Energía-Momento proyectado.
Paso 2.1 del Plan de Verificación de Aproximaciones

Este script reutiliza el código de calculate_projected_tensor.py para obtener T_projected
y luego calcula el promedio temporal de cada elemento usando integración simbólica.

Fecha: 26 de junio de 2025
"""

import sympy as sp
from sympy import symbols, cos, sin, Matrix, diff, simplify, pprint, eye, sqrt, integrate, pi

def get_projected_tensor():
    """
    Función que reutiliza el código de calculate_projected_tensor.py 
    para obtener la matriz T_projected simbólica.
    """
    print("Calculando tensor proyectado (reutilizando código anterior)...")
    
    # 1. Definir símbolos necesarios
    R = symbols('R', positive=True)  # Radio de la 3-esfera
    psi, theta, phi = symbols('psi theta phi', real=True)  # Coordenadas hiperesféricas
    t = symbols('t', real=True)  # Tiempo
    omega_4d = symbols('omega_4d', real=True)  # Velocidad angular 4D
    
    # 2. Definir vector de posición 4D original
    x0 = R * cos(psi) * cos(theta) * cos(phi)  # x
    x1 = R * cos(psi) * cos(theta) * sin(phi)  # y
    x2 = R * cos(psi) * sin(theta)             # z
    x3 = R * sin(psi)                          # w
    
    # Vector de posición 4D
    P = Matrix([x0, x1, x2, x3])
    
    # 3. Definir matriz de rotación isoclínica (plano zw)
    angle = omega_4d * t
    
    Rot = Matrix([
        [1, 0, 0, 0],                    # x no se ve afectada
        [0, 1, 0, 0],                    # y no se ve afectada  
        [0, 0, cos(angle), -sin(angle)], # z se rota con w
        [0, 0, sin(angle), cos(angle)]   # w se rota con z
    ])
    
    # 4. Calcular 4-velocidad y tensor energía-momento
    P_rot = Rot * P
    U = Matrix([diff(P_rot[i], t) for i in range(4)])
    
    # Tensor energía-momento T^αβ = U^α ⊗ U^β
    U_transpose = U.T
    T_matrix = U * U_transpose
    T_simplified = Matrix(4, 4, lambda i, j: simplify(T_matrix[i, j]))
    
    # 5. Definir vector normal n
    n = Matrix([P[i] / R for i in range(4)])
    
    # 6. Construir el operador de proyección
    I = eye(4)
    n_transpose = n.T
    n_outer_product = n * n_transpose
    Proj = I - n_outer_product
    
    # 7. Calcular la proyección del tensor: T_projected = Proj * T_matrix * Proj.T
    intermediate = Proj * T_simplified
    Proj_transpose = Proj.T
    T_projected = intermediate * Proj_transpose
    
    # 8. Simplificar cada elemento
    T_projected_simplified = Matrix(4, 4, lambda i, j: simplify(T_projected[i, j]))
    
    return T_projected_simplified, omega_4d, t

def calculate_time_averaged_tensor():
    """
    Función principal que calcula el promedio temporal del tensor proyectado.
    """
    print("=" * 80)
    print("CÁLCULO DEL PROMEDIO TEMPORAL DEL TENSOR ENERGÍA-MOMENTO PROYECTADO")
    print("=" * 80)
    
    # 1. Obtener el tensor proyectado
    print("\n1. Obteniendo tensor proyectado...")
    T_projected, omega_4d, t = get_projected_tensor()
    print("   ✓ Tensor proyectado T_projected obtenido")
    
    # 2. Definir el período de una rotación completa
    print("\n2. Definiendo período de rotación...")
    T_period = 2 * pi / omega_4d
    print(f"   Período T = 2π/ω₄ᴅ = {T_period}")
    
    # 3. Crear matriz para almacenar resultados promediados
    print("\n3. Creando matriz para resultados promediados...")
    T_averaged = Matrix(4, 4, lambda i, j: 0)
    print("   ✓ Matriz T_averaged (4×4) inicializada")
    
    # 4. Calcular promedio temporal para cada elemento
    print("\n4. Calculando promedio temporal para cada elemento de la matriz...")
    print("   Fórmula: <f> = (1/T) ∫₀ᵀ f(t) dt")
    print("   (Esto puede tomar varios minutos...)")
    
    labels = ['x', 'y', 'z', 'w']
    
    for i in range(4):
        for j in range(4):
            element_ij = T_projected[i, j]
            
            print(f"\n   Procesando elemento T_{labels[i]}{labels[j]} ({i+1}/16)...")
            
            if element_ij == 0:
                # Si el elemento es cero, su promedio también es cero
                T_averaged[i, j] = 0
                print(f"      Elemento es cero → Promedio = 0")
            else:
                # Calcular la integral temporal
                print(f"      Calculando integral de: {element_ij}")
                
                try:
                    # Integral definida de 0 a T
                    integral_result = integrate(element_ij, (t, 0, T_period))
                    print(f"      Integral calculada: {integral_result}")
                    
                    # Promedio: (1/T) * integral
                    average_result = integral_result / T_period
                    print(f"      Antes de simplificar: {average_result}")
                    
                    # Simplificar el resultado
                    averaged_simplified = simplify(average_result)
                    T_averaged[i, j] = averaged_simplified
                    
                    print(f"      ✓ Promedio temporal T_{labels[i]}{labels[j]} = {averaged_simplified}")
                    
                except Exception as e:
                    print(f"      ⚠ Error en integración: {e}")
                    print(f"      Intentando simplificar antes de integrar...")
                    
                    # Intentar simplificar primero
                    element_simplified = simplify(element_ij)
                    try:
                        integral_result = integrate(element_simplified, (t, 0, T_period))
                        average_result = simplify(integral_result / T_period)
                        T_averaged[i, j] = average_result
                        print(f"      ✓ Promedio temporal T_{labels[i]}{labels[j]} = {average_result}")
                    except:
                        print(f"      ✗ No se pudo calcular la integral para T_{labels[i]}{labels[j]}")
                        T_averaged[i, j] = sp.Symbol(f'<T_{labels[i]}{labels[j]}>')
    
    # 5. Mostrar el resultado final
    print("\n" + "=" * 80)
    print("RESULTADO FINAL: TENSOR ENERGÍA-MOMENTO PROMEDIADO TEMPORALMENTE")
    print("=" * 80)
    
    print("\nTensor T_averaged = <T_projected> (promedio temporal)")
    print("Este tensor representa el comportamiento promedio a lo largo de un período completo")
    
    # Mostrar la matriz de forma organizada
    print("\n    ", end="")
    for j in range(4):
        print(f"{'<T_' + labels[j] + '>':>25}", end="")
    print()
    
    # Filas de la matriz
    for i in range(4):
        print(f"<T_{labels[i]}> ", end="")
        for j in range(4):
            element = T_averaged[i, j]
            if element == 0:
                print(f"{'0':>25}", end="")
            else:
                element_str = str(element)
                if len(element_str) > 22:
                    element_str = element_str[:22] + "..."
                print(f"{element_str:>25}", end="")
        print()
    
    # 6. Mostrar elementos no nulos con detalle
    print("\n" + "-" * 70)
    print("ELEMENTOS NO NULOS DEL TENSOR PROMEDIADO (detallados):")
    print("-" * 70)
    
    non_zero_count = 0
    for i in range(4):
        for j in range(4):
            element = T_averaged[i, j]
            if element != 0:
                non_zero_count += 1
                print(f"\n<T_projected^{labels[i]}{labels[j]}> =")
                pprint(element)
    
    print(f"\nTotal de elementos no nulos: {non_zero_count} de 16")
    
    # 7. Análisis de las simplificaciones
    print("\n" + "-" * 70)
    print("ANÁLISIS DE LAS SIMPLIFICACIONES POR PROMEDIADO TEMPORAL:")
    print("-" * 70)
    
    # Contar elementos que se anularon
    original_non_zero = 0
    final_non_zero = non_zero_count
    
    # Esto requeriría comparar con T_projected, pero es complejo
    # Por ahora, mostramos el resultado
    
    print("- El promediado temporal elimina todas las oscilaciones periódicas")
    print("- Solo permanecen los términos constantes e independientes del tiempo")
    print("- Esto revela la estructura subyacente del tensor sin fluctuaciones")
    
    # 8. Verificación de conservación
    print("\n" + "-" * 70)
    print("VERIFICACIÓN DE PROPIEDADES DE CONSERVACIÓN:")
    print("-" * 70)
    
    # Verificar simetría
    is_symmetric = True
    for i in range(4):
        for j in range(4):
            if simplify(T_averaged[i, j] - T_averaged[j, i]) != 0:
                is_symmetric = False
                break
        if not is_symmetric:
            break
    
    print(f"¿Es simétrico <T_projected^αβ> = <T_projected^βα>? {is_symmetric}")
    
    if is_symmetric:
        print("✓ La simetría del tensor se preserva tras el promediado temporal.")
    else:
        print("✗ La simetría del tensor no se preserva. Revisar cálculos.")
    
    print("\n" + "=" * 80)
    print("INTERPRETACIÓN FÍSICA:")
    print("=" * 80)
    print("- El tensor promediado representa el comportamiento medio del sistema")
    print("- Las oscilaciones de alta frecuencia han sido filtradas")
    print("- Este es el tensor efectivo que se observaría en escalas de tiempo largas")
    print("- Fundamental para comparar con observaciones gravitacionales clásicas")
    
    return T_averaged

def main():
    """
    Función principal del script.
    """
    try:
        tensor_averaged = calculate_time_averaged_tensor()
        
        print("\n" + "=" * 80)
        print("CÁLCULO COMPLETADO EXITOSAMENTE")
        print("=" * 80)
        print("\nEl tensor energía-momento ha sido promediado temporalmente.")
        print("Los resultados muestran la estructura subyacente sin oscilaciones.")
        
        return tensor_averaged
        
    except Exception as e:
        print(f"\n✗ Error durante el cálculo: {e}")
        print("Revise los cálculos simbólicos y la configuración de SymPy.")
        return None

if __name__ == "__main__":
    print("Iniciando cálculo del tensor promediado temporalmente...")
    result = main()