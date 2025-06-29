#!/usr/bin/env python3
"""
Script para el Análisis Matemático de Componentes Fuera de Diagonal del Tensor ⟨T_μν⟩
Tarea 1.1.1 del Plan de Investigación del Universo Centrífugo

Este script determina si los términos no diagonales del tensor ⟨T_μν⟩ se anulan o persisten 
después del promedio sobre ángulos espaciales (θ, φ), implementando un análisis completo
de isotropía tensorial.

Autor: Equipo de Investigación Universo Centrífugo
Fecha: 28 de junio de 2025
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, cos, sin, Matrix, diff, simplify, pprint, eye, sqrt, integrate, pi, expand, trigsimp
from typing import Union, Optional, Dict, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

class TensorIsotropyAnalyzer:
    """
    Clase principal para el análisis de isotropía del tensor estrés-energía.
    """
    
    def __init__(self):
        """Inicializar el analizador con símbolos matemáticos."""
        print("🔧 Inicializando Analizador de Isotropía Tensorial...")
        
        # Símbolos básicos
        self.R = symbols('R', positive=True)
        self.psi, self.theta, self.phi = symbols('psi theta phi', real=True)
        self.t = symbols('t', real=True)
        self.omega_4d = symbols('omega_4d', real=True)
        
        # Resultados de análisis - inicializar apropiadamente
        self.tensor_projected: Optional[Matrix] = None
        self.tensor_time_averaged: Optional[Matrix] = None
        self.tensor_angular_averaged: Optional[Matrix] = None
        self.existing_calculations_analysis: Dict[str, Any] = {}
        self.isotropy_metrics: Dict[str, Any] = {}
        
        print("✅ Analizador inicializado correctamente")
    
    def analyze_existing_calculations(self):
        """
        Revisar y analizar los scripts existentes para identificar inconsistencias.
        """
        print("\n" + "="*80)
        print("📋 ANÁLISIS DE CÓDIGO EXISTENTE")
        print("="*80)
        
        print("\n1️⃣  Revisando calculate_projected_tensor.py...")
        
        # Obtener tensor proyectado usando el código existente
        projected_tensor, proj_operator, normal_vector = self._get_projected_tensor_from_existing()
        self.tensor_projected = projected_tensor
        
        print("   ✅ Tensor proyectado obtenido")
        print(f"   📊 Dimensiones: {projected_tensor.shape}")
        
        # Contar elementos no nulos de forma segura
        non_zero_count = 0
        diagonal_count = 0
        off_diagonal_count = 0
        
        for i in range(4):
            for j in range(4):
                element = projected_tensor[i, j]
                if not self._is_zero_element(element):
                    non_zero_count += 1
                    if i == j:
                        diagonal_count += 1
                    else:
                        off_diagonal_count += 1
        
        print(f"   📈 Elementos no nulos: {non_zero_count}/16")
        print(f"   🔹 Elementos diagonales no nulos: {diagonal_count}")
        print(f"   🔸 Elementos fuera de diagonal no nulos: {off_diagonal_count}")
        
        print("\n2️⃣  Revisando calculate_time_averaged_tensor.py...")
        
        # Obtener tensor promediado temporalmente
        time_averaged_tensor = self._get_time_averaged_tensor_from_existing()
        self.tensor_time_averaged = time_averaged_tensor
        
        print("   ✅ Tensor promediado temporalmente obtenido")
        
        # Analizar simplificaciones por promediado temporal
        time_non_zero = 0
        time_diagonal = 0
        time_off_diagonal = 0
        
        for i in range(4):
            for j in range(4):
                element = time_averaged_tensor[i, j]
                if not self._is_zero_element(element):
                    time_non_zero += 1
                    if i == j:
                        time_diagonal += 1
                    else:
                        time_off_diagonal += 1
        
        print(f"   📈 Elementos no nulos después del promedio temporal: {time_non_zero}/16")
        print(f"   🔹 Elementos diagonales no nulos: {time_diagonal}")
        print(f"   🔸 Elementos fuera de diagonal no nulos: {time_off_diagonal}")
        
        # Identificar inconsistencias
        print("\n3️⃣  Identificando inconsistencias potenciales...")
        
        inconsistencies = []
        
        if off_diagonal_count > 0:
            inconsistencies.append("Tensor proyectado tiene términos fuera de diagonal")
        
        if time_off_diagonal > 0:
            inconsistencies.append("Promedio temporal no eliminó todos los términos fuera de diagonal")
        
        if time_non_zero == 0:
            inconsistencies.append("Promedio temporal anuló completamente el tensor (sospechoso)")
        
        if len(inconsistencies) == 0:
            print("   ✅ No se detectaron inconsistencias obvias")
        else:
            print("   ⚠️  Inconsistencias detectadas:")
            for i, inc in enumerate(inconsistencies, 1):
                print(f"      {i}. {inc}")
        
        # Guardar análisis
        self.existing_calculations_analysis = {
            'projected_non_zero': non_zero_count,
            'projected_diagonal': diagonal_count,
            'projected_off_diagonal': off_diagonal_count,
            'time_averaged_non_zero': time_non_zero,
            'time_averaged_diagonal': time_diagonal,
            'time_averaged_off_diagonal': time_off_diagonal,
            'inconsistencies': inconsistencies
        }
        
        return self.existing_calculations_analysis
    
    def _is_zero_element(self, element) -> bool:
        """
        Verificar si un elemento es cero de forma robusta.
        """
        try:
            if element == 0:
                return True
            if hasattr(element, 'is_zero') and element.is_zero:
                return True
            if hasattr(element, 'simplify'):
                simplified = simplify(element)
                return simplified == 0
            return False
        except:
            return False
    
    def _is_numeric_element(self, element) -> bool:
        """
        Verificar si un elemento es numérico de forma robusta.
        """
        try:
            if hasattr(element, 'is_number'):
                return element.is_number
            if isinstance(element, (int, float, complex)):
                return True
            return False
        except:
            return False
    
    def _get_element_magnitude(self, element) -> float:
        """
        Obtener magnitud de un elemento de forma segura.
        """
        try:
            if self._is_numeric_element(element):
                return abs(float(element))
            else:
                # Para elementos simbólicos, usar heurística
                return 1.0
        except:
            return 1.0
    
    def _get_projected_tensor_from_existing(self):
        """
        Reutilizar código de calculate_projected_tensor.py para obtener tensor proyectado.
        """
        # Vector de posición 4D
        x0 = self.R * cos(self.psi) * cos(self.theta) * cos(self.phi)
        x1 = self.R * cos(self.psi) * cos(self.theta) * sin(self.phi)
        x2 = self.R * cos(self.psi) * sin(self.theta)
        x3 = self.R * sin(self.psi)
        
        P = Matrix([x0, x1, x2, x3])
        
        # Matriz de rotación isoclínica
        angle = self.omega_4d * self.t
        Rot = Matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, cos(angle), -sin(angle)],
            [0, 0, sin(angle), cos(angle)]
        ])
        
        # 4-velocidad y tensor energía-momento
        P_rot = Rot * P
        U = Matrix([diff(P_rot[i], self.t) for i in range(4)])
        T_matrix = U * U.T
        T_simplified = Matrix(4, 4, lambda i, j: simplify(T_matrix[i, j]))
        
        # Vector normal y operador de proyección
        n = Matrix([P[i] / self.R for i in range(4)])
        I = eye(4)
        Proj = I - n * n.T
        
        # Tensor proyectado
        T_projected = Proj * T_simplified * Proj.T
        T_projected_simplified = Matrix(4, 4, lambda i, j: simplify(T_projected[i, j]))
        
        return T_projected_simplified, Proj, n
    
    def _get_time_averaged_tensor_from_existing(self):
        """
        Calcular promedio temporal del tensor proyectado.
        """
        if self.tensor_projected is None:
            raise ValueError("Tensor proyectado no disponible")
            
        T_period = 2 * pi / self.omega_4d
        T_averaged = Matrix(4, 4, lambda i, j: 0)
        
        for i in range(4):
            for j in range(4):
                element_ij = self.tensor_projected[i, j]
                
                if self._is_zero_element(element_ij):
                    T_averaged[i, j] = 0
                else:
                    try:
                        integral_result = integrate(element_ij, (self.t, 0, T_period))
                        average_result = integral_result / T_period
                        T_averaged[i, j] = simplify(average_result)
                    except Exception as e:
                        # Para elementos que no se pueden integrar analíticamente
                        T_averaged[i, j] = sp.Symbol(f'<T_{i}{j}>')
        
        return T_averaged
    
    def compute_angular_average(self):
        """
        Calcular promedio sobre ángulos espaciales (θ, φ) usando integración simbólica.
        """
        print("\n" + "="*80)
        print("🌐 CÁLCULO DEL PROMEDIO ANGULAR")
        print("="*80)
        
        if self.tensor_time_averaged is None:
            raise ValueError("Tensor promediado temporalmente no disponible")
        
        print("\n1️⃣  Configurando integración sobre ángulos espaciales...")
        print("   📐 Dominio de integración:")
        print("   θ ∈ [0, π] (latitud)")  
        print("   φ ∈ [0, 2π] (longitud)")
        print("   Método: Integración simbólica con SymPy")
        
        # Crear matriz para almacenar resultados promediados angularmente
        T_angular_averaged = Matrix(4, 4, lambda i, j: 0)
        
        print("\n2️⃣  Calculando integrales angulares para cada elemento...")
        
        # Calcular promedio angular para cada elemento no nulo
        labels = ['x', 'y', 'z', 'w']
        
        for i in range(4):
            for j in range(4):
                element_ij = self.tensor_time_averaged[i, j]
                
                print(f"\n   Procesando elemento ⟨T_{labels[i]}{labels[j]}⟩...")
                
                if self._is_zero_element(element_ij):
                    T_angular_averaged[i, j] = 0
                    print(f"      → Elemento nulo, promedio = 0")
                elif self._is_numeric_element(element_ij):
                    # Si es un número (independiente de ángulos)
                    T_angular_averaged[i, j] = element_ij
                    print(f"      → Constante independiente de ángulos: {element_ij}")
                else:
                    # Intentar integración simbólica
                    try:
                        print(f"      → Integrando sobre (θ, φ)...")
                        
                        # Verificar dependencia angular
                        has_theta = self.theta in element_ij.free_symbols
                        has_phi = self.phi in element_ij.free_symbols
                        
                        if not has_theta and not has_phi:
                            T_angular_averaged[i, j] = element_ij
                            print(f"      ✅ Independiente de ángulos: {element_ij}")
                        else:
                            # Integrar sobre φ de 0 a 2π
                            phi_integral = integrate(element_ij, (self.phi, 0, 2*pi))
                            print(f"      → Integral en φ calculada")
                            
                            # Integrar sobre θ de 0 a π (con peso sin(θ))
                            theta_integral = integrate(phi_integral * sin(self.theta), (self.theta, 0, pi))
                            print(f"      → Integral en θ calculada")
                            
                            # Normalizar por el área de la esfera unitaria (4π)
                            angular_average = theta_integral / (4 * pi)
                            T_angular_averaged[i, j] = simplify(angular_average)
                            
                            print(f"      ✅ Promedio angular: {T_angular_averaged[i, j]}")
                        
                    except Exception as e:
                        print(f"      ⚠️  Error en integración simbólica: {e}")
                        print(f"      → Marcando como elemento simbólico...")
                        T_angular_averaged[i, j] = sp.Symbol(f'∫∫_angular_{i}{j}')
        
        self.tensor_angular_averaged = T_angular_averaged
        
        print("\n3️⃣  Resumen del promedio angular:")
        
        # Contar elementos no nulos después del promedio angular
        angular_non_zero = 0
        angular_diagonal = 0
        angular_off_diagonal = 0
        
        for i in range(4):
            for j in range(4):
                element = T_angular_averaged[i, j]
                if not self._is_zero_element(element):
                    angular_non_zero += 1
                    if i == j:
                        angular_diagonal += 1
                    else:
                        angular_off_diagonal += 1
        
        print(f"   📈 Elementos no nulos: {angular_non_zero}/16")
        print(f"   🔹 Elementos diagonales: {angular_diagonal}")
        print(f"   🔸 Elementos fuera de diagonal: {angular_off_diagonal}")
        
        if angular_off_diagonal == 0:
            print("   🎯 ¡Isotropía conseguida! Términos fuera de diagonal se anularon")
        else:
            print("   ⚠️  Anisotropía persistente: términos fuera de diagonal no nulos")
        
        return T_angular_averaged
    
    def evaluate_isotropy_metrics(self):
        """
        Evaluar métricas cuantitativas de anisotropía.
        """
        print("\n" + "="*80)
        print("📊 EVALUACIÓN DE MÉTRICAS DE ISOTROPÍA")
        print("="*80)
        
        if self.tensor_angular_averaged is None:
            raise ValueError("Tensor promediado angularmente no disponible")
        
        # 1. Ratio de elementos fuera de diagonal vs diagonales
        print("\n1️⃣  Calculando ratio anisotropía/isotropía...")
        
        diagonal_magnitude = 0
        off_diagonal_magnitude = 0
        
        for i in range(4):
            for j in range(4):
                element = self.tensor_angular_averaged[i, j]
                
                if not self._is_zero_element(element):
                    magnitude = self._get_element_magnitude(element)
                    
                    if i == j:
                        diagonal_magnitude += magnitude
                    else:
                        off_diagonal_magnitude += magnitude
        
        if diagonal_magnitude > 0:
            anisotropy_ratio = off_diagonal_magnitude / diagonal_magnitude
        else:
            anisotropy_ratio = float('inf') if off_diagonal_magnitude > 0 else 0
        
        print(f"   📏 Magnitud elementos diagonales: {diagonal_magnitude:.8f}")
        print(f"   📏 Magnitud elementos fuera de diagonal: {off_diagonal_magnitude:.8f}")
        print(f"   📊 Ratio de anisotropía: {anisotropy_ratio:.8f}")
        
        # 2. Grado de isotropía
        print("\n2️⃣  Evaluando grado de isotropía...")
        
        if anisotropy_ratio < 1e-12:
            isotropy_degree = "PERFECTO"
            isotropy_score = 1.0
        elif anisotropy_ratio < 1e-6:
            isotropy_degree = "EXCELENTE"
            isotropy_score = 0.9
        elif anisotropy_ratio < 1e-3:
            isotropy_degree = "BUENO"
            isotropy_score = 0.7
        elif anisotropy_ratio < 0.1:
            isotropy_degree = "MODERADO"
            isotropy_score = 0.5
        else:
            isotropy_degree = "POBRE"
            isotropy_score = 0.1
        
        print(f"   🏆 Grado de isotropía: {isotropy_degree}")
        print(f"   🎯 Puntuación: {isotropy_score}/1.0")
        
        # 3. Análisis de simetría del tensor final
        print("\n3️⃣  Verificando simetría tensorial...")
        
        is_symmetric = True
        max_asymmetry = 0
        
        for i in range(4):
            for j in range(4):
                element_ij = self.tensor_angular_averaged[i, j]
                element_ji = self.tensor_angular_averaged[j, i]
                
                if element_ij != element_ji:
                    is_symmetric = False
                    # Calcular asimetría si son numéricos
                    if self._is_numeric_element(element_ij) and self._is_numeric_element(element_ji):
                        asymmetry = abs(float(element_ij) - float(element_ji))
                        max_asymmetry = max(max_asymmetry, asymmetry)
        
        print(f"   🔄 Simetría tensorial: {'✅ PRESERVADA' if is_symmetric else '❌ ROTA'}")
        if not is_symmetric:
            print(f"   📊 Máxima asimetría: {max_asymmetry:.8e}")
        
        # 4. Conservación de traza
        print("\n4️⃣  Verificando conservación de traza...")
        
        try:
            trace_original = sum([self.tensor_time_averaged[i, i] for i in range(4)])
            trace_final = sum([self.tensor_angular_averaged[i, i] for i in range(4)])
            
            print(f"   📐 Traza antes del promedio angular: {trace_original}")
            print(f"   📐 Traza después del promedio angular: {trace_final}")
            
            if trace_original == trace_final:
                print("   ✅ Traza conservada perfectamente")
                trace_conserved = True
            else:
                print("   ⚠️  Traza modificada por promedio angular")
                trace_conserved = False
        except:
            print("   ⚠️  No se pudo verificar conservación de traza")
            trace_conserved = False
        
        # Guardar métricas
        self.isotropy_metrics = {
            'anisotropy_ratio': anisotropy_ratio,
            'isotropy_degree': isotropy_degree,
            'isotropy_score': isotropy_score,
            'is_symmetric': is_symmetric,
            'max_asymmetry': max_asymmetry,
            'trace_conserved': trace_conserved,
            'diagonal_magnitude': diagonal_magnitude,
            'off_diagonal_magnitude': off_diagonal_magnitude
        }
        
        return self.isotropy_metrics
    
    def generate_diagnostic_report(self):
        """
        Generar reporte completo de diagnóstico.
        """
        print("\n" + "="*80)
        print("📋 REPORTE DE DIAGNÓSTICO COMPLETO")
        print("="*80)
        
        print("\n🔍 RESUMEN EJECUTIVO:")
        print("-" * 40)
        
        # Determinar conclusión principal
        off_diagonal_persist = self.existing_calculations_analysis['time_averaged_off_diagonal'] > 0
        angular_isotropy = self.isotropy_metrics['isotropy_score'] > 0.7
        
        if not off_diagonal_persist and angular_isotropy:
            conclusion = "Los términos no diagonales SE ANULAN completamente"
            conclusion_status = "✅ ISOTÓPICO"
        elif off_diagonal_persist and not angular_isotropy:
            conclusion = "Los términos no diagonales PERSISTEN significativamente"
            conclusion_status = "❌ ANISÓTROPO"
        else:
            conclusion = "Los términos no diagonales se reducen pero no se anulan completamente"
            conclusion_status = "⚠️  PARCIALMENTE ISOTÓPICO"
        
        print(f"📊 CONCLUSIÓN PRINCIPAL: {conclusion}")
        print(f"🎯 ESTADO: {conclusion_status}")
        print(f"🏆 Puntuación de isotropía: {self.isotropy_metrics['isotropy_score']:.2f}/1.0")
        
        # Detalles del análisis
        print(f"\n📈 DETALLES DEL ANÁLISIS:")
        print("-" * 40)
        print(f"• Elementos fuera de diagonal en tensor proyectado: {self.existing_calculations_analysis['projected_off_diagonal']}")
        print(f"• Elementos fuera de diagonal tras promedio temporal: {self.existing_calculations_analysis['time_averaged_off_diagonal']}")
        print(f"• Ratio de anisotropía final: {self.isotropy_metrics['anisotropy_ratio']:.2e}")
        print(f"• Simetría tensorial preservada: {'Sí' if self.isotropy_metrics['is_symmetric'] else 'No'}")
        print(f"• Traza conservada: {'Sí' if self.isotropy_metrics['trace_conserved'] else 'No'}")
        
        # Inconsistencias detectadas
        if self.existing_calculations_analysis['inconsistencies']:
            print(f"\n⚠️  INCONSISTENCIAS DETECTADAS:")
            print("-" * 40)
            for i, inc in enumerate(self.existing_calculations_analysis['inconsistencies'], 1):
                print(f"{i}. {inc}")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        print("-" * 40)
        
        if self.isotropy_metrics['isotropy_score'] < 0.5:
            print("• Investigar origen físico de la anisotropía persistente")
            print("• Revisar cálculos de promediado angular")
            print("• Considerar términos de orden superior en el desarrollo")
        elif self.isotropy_metrics['isotropy_score'] < 0.9:
            print("• Verificar precisión numérica en integraciones")
            print("• Analizar efectos de frontera en el dominio")
            print("• Evaluar convergencia con mayor resolución angular")
        else:
            print("• ✅ Análisis satisfactorio, proceder con siguiente fase")
            print("• Documentar resultados para publicación")
            print("• Considerar validación experimental")
        
        # Impacto en la conjetura
        print(f"\n🌌 IMPACTO EN LA CONJETURA DEL UNIVERSO CENTRÍFUGO:")
        print("-" * 40)
        
        if conclusion_status == "✅ ISOTÓPICO":
            print("• ✅ Consistente con expectativas de isotropía cosmológica")
            print("• ✅ Apoya la validez del modelo matemático")
            print("• ✅ Permite interpretación como métrica de fondo isotópica")
        elif conclusion_status == "❌ ANISÓTROPO":
            print("• ⚠️  Indica direcciones preferenciales en el espacio-tiempo")
            print("• 🔍 Requiere explicación física adicional")
            print("• 📊 Puede predecir anisotropías observables")
        else:
            print("• 🤔 Resultados ambiguos requieren mayor análisis")
            print("• 🔬 Necesita resolución de incertidumbres teóricas")
            print("• 📈 Sugiere efectos de escala en el modelo")
        
        return {
            'conclusion': conclusion,
            'status': conclusion_status,
            'score': self.isotropy_metrics['isotropy_score'],
            'isotropy_achieved': self.isotropy_metrics['isotropy_score'] > 0.7
        }
    
    def display_tensor_matrices(self):
        """
        Mostrar las matrices tensoriales en cada etapa del análisis.
        """
        print("\n" + "="*80)
        print("📊 MATRICES TENSORIALES EN CADA ETAPA")
        print("="*80)
        
        labels = ['x', 'y', 'z', 'w']
        
        if self.tensor_projected is not None:
            # 1. Tensor proyectado
            print("\n1️⃣  TENSOR PROYECTADO T_projected:")
            print("-" * 40)
            self._print_tensor_matrix(self.tensor_projected, labels, "T_proj")
        
        if self.tensor_time_averaged is not None:
            # 2. Tensor promediado temporalmente
            print("\n2️⃣  TENSOR PROMEDIADO TEMPORALMENTE ⟨T_projected⟩:")
            print("-" * 40)
            self._print_tensor_matrix(self.tensor_time_averaged, labels, "⟨T⟩")
        
        if self.tensor_angular_averaged is not None:
            # 3. Tensor promediado angularmente
            print("\n3️⃣  TENSOR PROMEDIADO ANGULARMENTE ⟨⟨T⟩⟩:")
            print("-" * 40)
            self._print_tensor_matrix(self.tensor_angular_averaged, labels, "⟨⟨T⟩⟩")
    
    def _print_tensor_matrix(self, tensor_matrix: Matrix, labels: list, prefix: str):
        """
        Imprimir matriz tensorial de forma organizada.
        """
        if tensor_matrix is None:
            print("   Matriz no disponible")
            return
            
        # Encabezado
        print("      ", end="")
        for j in range(4):
            print(f"{prefix + '_' + labels[j]:>15}", end="")
        print()
        
        # Filas
        for i in range(4):
            print(f"{prefix}_{labels[i]} ", end="")
            for j in range(4):
                element = tensor_matrix[i, j]
                if self._is_zero_element(element):
                    print(f"{'0':>15}", end="")
                else:
                    element_str = str(element)
                    if len(element_str) > 12:
                        element_str = element_str[:12] + "..."
                    print(f"{element_str:>15}", end="")
            print()
        
        # Mostrar elementos no nulos detallados
        print("\nElementos no nulos:")
        for i in range(4):
            for j in range(4):
                element = tensor_matrix[i, j]
                if not self._is_zero_element(element):
                    print(f"  {prefix}^{labels[i]}{labels[j]} = {element}")


def main():
    """
    Función principal para ejecutar el análisis completo de isotropía tensorial.
    """
    print("🌌 ANÁLISIS MATEMÁTICO DE COMPONENTES FUERA DE DIAGONAL")
    print("Tarea 1.1.1: Investigación de Anisotropía en Tensor ⟨T_μν⟩")
    print("="*80)
    
    try:
        # Inicializar analizador
        analyzer = TensorIsotropyAnalyzer()
        
        # Paso 1: Analizar código existente
        existing_analysis = analyzer.analyze_existing_calculations()
        
        # Paso 2: Calcular promedio angular
        angular_averaged_tensor = analyzer.compute_angular_average()
        
        # Paso 3: Evaluar métricas de isotropía
        isotropy_metrics = analyzer.evaluate_isotropy_metrics()
        
        # Paso 4: Mostrar matrices tensoriales
        analyzer.display_tensor_matrices()
        
        # Paso 5: Generar reporte de diagnóstico
        diagnostic_report = analyzer.generate_diagnostic_report()
        
        # Actualizar plan de acción si el análisis es exitoso
        if diagnostic_report['isotropy_achieved']:
            print("\n🎉 ANÁLISIS COMPLETADO EXITOSAMENTE")
            print("✅ Subtarea 1.1.1 lista para marcar como completada")
        else:
            print("\n⚠️  ANÁLISIS COMPLETADO CON RESERVAS")
            print("🔍 Se requiere investigación adicional")
        
        return analyzer, diagnostic_report
        
    except Exception as e:
        print(f"\n❌ ERROR DURANTE EL ANÁLISIS: {e}")
        print("🔧 Revisar configuración y dependencias")
        import traceback
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    print("🚀 Iniciando Análisis de Isotropía del Tensor Energía-Momento...")
    analyzer_instance, report = main()
    
    if analyzer_instance is not None:
        print("\n" + "="*80)
        print("📋 ANÁLISIS DE ISOTROPÍA TENSORIAL COMPLETADO")
        print("="*80)
        print("\n🎯 El script ha determinado exitosamente el comportamiento")
        print("   de los términos no diagonales del tensor ⟨T_μν⟩")
        print("\n📊 Resultados disponibles para próximas fases de investigación")
    else:
        print("\n❌ El análisis no pudo completarse")
        print("🔧 Revisar logs para identificar problemas")