#!/usr/bin/env python3
"""
Script para configurar la malla de alta resolución y los datos iniciales.
FASE 1.2 del Plan de Simulación de Gravedad Local

Objetivos:
1.  Implementar una malla de alta resolución (hasta 128³).
2.  Utilizar un dominio extendido (L=20) para observar el decaimiento.
3.  Adaptar la resolución según los recursos del sistema (RAM, CPU).
4.  Generar archivos de datos iniciales para múltiples resoluciones.
5.  Validar la configuración y estimar tiempos de cálculo.

Fecha: 27 de junio de 2025
"""

import numpy as np
import sympy as sp
from sympy import symbols, cos, sin, Matrix, lambdify
import psutil
import multiprocessing as mp
import time
import os
import warnings

# Suprimir advertencias de EinsteinPy si se usa en el futuro
warnings.filterwarnings('ignore')

class HighResolutionSetup:
    """
    Coordina la generación de datos iniciales para simulaciones de alta resolución.
    """
    def __init__(self, resolutions_to_generate, domain_size_l=20.0):
        self.resolutions = sorted(resolutions_to_generate)
        self.domain_size_l = domain_size_l
        self.system_info = self._analyze_system()
        
        # Preparar las funciones del tensor de expansión una sola vez
        self.T_expansion_sym, self.symbols_tuple = self._get_expansion_tensor_symbolic()
        self.T_expansion_num_func = self._create_numerical_tensor_function()

    def _analyze_system(self):
        """Analiza las características clave del sistema."""
        print("1. Analizando los recursos del sistema...")
        memory = psutil.virtual_memory()
        info = {
            'cpu_count': mp.cpu_count(),
            'available_ram_gb': memory.available / (1024**3)
        }
        print(f"   - CPUs detectadas: {info['cpu_count']}")
        print(f"   - RAM disponible: {info['available_ram_gb']:.2f} GB")
        return info

    def _get_expansion_tensor_symbolic(self):
        """Genera la expresión simbólica para T_expansion."""
        R, psi, theta, phi, omega_4d = symbols('R psi theta phi omega_4d', real=True)
        T_exp = Matrix(4, 4, lambda i, j: 0)
        T_exp[0, 0] = R**2 * omega_4d**2 * (cos(psi)**2 * cos(theta)**2 - 1)**2 * cos(phi)**2 * cos(psi)**2 * cos(theta)**2 / 2
        T_exp[1, 1] = R**2 * omega_4d**2 * (cos(psi)**2 * cos(theta)**2 - 1)**2 * sin(phi)**2 * cos(psi)**2 * cos(theta)**2 / 2
        T_exp[2, 2] = R**2 * omega_4d**2 * (sin(psi)**2 + sin(theta)**2 * cos(psi)**6 * cos(theta)**4) / 2
        T_exp[3, 3] = R**2 * omega_4d**2 * (-(cos(4*psi) - 1) * cos(theta)**4 + 8*sin(theta)**2) * cos(psi)**2 / 16
        T_exp[0, 1] = T_exp[1, 0] = R**2 * omega_4d**2 * (cos(psi)**2 * cos(theta)**2 - 1)**2 * sin(phi) * cos(phi) * cos(psi)**2 * cos(theta)**2 / 2
        T_exp[2, 3] = T_exp[3, 2] = R**2 * omega_4d**2 * (cos(psi)**4 * cos(theta)**4 - 1) * sin(psi) * sin(theta) * cos(psi) / 2
        return T_exp, (R, psi, theta, phi, omega_4d)

    def _create_numerical_tensor_function(self):
        """Convierte la matriz simbólica en una función numérica evaluable."""
        T_numerical = {}
        for i in range(4):
            for j in range(4):
                element = self.T_expansion_sym[i, j]
                if element != 0:
                    T_numerical[(i, j)] = lambdify(self.symbols_tuple, element, modules=['numpy'])
                else:
                    T_numerical[(i, j)] = lambda *args, **kwargs: 0.0
        return T_numerical

    def _estimate_memory_usage_gb(self, grid_size):
        """Estima el uso de memoria para generar los datos de una resolución."""
        # 3 tensores (total, expansión, masa) + 3 mallas de coordenadas
        # (16 componentes * 8 bytes/componente) * 3 tensores + 3 mallas * 8 bytes
        bytes_per_point = (16 * 8 * 3) + (3 * 8)
        total_bytes = (grid_size**3) * bytes_per_point
        safety_factor = 2.0  # Para objetos intermedios y sobrecarga de Python
        return total_bytes * safety_factor / (1024**3)

    def _calculate_optimal_sigma(self, grid_size, target_points=3.5):
        """Calcula el sigma óptimo para que ocupe ~target_points en la malla."""
        dx = (2 * self.domain_size_l) / grid_size
        return dx * target_points

    def _validate_parameters(self, grid_size, optimal_sigma):
        """Valida si la configuración cumple los criterios."""
        print(f"   - Validando parámetros para {grid_size}³ con σ={optimal_sigma:.4f}:")
        is_valid = True
        
        # 1. Validación de resolución de la Gaussiana
        dx = (2 * self.domain_size_l) / grid_size
        points_for_sigma = optimal_sigma / dx
        print(f"     - Criterio de resolución de σ: {points_for_sigma:.2f} puntos de malla (objetivo: 3-4).")
        if not (3 <= points_for_sigma <= 4):
            # Esta advertencia ahora sería inesperada, pero se mantiene por seguridad
            print("       ADVERTENCIA: La escala de la masa (σ) no está resuelta de forma óptima en esta malla.")

        # 2. Validación de tamaño de archivo
        estimated_file_size_gb = (grid_size**3 * 16 * 8 * 3) / (1024**3) # 3 tensores
        print(f"     - Tamaño estimado del archivo de salida: {estimated_file_size_gb:.3f} GB (límite: 2 GB).")
        if estimated_file_size_gb > 2.0:
            print("       ERROR: El archivo de salida estimado excede los 2 GB.")
            is_valid = False

        return is_valid

    def _estimate_generation_time_sec(self, grid_size):
        """Estima el tiempo de cálculo para la generación de datos."""
        # Estimación empírica basada en operaciones por punto
        # (muy dependiente del hardware)
        ops_per_point = 5000  # Incluye conversiones de coordenadas y evaluación de tensor
        total_ops = grid_size**3 * ops_per_point
        # Rendimiento estimado por core (operaciones/segundo)
        ops_per_core_per_sec = 0.5e9  # 0.5 GFLOP/s (conservador)
        
        effective_performance = self.system_info['cpu_count'] * ops_per_core_per_sec
        estimated_seconds = total_ops / effective_performance
        return estimated_seconds

    def generate_data_for_resolution(self, grid_size):
        """Genera y guarda el archivo de datos para una resolución específica."""
        print("-" * 80)
        print(f"Iniciando generación para resolución {grid_size}³")
        
        # --- Cálculo de Sigma Óptimo ---
        optimal_sigma = self._calculate_optimal_sigma(grid_size)
        
        # --- Validación y Estimación ---
        if not self._validate_parameters(grid_size, optimal_sigma):
            print(f"Generación para {grid_size}³ cancelada debido a errores de validación.")
            return

        estimated_ram_gb = self._estimate_memory_usage_gb(grid_size)
        print(f"     - Memoria RAM estimada para la generación: {estimated_ram_gb:.2f} GB.")
        if estimated_ram_gb > self.system_info['available_ram_gb']:
            print(f"       ERROR: RAM insuficiente ({self.system_info['available_ram_gb']:.2f} GB disponible).")
            print(f"Generación para {grid_size}³ cancelada.")
            return
            
        estimated_time_sec = self._estimate_generation_time_sec(grid_size)
        print(f"     - Tiempo de generación estimado: {estimated_time_sec:.1f} segundos.")

        start_time = time.time()

        # --- Configuración de Malla ---
        print("   - Configurando malla de cálculo...")
        L = self.domain_size_l
        x = np.linspace(-L, L, grid_size)
        y = np.linspace(-L, L, grid_size)
        z = np.linspace(-L, L, grid_size)
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

        # --- Parámetros Físicos ---
        R_param, omega_4d_param, M_particula = 1.0, 0.1, 0.5
        
        # --- Cálculo de Tensores ---
        print(f"   - Calculando tensor de masa (T_masa) con σ={optimal_sigma:.4f}...")
        T_masa = np.zeros((*X.shape, 4, 4))
        norm_factor = M_particula / (optimal_sigma * np.sqrt(2 * np.pi))**3
        exponent = -(X**2 + Y**2 + Z**2) / (2 * optimal_sigma**2)
        rho = norm_factor * np.exp(exponent)
        T_masa[..., 0, 0] = rho

        print("   - Evaluando tensor de expansión (T_expansion)...")
        T_expansion_grid = np.zeros((*X.shape, 4, 4))
        r = np.sqrt(X**2 + Y**2 + Z**2)
        psi = np.arctan(r / R_param)
        theta = np.arccos(np.clip(Z / (r + 1e-12), -1, 1))
        phi = np.arctan2(Y, X)
        
        for alpha in range(4):
            for beta in range(4):
                if self.T_expansion_num_func[(alpha, beta)].__name__ != '<lambda>':
                    T_expansion_grid[..., alpha, beta] = self.T_expansion_num_func[(alpha, beta)](
                        R_param, psi, theta, phi, omega_4d_param
                    )

        # --- Superposición y Guardado ---
        print("   - Superponiendo fuentes y guardando datos...")
        T_total_grid = T_expansion_grid + T_masa
        
        output_filename = f"initial_data_{grid_size}cubed.npz"
        np.savez_compressed(
            output_filename,
            X=X, Y=Y, Z=Z,
            T_total_mu_nu=T_total_grid,
            metadata=np.array({'grid_size': grid_size, 'domain_L': L, 'mass_sigma': optimal_sigma})
        )
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"✓ Datos para {grid_size}³ generados y guardados en '{output_filename}'")
        print(f"  Tiempo real de generación: {duration:.1f} segundos.")

    def run(self):
        """Ejecuta el proceso de generación para todas las resoluciones configuradas."""
        print("=" * 80)
        print("FASE 1.2: GENERACIÓN DE DATOS INICIALES DE ALTA RESOLUCIÓN")
        print("=" * 80)
        
        for res in self.resolutions:
            self.generate_data_for_resolution(res)
            
        print("-" * 80)
        print("Proceso de generación de datos completado.")
        print("Los archivos .npz están listos para ser usados en 'run_numerical_simulation.py'.")


if __name__ == "__main__":
    # Definir las resoluciones que se intentarán generar
    # El script evaluará si el sistema tiene recursos suficientes para cada una
    target_resolutions = [32, 64, 128]
    
    setup = HighResolutionSetup(
        resolutions_to_generate=target_resolutions,
        domain_size_l=20.0
    )
    setup.run()